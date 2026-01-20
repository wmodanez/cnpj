#!/usr/bin/env python3
"""
Script para atualizar a versão do projeto CNPJ e publicar automaticamente

Uso básico:
    python scripts/update_version.py 3.8.0
    python scripts/update_version.py 3.8.0 --publish         # Atualizar e publicar no PyPI
    python scripts/update_version.py --auto --publish        # Workflow completo automático
    
Uso avançado:
    python scripts/update_version.py 3.8.0 --api-only
    python scripts/update_version.py 3.8.0 --api-version 3.8.1
    python scripts/update_version.py --auto --increment minor --publish

Nota: TestPyPI deve ser testado manualmente com:
    python scripts/build_and_publish.py --test
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def get_git_latest_tag():
    """Obtém a tag mais recente do git."""
    try:
        result = subprocess.run(
            ['git', 'describe', '--tags', '--abbrev=0'],
            capture_output=True,
            text=True,
            check=True
        )
        tag = result.stdout.strip()
        if tag.startswith('v'):
            tag = tag[1:]
        return tag
    except subprocess.CalledProcessError:
        print("Erro: Não foi possível obter a tag do git")
        return None


def increment_version(version, part='patch'):
    """Incrementa a versão (major, minor ou patch)."""
    try:
        major, minor, patch = map(int, version.split('.'))
        
        if part == 'major':
            major += 1
            minor = 0
            patch = 0
        elif part == 'minor':
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
        
        return f"{major}.{minor}.{patch}"
    except:
        return None


def update_api_version(version):
    """Atualiza o arquivo cnpj_processor/__version__.py com a nova versão."""
    version_file = Path("cnpj_processor/__version__.py")
    
    if not version_file.exists():
        print(f"Erro: {version_file} não encontrado")
        return False
    
    content = version_file.read_text(encoding='utf-8')
    pattern = r'__version__ = "[^"]*"'
    replacement = f'__version__ = "{version}"'
    new_content = re.sub(pattern, replacement, content)
    
    if new_content == content:
        print("Aviso: Nenhuma alteração foi feita no arquivo de versão da API")
        return False
    
    version_file.write_text(new_content, encoding='utf-8')
    print(f"✅ Versão da API atualizada para {version} em {version_file}")
    return True


def update_project_version(version):
    """Atualiza o arquivo src/__version__.py com a nova versão."""
    version_file = Path("src/__version__.py")
    
    if not version_file.exists():
        print(f"Erro: {version_file} não encontrado")
        return False
    
    content = version_file.read_text(encoding='utf-8')
    pattern = r'__version_fallback__ = "[^"]*"'
    replacement = f'__version_fallback__ = "{version}"'
    new_content = re.sub(pattern, replacement, content)
    
    if new_content == content:
        print("Aviso: Nenhuma alteração foi feita no arquivo de versão do projeto")
        return False
    
    version_file.write_text(new_content, encoding='utf-8')
    print(f"✅ Versão do projeto atualizada para {version} em {version_file}")
    return True


def validate_version(version):
    """Valida se a versão está no formato correto (X.Y.Z)."""
    pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)*$'
    return re.match(pattern, version) is not None


def run_command(cmd, description):
    """Executa um comando e retorna True se bem-sucedido."""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    print(f"Comando: {' '.join(cmd)}")
    print()
    
    try:
        subprocess.run(cmd, check=True, capture_output=False, text=True)
        print(f"\n✅ {description} - SUCESSO")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} - FALHOU")
        print(f"Erro: {e}")
        return False
    except FileNotFoundError:
        print(f"\n❌ Comando não encontrado: {cmd[0]}")
        return False


def clean_build():
    """Remove diretórios de build anteriores."""
    print("\n🧹 Limpando builds anteriores...")
    removed = []
    
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            removed.append(dir_name)
            print(f"  ✓ Removido: {dir_name}/")
    
    for item in Path('.').glob('*.egg-info'):
        if item.is_dir():
            shutil.rmtree(item)
            removed.append(str(item))
            print(f"  ✓ Removido: {item}/")
    
    if removed:
        print(f"\n✅ Limpeza concluída: {len(removed)} itens removidos")
    return True


def build_package():
    """Faz o build do pacote."""
    return run_command([sys.executable, '-m', 'build'], "Construindo pacote")


def check_package():
    """Verifica o pacote usando twine."""
    if not os.path.exists('dist'):
        print("\n❌ Diretório dist/ não encontrado.")
        return False
    
    dist_files = list(Path('dist').glob('*'))
    if not dist_files:
        print("\n❌ Nenhum arquivo encontrado em dist/.")
        return False
    
    return run_command([sys.executable, '-m', 'twine', 'check', 'dist/*'], "Verificando pacote")


def upload_pypi():
    """Upload para PyPI (PRODUÇÃO)."""
    if not os.path.exists('dist'):
        print("\n❌ Diretório dist/ não encontrado.")
        return False
    
    print("\n" + "="*60)
    print("⚠️  ATENÇÃO: UPLOAD PARA PYPI DE PRODUÇÃO!")
    print("="*60)
    response = input("Tem certeza que deseja fazer upload para o PyPI de PRODUÇÃO? (sim/não): ")
    
    if response.lower() not in ['sim', 'yes', 's', 'y']:
        print("❌ Upload cancelado pelo usuário")
        return False
    
    return run_command([sys.executable, '-m', 'twine', 'upload', 'dist/*'], "Upload para PyPI (PRODUÇÃO)")


def check_dependencies():
    """Verifica se as dependências necessárias estão instaladas."""
    print("\n🔍 Verificando dependências de publicação...")
    
    required = {'build': 'build', 'twine': 'twine'}
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
        print(f"Instale com: pip install {' '.join(missing)}")
        return False
    
    print("\n✅ Todas as dependências instaladas")
    return True


def git_commit_and_tag(version, files_changed):
    """Faz commit e cria tag no git."""
    print(f"\n{'='*60}")
    print("📝 Fazendo commit e criando tag no Git")
    print(f"{'='*60}")
    
    try:
        subprocess.run(['git', 'add'] + files_changed, check=True, capture_output=True)
        print(f"✓ Arquivos adicionados: {', '.join(files_changed)}")
        
        commit_msg = f"Bump version to v{version}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True)
        print(f"✓ Commit criado: {commit_msg}")
        
        tag_name = f"v{version}"
        subprocess.run(['git', 'tag', tag_name], check=True, capture_output=True)
        print(f"✓ Tag criada: {tag_name}")
        
        print("\n✅ Commit e tag criados com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro no git: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Atualizar versão do projeto CNPJ e publicar no PyPI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Atualizar versão apenas (sem publicar)
  python scripts/update_version.py 3.8.0
  
  # Atualizar e publicar no PyPI automaticamente
  python scripts/update_version.py 3.8.0 --publish
  
  # Workflow completo automático (incrementa patch + publica)
  python scripts/update_version.py --auto --publish
  
  # Incrementar minor version automaticamente
  python scripts/update_version.py --auto --increment minor --publish
  
  # Testar no TestPyPI manualmente (depois de atualizar versão)
  python scripts/build_and_publish.py --test
        """
    )
    parser.add_argument('version', nargs='?', help='Nova versão (formato X.Y.Z)')
    parser.add_argument('--auto', action='store_true', 
                       help='Usar tag mais recente do git e incrementar')
    parser.add_argument('--increment', choices=['major', 'minor', 'patch'], default='patch',
                       help='Tipo de incremento para --auto (padrão: patch)')
    parser.add_argument('--publish', action='store_true',
                       help='Publicar automaticamente no PyPI após atualizar versão')
    parser.add_argument('--api-only', action='store_true', 
                       help='Atualizar apenas a versão da API')
    parser.add_argument('--api-version', type=str, 
                       help='Versão específica para a API (diferente do projeto)')
    
    args = parser.parse_args()
    
    # Determinar versão principal
    if args.auto:
        base_version = get_git_latest_tag()
        if not base_version:
            print("Erro: Não foi possível obter versão do git")
            sys.exit(1)
        
        version = increment_version(base_version, args.increment)
        if not version:
            print(f"Erro: Não foi possível incrementar versão {base_version}")
            sys.exit(1)
        
        print(f"🔄 Versão anterior: {base_version}")
        print(f"🔄 Nova versão ({args.increment}): {version}\n")
    elif args.version:
        version = args.version
    else:
        print("Erro: Especifique uma versão ou use --auto")
        parser.print_help()
        sys.exit(1)
    
    if not validate_version(version):
        print(f"Erro: Versão '{version}' não está no formato válido (X.Y.Z)")
        sys.exit(1)
    
    # Determinar versão da API
    api_version = args.api_version if args.api_version else version
    if not validate_version(api_version):
        print(f"Erro: Versão da API '{api_version}' não está no formato válido (X.Y.Z)")
        sys.exit(1)
    
    print("="*60)
    print("🚀 CNPJ Processor - Update & Publish")
    print("="*60)
    print(f"\nAtualizando versões:")
    if not args.api_only:
        print(f"  - Projeto (src): {version}")
    print(f"  - API (cnpj_processor): {api_version}")
    print()
    
    success = True
    files_changed = []
    
    # Atualizar versão da API
    if update_api_version(api_version):
        files_changed.append("cnpj_processor/__version__.py")
    else:
        success = False
    
    # Atualizar versão do projeto (a menos que seja --api-only)
    if not args.api_only:
        if update_project_version(version):
            files_changed.append("src/__version__.py")
        else:
            success = False
    
    if not success or not files_changed:
        print("\n❌ Falha ao atualizar versão")
        sys.exit(1)
    
    print("\n✅ Versão(ões) atualizada(s) com sucesso!")
    
    # Fazer commit e tag
    if not git_commit_and_tag(api_version, files_changed):
        print("\n⚠️  Arquivos atualizados mas commit/tag falharam")
        sys.exit(1)
    
    # Publicar no PyPI se solicitado
    if args.publish:
        print("\n" + "="*60)
        print("📦 Iniciando publicação no PyPI")
        print("="*60)
        
        if not check_dependencies():
            print("\n⚠️  Versão atualizada e commitada, mas publicação cancelada")
            print("Instale as dependências e use: python scripts/build_and_publish.py --production")
            sys.exit(1)
        
        # Clean, build, check, upload
        if not clean_build():
            sys.exit(1)
        if not build_package():
            sys.exit(1)
        if not check_package():
            sys.exit(1)
        if not upload_pypi():
            print("\n⚠️  Versão atualizada e commitada, mas upload cancelado")
            print("Para publicar depois: python scripts/build_and_publish.py --production")
            sys.exit(1)
        
        print("\n" + "="*60)
        print("🎉 SUCESSO COMPLETO!")
        print("="*60)
        print(f"\n✅ Versão {api_version} publicada no PyPI!")
        print(f"\n📤 Não esqueça de enviar ao repositório:")
        print(f"   git push origin develop --tags")
        print(f"\n📦 Para instalar:")
        print(f"   pip install cnpj-processor=={api_version}")
    else:
        print(f"\n📋 Próximos passos:")
        print(f"1. Push: git push origin develop --tags")
        print(f"2. Publicar: python scripts/update_version.py {api_version} --publish")
        print(f"   ou: python scripts/build_and_publish.py --production")
    
    if args.api_version:
        print(f"\n⚠️  Nota: Projeto em v{version}, mas API em v{api_version}")


if __name__ == "__main__":
    main()
