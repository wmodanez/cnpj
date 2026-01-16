# 🚀 Quick Start - CNPJ Processor

Guia rápido para começar a usar o pacote `cnpj-processor`.

## 📦 Instalação

```bash
pip install cnpj-processor
```

## ✅ Verificação

```bash
# Ver versão
cnpj-processor --version

# Ver ajuda
cnpj --help
```

## 🎯 Uso Básico

### Download e Processamento Completo

```bash
# Processar todos os tipos de dados (download + process + database)
cnpj

# Processar apenas empresas
cnpj -t empresas

# Processar empresas e estabelecimentos
cnpj -t empresas estabelecimentos
```

### Processamento por Etapas

```bash
# Apenas download
cnpj -s download

# Apenas processar arquivos já baixados
cnpj -s process

# Apenas criar banco de dados
cnpj -s database
```

### Economia de Espaço

```bash
# Deletar ZIPs após extração
cnpj -d

# Deletar parquets após criar banco
cnpj -c

# Máxima economia (deletar ZIPs E parquets)
cnpj -C
```

### Modo Silencioso

```bash
# Processamento sem output visual
cnpj -q

# Combinado com economia
cnpj -t empresas -q -C
```

## 📊 Processamento de Painel (Dados Consolidados)

```bash
# Gerar painel completo
cnpj --processar-painel

# Painel filtrado por UF
cnpj --processar-painel --painel-uf SP

# Painel filtrado por situação (2=Ativa)
cnpj --processar-painel --painel-situacao 2

# Painel com múltiplos filtros
cnpj --processar-painel --painel-uf SP --painel-situacao 2
```

## 🔧 Opções Avançadas

```bash
# Processar pasta específica
cnpj -r 2024-01

# Processar de pasta ZIP específica
cnpj -s process -z /caminho/para/zips

# Salvar em subpasta específica
cnpj -o minha_pasta

# Download de todas as pastas disponíveis
cnpj -a -s download

# Processar todas as pastas desde uma data
cnpj -a -f 2023-01
```

## 📚 Uso Programático (Python)

```python
from cnpj_processor import __version__, Config
from cnpj_processor.Entity.Empresa import Empresa
from cnpj_processor.Entity.Estabelecimento import Estabelecimento

# Ver versão
print(__version__)

# Configurar
config = Config()

# Usar entidades
empresas = Empresa()
estabelecimentos = Estabelecimento()

# Processar dados
# ... seu código aqui
```

## 📖 Documentação Completa

- [README Principal](README.md) - Documentação completa
- [Sistema de Atalhos](ATALHOS.md) - Lista completa de atalhos
- [Processamento de Painel](README_Painel_Processor.md) - Guia do painel
- [Publicação PyPI](README_PYPI.md) - Para mantenedores

## 🆘 Ajuda

```bash
# Ver todos os argumentos disponíveis
cnpj --help

# Ver informações de versão
cnpj --version
```

## 🔗 Links

- **GitHub**: https://github.com/wmodanez/cnpj
- **PyPI**: https://pypi.org/project/cnpj-processor/
- **Issues**: https://github.com/wmodanez/cnpj/issues

## 💡 Exemplos Práticos

### 1. Download Rápido de Empresas
```bash
cnpj -t empresas -s download -q
```

### 2. Processamento Local de ZIPs Existentes
```bash
cnpj -s process -z ./meus-zips -o resultado
```

### 3. Pipeline Completo com Economia Máxima
```bash
cnpj -t estabelecimentos -C -q
```

### 4. Criar Banco DuckDB a partir de Parquets Existentes
```bash
cnpj -s database -z ./parquet/2024-01
```

### 5. Painel de São Paulo com Empresas Ativas
```bash
cnpj --processar-painel --painel-uf SP --painel-situacao 2
```

---

**Versão**: 3.5.0  
**Última atualização**: Janeiro 2026
