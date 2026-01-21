"""
Módulo CLI para o CNPJ Processor.

Este módulo expõe todos os parâmetros como uma interface
de linha de comando instalável.
"""

import sys
from pathlib import Path

def main():
    """
    Entry point principal para o comando cnpj-processor.
    
    Carrega e executa a aplicação principal.
    """
    # Adicionar o diretório raiz ao path
    root_dir = Path(__file__).parent.parent
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))
    
    try:
        # Importar a função main do arquivo principal
        # O arquivo main.py deve estar no mesmo nível que o pacote cnpj_processor
        import main
        return main.main()
    except ImportError as e:
        print(f"Erro ao importar módulo principal: {e}")
        print(f"Certifique-se de que o arquivo main.py está acessível no PYTHONPATH")
        print(f"Diretório raiz: {root_dir}")
        sys.exit(1)

if __name__ == '__main__':
    sys.exit(main())
