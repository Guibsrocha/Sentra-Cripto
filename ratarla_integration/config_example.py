"""
RatarlA Squad - Configurações Centralizadas (EXEMPLO)
Sistema de Trading Automatizado com 8 Agentes de IA

IMPORTANTE: Copie este arquivo para 'config.py' e preencha com suas credenciais reais
"""
import os
from pathlib import Path

# ===========================
# DIRETÓRIOS
# ===========================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
STRATEGIES_DIR = BASE_DIR / "strategies"

# Criar diretórios se não existirem
for dir_path in [DATA_DIR, LOGS_DIR, STRATEGIES_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# ===========================
# BINANCE API
# ===========================
BINANCE_API_KEY = "sua_binance_api_key_aqui"
BINANCE_API_SECRET = "sua_binance_secret_key_aqui"

# ===========================
# FREQTRADE API
# ===========================
FREQTRADE_API_URL = "http://localhost:8080/api/v1"
FREQTRADE_USERNAME = "admin"
FREQTRADE_PASSWORD = "sua_senha_freqtrade"

# ===========================
# OPENROUTER LLM (com fallback)
# ===========================
OPENROUTER_API_KEY = "sua_openrouter_api_key_ou_deixe_vazio"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
USE_LLM_FALLBACK = True  # Se True, usa análise rule-based quando LLM falhar

# ===========================
# TWITTER API (Opcional)
# ===========================
TWITTER_API_KEY = "sua_twitter_api_key"
TWITTER_API_SECRET = "sua_twitter_api_secret"
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")

# ===========================
# TELEGRAM BOT (Opcional)
# ===========================
TELEGRAM_BOT_TOKEN = "seu_telegram_bot_token"
TELEGRAM_CHAT_ID = "seu_telegram_chat_id"

# ===========================
# PARES DE TRADING
# ===========================
TRADING_PAIRS = [
    "BTC/USDT",
    "ETH/USDT",
    "BNB/USDT",
    "SOL/USDT",
    "XRP/USDT",
    "ADA/USDT",
    "DOGE/USDT",
    "MATIC/USDT"
]

# ===========================
# CONFIGURAÇÕES DE RISCO
# ===========================
MAX_OPEN_TRADES = 3
STAKE_AMOUNT = 100  # USDT por trade
MAX_DRAWDOWN_PERCENT = 20  # Máximo drawdown permitido
STOP_LOSS_PERCENT = 2  # Stop loss padrão
TAKE_PROFIT_PERCENT = 5  # Take profit padrão

# ===========================
# INDICADORES TÉCNICOS
# ===========================
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

EMA_SHORT = 9
EMA_LONG = 21

BOLLINGER_PERIOD = 20
BOLLINGER_STD = 2

# ===========================
# CONFIGURAÇÕES DOS AGENTES
# ===========================
AGENT_CYCLE_INTERVAL = 300  # segundos (5 minutos)
ENABLE_SENTIMENT_ANALYSIS = True
ENABLE_WHALE_MONITORING = True
ENABLE_RESEARCH_AGENT = True

# ===========================
# LOGGING
# ===========================
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "ratarla_squad.log"

# ===========================
# DATABASE
# ===========================
DATABASE_PATH = DATA_DIR / "ratarla_squad.db"
