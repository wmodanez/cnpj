# CNPJ Processor 🏢

[![PyPI version](https://badge.fury.io/py/cnpj-processor.svg)](https://badge.fury.io/py/cnpj-processor)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Sistema profissional de processamento de dados públicos CNPJ da Receita Federal do Brasil

Automatize o download, processamento e análise dos dados públicos de CNPJ com performance excepcional e API simplificada.

## 🚀 Instalação

```bash
pip install cnpj-processor
```

## ☁️ Suporte ao Nextcloud da Receita Federal

**🆕 Integrado**: O cnpj-processor agora suporta nativamente a infraestrutura **Nextcloud** da Receita Federal!

### 🎯 Como Funciona

O sistema detecta automaticamente URLs Nextcloud e aplica autenticação apropriada:

```python
from cnpj_processor import CNPJProcessor

# Funciona automaticamente com Nextcloud
processor = CNPJProcessor()
success, folder = processor.run()

# O sistema detecta e autentica automaticamente em:
# https://arquivos.receitafederal.gov.br/index.php/s/gn672Ad4CF8N6TK?dir=/Dados/Cadastros/CNPJ
```

### 📦 Dados Disponíveis

O Nextcloud da Receita Federal disponibiliza:

- **33 pastas históricas** desde 2023-05
- **Pasta mais recente**: 2026-01 (37 arquivos, 6.79 GB)
- **Dados completos**: Empresas, Estabelecimentos, Sócios, Simples Nacional
- **Atualização mensal**: Novos dados publicados mensalmente

## ⚡ Início Rápido

### Via Linha de Comando (CLI)

```bash
# Pipeline completo (download + processamento + banco de dados)
cnpj-processor

# Download apenas
cnpj-processor --step download --types empresas estabelecimentos

# Processar painel consolidado por UF
cnpj-processor --step painel --painel-uf GO --painel-situacao 2
```

### Via API Python

```python
from cnpj_processor import CNPJProcessor

# Criar processador
processor = CNPJProcessor()

# Pipeline completo
success, folder = processor.run()

# Painel de empresas ativas em São Paulo
success, folder = processor.run(
    step='painel',
    painel_uf='GO',
    painel_situacao=2  # Ativas
)
```

## 🎯 Principais Funcionalidades

### 📥 Download Inteligente

- Download assíncrono de alta performance
- Retomada automática em caso de falha
- Verificação de integridade de arquivos
- Cache inteligente para evitar downloads duplicados

### ⚙️ Processamento Otimizado

- Pipeline paralelo: download e processamento simultâneos
- Até **70% mais rápido** que processamento sequencial
- **Padronização automática de colunas**: CSVs renomeados conforme padrão esperado
- Suporte a múltiplos tipos: empresas, estabelecimentos, sócios, simples
- Exportação para Parquet com compressão eficiente

### 💾 Gestão Inteligente de Espaço

- **Limpeza automática**: Remove ZIPs e arquivos temporários por padrão
- **Banco opcional**: DuckDB criado apenas quando solicitado
- **Múltiplas estratégias**: De 15 GB (apenas banco) até 93 GB (tudo)
- **Controle total**: Flags para customizar retenção de artefatos

### 🎨 Painel Consolidado

- Combinação inteligente de dados de múltiplas fontes
- Filtros avançados: UF, situação cadastral, Simples Nacional
- Ideal para análises e dashboards
- Formato otimizado para BI tools

### 💾 Banco de Dados

- Geração automática de banco DuckDB
- Queries SQL de alta performance
- Integração perfeita com ferramentas de análise

## 📚 API Simplificada

A API do `cnpj-processor` foi projetada para ser **simples, poderosa e intuitiva**.

### Métodos Principais

#### `run()` - Método Universal

Execute qualquer operação com um único método:

```python
processor = CNPJProcessor()

# Pipeline completo
processor.run()

# Download específico
processor.run(step='download', tipos=['empresas'], remote_folder='2026-01')

# Processamento com economia de espaço
processor.run(
    step='all',
    delete_zips_after_extract=True,
    cleanup_all_after_db=True
)

# Painel customizado
processor.run(
    step='painel',
    painel_uf='GO',
    painel_situacao=2,
    output_subfolder='painel_go_ativas'
)
```

**Parâmetros do `run()`:**

| Parâmetro | Tipo | Descrição |
| --------- | ---- | --------- |
| `step` | str | Etapa: 'download', 'extract', 'csv', 'process', 'database', 'painel', 'all' |
| `type` | list | Tipos a processar: ['empresas', 'estabelecimentos', 'simples', 'socios'] |
| `remote_folder` | str | Pasta remota (formato AAAA-MM) |
| `output_subfolder` | str | Subpasta de saída |
| `source_zip_folder` | str | Pasta de origem dos ZIPs (para extract/process) |
| `force_download` | bool | Forçar re-download |
| `keep_artifacts` | bool | Manter ZIPs e arquivos temporários (padrão: False) |
| `create_database` | bool | Criar banco DuckDB (padrão: False) |
| `cleanup_after_db` | bool | Remover parquets após criar banco |
| `keep_parquet_after_db` | bool | Manter parquets após criar banco |
| `processar_painel` | bool | Processar painel consolidado |
| `painel_uf` | str | Filtrar painel por UF |
| `painel_situacao` | int | Filtrar por situação (1=Nula, 2=Ativa, 3=Suspensa, 4=Inapta, 8=Baixada) |
| `criar_empresa_privada` | bool | Criar subset de empresas privadas |
| `criar_subset_uf` | str | Criar subset por UF |
| `quiet` | bool | Modo silencioso |
| `log_level` | str | Nível de log ('DEBUG', 'INFO', 'WARNING', 'ERROR') |

#### `get_latest_folder()` - Consultar Pasta Mais Recente

```python
processor = CNPJProcessor()
latest = processor.get_latest_folder()
print(f"Pasta mais recente: {latest}")  # '2026-01'
```

#### `get_available_folders()` - Listar Pastas Disponíveis

```python
processor = CNPJProcessor()
folders = processor.get_available_folders()
print(f"Disponíveis: {folders}")  # ['2026-01', '2025-12', ...]
```

## 💡 Exemplos Práticos

### Exemplo 1: Pipeline Completo

```python
from cnpj_processor import CNPJProcessor

processor = CNPJProcessor()
success, folder = processor.run()

if success:
    print(f"✅ Dados processados em: {folder}")
```

### Exemplo 2: Download Seletivo

```python
# Baixar apenas empresas e estabelecimentos
processor = CNPJProcessor()
success, folder = processor.run(
    step='download',
    tipos=['empresas', 'estabelecimentos'],
    remote_folder='2026-01'
)
```

### Exemplo 3: Processamento com Economia de Espaço

```python
# Padrão: Remove ZIPs e temporários automaticamente, mantém apenas parquets
processor = CNPJProcessor()
success, folder = processor.run()  # ~20 GB

# Máxima economia: Criar banco e remover parquets
success, folder = processor.run(
    create_database=True,    # Cria banco DuckDB
    cleanup_after_db=True    # Remove parquets
)  # ~15 GB
```

### Exemplo 4: Painel Analítico Customizado

```python
# Painel apenas de empresas ativas de Goiás
processor = CNPJProcessor()
success, folder = processor.run(
    step='painel',
    painel_uf='GO',
    painel_situacao=2,  # Ativas
    output_subfolder='painel_go_ativas'
)
```

### Exemplo 5: Processar Múltiplos Períodos

```python
processor = CNPJProcessor()
pastas = ['2025-12', '2026-01']

for pasta in pastas:
    print(f"Processando {pasta}...")
    success, folder = processor.run(
        step='all',
        remote_folder=pasta,
        output_subfolder=f'dados_{pasta.replace("-", "_")}'
    )
    print(f"{'✅' if success else '❌'} {pasta}")
```

### Exemplo 6: Descompactação de ZIPs

```python
# Apenas descompactar arquivos ZIP (sem processar)
processor = CNPJProcessor()
success, folder = processor.run(
    step='extract',
    source_zip_folder='dados-abertos-zip/2026-01'
)

# Gerar CSVs normalizados (sem converter para parquet)
success, folder = processor.run(
    step='csv',
    tipos=['socios'],
    output_csv_folder='csvs_normalizados'
)

# Útil quando você:
# - Quer verificar conteúdo dos ZIPs manualmente (extract)
# - Precisa de CSVs com nomes de colunas padronizados (csv)
# - Prefere fazer o processamento depois
# - Usa ferramentas externas para análise dos CSVs

# NOTA: Durante o processamento normal (step='process' ou 'all'),
# os nomes das colunas dos CSVs são automaticamente padronizados
# para corresponder ao esquema esperado do Parquet, sem necessidade
# de configuração adicional!
```

### Exemplo 7: Subset Especializado

```python
# Apenas empresas privadas
processor = CNPJProcessor()
success, folder = processor.run(
    step='all',
    tipos=['empresas'],
    criar_empresa_privada=True,
    output_subfolder='empresas_privadas'
)

# Apenas estabelecimentos de uma UF
success, folder = processor.run(
    step='all',
    tipos=['estabelecimentos'],
    criar_subset_uf='GO',
    output_subfolder='estabelecimentos_sp'
)
```

### Exemplo 8: Estratégias de Espaço em Disco

```python
processor = CNPJProcessor()

# Estratégia 1: Análise de dados (padrão)
success, folder = processor.run()
# Espaço: ~20 GB (apenas parquets)

# Estratégia 2: Com banco de dados
success, folder = processor.run(create_database=True)
# Espaço: ~35 GB (parquets + banco)

# Estratégia 3: Máxima economia
success, folder = processor.run(
    create_database=True,
    cleanup_after_db=True
)
# Espaço: ~15 GB (apenas banco)

# Estratégia 4: Manter tudo (desenvolvimento)
success, folder = processor.run(
    keep_artifacts=True,
    create_database=True,
    keep_parquet_after_db=True
)
# Espaço: ~93 GB (ZIPs + temporários + parquets + banco)
```

## 🔧 Uso via CLI

O `cnpj-processor` também oferece interface completa de linha de comando:

```bash
# Pipeline completo
cnpj-processor

# Download de pasta específica
cnpj-processor --step download --remote-folder 2026-01

# Apenas descompactar ZIPs (sem processar)
cnpj-processor --step extract --source-zip-folder dados-abertos-zip/2026-01

# Gerar CSVs normalizados
cnpj-processor --step csv --types socios --output-csv-folder csvs_normalizados

# Processar dados já descompactados
cnpj-processor --step process --source-zip-folder dados-abertos-zip/2026-01 --output-subfolder processados

# Processar apenas estabelecimentos
cnpj-processor --types estabelecimentos

# Painel filtrado
cnpj-processor --step painel --painel-uf GO --painel-situacao 2

# Criar banco de dados (opcional)
cnpj-processor --create-database

# Máxima economia de espaço
cnpj-processor --create-database --cleanup-after-db

# Ver pasta mais recente disponível
cnpj-processor --show-latest-folder

# Ver versão
cnpj-processor --version

# Ajuda completa
cnpj-processor --help
```

### Atalhos de CLI

Interface otimizada com atalhos intuitivos:

```bash
# Equivalentes (forma completa vs. atalho)
cnpj-processor --types empresas --step download --remote-folder 2026-01
cnpj-processor -t empresas -s download -r 2026-01

# Descompactar e processar com atalhos
cnpj-processor --step extract --source-zip-folder dados-abertos-zip/2026-01
cnpj-processor -s extract -z dados-abertos-zip/2026-01

# Gerar CSVs normalizados com atalhos
cnpj-processor --step csv --types socios
cnpj-processor -s csv -t socios

# Criar banco com economia de espaço
cnpj-processor --create-database --cleanup-after-db --quiet
cnpj-processor -D -c -q

# Manter todos os artefatos
cnpj-processor --keep-artifacts --create-database --keep-parquet-after-db
cnpj-processor -k -D -K

# Painel filtrado
cnpj-processor --step painel --painel-uf GO --painel-situacao 2
cnpj-processor -s painel --painel-uf GO --painel-situacao 2
```

## 📊 Estrutura de Dados

### Arquivos Gerados

```folder
parquet/
├── 2026-01/                    # Pasta por período
│   ├── empresa/               # Dados de empresas
│   ├── estabelecimento/       # Dados de estabelecimentos
│   ├── simples/              # Dados do Simples Nacional
│   ├── socio/                # Dados de sócios
│   ├── painel_dados.parquet  # Painel consolidado
│   └── cnpj.duckdb          # Banco de dados
```

### Formato Painel

O painel consolidado combina dados de três fontes:

- **Estabelecimento**: CNPJ, razão social, endereço, situação
- **Empresa**: Nome fantasia, capital social, porte
- **Simples**: Opção pelo Simples Nacional, data de inclusão

Campos principais:

- `cnpj_basico`: CNPJ raiz (8 dígitos)
- `cnpj_completo`: CNPJ completo (14 dígitos)
- `razao_social`: Nome empresarial
- `nome_fantasia`: Nome fantasia
- `uf`: Unidade Federativa
- `municipio`: Município
- `situacao_cadastral`: Situação (Ativa, Baixada, etc.)
- `opcao_simples`: Se optante pelo Simples
- `capital_social`: Capital social da empresa
- `porte`: Porte da empresa

## 🎯 Casos de Uso

### 1. Análise de Mercado

```python
# Obter painel de empresas ativas por estado
processor = CNPJProcessor()
success, folder = processor.run(
    step='painel',
    painel_uf='GO',
    painel_situacao=2
)
```

### 2. Compliance e Due Diligence

```python
# Download completo para análise interna
processor = CNPJProcessor()
success, folder = processor.run(
    step='all',
    tipos=['empresas', 'estabelecimentos', 'socios']
)
```

### 3. Data Science / ML

```python
# Preparar dados para modelos
processor = CNPJProcessor()
success, folder = processor.run(
    step='all',
    cleanup_after_db=True  # Mantém apenas banco final
)
```

### 4. Dashboards BI

```python
# Gerar painel para PowerBI/Tableau
processor = CNPJProcessor()
success, folder = processor.run(
    step='painel',
    processar_painel=True
)
```

## 🔍 Requisitos do Sistema

- **Python**: 3.9 ou superior
- **Sistema Operacional**: Windows, Linux, macOS
- **Espaço em Disco**: Mínimo 50GB recomendado
- **Memória RAM**: Mínimo 4GB, recomendado 8GB+
- **Conexão Internet**: Necessária para download

## 🛡️ Tratamento de Erros

```python
from cnpj_processor import CNPJProcessor

processor = CNPJProcessor()

try:
    success, folder = processor.run(
        step='all',
        tipos=['empresas']
    )
    
    if success:
        print(f"✅ Sucesso! Dados em: {folder}")
    else:
        print("⚠️ Concluído com avisos. Verifique os logs.")
        
except KeyboardInterrupt:
    print("\n🛑 Processamento interrompido pelo usuário")
except Exception as e:
    print(f"❌ Erro: {e}")
```

## 📈 Performance

### Benchmarks

- **Pipeline Otimizado**: 70% mais rápido que processamento sequencial
- **Download Assíncrono**: Múltiplos arquivos simultâneos
- **Processamento Paralelo**: Utilização eficiente de múltiplos cores
- **Compressão Inteligente**: Arquivos Parquet com zstd

### Tempos Típicos

| Operação | Tempo Estimado |
| -------- | -------------- |
| Download completo | 5-15 minutos |
| Processamento (todos os tipos) | 10-30 minutos |
| Geração de banco | 2-5 minutos |
| Painel consolidado | 5-10 minutos |

> Tempos variam conforme hardware e conexão de rede

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🔗 Links Úteis

- **PyPI**: <https://pypi.org/project/cnpj-processor/>
- **Documentação Completa**: Ver pasta `docs/` no repositório
- **Issues**: Reporte bugs e sugira melhorias
- **Dados CNPJ**: [Receita Federal - Dados Públicos](https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj)

## 🙏 Agradecimentos

- Receita Federal do Brasil pela disponibilização dos dados públicos
- Comunidade Python pelo ecossistema de ferramentas excepcionais
- Todos os contribuidores do projeto
