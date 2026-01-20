"""
Versionamento da API cnpj_processor para PyPI

A partir da v3.7.0, a versão da API está unificada com a versão do projeto.
Ambas seguem versionamento semântico.
"""

# Versão da API pública
__version__ = "3.7.0"
__title__ = "CNPJ Processor"
__author__ = "wmodanez"
__license__ = "MIT"

def get_version():
    """Retorna a versão da API."""
    return __version__

def get_full_description():
    """Retorna a descrição completa da API."""
    return f"{__title__} v{__version__} - Sistema de Processamento de Dados CNPJ da Receita Federal do Brasil"

__all__ = [
    '__version__',
    '__title__',
    '__author__',
    '__license__',
    'get_version',
    'get_full_description'
]
