"""
Yellow Rat - Agente de Gestão de Risco (Risk Agent)
Responsável por calcular riscos, stop loss, take profit
"""
import logging
import pandas as pd
from typing import Dict, Optional
import config

logger = logging.getLogger(__name__)


class YellowRat:
    """Agente de Gestão de Risco"""
    
    def __init__(self):
        self.name = "YELLOW RAT (Risk Agent)"
        self.logger = logging.getLogger(self.name)
    
    def calculate_risk_params(self, dataframe: pd.DataFrame, pair: str, 
                             action: str) -> Dict:
        """
        Calcula parâmetros de risco para um trade
        
        Args:
            dataframe: DataFrame com OHLCV e indicadores
            pair: Par de trading
            action: LONG ou SHORT
            
        Returns:
            Dict com stop_loss, take_profit, position_size
        """
        try:
            if dataframe.empty or action == 'HOLD':
                return self._default_risk_params()
            
            current = dataframe.iloc[-1]
            price = current['close']
            
            # Calcular ATR (Average True Range) para volatilidade
            atr = self._calculate_atr(dataframe)
            
            # Calcular stop loss baseado em ATR
            if action == 'LONG':
                stop_loss = price - (atr * 1.5)  # 1.5 ATR abaixo do preço
                take_profit = price + (atr * 3.0)  # 3 ATR acima (risk/reward 2:1)
            else:  # SHORT
                stop_loss = price + (atr * 1.5)
                take_profit = price - (atr * 3.0)
            
            # Calcular tamanho da posição baseado em risco
            risk_amount = config.STAKE_AMOUNT * (config.STOP_LOSS_PERCENT / 100)
            stop_loss_distance = abs(price - stop_loss)
            position_size = risk_amount / stop_loss_distance if stop_loss_distance > 0 else 1.0
            
            # Ajustar para stake amount
            position_size = min(position_size, config.STAKE_AMOUNT / price)
            
            result = {
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'position_size': position_size,
                'risk_reward_ratio': abs(take_profit - price) / abs(stop_loss - price),
                'atr': atr,
                'max_risk_amount': risk_amount
            }
            
            self.logger.info(f"{pair} Risk Params: SL={stop_loss:.2f}, TP={take_profit:.2f}, "
                           f"Size={position_size:.6f}, R/R={result['risk_reward_ratio']:.2f}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular risco: {str(e)}")
            return self._default_risk_params()
    
    def _calculate_atr(self, dataframe: pd.DataFrame, period: int = 14) -> float:
        """Calcula Average True Range"""
        try:
            df = dataframe.copy()
            
            df['h-l'] = df['high'] - df['low']
            df['h-pc'] = abs(df['high'] - df['close'].shift(1))
            df['l-pc'] = abs(df['low'] - df['close'].shift(1))
            
            df['tr'] = df[['h-l', 'h-pc', 'l-pc']].max(axis=1)
            atr = df['tr'].rolling(window=period).mean().iloc[-1]
            
            return atr if not pd.isna(atr) else df['close'].iloc[-1] * 0.02  # 2% como fallback
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular ATR: {str(e)}")
            return dataframe['close'].iloc[-1] * 0.02
    
    def check_portfolio_risk(self, open_trades: int, total_exposure: float) -> Dict:
        """
        Verifica risco total do portfólio
        
        Args:
            open_trades: Número de trades abertos
            total_exposure: Exposição total em USDT
            
        Returns:
            Dict com status e recomendações
        """
        warnings = []
        can_open_new = True
        
        # Verificar número máximo de trades
        if open_trades >= config.MAX_OPEN_TRADES:
            warnings.append(f"Máximo de trades abertos ({config.MAX_OPEN_TRADES})")
            can_open_new = False
        
        # Verificar exposição total (exemplo: não exceder 80% do capital)
        max_exposure = config.STAKE_AMOUNT * config.MAX_OPEN_TRADES * 0.8
        if total_exposure > max_exposure:
            warnings.append(f"Exposição total muito alta: {total_exposure:.2f} USDT")
            can_open_new = False
        
        return {
            'can_open_new_trade': can_open_new,
            'warnings': warnings,
            'open_trades': open_trades,
            'total_exposure': total_exposure,
            'risk_level': self._calculate_risk_level(open_trades, total_exposure)
        }
    
    def _calculate_risk_level(self, open_trades: int, total_exposure: float) -> str:
        """Calcula nível de risco do portfólio"""
        max_trades = config.MAX_OPEN_TRADES
        max_exposure = config.STAKE_AMOUNT * max_trades
        
        trade_ratio = open_trades / max_trades
        exposure_ratio = total_exposure / max_exposure
        
        risk_score = (trade_ratio + exposure_ratio) / 2
        
        if risk_score < 0.3:
            return "BAIXO"
        elif risk_score < 0.7:
            return "MÉDIO"
        else:
            return "ALTO"
    
    def _default_risk_params(self) -> Dict:
        """Retorna parâmetros de risco padrão"""
        return {
            'stop_loss': 0,
            'take_profit': 0,
            'position_size': 1.0,
            'risk_reward_ratio': 2.0,
            'atr': 0,
            'max_risk_amount': config.STAKE_AMOUNT * 0.02
        }
