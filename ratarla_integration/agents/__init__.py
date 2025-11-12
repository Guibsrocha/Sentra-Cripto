"""
RatarlA Squad Agents Package
Sistema de 8 Agentes de IA para Trading Automatizado
"""

__version__ = "1.0.0"
__author__ = "Sentra Cripto Team"

# Importar agentes principais
try:
    from .green_rat import GreenRat
    from .yellow_rat import YellowRat
    
    __all__ = [
        'GreenRat',
        'YellowRat',
    ]
except ImportError:
    # Caso módulos não estejam disponíveis
    __all__ = []
