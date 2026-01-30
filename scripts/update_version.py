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
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


def get_pypi_latest_version(package_name='cnpj-processor'):
    """Obtém a última versão publicada no PyPI."""
    try:
        url = f"https://pypi.org/pypi/{package_name}/json"
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            version = data['info']['version']
            print(f"📦 Última versão no PyPI: {version}")
            return version
    except (URLError, HTTPError, KeyError, json.JSONDecodeError) as e:
        print(f"⚠️  Não foi possível obter versão do PyPI: {e}")
        return None


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
        print("⚠️  Não foi possível obter a tag do git")
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


def update_pyproject_version(version):
    """Atualiza o arquivo pyproject.toml com a nova versão."""
    pyproject_file = Path("pyproject.toml")
    
    if not pyproject_file.exists():
        print(f"Erro: {pyproject_file} não encontrado")
        return False
    
    content = pyproject_file.read_text(encoding='utf-8')
    pattern = r'version = "[^"]*"'
    replacement = f'version = "{version}"'
    new_content = re.sub(pattern, replacement, content, count=1)
    
    if new_content == content:
        print("Aviso: Nenhuma alteração foi feita no pyproject.toml")
        return False
    
    pyproject_file.write_text(new_content, encoding='utf-8')
    print(f"✅ Versão atualizada para {version} em {pyproject_file}")
    return True


def update_version_file(version):
    """Atualiza o arquivo VERSION com a nova versão."""
    version_file = Path("VERSION")
    
    if not version_file.exists():
        print(f"Aviso: {version_file} não encontrado, criando...")
    
    version_file.write_text(version, encoding='utf-8')
    print(f"✅ Versão atualizada para {version} em {version_file}")
    return True


def validate_version(version):
    """Valida se a versão está no formato correto (X.Y.Z)."""
    pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)*$'
    return re.match(pattern, version) is not None


def call_build_and_publish():
    """Chama o script build_and_publish.py para fazer build e upload."""
    build_script = Path(__file__).parent / 'build_and_publish.py'
    
    if not build_script.exists():
        print(f"\n❌ Script não encontrado: {build_script}")
        return False
    
    print("\n" + "="*60)
    print("📦 Chamando build_and_publish.py")
    print("="*60)
    
    try:
        result = subprocess.run(
            [sys.executable, str(build_script), '--production', '--force'],
            check=True,
            capture_output=False,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Falha ao executar build_and_publish.py")
        return False


def git_commit_and_tag(version, files_changed):
    """Faz commit e cria tag no git."""
    print(f"\n{'='*60}")
    print("📝 Fazendo commit e criando tag no Git")
    print(f"{'='*60}")
    
    try:
        # Verificar se há mudanças para commitar
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        if not result.stdout.strip():
            print("⚠️  Nenhuma mudança para commitar")
            return True
        
        subprocess.run(['git', 'add'] + files_changed, check=True, capture_output=True)
        print(f"✓ Arquivos adicionados: {', '.join(files_changed)}")
        
        commit_msg = f"Bump version to v{version}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True)
        print(f"✓ Commit criado: {commit_msg}")
        
        tag_name = f"v{version}"
        # Verificar se a tag já existe
        tag_check = subprocess.run(['git', 'tag', '-l', tag_name], 
                                   capture_output=True, text=True)
        if tag_check.stdout.strip():
            print(f"⚠️  Tag {tag_name} já existe, removendo...")
            subprocess.run(['git', 'tag', '-d', tag_name], check=True, capture_output=True)
        
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
        # Verificar versão no PyPI primeiro
        pypi_version = get_pypi_latest_version()
        git_version = get_git_latest_tag()
        
        # Usar a maior versão entre PyPI e Git
        base_version = None
        if pypi_version and git_version:
            base_version = max(pypi_version, git_version, key=lambda v: tuple(map(int, v.split('.'))))
            print(f"🔄 Git: {git_version}, PyPI: {pypi_version}")
        elif pypi_version:
            base_version = pypi_version
            print(f"🔄 Versão base (PyPI): {base_version}")
        elif git_version:
            base_version = git_version
            print(f"🔄 Versão base (Git): {base_version}")
        else:
            print("Erro: Não foi possível obter versão do git ou PyPI")
            sys.exit(1)
        
        version = increment_version(base_version, args.increment)
        if not version:
            print(f"Erro: Não foi possível incrementar versão {base_version}")
            sys.exit(1)
        
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
    
    # Atualizar pyproject.toml
    if update_pyproject_version(api_version):
        files_changed.append("pyproject.toml")
    else:
        success = False
    
    # Atualizar VERSION
    if update_version_file(api_version):
        files_changed.append("VERSION")
    
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
        
        if not call_build_and_publish():
            print("\n⚠️  Versão atualizada e commitada, mas publicação falhou")
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
