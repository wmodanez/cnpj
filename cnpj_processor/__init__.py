"""
CNPJ Processor - Sistema de Processamento de Dados CNPJ da Receita Federal

Este pacote fornece ferramentas para download, processamento e análise
dos dados públicos de CNPJ disponibilizados pela Receita Federal do Brasil.

Uso básico:
    from cnpj_processor import CNPJProcessor
    
    # Criar processador
    processor = CNPJProcessor()
    
    # Processar dados
    processor.download_and_process()
    
Uso via CLI:
    cnpj-processor --help
    cnpj-processor --tipos empresas estabelecimentos
    cnpj-processor --step download --remote-folder 2024-05
"""

# Importar versão da API
from cnpj_processor.__version__ import (
    __version__,
    __title__,
    __author__,
    __license__,
    get_version,
    get_full_description
)

# Importar classes principais
from src.config import config
from src.database import create_duckdb_file

# Importar processadores
from src.process.processors.empresa_processor import EmpresaProcessor
from src.process.processors.estabelecimento_processor import EstabelecimentoProcessor
from src.process.processors.simples_processor import SimplesProcessor
from src.process.processors.socio_processor import SocioProcessor
from src.process.processors.painel_processor import PainelProcessor

# Importar entidades
from src.Entity.Empresa import Empresa
from src.Entity.Estabelecimento import Estabelecimento
from src.Entity.Simples import Simples
from src.Entity.Socio import Socio
from src.Entity.Painel import Painel

# Importar utilitários principais
from src.async_downloader import (
    download_multiple_files,
    get_latest_month_zip_urls,
    get_remote_folders,
    get_latest_remote_folder
)

# Classe principal wrapper
class CNPJProcessor:
    """
    Classe principal para processar dados CNPJ.
    
    Esta classe encapsula todas as funcionalidades do sistema,
    permitindo processamento programático dos dados CNPJ.
    
    Attributes:
        config: Configuração global do sistema
        
    Examples:
        >>> processor = CNPJProcessor()
        >>> processor.download_latest()
        >>> processor.process_all_types()
    """
    
    def __init__(self):
        """Inicializa o processador CNPJ."""
        self.config = config
        self.empresa_processor = EmpresaProcessor
        self.estabelecimento_processor = EstabelecimentoProcessor
        self.simples_processor = SimplesProcessor
        self.socio_processor = SocioProcessor
        self.painel_processor = PainelProcessor
    
    def get_latest_folder(self) -> str:
        """
        Obtém a pasta remota mais recente disponível.
        
        Returns:
            str: Nome da pasta mais recente (formato AAAA-MM)
        """
        return get_latest_remote_folder()
    
    def get_available_folders(self) -> list:
        """
        Obtém lista de todas as pastas remotas disponíveis.
        
        Returns:
            list: Lista de nomes de pastas disponíveis
        """
        return get_remote_folders()
    
    def download_latest(self, tipos=None, force=False):
        """
        Baixa os arquivos mais recentes.
        
        Args:
            tipos: Lista de tipos a baixar (empresas, estabelecimentos, simples, socios)
            force: Forçar download mesmo se arquivo existir
            
        Returns:
            bool: True se bem-sucedido
        """
        import asyncio
        urls = get_latest_month_zip_urls(tipos)
        return asyncio.run(download_multiple_files(urls, force_download=force))
    
    def create_database(self, parquet_folder: str, output_file: str = None):
        """
        Cria banco de dados DuckDB a partir dos parquets.
        
        Args:
            parquet_folder: Pasta com os arquivos parquet
            output_file: Nome do arquivo de saída (opcional)
            
        Returns:
            bool: True se bem-sucedido
        """
        return create_duckdb_file(parquet_folder, output_file)

# Exportar símbolos principais
__all__ = [
    # Versão e metadados
    '__version__',
    '__title__',
    '__author__',
    '__license__',
    'get_version',
    'get_full_description',
    
    # Classe principal
    'CNPJProcessor',
    
    # Configuração
    'config',
    
    # Processadores
    'EmpresaProcessor',
    'EstabelecimentoProcessor',
    'SimplesProcessor',
    'SocioProcessor',
    'PainelProcessor',
    
    # Entidades
    'Empresa',
    'Estabelecimento',
    'Simples',
    'Socio',
    'Painel',
    
    # Funções de download
    'download_multiple_files',
    'get_latest_month_zip_urls',
    'get_remote_folders',
    'get_latest_remote_folder',
    
    # Database
    'create_duckdb_file',
]
