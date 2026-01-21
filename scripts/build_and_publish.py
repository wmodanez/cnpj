#!/usr/bin/env python3
"""
Script de automação para build e publicação do pacote cnpj-processor no PyPI.

Uso:
    python scripts/build_and_publish.py --clean          # Limpar builds anteriores
    python scripts/build_and_publish.py --build          # Fazer build
    python scripts/build_and_publish.py --check          # Verificar build
    python scripts/build_and_publish.py --test           # Upload para TestPyPI
    python scripts/build_and_publish.py --publish        # Upload para PyPI (PRODUÇÃO!)
    python scripts/build_and_publish.py --all            # Limpar + Build + Check + TestPyPI
    python scripts/build_and_publish.py --production     # Build + Check + PyPI (CUIDADO!)
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Executa um comando e retorna True se bem-sucedido."""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    print(f"Comando: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False, text=True)
        print(f"\n✅ {description} - SUCESSO")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} - FALHOU")
        print(f"Erro: {e}")
        return False
    except FileNotFoundError:
        print(f"\n❌ Comando não encontrado: {cmd[0]}")
        print("Certifique-se de que a ferramenta está instalada e no PATH")
        return False


def clean_build():
    """Remove diretórios de build anteriores."""
    dirs_to_remove = ['build', 'dist', '*.egg-info']
    removed = []
    
    print("\n🧹 Limpando builds anteriores...")
    
    # Remover diretórios específicos
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            removed.append(dir_name)
            print(f"  ✓ Removido: {dir_name}/")
    
    # Remover diretórios .egg-info
    for item in Path('.').glob('*.egg-info'):
        if item.is_dir():
            shutil.rmtree(item)
            removed.append(str(item))
            print(f"  ✓ Removido: {item}/")
    
    if removed:
        print(f"\n✅ Limpeza concluída: {len(removed)} itens removidos")
    else:
        print("\n✓ Nenhum arquivo de build encontrado")
    
    return True


def build_package():
    """Faz o build do pacote."""
    return run_command(
        [sys.executable, '-m', 'build'],
        "Construindo pacote"
    )


def check_package():
    """Verifica o pacote usando twine."""
    if not os.path.exists('dist'):
        print("\n❌ Diretório dist/ não encontrado. Execute --build primeiro.")
        return False
    
    dist_files = list(Path('dist').glob('*'))
    if not dist_files:
        print("\n❌ Nenhum arquivo encontrado em dist/. Execute --build primeiro.")
        return False
    
    return run_command(
        [sys.executable, '-m', 'twine', 'check', 'dist/*'],
        "Verificando pacote"
    )


def upload_testpypi():
    """Upload para TestPyPI."""
    if not os.path.exists('dist'):
        print("\n❌ Diretório dist/ não encontrado. Execute --build primeiro.")
        return False
    
    print("\n⚠️  Fazendo upload para TestPyPI (ambiente de testes)")
    return run_command(
        [sys.executable, '-m', 'twine', 'upload', '--repository', 'testpypi', 'dist/*'],
        "Upload para TestPyPI"
    )


def upload_pypi(force=False):
    """Upload para PyPI (PRODUÇÃO)."""
    if not os.path.exists('dist'):
        print("\n❌ Diretório dist/ não encontrado. Execute --build primeiro.")
        return False
    
    if not force:
        print("\n" + "="*60)
        print("⚠️  ATENÇÃO: UPLOAD PARA PYPI DE PRODUÇÃO!")
        print("="*60)
        response = input("Tem certeza que deseja fazer upload para o PyPI de PRODUÇÃO? (sim/não): ")
        
        if response.lower() not in ['sim', 'yes', 's', 'y']:
            print("❌ Upload cancelado pelo usuário")
            return False
    else:
        print("\n" + "="*60)
        print("⚠️  UPLOAD PARA PYPI DE PRODUÇÃO (--force)")
        print("="*60)
    
    return run_command(
        [sys.executable, '-m', 'twine', 'upload', 'dist/*'],
        "Upload para PyPI (PRODUÇÃO)"
    )


def check_dependencies():
    """Verifica se as dependências necessárias estão instaladas."""
    print("\n🔍 Verificando dependências...")
    
    required = {
        'build': 'build',
        'twine': 'twine',
    }
    
    missing = []
    for package, module in required.items():
        try:
            __import__(module)
            print(f"  ✓ {package} instalado")
        except ImportError:
            missing.append(package)
            print(f"  ✗ {package} NÃO instalado")
    
    if missing:
        print(f"\n❌ Dependências faltando: {', '.join(missing)}")
        print("\nInstale com:")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    print("\n✅ Todas as dependências instaladas")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Script de automação para build e publicação do pacote cnpj-processor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  # Workflow completo para teste
  python scripts/build_and_publish.py --all
  
  # Workflow para produção (CUIDADO!)
  python scripts/build_and_publish.py --production
  
  # Workflow para produção sem confirmação
  python scripts/build_and_publish.py --production --force
  
  # Apenas build e verificação
  python scripts/build_and_publish.py --clean --build --check
  
  # Upload manual após verificar os arquivos
  python scripts/build_and_publish.py --test
  python scripts/build_and_publish.py --publish --force
        """
    )
    
    parser.add_argument('--clean', action='store_true', 
                       help='Limpar builds anteriores')
    parser.add_argument('--build', action='store_true',
                       help='Fazer build do pacote')
    parser.add_argument('--check', action='store_true',
                       help='Verificar pacote com twine')
    parser.add_argument('--test', action='store_true',
                       help='Upload para TestPyPI')
    parser.add_argument('--publish', action='store_true',
                       help='Upload para PyPI (PRODUÇÃO)')
    parser.add_argument('--all', action='store_true',
                       help='Executar: clean + build + check + test')
    parser.add_argument('--production', action='store_true',
                       help='Executar: clean + build + check + publish (CUIDADO!)')
    parser.add_argument('--force', action='store_true',
                       help='Pular confirmação de upload para PyPI (use com cuidado!)')
    
    args = parser.parse_args()
    
    # Se nenhum argumento, mostrar help
    if not any(vars(args).values()):
        parser.print_help()
        return 0
    
    print("="*60)
    print("🚀 CNPJ Processor - Build & Publish")
    print("="*60)
    
    # Verificar dependências
    if not check_dependencies():
        return 1
    
    success = True
    
    # Workflow --all
    if args.all:
        args.clean = True
        args.build = True
        args.check = True
        args.test = True
    
    # Workflow --production
    if args.production:
        args.clean = True
        args.build = True
        args.check = True
        args.publish = True
    
    # Executar etapas
    if args.clean:
        success = clean_build() and success
    
    if args.build and success:
        success = build_package() and success
    
    if args.check and success:
        success = check_package() and success
    
    if args.test and success:
        success = upload_testpypi() and success
    
    if args.publish and success:
        success = upload_pypi(force=args.force) and success
    
    # Resultado final
    print("\n" + "="*60)
    if success:
        print("✅ Todas as operações concluídas com sucesso!")
        
        if args.test:
            print("\n📦 Pacote publicado no TestPyPI!")
            print("Teste a instalação com:")
            print("  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ cnpj-processor")
        
        if args.publish:
            print("\n🎉 Pacote publicado no PyPI!")
            print("Instale com:")
            print("  pip install cnpj-processor")
    else:
        print("❌ Algumas operações falharam. Verifique os logs acima.")
    print("="*60)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
