"""
CNPJ Processor - Sistema de Processamento de Dados CNPJ da Receita Federal

Este pacote fornece ferramentas para download, processamento e armazenamento
automatizado de dados públicos de CNPJ disponibilizados pela Receita Federal.

Uso básico:
    >>> from src import __version__
    >>> print(__version__)
    
Uso via linha de comando:
    $ cnpj-processor --help
    $ cnpj --tipos empresas --step download
"""

from cnpj_processor.__version__ import (
    __version__,
    __title__,
    __author__,
    __email__,
    __url__,
    __license__,
    get_version,
    get_full_description,
)

# Importar componentes principais para fácil acesso
from cnpj_processor.config import Config, config
from cnpj_processor.database import create_duckdb_file, verify_parquet_file

# Exportar símbolos principais
__all__ = [
    # Versão e metadados
    "__version__",
    "__title__",
    "__author__",
    "__email__",
    "__url__",
    "__license__",
    "get_version",
    "get_full_description",
    # Core
    "Config",
    "config",
    "create_duckdb_file",
    "verify_parquet_file",
] 