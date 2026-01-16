# 📦 Guia de Publicação no PyPI

Este guia detalha o processo completo para publicar o pacote `cnpj-processor` no Python Package Index (PyPI).

## 📋 Índice

- [Pré-requisitos](#pré-requisitos)
- [Configuração Inicial](#configuração-inicial)
- [Build do Pacote](#build-do-pacote)
- [Testes Locais](#testes-locais)
- [Publicação no TestPyPI](#publicação-no-testpypi)
- [Publicação no PyPI](#publicação-no-pypi)
- [Checklist de Publicação](#checklist-de-publicação)
- [Solução de Problemas](#solução-de-problemas)

## 🔧 Pré-requisitos

### 1. Instalar Ferramentas de Build

```bash
# Instalar build e twine
pip install --upgrade pip
pip install --upgrade build twine
```

### 2. Criar Contas

1. **PyPI Principal**: https://pypi.org/account/register/
2. **TestPyPI** (ambiente de testes): https://test.pypi.org/account/register/

### 3. Configurar 2FA (Two-Factor Authentication)

⚠️ **OBRIGATÓRIO** para publicar no PyPI desde 2023.

1. Acesse Account Settings em ambas as contas
2. Ative 2FA (use app como Google Authenticator, Authy, etc.)
3. Salve os códigos de recuperação em local seguro

### 4. Criar API Tokens

**No PyPI:**
1. Vá em Account Settings > API tokens
2. Clique em "Add API token"
3. Nome: `cnpj-processor-upload`
4. Escopo: 
   - Primeiro upload: "Entire account"
   - Uploads subsequentes: "Project: cnpj-processor" (mais seguro)
5. Copie o token (começa com `pypi-`)

**No TestPyPI:**
- Repita o processo acima

### 5. Configurar Credenciais

**Opção A: Arquivo .pypirc (Recomendado)**

```bash
# Linux/Mac
cp .pypirc.example ~/.pypirc
chmod 600 ~/.pypirc  # Proteger o arquivo

# Windows PowerShell
Copy-Item .pypirc.example $env:USERPROFILE\.pypirc
```

Edite `~/.pypirc` ou `%USERPROFILE%\.pypirc` e adicione seus tokens:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-SEU_TOKEN_PYPI_AQUI

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-SEU_TOKEN_TESTPYPI_AQUI
```

**Opção B: Variáveis de Ambiente**

```bash
# Linux/Mac
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-SEU_TOKEN_AQUI

# Windows PowerShell
$env:TWINE_USERNAME="__token__"
$env:TWINE_PASSWORD="pypi-SEU_TOKEN_AQUI"
```

## 🏗️ Build do Pacote

### 1. Atualizar Versão

Edite `pyproject.toml`:
```toml
[project]
version = "3.5.0"  # Atualize conforme semantic versioning
```

Ou use o script automático:
```bash
python scripts/release.py --patch  # 3.5.0 -> 3.5.1
python scripts/release.py --minor  # 3.5.0 -> 3.6.0
python scripts/release.py --major  # 3.5.0 -> 4.0.0
python scripts/release.py 3.6.0    # Versão específica
```

### 2. Limpar Builds Anteriores

```bash
# Linux/Mac
rm -rf build/ dist/ *.egg-info

# Windows PowerShell
Remove-Item -Recurse -Force build, dist, *.egg-info -ErrorAction SilentlyContinue
```

### 3. Buildar o Pacote

```bash
python -m build
```

Isso criará:
- `dist/cnpj_processor-3.5.0-py3-none-any.whl` (wheel)
- `dist/cnpj-processor-3.5.0.tar.gz` (source distribution)

### 4. Verificar o Build

```bash
twine check dist/*
```

Deve retornar: `Checking dist/... PASSED`

## 🧪 Testes Locais

### 1. Instalar Localmente

```bash
# Instalar em modo editável
pip install -e .

# Ou instalar o wheel gerado
pip install dist/cnpj_processor-3.5.0-py3-none-any.whl
```

### 2. Testar Comandos

```bash
# Testar entry point
cnpj-processor --version
cnpj --help

# Testar importação
python -c "from src import __version__; print(__version__)"
```

### 3. Testar Funcionalidades

```bash
# Teste rápido
cnpj -t empresas -s download -l 1 -q

# Teste de processamento
cnpj -t estabelecimentos -s all -l 2
```

## 🧪 Publicação no TestPyPI

⚠️ **SEMPRE teste no TestPyPI primeiro!**

```bash
twine upload --repository testpypi dist/*
```

### Verificar no TestPyPI

1. Acesse: https://test.pypi.org/project/cnpj-processor/
2. Verifique metadados, README, links
3. Teste instalação:

```bash
# Criar ambiente limpo
python -m venv test_env
source test_env/bin/activate  # Linux/Mac
# ou
.\test_env\Scripts\Activate.ps1  # Windows

# Instalar do TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ cnpj-processor

# Testar
cnpj-processor --version
```

## 🚀 Publicação no PyPI

**Após testar no TestPyPI e confirmar que tudo está OK:**

```bash
twine upload dist/*
```

### Verificar no PyPI

1. Acesse: https://pypi.org/project/cnpj-processor/
2. Verifique a página do projeto
3. Teste instalação:

```bash
pip install cnpj-processor
cnpj-processor --version
```

## ✅ Checklist de Publicação

Use este checklist antes de cada publicação:

### Antes do Build
- [ ] Versão atualizada em `pyproject.toml`
- [ ] README.md atualizado com novidades
- [ ] VERSIONAMENTO.md atualizado com changelog
- [ ] Testes passando (`pytest`)
- [ ] Código lintado (`black`, `isort`, `flake8`)
- [ ] Git tag criada (`git tag v3.5.0`)
- [ ] Commit e push feitos

### Build e Validação
- [ ] `rm -rf build/ dist/ *.egg-info` executado
- [ ] `python -m build` executado com sucesso
- [ ] `twine check dist/*` passou
- [ ] Instalação local testada (`pip install -e .`)
- [ ] Entry points funcionando (`cnpj --version`)
- [ ] Imports funcionando

### TestPyPI
- [ ] Upload para TestPyPI bem-sucedido
- [ ] Página do TestPyPI verificada
- [ ] Instalação do TestPyPI testada
- [ ] Funcionalidades testadas

### PyPI (Produção)
- [ ] Upload para PyPI bem-sucedido
- [ ] Página do PyPI verificada
- [ ] Instalação testada: `pip install cnpj-processor`
- [ ] Comandos testados
- [ ] Anúncio da release (GitHub, etc.)

## 🔥 Comandos Rápidos

### Build Completo + Upload TestPyPI
```bash
# Limpar
rm -rf build/ dist/ *.egg-info

# Build
python -m build

# Verificar
twine check dist/*

# Upload TestPyPI
twine upload --repository testpypi dist/*
```

### Build Completo + Upload PyPI
```bash
# Limpar
rm -rf build/ dist/ *.egg-info

# Build
python -m build

# Verificar
twine check dist/*

# Upload PyPI (PRODUÇÃO!)
twine upload dist/*
```

### PowerShell (Windows)
```powershell
# Limpar
Remove-Item -Recurse -Force build, dist, *.egg-info -ErrorAction SilentlyContinue

# Build
python -m build

# Verificar
twine check dist/*

# Upload TestPyPI
twine upload --repository testpypi dist/*

# Upload PyPI (após testar no TestPyPI)
twine upload dist/*
```

## 🐛 Solução de Problemas

### Erro: "Invalid or non-existent authentication"
- Verifique se o token está correto no `.pypirc`
- Token deve começar com `pypi-`
- Username deve ser `__token__` (com underscores duplos)

### Erro: "File already exists"
- Não é possível re-upload da mesma versão
- Incremente a versão no `pyproject.toml`
- Ou delete a release anterior (não recomendado)

### Erro: "Package name already taken"
- O nome `cnpj-processor` pode já existir
- Escolha outro nome único no `pyproject.toml`
- Exemplo: `cnpj-processor-br`, `cnpj-dados-abertos`, etc.

### Erro: "403 Forbidden"
- Token pode estar expirado ou sem permissões
- Crie novo token com permissões corretas
- Para primeiro upload, use token com escopo "Entire account"

### Entry Points Não Funcionam
- Verifique `[project.scripts]` no `pyproject.toml`
- Reinstale o pacote: `pip install --force-reinstall cnpj-processor`
- Em desenvolvimento, use: `pip install -e .`

### README Não Aparece no PyPI
- Verifique que `readme = "README.md"` está no `pyproject.toml`
- README deve estar em Markdown válido
- Use `twine check dist/*` para validar

### Dependências Não Instalam
- Verifique sintaxe em `[project.dependencies]`
- Teste localmente: `pip install -e .`
- Versões devem existir no PyPI

## 📚 Recursos Adicionais

- **Documentação Oficial PyPI**: https://packaging.python.org/
- **Twine Docs**: https://twine.readthedocs.io/
- **Semantic Versioning**: https://semver.org/
- **pyproject.toml Spec**: https://peps.python.org/pep-0621/

## 🔄 Workflow Recomendado

1. **Desenvolvimento**: 
   - Trabalhe em branch `develop` ou `feature/xxx`
   - Instale em modo editável: `pip install -e .`

2. **Preparação Release**:
   - Merge para `main`
   - Atualize versão
   - Atualize changelog
   - Crie git tag

3. **Build e Teste**:
   - Build local
   - Upload para TestPyPI
   - Teste instalação do TestPyPI

4. **Release Produção**:
   - Upload para PyPI
   - Teste instalação do PyPI
   - Anuncie release

5. **Pós-Release**:
   - Monitore issues
   - Responda feedback
   - Planeje próxima versão

## 🎯 Próximos Passos Após Publicação

1. **Adicionar badge no README**:
```markdown
[![PyPI version](https://badge.fury.io/py/cnpj-processor.svg)](https://badge.fury.io/py/cnpj-processor)
[![Downloads](https://pepy.tech/badge/cnpj-processor)](https://pepy.tech/project/cnpj-processor)
```

2. **Criar GitHub Release**:
   - Vincular à tag
   - Incluir changelog
   - Anexar wheels/source dist

3. **Atualizar Documentação**:
   - Instruções de instalação via pip
   - Exemplos de uso
   - Troubleshooting

4. **Divulgar**:
   - Reddit: r/Python, r/brasil
   - Twitter/X
   - LinkedIn
   - Dev.to

---

**Última atualização**: Janeiro 2026
**Versão do guia**: 1.0.0
