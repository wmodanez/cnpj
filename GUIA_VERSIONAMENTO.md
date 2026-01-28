# Guia Completo: Versionamento e Publicação no PyPI

> **Última atualização**: v3.7.0 (Unificado)  
> Este guia consolida o versionamento e publicação em um único documento.

## 📋 Índice

1. [Estrutura do Pacote](#-estrutura-do-pacote)
2. [Como Usar Após Instalação](#-como-usar-o-pacote-após-instalação)
3. [Versionamento](#-versionamento)
4. [Processo de Publicação](#-processo-de-publicação)
5. [Desenvolvimento](#-comandos-úteis-de-desenvolvimento)
6. [Checklist](#-checklist-de-publicação)
7. [Troubleshooting](#-solução-de-problemas)

---

## 📦 Estrutura do Pacote

O projeto foi estruturado para publicação no PyPI mantendo a pasta `src/` original:

```folder
cnpj/
├── cnpj_processor/          # Pacote público (wrapper)
│   ├── __init__.py         # Exporta toda funcionalidade
│   ├── __version__.py      # Re-exporta versão
│   └── cli.py             # Entry point CLI
├── src/                    # Código fonte original
│   ├── Entity/
│   ├── process/
│   ├── utils/
│   └── __version__.py      # Versão sincronizada
├── setup.py               # Configuração setuptools
├── pyproject.toml         # Configuração moderna
├── MANIFEST.in           # Arquivos inclusos no build
└── scripts/
    ├── update_version.py  # Automatiza versioning + publicação
    └── build_and_publish.py # Alternativa manual
```

---

## 🚀 Como Usar o Pacote Após Instalação

### Instalação via pip

```bash
# Do PyPI (após publicação)
pip install cnpj-processor

# Do TestPyPI (para testes)
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ cnpj-processor
```

### Uso Programático

```python
# Importar o pacote
from cnpj_processor import CNPJProcessor

# Criar processador
processor = CNPJProcessor()

# Obter pasta mais recente
latest = processor.get_latest_folder()
print(f"Pasta mais recente: {latest}")

# Baixar arquivos
processor.download_latest(tipos=['empresas', 'estabelecimentos'])

# Criar banco de dados
processor.create_database('parquet/2024-05', 'cnpj.duckdb')
```

### Importar Classes Específicas

```python
# Importar processadores específicos
from cnpj_processor import (
    EmpresaProcessor,
    EstabelecimentoProcessor,
    SimplesProcessor,
    SocioProcessor,
    PainelProcessor
)

# Importar entidades
from cnpj_processor import (
    Empresa,
    Estabelecimento,
    Simples,
    Socio,
    Painel
)

# Importar utilitários
from cnpj_processor import (
    config,
    download_multiple_files,
    get_latest_remote_folder
)
```

### Uso via CLI

Todos os parâmetros do `main.py` estão disponíveis:

```bash
# Ver ajuda
cnpj-processor --help

# Processar tudo
cnpj-processor

# Processar tipos específicos
cnpj-processor --types empresas estabelecimentos

# Download com pasta específica
cnpj-processor --step download --remote-folder 2024-05

# Processamento completo com economia de espaço
cnpj-processor --delete-zips-after-extract --cleanup-all-after-db

# Processar painel filtrado
cnpj-processor --processar-painel --painel-uf SP --painel-situacao 2

# Ver pasta mais recente
cnpj-processor --show-latest-folder
```

---

## 📌 Versionamento

### Como Funciona

O sistema detecta automaticamente a versão baseado nas **tags do git**, com fallback para `src/__version__.py`:

1. **Git Tags** (prioridade alta) - Obtém da tag mais recente
2. **Fallback** (prioridade baixa) - Usa a versão definida em `src/__version__.py`

### Versioning Strategy (SemVer)

O projeto segue o padrão `MAJOR.MINOR.PATCH`:

```version
3.7.0
│ │ │
│ │ └─ PATCH: Bug fixes, correções menores
│ └─── MINOR: Novas funcionalidades (compatível com anterior)
└───── MAJOR: Breaking changes (incompatível com anterior)
```

**Exemplos de quando incrementar:**

- **PATCH** (3.7.0 → 3.7.1): Correção de bugs, melhorias de performance
- **MINOR** (3.7.0 → 3.8.0): Novas funcionalidades, parâmetros opcionais
- **MAJOR** (3.7.0 → 4.0.0): Remoção/mudança de APIs, quebra de compatibilidade

### Verificar Versão Atual

```bash
# Via Python
python -c "from src.__version__ import get_version; print(get_version())"

# Via Git
git describe --tags --abbrev=0

# Via CLI instalado
cnpj-processor --version
```

### Listar e Gerenciar Tags

```bash
# Listar todas as tags
git tag --list

# Listar tags ordenadas por versão
git tag --list | sort -V

# Ver detalhes de uma tag
git show v3.2.0

# Ver tag mais recente
git describe --tags --abbrev=0

# Deletar tag (CUIDADO!)
git tag -d v3.2.0        # Local
git push origin :v3.2.0  # Remoto
```

---

## 📝 Processo de Publicação

### ⚡ Opção Recomendada: Script Automático (v3.7.0+)

**O script `update_version.py` unifica TODAS as operações em um único comando:**

```bash
# Opção 1: Auto-incrementar patch e publicar (MAIS COMUM)
python scripts/update_version.py --auto --publish

# Opção 2: Versão específica com publicação
python scripts/update_version.py 3.8.0 --publish

# Opção 3: Apenas atualizar versão (sem publicar)
python scripts/update_version.py 3.8.0

# Opção 4: Ver ajuda e exemplos
python scripts/update_version.py --help
```

**O que o script faz automaticamente:**

1. ✅ Detecta última versão git (ou usa fallback)
2. ✅ Incrementa versão (patch por padrão com `--auto`)
3. ✅ Atualiza `cnpj_processor/__version__.py`
4. ✅ Atualiza `src/__version__.py`
5. ✅ Faz commit git: "Bump version to v3.X.X"
6. ✅ Cria tag git: v3.X.X
7. ✅ Limpa build anterior
8. ✅ Compila pacote (.whl + .tar.gz)
9. ✅ Verifica com twine
10. ✅ **Publica no PyPI** (se `--publish` usado)

**Após execução:**

```bash
# Fazer push das tags para GitHub
git push origin develop --tags
```

### Opção Alternativa: Script Manual (casos especiais)

Use `build_and_publish.py` apenas para **testes em TestPyPI** ou quando precisar de controle granular:

```bash
# 1. Atualizar versão manualmente
python scripts/update_version.py 3.8.0

# 2. Testar build localmente
python scripts/build_and_publish.py --clean --build --check

# 3. Testar em TestPyPI (opcional)
python scripts/build_and_publish.py --test

# 4. Publicar no PyPI
python scripts/build_and_publish.py --production

# 5. Versionar no git
git add .
git commit -m "Release v3.8.0"
git tag v3.8.0
git push origin develop --tags
```

### Workflow Desenvolvimento Normal

```bash
# 1. Fazer commits das suas alterações
git add .
git commit -m "Implementar nova funcionalidade X"

# 2. Quando pronto para release, publicar
python scripts/update_version.py --auto --publish

# 3. Sincronizar tags
git push origin develop --tags

# 4. Pronto! Versão está no PyPI
```

---

## 🔧 Comandos Úteis de Desenvolvimento

### Instalar em Modo Desenvolvimento

```bash
# Instalar localmente em modo editável
pip install -e .

# Com dependências de desenvolvimento
pip install -e ".[dev]"
```

### Testar Importação Local

```python
# Testar imports sem instalar
import sys
sys.path.insert(0, 'caminho/para/cnpj')

from cnpj_processor import CNPJProcessor
processor = CNPJProcessor()
```

### Verificar Estrutura do Pacote

```bash
# Ver conteúdo do arquivo .whl
python -m zipfile -l dist/cnpj_processor-3.1.4-py3-none-any.whl

# Ver conteúdo do .tar.gz
tar -tzf dist/cnpj_processor-3.6.0.tar.gz
```

### Limpeza e Rebuild

```bash
# Limpar builds antigos
rm -rf build/ dist/ *.egg-info

# Limpar cache do pip
pip cache purge

# Desinstalar pacote local
pip uninstall cnpj-processor -y

# Fazer rebuild completo
python -m build

# Verificar antes de publicar
twine check dist/*
```

### Reinstalar em Modo Desenvolvimento (Com Limpeza Completa)

```bash
# Quando o cache causa problemas com importações antigas
cd /caminho/para/cnpj

# 1. Desinstalar versão anterior
pip uninstall cnpj-processor -y

# 2. Limpar cache do pip completamente
pip cache purge

# 3. Reinstalar em modo desenvolvimento (editable)
python -m pip install -e .

# 4. Verificar instalação
pip show cnpj-processor

# 5. Testar import
python -c "from cnpj_processor import CNPJProcessor; print('OK')"
```

## 📋 Checklist de Publicação

### ✅ Workflow Simplificado (Recomendado)

Use `update_version.py --auto --publish`:

- [ ] Fazer commits de todas as alterações
- [ ] Executar: `python scripts/update_version.py --auto --publish`
- [ ] Confirmar publicação quando solicitado
- [ ] Executar: `git push origin develop --tags`
- [ ] Verificar no PyPI: <https://pypi.org/project/cnpj-processor/>
- [ ] Testar instalação: `pip install cnpj-processor --upgrade`
- [ ] Testar CLI: `cnpj-processor --version`

### ✅ Workflow Manual (Se Necessário)

Para controle total ou testes em TestPyPI:

- [ ] Atualizar versão: `python scripts/update_version.py X.Y.Z`
- [ ] Testar build localmente: `python scripts/build_and_publish.py --check`
- [ ] (Opcional) Testar em TestPyPI: `python scripts/build_and_publish.py --test`
- [ ] Publicar: `python scripts/build_and_publish.py --production`
- [ ] Criar tag git: `git tag vX.Y.Z`
- [ ] Push com tags: `git push origin develop --tags`
- [ ] Atualizar documentação se necessário

---

## 🐛 Solução de Problemas

### Erro: "File already exists"

Versões no PyPI não podem ser substituídas. Incremente a versão:

```bash
python scripts/update_version.py 3.2.1
python scripts/build_and_publish.py --clean --build --publish
```

### Erro: Import não funciona após instalação

Verifique se instalou do índice correto:

```bash
# Ver onde o pacote foi instalado
pip show cnpj-processor

# Reinstalar forçando com limpeza completa
pip uninstall cnpj-processor -y
pip cache purge
pip install -e .

# Testar import
python -c "from cnpj_processor import CNPJProcessor; print('OK')"
```

### CLI não é reconhecido

Verifique se o diretório Scripts está no PATH:

```bash
# Windows
where cnpj-processor

# Linux/Mac
which cnpj-processor

# Ou use via Python
python -m cnpj_processor.cli --help
```

### Erro: Tag já existe

Se a tag já foi criada localmente:

```bash
# Deletar tag local
git tag -d v3.7.0

# Deletar tag remota
git push origin --delete v3.7.0

# Agora criar novamente
python scripts/update_version.py 3.7.0 --publish
```

### Sistema não detecta nova tag

```bash
# Recarregar o módulo Python
python -c "import importlib; import src.__version__; importlib.reload(src.__version__); from src.__version__ import get_version; print(get_version())"

# Verificar git localmente
git describe --tags --abbrev=0

# Listar tags em ordem
git tag --list | sort -V
```

---

## 🔐 Autenticação PyPI

Configure suas credenciais antes de publicar:

### Opção 1: Arquivo `.pypirc`

```bash
# Criar arquivo ~/.pypirc (Linux/Mac) ou %USERPROFILE%\.pypirc (Windows)
[pypi]
username = __token__
password = pypi-SEU_TOKEN_AQUI

[testpypi]
username = __token__
password = pypi-SEU_TOKEN_TEST_AQUI
```

### Opção 2: Variáveis de Ambiente

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-SEU_TOKEN_AQUI
```

> 💡 **Dica**: Gere tokens em <https://pypi.org/manage/account/tokens/>

---

## ✅ Exemplos Práticos

### Exemplo 1: Publicação Automática Simples

```bash
# 1. Fazer commit das alterações
git add .
git commit -m "Implementar novo recurso X"

# 2. Publicar (um comando!)
python scripts/update_version.py --auto --publish
# Irá:
#   ✅ Auto-incrementar versão (3.7.0 → 3.7.1)
#   ✅ Atualizar ambos os arquivos de versão
#   ✅ Fazer commit git
#   ✅ Criar tag git (v3.7.1)
#   ✅ Compilar pacote
#   ✅ Verificar com twine
#   ✅ Publicar no PyPI

# 3. Sincronizar tags com GitHub
git push origin develop --tags

# 4. Testar instalação
pip install cnpj-processor --upgrade
cnpj-processor --version  # Output: v3.7.1
```

### Exemplo 2: Publicação com Versão Específica

```bash
# Publicar versão exata
python scripts/update_version.py 3.8.0 --publish

# Sincronizar
git push origin develop --tags

# Verificar no PyPI
pip install cnpj-processor==3.8.0
```

### Exemplo 3: Apenas Atualizar Versão (Sem Publicar)

```bash
# Apenas versioning (útil para branches de desenvolvimento)
python scripts/update_version.py 3.8.0

# Fazer commit e push normalmente
git add .
git commit -m "Versão 3.8.0 (preparação)"
git push origin develop
```

### Exemplo 4: Testar em TestPyPI Antes de Publicar

```bash
# 1. Atualizar versão
python scripts/update_version.py 3.8.0

# 2. Testar build
python scripts/build_and_publish.py --clean --build --check

# 3. Publicar em TestPyPI
python scripts/build_and_publish.py --test

# 4. Instalar de TestPyPI para testar
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ cnpj-processor==3.8.0

# 5. Se tudo OK, publicar no PyPI
python scripts/build_and_publish.py --production

# 6. Versionar git
git add .
git commit -m "Release v3.8.0"
git tag v3.8.0
git push origin develop --tags
```

---

## 📚 Recursos

- **PyPI**: <https://pypi.org/project/cnpj-processor/>
- **TestPyPI**: <https://test.pypi.org/project/cnpj-processor/>
- **GitHub**: <https://github.com/wmodanez/cnpj>
- **Python Packaging**: <https://packaging.python.org/>
- **Semantic Versioning**: <https://semver.org/>

---

## 💡 Dicas e Boas Práticas

✅ **Use `--auto --publish`** para a maioria das releases  
✅ **Sempre faça commit antes de versioning** para não perder código  
✅ **Teste em TestPyPI** antes da primeira publicação de uma versão major  
✅ **Mantenha CHANGELOG atualizado** junto com releases  
✅ **Use commits atômicos** para facilitar rastreamento de versões  
✅ **Sincronize tags com `--tags`** para manter histórico consistente  

⚠️ **Evite**: Deletar tags publicadas no PyPI (irreversível)  
⚠️ **Evite**: Forçar push sem tags (`git push -f`)  
⚠️ **Evite**: Publicar sem testar localmente antes  

---

**Última atualização**: Janeiro 2026 | v3.7.0 (Unificado)
