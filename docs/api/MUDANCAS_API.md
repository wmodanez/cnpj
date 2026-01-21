# API CNPJProcessor - Resumo das Mudanças

## 📋 Visão Geral

A API do `CNPJProcessor` foi completamente redesenhada para corresponder exatamente às funcionalidades disponíveis no `main.py`. Todos os métodos desnecessários foram removidos e substituídos por uma API simplificada e poderosa.

## ✅ Métodos Disponíveis na Nova API

### 1. `run()` - Método Principal

Executa o processamento de dados CNPJ com todas as opções disponíveis via linha de comando.

**Assinatura:**

```python
def run(
    step: str = 'all',
    tipos: list = None,
    remote_folder: str = None,
    output_subfolder: str = None,
    source_zip_folder: str = None,
    force_download: bool = False,
    delete_zips_after_extract: bool = False,
    cleanup_after_db: bool = False,
    cleanup_all_after_db: bool = False,
    processar_painel: bool = False,
    painel_uf: str = None,
    painel_situacao: int = None,
    painel_incluir_inativos: bool = False,
    criar_empresa_privada: bool = False,
    criar_subset_uf: str = None,
    quiet: bool = False,
    log_level: str = 'INFO'
) -> tuple[bool, str]
```

**Parâmetros:**

- `step`: Etapa a executar ('download', 'process', 'database', 'painel', 'all')
- `tipos`: Lista de tipos a processar (['empresas', 'estabelecimentos', 'simples', 'socios'])
- `remote_folder`: Pasta remota específica (formato AAAA-MM)
- `output_subfolder`: Subpasta de saída para os parquets
- `source_zip_folder`: Pasta com arquivos ZIP para processamento
- `force_download`: Forçar download mesmo se arquivo existir
- `delete_zips_after_extract`: Deletar ZIPs após extração
- `cleanup_after_db`: Deletar parquets após criação do banco
- `cleanup_all_after_db`: Deletar parquets E ZIPs após criação do banco
- `processar_painel`: Processar dados do painel consolidado
- `painel_uf`: Filtrar painel por UF
- `painel_situacao`: Filtrar painel por situação cadastral
- `painel_incluir_inativos`: Incluir estabelecimentos inativos no painel
- `criar_empresa_privada`: Criar subconjunto de empresas privadas
- `criar_subset_uf`: Criar subconjunto por UF
- `quiet`: Modo silencioso
- `log_level`: Nível de logging

**Retorna:**

- `tuple`: (sucesso: bool, pasta_output: str)

### 2. `get_latest_folder()` - Obter Pasta Mais Recente

Obtém a pasta remota mais recente disponível.

**Assinatura:**

```python
def get_latest_folder() -> str
```

**Retorna:**

- `str`: Nome da pasta mais recente (formato AAAA-MM)

### 3. `get_available_folders()` - Listar Pastas Disponíveis

Obtém lista de todas as pastas remotas disponíveis.

**Assinatura:**

```python
def get_available_folders() -> list
```

**Retorna:**

- `list`: Lista de nomes de pastas disponíveis (formato AAAA-MM)

## ❌ Métodos Removidos

Os seguintes métodos foram **removidos** por não corresponderem à funcionalidade do main.py:

1. `download_latest()` - substituído por `run(step='download')`
2. `create_database()` - substituído por `run(step='database')`
3. `process()` - substituído por `run(step='process')`
4. `process_all()` - substituído por `run(step='all')`
5. `process_painel()` - substituído por `run(step='painel')`
6. `empresa_processor` - uso interno, não deve estar exposto
7. `estabelecimento_processor` - uso interno, não deve estar exposto
8. `simples_processor` - uso interno, não deve estar exposto
9. `socio_processor` - uso interno, não deve estar exposto
10. `painel_processor` - uso interno, não deve estar exposto

## 📚 Exemplos de Uso

### Pipeline Completo

```python
from cnpj_processor import CNPJProcessor

processor = CNPJProcessor()
success, folder = processor.run()
```

### Download Apenas

```python
processor = CNPJProcessor()
success, folder = processor.run(
    step='download',
    tipos=['empresas', 'estabelecimentos'],
    remote_folder='2026-01'
)
```

### Processamento com Economia de Espaço

```python
processor = CNPJProcessor()
success, folder = processor.run(
    step='all',
    delete_zips_after_extract=True,
    cleanup_all_after_db=True
)
```

### Painel Filtrado por UF

```python
processor = CNPJProcessor()
success, folder = processor.run(
    step='painel',
    painel_uf='GO',
    painel_situacao=2,  # Ativas
    remote_folder='2026-01'
)
```

### Consultar Pastas Disponíveis

```python
processor = CNPJProcessor()

# Pasta mais recente
latest = processor.get_latest_folder()
print(f"Mais recente: {latest}")

# Todas as pastas
folders = processor.get_available_folders()
print(f"Disponíveis: {folders}")
```

## 🎯 Vantagens da Nova API

1. **Consistência Total**: A API replica exatamente os parâmetros do `main.py`
2. **Simplicidade**: Apenas 3 métodos públicos focados
3. **Poder**: O método `run()` suporta todas as funcionalidades disponíveis
4. **Documentação Clara**: Cada parâmetro está bem documentado
5. **Exemplos Práticos**: Arquivo de exemplos completo com 13 casos de uso

## 📁 Arquivos Alterados

1. **cnpj_processor/__init__.py**: API completamente redesenhada
2. **docs/examples/api-usage-examples.py**: Novos exemplos alinhados com a API
3. **test_api.py**: Script de teste da API (criado)

## ✅ Testes Realizados

- ✅ Métodos disponíveis verificados
- ✅ Assinaturas corretas confirmadas
- ✅ Exemplos de consulta de pastas funcionando
- ✅ Documentação inline completa

## 📖 Próximos Passos

Para usar a nova API:

1. **Instalar o pacote:**
   ```bash
   pip install cnpj-processor
   ```

2. **Importar e usar:**
   ```python
   from cnpj_processor import CNPJProcessor
   processor = CNPJProcessor()
   success, folder = processor.run()
   ```

3. **Consultar exemplos:**
   - Ver `docs/examples/api-usage-examples.py` para casos de uso completos
   - Ver `test_api.py` para testes básicos
