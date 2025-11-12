"""
Cliente LLM com Fallback Rule-Based
Integra OpenRouter com análise técnica tradicional como backup
"""
import logging
import requests
import re
from typing import List, Dict, Optional
import config

logger = logging.getLogger(__name__)


class LLMClient:
    """Cliente para OpenRouter com fallback para análise rule-based"""
    
    def __init__(self):
        self.api_key = config.OPENROUTER_API_KEY
        self.api_url = config.OPENROUTER_API_URL
        self.use_fallback = config.USE_LLM_FALLBACK
        
    def chat(self, model: str, messages: List[Dict], temperature: float = 0.7, 
             max_tokens: int = 2000) -> Optional[str]:
        """
        Envia requisição para OpenRouter LLM
        Se falhar, usa análise rule-based como fallback
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # Se receber 402 (Payment Required), usar fallback
            if response.status_code == 402:
                logger.warning("⚠️  OpenRouter sem créditos - usando análise rule-based")
                return self._fallback_analysis(messages)
            
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                logger.error("Resposta LLM sem conteúdo")
                return self._fallback_analysis(messages)
                
        except Exception as e:
            logger.error(f"Erro ao chamar OpenRouter: {str(e)}")
            if self.use_fallback:
                return self._fallback_analysis(messages)
            return None
    
    def _fallback_analysis(self, messages: List[Dict]) -> str:
        """
        Análise técnica rule-based quando LLM não está disponível
        Usa indicadores técnicos tradicionais para decisão
        """
        last_message = messages[-1]['content'] if messages else ""
        
        # Extrair indicadores da mensagem
        analysis = {
            'rsi': self._extract_number(last_message, r'RSI[:\s]+([0-9.]+)'),
            'macd': self._extract_number(last_message, r'MACD[:\s]+(-?[0-9.]+)'),
            'ema_short': self._extract_number(last_message, r'EMA.*?9[:\s]+([0-9.]+)'),
            'ema_long': self._extract_number(last_message, r'EMA.*?21[:\s]+([0-9.]+)'),
            'price': self._extract_number(last_message, r'Pre[çc]o[:\s]+([0-9.]+)'),
        }
        
        # Lógica de decisão baseada em regras
        signals = []
        
        # RSI Analysis
        if analysis['rsi']:
            if analysis['rsi'] < config.RSI_OVERSOLD:
                signals.append(("LONG", "RSI oversold", 0.8))
            elif analysis['rsi'] > config.RSI_OVERBOUGHT:
                signals.append(("SHORT", "RSI overbought", 0.8))
            else:
                signals.append(("HOLD", "RSI neutral", 0.3))
        
        # MACD Analysis
        if analysis['macd']:
            if analysis['macd'] > 0:
                signals.append(("LONG", "MACD positive", 0.6))
            else:
                signals.append(("SHORT", "MACD negative", 0.6))
        
        # EMA Crossover
        if analysis['ema_short'] and analysis['ema_long']:
            if analysis['ema_short'] > analysis['ema_long']:
                signals.append(("LONG", "EMA bullish crossover", 0.7))
            else:
                signals.append(("SHORT", "EMA bearish crossover", 0.7))
        
        # Consolidar sinais
        if not signals:
            return "HOLD - Dados insuficientes para análise"
        
        # Calcular confiança ponderada
        long_score = sum(weight for action, _, weight in signals if action == "LONG")
        short_score = sum(weight for action, _, weight in signals if action == "SHORT")
        
        if long_score > short_score and long_score > 1.0:
            reasons = [reason for action, reason, _ in signals if action == "LONG"]
            return f"LONG (Confiança: {long_score:.2f}) - Razões: {', '.join(reasons)}"
        elif short_score > long_score and short_score > 1.0:
            reasons = [reason for action, reason, _ in signals if action == "SHORT"]
            return f"SHORT (Confiança: {short_score:.2f}) - Razões: {', '.join(reasons)}"
        else:
            return "HOLD - Sinais conflitantes ou fracos"
    
    def _extract_number(self, text: str, pattern: str) -> Optional[float]:
        """Extrai número usando regex"""
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except:
                return None
        return None


# Instância global
llm_client = LLMClient()
