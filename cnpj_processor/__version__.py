"""
Versonamento da API cnpj_processor para PyPI

A versão é obtida EXCLUSIVAMENTE das git tags do repositório.
Isso garante sincronização perfeita entre código e releases.
"""
import subprocess

__title__ = "CNPJ Processor"
__author__ = "Wesley Modanez Freitas"
__version__ = "4.0.9"
__license__ = "MIT"

def get_version():
    """Retorna a versão da API a partir das git tags."""
    try:
        result = subprocess.run(
            ['git', 'describe', '--tags', '--abbrev=0'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            # Remove 'v' prefix se existir
            return version[1:] if version.startswith('v') else version
    except Exception:
        pass
    
    raise RuntimeError(
        "Não foi possível obter versão do git. "
        "Execute: python scripts/release.py --major|--minor|--patch"
    )

# Expor versão como variável de módulo
try:
    __version__ = get_version()
except RuntimeError:
    __version__ = "4.0.6"

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
