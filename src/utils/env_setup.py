"""
Módulo para inicialização e configuração do ambiente CNPJ Processor.

Estratégia de carregamento de .env:
- Usa APENAS o .env do pacote instalado (valores necessários)
- Nunca carrega o .env do usuário para evitar conflitos
- Garante comportamento consistente e previsível da API
"""
import os
from pathlib import Path


DEFAULT_ENV_CONTENT = """# Configurações de diretórios
PATH_ZIP=dados-abertos-zip/
PATH_UNZIP=dados-abertos/
PATH_PARQUET=parquet/
FILE_DB_PARQUET=cnpj.duckdb
PATH_REMOTE_PARQUET=destino/

# URL base para download dos arquivos
BASE_URL=https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/

# Configurações de cache
CACHE_ENABLED=true
CACHE_PATH=cache/
"""


def get_package_env_path() -> Path:
    """
    Retorna o caminho do arquivo .env do pacote.
    Este arquivo contém as configurações necessárias para o cnpj-processor.
    
    O arquivo fica na raiz do pacote (mesmo nível do pyproject.toml).
    """
    # Encontrar a raiz do pacote: src/utils/env_setup.py -> raiz
    return Path(__file__).parent.parent.parent / '.env'


def ensure_package_env_file() -> bool:
    """
    Garante que o arquivo .env existe na raiz do pacote com as configurações necessárias.
    
    Returns:
        bool: True se o arquivo foi criado, False se já existia.
    """
    env_path = get_package_env_path()
    
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
        'BASE_URL': 'https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/',
        'CACHE_ENABLED': 'true',
        'CACHE_PATH': 'cache/'
    }


def load_env_with_defaults(working_dir: str = None, silent: bool = False):
    """
    Carrega APENAS o .env do pacote (não carrega o .env do usuário).
    
    Isso garante que:
    - A API sempre usa as configurações corretas
    - Não há conflitos com variáveis do .env do usuário
    - O comportamento é previsível e consistente
    
    Args:
        working_dir: Não é usado (mantido para compatibilidade). O .env carregado é sempre do pacote.
        silent: Se True, não exibe mensagens informativas.
    """
    from dotenv import load_dotenv
    
    # 1. Garantir que o .env do pacote existe
    ensure_package_env_file()
    
    # 2. Carregar .env do pacote (ÚNICA fonte de configuração para a API)
    package_env = get_package_env_path()
    if package_env.exists():
        load_dotenv(package_env, override=False)
    else:
        # Fallback: aplicar defaults em memória se o arquivo não existir
        defaults = get_default_env_vars()
        for key, default_value in defaults.items():
            if not os.getenv(key):
                os.environ[key] = default_value
    
    if not silent:
        print(f"✓ Configurações carregadas do pacote: {package_env}")
