"""
Módulo para inicialização e configuração do ambiente CNPJ Processor.

Estratégia de carregamento de .env:
- Primeiro, verifica se existe .env no diretório de trabalho atual
- Se não existir, copia o .env.example ou cria um com valores padrão
- Isso garante que o usuário final sempre tem o .env necessário
"""
import os
import shutil
from pathlib import Path


DEFAULT_ENV_CONTENT = """# Configurações de diretórios
PATH_ZIP=dados-abertos-zip/
PATH_UNZIP=dados-abertos/
PATH_PARQUET=parquet/
FILE_DB_PARQUET=cnpj.duckdb
PATH_REMOTE_PARQUET=destino/

# URL base para download dos arquivos - Nextcloud da Receita Federal
# Formato: https://domain/index.php/s/{TOKEN}?dir={PATH}
# O código detecta automaticamente se é Nextcloud e extrai o token
BASE_URL=https://arquivos.receitafederal.gov.br/index.php/s/gn672Ad4CF8N6TK?dir=/Dados/Cadastros/CNPJ

# Configurações de cache
CACHE_ENABLED=true
CACHE_PATH=cache/
"""


def get_package_env_path() -> Path:
    """
    Retorna o caminho do arquivo .env no pacote instalado.
    
    O arquivo fica protegido dentro da instalação do pacote.
    """
    # src/utils/env_setup.py -> src -> site-packages/cnpj_processor
    return Path(__file__).parent.parent.parent


def get_local_env_path() -> Path:
    """Retorna o caminho do .env no diretório de trabalho atual."""
    return Path.cwd() / '.env'


def ensure_local_env_file() -> bool:
    """
    Garante que existe um arquivo .env no diretório de trabalho do usuário.
    
    Estratégia:
    1. Se .env já existe localmente, usa o existente
    2. Tenta copiar .env do pacote instalado
    3. Se não conseguir, cria um novo com valores padrão
    
    Returns:
        bool: True se o arquivo foi criado/configurado, False se já existia.
    """
    local_env = get_local_env_path()
    
    # Se já existe, não faz nada
    if local_env.exists():
        return False
    
    # Tentar copiar .env do pacote
    try:
        package_root = get_package_env_path()
        package_env = package_root / '.env'
        package_env_example = package_root / '.env.example'
        
        # Preferência: copiar .env do pacote, fallback para .env.example
        if package_env.exists():
            shutil.copy(package_env, local_env)
            return True
        elif package_env_example.exists():
            shutil.copy(package_env_example, local_env)
            return True
    except Exception as e:
        # Se não conseguir copiar, cria um novo com valores padrão
        pass
    
    # Fallback: criar arquivo com valores padrão
    try:
        local_env.write_text(DEFAULT_ENV_CONTENT, encoding='utf-8')
        return True
    except Exception:
        # Se falhar completamente, o código ainda funciona com defaults em memória
        return False


def get_package_env_path_old() -> Path:
    """
    Retorna o caminho do arquivo .env.cnpj-processor em site-packages/cnpj_processor/.
    
    O arquivo fica protegido dentro da instalação do pacote, evitando deleções 
    acidentais e conflitos com .env do usuário.
    """
    # src/utils/env_setup.py -> src -> site-packages
    site_packages = Path(__file__).parent.parent.parent.parent
    return site_packages / 'cnpj_processor' / '.env.cnpj-processor'


def ensure_package_env_file() -> bool:
    """
    Garante que o arquivo .env existe na raiz do pacote com as configurações necessárias.
    (Mantido para compatibilidade)
    
    Returns:
        bool: True se o arquivo foi criado, False se já existia.
    """
    env_path = get_package_env_path_old()
    
    # Se já existe, não faz nada
    if env_path.exists():
        return False
    
    # Criar arquivo .env com valores padrão
    try:
        env_path.parent.mkdir(parents=True, exist_ok=True)
        env_path.write_text(DEFAULT_ENV_CONTENT, encoding='utf-8')
        return True
    except Exception:
        # Se falhar, o código ainda funciona com defaults em memória
        return False


def get_default_env_vars() -> dict:
    """
    Retorna um dicionário com as variáveis de ambiente padrão.
    
    Returns:
        dict: Dicionário com as variáveis de ambiente padrão.
    """
    return {
        'PATH_ZIP': 'dados-abertos-zip/',
        'PATH_UNZIP': 'dados-abertos/',
        'PATH_PARQUET': 'parquet/',
        'FILE_DB_PARQUET': 'cnpj.duckdb',
        'PATH_REMOTE_PARQUET': 'destino/',
        'BASE_URL': 'https://arquivos.receitafederal.gov.br/index.php/s/gn672Ad4CF8N6TK?dir=/Dados/Cadastros/CNPJ',
        'CACHE_ENABLED': 'true',
        'CACHE_PATH': 'cache/'
    }


def load_env_with_defaults(working_dir: str = None, silent: bool = True):
    """
    Carrega o .env local (ou cria um se não existir) e configura as variáveis de ambiente.
    
    Estratégia:
    1. Garante que existe .env no diretório de trabalho
    2. Carrega as variáveis usando python-dotenv
    3. Define defaults para variáveis que faltam
    
    Args:
        working_dir: Diretório de trabalho (não utilizado, mantido para compatibilidade)
        silent: Se True (padrão), não exibe mensagens informativas
    """
    from dotenv import load_dotenv
    
    # 1. Garantir que o .env local existe
    ensure_local_env_file()
    
    # 2. Carregar .env local
    local_env = get_local_env_path()
    if local_env.exists():
        load_dotenv(local_env, override=False)
    
    # 3. Garantir que variables críticas estão definidas
    defaults = get_default_env_vars()
    for key, value in defaults.items():
        if not os.getenv(key):
            os.environ[key] = value

