"""
Entry point module for cnpj-processor package.
This module provides the main() function that serves as the console script entry point.
"""
import sys
import os

# Importar a função main do main.py raiz
import sys
import os

# Adicionar o diretório raiz ao path para importar o main.py da raiz
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from main import main as _main

def main():
    """
    Entry point para o comando cnpj-processor.
    """
    return _main()

if __name__ == '__main__':
    sys.exit(main() or 0)
