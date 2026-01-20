"""
Módulo CLI para o CNPJ Processor.

Este módulo expõe todos os parâmetros do main.py como uma interface
de linha de comando instalável.
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao path para importar main
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

def main():
    """
    Entry point principal para o comando cnpj-processor.
    
    Redireciona para a função main() do main.py, preservando
    todos os argumentos e funcionalidades.
    """
    # Importar e executar main
    from main import main as main_function
    return main_function()

if __name__ == '__main__':
    sys.exit(main())
