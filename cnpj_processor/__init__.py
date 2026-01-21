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
    
    Esta classe encapsula todas as funcionalidades do sistema de processamento
    de dados públicos CNPJ da Receita Federal, permitindo uso programático
    das mesmas funcionalidades disponíveis via linha de comando.
    
    Attributes:
        config: Configuração global do sistema
        
    Examples:
        >>> # Pipeline completo
        >>> processor = CNPJProcessor()
        >>> processor.run(step='all', tipos=['empresas', 'estabelecimentos'])
        
        >>> # Apenas download
        >>> processor.run(step='download', remote_folder='2024-05')
        
        >>> # Apenas processamento
        >>> processor.run(step='process', source_zip_folder='./dados-zip/2024-05', 
        ...               output_subfolder='processados_2024_05')
        
        >>> # Processar painel com filtros
        >>> processor.run(step='painel', painel_uf='SP', painel_situacao=2)
    """
    
    def __init__(self):
        """Inicializa o processador CNPJ."""
        self.config = config
    
    def run(self,
            step: str = 'all',
            tipos: list = None,
            remote_folder: str = None,
            output_subfolder: str = None,
            source_zip_folder: str = None,
            force_download: bool = False,
            delete_zips_after_extract: bool = False,
            cleanup_after_db: bool = False,
            cleanup_all_after_db: bool = False,
            processar_painel: bool = False,
            painel_uf: str = None,
            painel_situacao: int = None,
            painel_incluir_inativos: bool = False,
            criar_empresa_privada: bool = False,
            criar_subset_uf: str = None,
            quiet: bool = False,
            log_level: str = 'INFO') -> tuple:
        """
        Executa o processamento de dados CNPJ.
        
        Este método replica todas as funcionalidades do main.py, permitindo
        uso programático do sistema.
        
        Args:
            step: Etapa a executar ('download', 'process', 'database', 'painel', 'all')
            tipos: Lista de tipos a processar (['empresas', 'estabelecimentos', 'simples', 'socios'])
            remote_folder: Pasta remota específica (formato AAAA-MM)
            output_subfolder: Subpasta de saída para os parquets (use "." para pasta raiz)
            source_zip_folder: Pasta com arquivos ZIP para processamento
            force_download: Forçar download mesmo se arquivo existir
            delete_zips_after_extract: Deletar ZIPs após extração bem-sucedida
            cleanup_after_db: Deletar parquets após criação do banco
            cleanup_all_after_db: Deletar parquets E ZIPs após criação do banco
            processar_painel: Processar dados do painel consolidado
            painel_uf: Filtrar painel por UF (ex: 'SP', 'GO')
            painel_situacao: Filtrar painel por situação cadastral (1=Nula, 2=Ativa, etc.)
            painel_incluir_inativos: Incluir estabelecimentos inativos no painel
            criar_empresa_privada: Criar subconjunto de empresas privadas
            criar_subset_uf: Criar subconjunto por UF para estabelecimentos
            quiet: Modo silencioso (reduz saídas no console)
            log_level: Nível de logging ('DEBUG', 'INFO', 'WARNING', 'ERROR')
            
        Returns:
            tuple: (sucesso: bool, pasta_output: str)
            
        Examples:
            >>> # Pipeline completo padrão
            >>> processor = CNPJProcessor()
            >>> success, folder = processor.run()
            
            >>> # Download de tipos específicos
            >>> success, folder = processor.run(
            ...     step='download',
            ...     tipos=['empresas', 'estabelecimentos'],
            ...     remote_folder='2024-05'
            ... )
            
            >>> # Processamento com economia de espaço
            >>> success, folder = processor.run(
            ...     step='all',
            ...     delete_zips_after_extract=True,
            ...     cleanup_all_after_db=True
            ... )
            
            >>> # Painel filtrado por UF e situação
            >>> success, folder = processor.run(
            ...     step='painel',
            ...     painel_uf='SP',
            ...     painel_situacao=2,
            ...     remote_folder='2024-05'
            ... )
        """
        import sys
        import asyncio
        from pathlib import Path
        
        # Construir argumentos simulando linha de comando
        sys.argv = ['cnpj-processor', f'--step={step}', f'--log-level={log_level}']
        
        if tipos:
            sys.argv.extend(['--tipos'] + tipos)
        if remote_folder:
            sys.argv.extend(['--remote-folder', remote_folder])
        if output_subfolder:
            sys.argv.extend(['--output-subfolder', output_subfolder])
        if source_zip_folder:
            sys.argv.extend(['--source-zip-folder', source_zip_folder])
        if force_download:
            sys.argv.append('--force-download')
        if delete_zips_after_extract:
            sys.argv.append('--delete-zips-after-extract')
        if cleanup_after_db:
            sys.argv.append('--cleanup-after-db')
        if cleanup_all_after_db:
            sys.argv.append('--cleanup-all-after-db')
        if processar_painel:
            sys.argv.append('--processar-painel')
        if painel_uf:
            sys.argv.extend(['--painel-uf', painel_uf])
        if painel_situacao is not None:
            sys.argv.extend(['--painel-situacao', str(painel_situacao)])
        if painel_incluir_inativos:
            sys.argv.append('--painel-incluir-inativos')
        if criar_empresa_privada:
            sys.argv.append('--criar-empresa-privada')
        if criar_subset_uf:
            sys.argv.extend(['--criar-subset-uf', criar_subset_uf])
        if quiet:
            sys.argv.append('--quiet')
        
        # Importar e executar função principal
        root_dir = Path(__file__).parent.parent
        sys.path.insert(0, str(root_dir))
        
        from main import async_main
        
        # Executar de forma assíncrona
        return asyncio.run(async_main())
    
    def get_latest_folder(self) -> str:
        """
        Obtém a pasta remota mais recente disponível.
        
        Returns:
            str: Nome da pasta mais recente (formato AAAA-MM)
            
        Examples:
            >>> processor = CNPJProcessor()
            >>> latest = processor.get_latest_folder()
            >>> print(latest)  # '2024-05'
        """
        import asyncio
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        base_url = os.getenv('BASE_URL')
        return asyncio.run(get_latest_remote_folder(base_url))
    
    def get_available_folders(self) -> list:
        """
        Obtém lista de todas as pastas remotas disponíveis.
        
        Returns:
            list: Lista de nomes de pastas disponíveis (formato AAAA-MM)
            
        Examples:
            >>> processor = CNPJProcessor()
            >>> folders = processor.get_available_folders()
            >>> print(folders)  # ['2024-01', '2024-02', '2024-03', ...]
        """
        import asyncio
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        base_url = os.getenv('BASE_URL')
        return asyncio.run(get_remote_folders(base_url))

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
