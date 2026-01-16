# 📋 Checklist Rápido - Publicação PyPI

## ✅ Configuração Inicial Completa

- [x] ✅ Pacote renomeado de `src` para `cnpj_processor`
- [x] ✅ Todas as importações atualizadas
- [x] ✅ `pyproject.toml` configurado (nome: cnpj-processor)
- [x] ✅ Entry points funcionando (`cnpj-processor`, `cnpj`)
- [x] ✅ Instalação local testada (`pip install -e .`)
- [x] ✅ Pydantic v2 compatível
- [x] ✅ UTF-8 encoding configurado para Windows
- [x] ✅ Versão 3.6.0 (git tag) funcionando

## Antes de Publicar

### 1. Preparação do Código

- [ ] Código testado e funcionando
- [ ] Versão sincronizada (`pyproject.toml` = 3.6.0)
- [ ] Changelog atualizado em `VERSIONAMENTO.md`
- [ ] README.md atualizado
- [ ] Commit e push para repositório

### 2. Atualizar Versão (se necessário)

```bash
# Atualizar versão automaticamente do git tag
python scripts/update_version.py --auto

# OU especificar versão manualmente
python scripts/update_version.py 3.6.0
```

### 3. Git Tag e Commit

```bash
# Adicionar alterações
git add .
git commit -m "chore: preparar pacote cnpj-processor para PyPI v3.6.0"

# Criar tag (se ainda não existe)
git tag v3.6.0
git push origin develop --tags
```

### 4. Instalação de Ferramentas

```bash
pip install --upgrade pip build twine
```

## Processo de Publicação

### Teste Local

```powershell
# Limpar builds anteriores
python scripts/build_and_publish.py --clean

# Build + Check
python scripts/build_and_publish.py --build --check

# Instalar localmente (editable mode)
pip install -e .

# Testar importações
python -c "import cnpj_processor; print(cnpj_processor.__version__)"

# Testar entry points
cnpj-processor --version
cnpj --help
python -m cnpj_processor.main --version
```

### TestPyPI (SEMPRE TESTE PRIMEIRO!)

```bash
# Upload para TestPyPI
python scripts/build_and_publish.py --test

# OU workflow completo de teste
python scripts/build_and_publish.py --all

# Testar instalação do TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ cnpj-processor

# Verificar funcionamento
cnpj-processor --version
```

### PyPI Produção (CUIDADO!)

```bash
# Após confirmar que funciona no TestPyPI
python scripts/build_and_publish.py --publish

# OU workflow completo de produção (CUIDADO!)
python scripts/build_and_publish.py --production
```

## Pós-Publicação

### Verificação

- [ ] Acessar https://pypi.org/project/cnpj-processor/
- [ ] Verificar página do projeto
- [ ] Testar instalação: `pip install cnpj-processor`
- [ ] Testar comandos: `cnpj-processor --version`

### Documentação

- [ ] Criar GitHub Release
- [ ] Atualizar README com badge do PyPI
- [ ] Anunciar nos canais relevantes

## Comandos Úteis

### Windows PowerShell

```powershell
# Limpar
Remove-Item -Recurse -Force build, dist, *.egg-info -ErrorAction SilentlyContinue

# Build
python -m build

# Check
python -m twine check dist/*

# Upload TestPyPI
python -m twine upload --repository testpypi dist/*

# Upload PyPI
python -m twine upload dist/*
```

### Linux/Mac Bash

```bash
# Limpar
rm -rf build/ dist/ *.egg-info

# Build
python -m build

# Check
twine check dist/*

# Upload TestPyPI
twine upload --repository testpypi dist/*

# Upload PyPI
twine upload dist/*
```

## Solução de Problemas Comuns

### "File already exists"

- Incremente a versão em `pyproject.toml`
- Não é possível re-upload da mesma versão

### "Invalid or non-existent authentication"

- Verifique `.pypirc` ou variáveis de ambiente
- Token deve começar com `pypi-`
- Username deve ser `__token__`

### Entry points não funcionam

- Reinstale: `pip install --force-reinstall cnpj-processor`
- Em dev: `pip install -e .`

### README não aparece no PyPI

- Verifique `readme = "README.md"` em `pyproject.toml`
- README deve ser Markdown válido
- Use `twine check dist/*`

## Links Importantes

- PyPI: https://pypi.org/project/cnpj-processor/
- TestPyPI: https://test.pypi.org/project/cnpj-processor/
- Guia Completo: README_PYPI.md
- Documentação: https://packaging.python.org/
