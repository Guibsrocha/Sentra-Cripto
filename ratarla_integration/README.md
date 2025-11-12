# RatarlA Squad - Sistema de Trading Automatizado com 8 Agentes de IA

Sistema de trading automatizado integrado ao Freqtrade, utilizando 8 agentes de IA especializados para análise de mercado e execução de trades.

## 🐀 Os 8 Agentes

### Trading Team
1. **Black Rat (Trading Agent)** - Execução de ordens e gestão do portfólio
2. **Orange Rat (Test Agent)** - Validação de estratégias através de backtesting
3. **Pink Rat (Strategy Agent)** - Gestão e otimização de estratégias

### Research Team
4. **Purple Rat (Research Agent)** - Descoberta de novas estratégias (YouTube, PDFs, Twitter, on-chain)

### Market Analysis Team
5. **Yellow Rat (Risk Agent)** - Gestão de riscos, cálculo de stop loss e take profit
6. **White Rat (Sentiment Agent)** - Análise de sentimento em redes sociais (Twitter)
7. **Green Rat (Chart Agent)** - Análise técnica de gráficos (RSI, MACD, Bollinger, etc.)
8. **Brown Rat (Whale Agent)** - Monitoramento de movimentações de baleias

## 🚀 Características

- **Integração Nativa com Freqtrade**: Funciona como uma estratégia customizada
- **Análise Multi-Dimensional**: Combina análise técnica, sentimento e risco
- **LLM com Fallback**: Usa OpenRouter LLM com fallback para análise rule-based
- **Gestão de Risco Dinâmica**: Stop loss e position sizing adaptativos
- **Suporte a Long e Short**: Opera em ambas as direções do mercado
- **Modo Dry Run**: Teste com dinheiro virtual antes de usar capital real

## 📋 Requisitos

- Python 3.8+
- Freqtrade 2023.1+
- Binance API Keys
- OpenRouter API Key (opcional - funciona sem)

## 🔧 Instalação

### 1. Instalar Freqtrade

```bash
# Clone Freqtrade
git clone https://github.com/freqtrade/freqtrade.git
cd freqtrade

# Instalar
./setup.sh -i
```

### 2. Instalar RatarlA Squad

```bash
# Clone este repositório
git clone https://github.com/Guibsrocha/ratarla-squad.git
cd ratarla-squad

# Copiar estratégia para Freqtrade
cp strategies/ratarla_squad_strategy.py ../freqtrade/user_data/strategies/

# Copiar agentes
cp -r agents ../freqtrade/user_data/
cp llm_client.py ../freqtrade/user_data/
cp config.py ../freqtrade/user_data/

# Instalar dependências adicionais
pip install -r requirements.txt
```

### 3. Configurar API Keys

Edite `config.py`:

```python
BINANCE_API_KEY = "sua_binance_api_key"
BINANCE_API_SECRET = "sua_binance_secret"
OPENROUTER_API_KEY = "sua_openrouter_key"  # Opcional
```

### 4. Configurar Freqtrade

Edite `config.json`:

```json
{
  "strategy": "RatarlASquadStrategy",
  "exchange": {
    "name": "binance",
    "key": "sua_binance_api_key",
    "secret": "sua_binance_secret"
  },
  "dry_run": true,
  ...
}
```

## 🎯 Uso

### Modo Dry Run (Simulação)

```bash
cd freqtrade
freqtrade trade --config user_data/config.json --strategy RatarlASquadStrategy
```

### Backtesting

```bash
freqtrade backtesting \
  --config user_data/config.json \
  --strategy RatarlASquadStrategy \
  --timerange 20231101-20231201
```

### Modo Live (Dinheiro Real)

⚠️ **ATENÇÃO**: Apenas use modo live após validar extensivamente em dry_run!

```bash
# Edite config.json: "dry_run": false
freqtrade trade --config user_data/config.json --strategy RatarlASquadStrategy
```

## 📊 Arquitetura

```
RatarlA Squad
├── config.py              # Configurações centralizadas
├── llm_client.py          # Cliente LLM com fallback
├── agents/
│   ├── green_rat.py       # Análise Técnica
│   ├── yellow_rat.py      # Gestão de Risco
│   ├── white_rat.py       # Análise de Sentimento
│   ├── brown_rat.py       # Monitoramento de Baleias
│   ├── purple_rat.py      # Pesquisa de Estratégias
│   ├── pink_rat.py        # Gestão de Estratégias
│   ├── orange_rat.py      # Backtesting
│   └── black_rat.py       # Execução de Trades
└── strategies/
    └── ratarla_squad_strategy.py  # Estratégia Freqtrade
```

## 🔍 Fluxo de Trabalho

1. **Coleta de Dados**: Purple Rat, White Rat, Brown Rat coletam informações
2. **Análise Técnica**: Green Rat analisa indicadores e padrões
3. **Análise de Risco**: Yellow Rat calcula stop loss e position size
4. **Decisão**: Combinação de todos os sinais para LONG/SHORT/HOLD
5. **Validação**: Orange Rat valida através de backtesting (offline)
6. **Execução**: Black Rat executa a ordem via Freqtrade

## 📈 Indicadores Utilizados

- **RSI (Relative Strength Index)**: Sobrecompra/sobrevenda
- **MACD (Moving Average Convergence Divergence)**: Momentum
- **EMA (Exponential Moving Averages)**: Tendência
- **Bollinger Bands**: Volatilidade
- **ATR (Average True Range)**: Volatilidade para stop loss
- **Volume**: Confirmação de movimentos
- **Stochastic**: Momentum adicional
- **ADX (Average Directional Index)**: Força da tendência

## ⚙️ Configuração Avançada

### Ajustar Parâmetros de Risco

Em `config.py`:

```python
MAX_OPEN_TRADES = 3          # Máximo de trades simultâneos
STAKE_AMOUNT = 100           # USDT por trade
STOP_LOSS_PERCENT = 2        # Stop loss padrão (%)
TAKE_PROFIT_PERCENT = 5      # Take profit padrão (%)
```

### Ajustar Indicadores

```python
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
```

## 🧪 Testing

### Executar Backtesting

```bash
freqtrade backtesting \
  --strategy RatarlASquadStrategy \
  --timerange 20230101-20231231 \
  --export trades
```

### Plotar Resultados

```bash
freqtrade plot-dataframe \
  --strategy RatarlASquadStrategy \
  --pairs BTC/USDT \
  --timerange 20231101-20231201
```

## 🔐 Segurança

- **NUNCA** commite API keys para repositórios públicos
- Use variáveis de ambiente para credenciais sensíveis
- Teste SEMPRE em modo dry_run antes de live
- Monitore constantemente os trades em modo live
- Configure alertas via Telegram

## 📝 Logs

Logs são salvos em `/workspace/ratarla_integration/logs/ratarla_squad.log`

Níveis de log disponíveis:
- `DEBUG`: Informações detalhadas
- `INFO`: Operações normais
- `WARNING`: Avisos importantes
- `ERROR`: Erros que precisam atenção

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## ⚠️ Disclaimer

**AVISO IMPORTANTE**: Trading de criptomoedas envolve riscos significativos. Este software é fornecido "como está", sem garantias de qualquer tipo. Use por sua própria conta e risco. Os desenvolvedores não são responsáveis por perdas financeiras.

- Sempre teste em modo dry_run primeiro
- Nunca invista mais do que pode perder
- Não garante lucros
- Resultados passados não garantem resultados futuros

## 📄 Licença

MIT License - veja LICENSE para detalhes

## 📞 Suporte

- **Issues**: https://github.com/Guibsrocha/ratarla-squad/issues
- **Discussions**: https://github.com/Guibsrocha/ratarla-squad/discussions
- **Email**: guilherme@sentra.com.br

## 🙏 Agradecimentos

- Freqtrade Team pelo excelente framework
- Comunidade de trading algorítmico
- OpenRouter por disponibilizar acesso a LLMs

---

**Desenvolvido com 🐀 por Sentra Cripto Team**
