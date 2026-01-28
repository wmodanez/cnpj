"""
MÓDULO INTERNO: src

AVISO IMPORTANTE:
================

Este módulo é um componente INTERNO do cnpj-processor. 

Usuários e desenvolvedores DEVEM importar através do wrapper público:
    from cnpj_processor import ...

NÃO importar diretamente de src:
    ✗ from src.config import config
    ✗ from src.Entity.Empresa import Empresa
    
SIM, usar o wrapper público:
    ✓ from cnpj_processor import config
    ✓ from cnpj_processor import Empresa

O acesso direto ao src pode quebrar a abstração da arquitetura e
cause problemas de manutenibilidade do projeto.

Para mais detalhes, consulte a documentação de arquitetura do projeto.
"""

import sys
import inspect
import warnings

# Detectar se está sendo importado de fora do projeto
def _check_direct_import():
    """Valida se o import está ocorrendo através do wrapper apropriado."""
    frame = inspect.currentframe()
    
    try:
        # Obter o frame do chamador
        caller_frame = frame.f_back
        caller_file = caller_frame.f_globals.get('__file__', '')
        
        # Permitir imports internos dentro do próprio src
        if 'src' in caller_file or 'cnpj_processor' in caller_file:
            return
        
        # Permitir imports dentro do próprio main.py (já corrigido)
        if 'main.py' in caller_file:
            # Se ainda está tentando importar direto, avisar
            # Após correção, esta verificação será removida
            pass
            
        # Permitir imports de testes
        if 'test' in caller_file or 'pytest' in caller_file:
            return
        
        # Avisar sobre imports diretos de fora
        if caller_file and not any(x in caller_file for x in 
            ['cnpj_processor', '__init__', 'site-packages']):
            warnings.warn(
                f"\n{'='*60}\n"
                f"AVISO: Import direto de 'src' detectado!\n"
                f"Arquivo: {caller_file}\n"
                f"\n"
                f"Use o wrapper público 'cnpj_processor' em vez disso:\n"
                f"  from cnpj_processor import ...\n"
                f"{'='*60}\n",
                DeprecationWarning,
                stacklevel=3
            )
    finally:
        del frame

# Executar verificação
_check_direct_import()

__all__ = [] 