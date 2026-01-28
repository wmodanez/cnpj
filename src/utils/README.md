# Módulo Utils - Organização e Responsabilidades

Este diretório contém utilitários reutilizáveis organizados por responsabilidade.

## 📁 Estrutura e Responsabilidades

### 🌐 `network.py` - Conectividade e Download

**Responsabilidades:**

- Verificação de conectividade com internet
- Testes de qualidade e velocidade de conexão
- Recomendações adaptativas baseadas na qualidade da rede
- **Gerenciamento completo de download de arquivos**
  - `ensure_files_downloaded()` - Verifica, compara e baixa arquivos necessários

**Use quando precisar:**

- Verificar se há internet disponível
- Baixar arquivos de URLs remotas
- Obter recomendações de configuração de rede

---

### 📦 `files.py` - Manipulação de Arquivos Locais

**Responsabilidades:**

- Verificação de espaço em disco
- **Extração paralela de arquivos ZIP**
  - `file_extractor()` - Função base de extração paralela
  - `extract_zip_files()` - Wrapper de alto nível (usa file_extractor)
- Remoção de arquivos
- Estimativa de tamanho de ZIPs extraídos
- Gerenciamento seguro de exclusão de ZIPs após extração

**Use quando precisar:**

- Extrair arquivos ZIP localmente
- Verificar espaço disponível em disco
- Remover arquivos com segurança
- Estimar espaço necessário para extração

---

### ⚡ `parallel.py` - Processamento Paralelo de CSVs

**Responsabilidades:**

- Processamento paralelo de múltiplos arquivos CSV
- Verificação de integridade de CSVs
- Conversão de CSV para DataFrame Polars
- Aplicação de operações em lote em DataFrames

**Use quando precisar:**

- Processar muitos arquivos CSV simultaneamente
- Verificar se um CSV é válido
- Converter CSV para DataFrame com configurações específicas

---

### 💾 `cache.py` - Sistema de Cache

**Responsabilidades:**

- Cache de downloads para evitar re-downloads
- Gerenciamento de metadados de cache
- Validação de integridade de arquivos em cache

---

### 🎨 `colors.py` - Formatação de Console

**Responsabilidades:**

- Códigos de cores ANSI para terminal
- Formatação de mensagens coloridas no console

---

### 📊 `statistics.py` - Coleta de Estatísticas

**Responsabilidades:**

- Coleta de métricas de processamento
- Agregação de estatísticas de sessão
- Geração de relatórios detalhados

---

### ⏱️ `time_utils.py` - Utilitários de Tempo

**Responsabilidades:**

- Formatação de durações
- Cálculo de tempos decorridos
- Conversões de unidades de tempo

---

### 🛡️ `global_circuit_breaker.py` - Controle de Falhas

**Responsabilidades:**

- Circuit breaker para falhas críticas
- Gestão de falhas em cascata
- Interrupção controlada de processos

---

### 📁 `folders.py` - Gerenciamento de Diretórios

**Responsabilidades:**

- Criação e verificação de estrutura de pastas
- Validação de diretórios necessários

---

### 🔧 `utils.py` - Utilitários Gerais

**Responsabilidades:**

- Funções auxiliares diversas
- Criação de nomes de arquivos parquet
- Outras utilidades de propósito geral

---

## 🚫 O Que NÃO Fazer (Anti-Patterns)

### ❌ NÃO duplique funções entre módulos

- Se `file_extractor()` já existe, use-o via wrapper
- Se `ensure_files_downloaded()` gerencia download, não reimplemente

### ❌ NÃO misture responsabilidades

- Download pertence a `network.py`
- Extração pertence a `files.py`
- Processamento pertence a `parallel.py`

### ❌ NÃO crie wrappers que reimplementam

```python
# ERRADO - Reimplementa a lógica
def extract_zip_files():
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(dest)

# CORRETO - Reutiliza função existente
def extract_zip_files():
    file_extractor(source, dest, '*.zip')
```

---

## ✅ Padrões de Uso Correto

### Exemplo 1: Pipeline Completo

```python
from src.utils import ensure_files_downloaded, extract_zip_files
from src.utils.parallel import process_csv_files_parallel

# 1. Download
success, path, files = await ensure_files_downloaded(args, PATH_ZIP)

# 2. Extração
extract_zip_files(path, PATH_UNZIP, delete_after=True)

# 3. Processamento
process_csv_files_parallel(csv_files, PATH_UNZIP, process_func)
```

### Exemplo 2: Verificações

```python
from src.utils.network import check_internet_connection
from src.utils.files import check_disk_space

# Verificar pré-requisitos
if not check_internet_connection()[0]:
    print("Sem internet")
    return

has_space, available = check_disk_space(path, required_mb=1000)
if not has_space:
    print(f"Espaço insuficiente: {available}MB")
    return
```

---

## 📝 Convenções

1. **Imports locais**: Use imports relativos dentro do módulo utils
2. **Logging**: Sempre use `logger = logging.getLogger(__name__)`
3. **Type hints**: Forneça type hints completos para melhor IDE support
4. **Docstrings**: Documente Args, Returns e Raises
5. **Reutilização**: Sempre verifique se já existe função antes de criar nova

---

## 🔄 Hierarquia de Dependências

```plaintext

network.py (nível mais alto - download)
    ↓
files.py (nível médio - extração local)
    ↓
parallel.py (nível de processamento - CSVs)
```

**Regra**: Módulos de nível mais baixo NÃO devem importar módulos de nível mais alto.

---

## 📚 Referências Rápidas

| Preciso... | Use... |
| ------------ | -------- |
| Baixar arquivos | `network.ensure_files_downloaded()` |
| Extrair ZIPs | `files.extract_zip_files()` |
| Processar CSVs | `parallel.process_csv_files_parallel()` |
| Verificar espaço | `files.check_disk_space()` |
| Verificar internet | `network.check_internet_connection()` |
| Deletar ZIPs | `files.delete_zip_after_extraction()` |
