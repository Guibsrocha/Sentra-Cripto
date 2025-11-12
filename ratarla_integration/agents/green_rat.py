"""
Green Rat - Agente de Análise Técnica (Chart Agent)
Responsável por analisar gráficos e indicadores técnicos
"""
import logging
import pandas as pd
import numpy as np
from typing import Dict, Optional
import config
from llm_client import llm_client

logger = logging.getLogger(__name__)


class GreenRat:
    """Agente de Análise Técnica"""
    
    def __init__(self):
        self.name = "GREEN RAT (Chart Agent)"
        self.logger = logging.getLogger(self.name)
    
    def analyze(self, dataframe: pd.DataFrame, pair: str) -> Dict:
        """
        Analisa dados técnicos e retorna sinal de trading
        
        Args:
            dataframe: DataFrame com OHLCV e indicadores
            pair: Par de trading (ex: BTC/USDT)
            
        Returns:
            Dict com sinal, confiança e razão
        """
        try:
            if dataframe.empty:
                return self._no_signal("DataFrame vazio")
            
            # Pegar última linha de dados
            current = dataframe.iloc[-1]
            
            # Calcular indicadores se não existirem
            if 'rsi' not in dataframe.columns:
                dataframe = self._calculate_indicators(dataframe)
                current = dataframe.iloc[-1]
            
            # Criar mensagem para análise
            analysis_message = self._create_analysis_message(current, pair)
            
            # Tentar usar LLM primeiro
            llm_response = llm_client.chat(
                model="anthropic/claude-3.5-sonnet",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um analista técnico especializado em criptomoedas. "
                                   "Analise os indicadores e responda apenas: LONG, SHORT ou HOLD, "
                                   "seguido da razão."
                    },
                    {
                        "role": "user",
                        "content": analysis_message
                    }
                ]
            )
            
            # Processar resposta
            if llm_response:
                signal = self._parse_signal(llm_response)
                self.logger.info(f"{pair}: {signal['action']} (Confiança: {signal['confidence']:.2f})")
                return signal
            else:
                return self._no_signal("LLM não disponível e fallback falhou")
                
        except Exception as e:
            self.logger.error(f"Erro na análise: {str(e)}")
            return self._no_signal(f"Erro: {str(e)}")
    
    def _calculate_indicators(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Calcula indicadores técnicos"""
        df = dataframe.copy()
        
        try:
            # RSI
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=config.RSI_PERIOD).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=config.RSI_PERIOD).mean()
            rs = gain / loss
            df['rsi'] = 100 - (100 / (1 + rs))
            
            # MACD
            ema_fast = df['close'].ewm(span=config.MACD_FAST).mean()
            ema_slow = df['close'].ewm(span=config.MACD_SLOW).mean()
            df['macd'] = ema_fast - ema_slow
            df['macd_signal'] = df['macd'].ewm(span=config.MACD_SIGNAL).mean()
            df['macd_diff'] = df['macd'] - df['macd_signal']
            
            # EMAs
            df['ema_short'] = df['close'].ewm(span=config.EMA_SHORT).mean()
            df['ema_long'] = df['close'].ewm(span=config.EMA_LONG).mean()
            
            # Bollinger Bands
            sma = df['close'].rolling(window=config.BOLLINGER_PERIOD).mean()
            std = df['close'].rolling(window=config.BOLLINGER_PERIOD).std()
            df['bb_upper'] = sma + (std * config.BOLLINGER_STD)
            df['bb_middle'] = sma
            df['bb_lower'] = sma - (std * config.BOLLINGER_STD)
            
            # Volume
            df['volume_sma'] = df['volume'].rolling(window=20).mean()
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular indicadores: {str(e)}")
        
        return df
    
    def _create_analysis_message(self, current: pd.Series, pair: str) -> str:
        """Cria mensagem formatada para análise"""
        message = f"""
Análise Técnica - {pair}

Preço Atual: {current['close']:.2f} USDT

Indicadores:
- RSI(14): {current.get('rsi', 0):.2f}
- MACD: {current.get('macd', 0):.4f}
- MACD Signal: {current.get('macd_signal', 0):.4f}
- MACD Diff: {current.get('macd_diff', 0):.4f}
- EMA(9): {current.get('ema_short', 0):.2f}
- EMA(21): {current.get('ema_long', 0):.2f}
- BB Upper: {current.get('bb_upper', 0):.2f}
- BB Middle: {current.get('bb_middle', 0):.2f}
- BB Lower: {current.get('bb_lower', 0):.2f}
- Volume: {current.get('volume', 0):.2f}
- Volume SMA: {current.get('volume_sma', 0):.2f}

Baseado nestes indicadores, qual a recomendação? LONG, SHORT ou HOLD?
"""
        return message
    
    def _parse_signal(self, response: str) -> Dict:
        """Extrai sinal da resposta LLM"""
        response_upper = response.upper()
        
        if 'LONG' in response_upper:
            action = 'LONG'
            confidence = self._extract_confidence(response)
        elif 'SHORT' in response_upper:
            action = 'SHORT'
            confidence = self._extract_confidence(response)
        else:
            action = 'HOLD'
            confidence = 0.5
        
        return {
            'action': action,
            'confidence': confidence,
            'reason': response,
            'agent': self.name
        }
    
    def _extract_confidence(self, text: str) -> float:
        """Extrai nível de confiança da resposta"""
        import re
        match = re.search(r'confian[çc]a[:\s]+([0-9.]+)', text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except:
                pass
        return 0.7  # Confiança padrão
    
    def _no_signal(self, reason: str) -> Dict:
        """Retorna sinal neutro"""
        return {
            'action': 'HOLD',
            'confidence': 0.0,
            'reason': reason,
            'agent': self.name
        }
