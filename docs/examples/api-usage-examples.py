"""
Exemplos de uso da API cnpj_processor após instalação via pip

Instalação:
    pip install cnpj-processor

Este arquivo demonstra os principais casos de uso da API.
"""

# =============================================================================
# EXEMPLO 1: Uso Básico - Obter informações
# =============================================================================

from cnpj_processor import CNPJProcessor

# Criar instância do processador
processor = CNPJProcessor()

# Obter a pasta remota mais recente
latest_folder = processor.get_latest_folder()
print(f"Pasta mais recente disponível: {latest_folder}")

# Obter todas as pastas disponíveis
all_folders = processor.get_available_folders()
print(f"Pastas disponíveis: {all_folders}")

# =============================================================================
# EXEMPLO 2: Download de Dados
# =============================================================================

from cnpj_processor import CNPJProcessor

processor = CNPJProcessor()

# Download de todos os tipos da pasta mais recente
processor.download_latest()

# Download apenas de tipos específicos
processor.download_latest(tipos=['empresas', 'estabelecimentos'])

# Download forçado (mesmo se arquivo já existe)
processor.download_latest(force=True)

# =============================================================================
# EXEMPLO 3: Criar Banco de Dados DuckDB
# =============================================================================

from cnpj_processor import CNPJProcessor

processor = CNPJProcessor()

# Criar banco a partir de pasta de parquets
processor.create_database(
    parquet_folder='parquet/2024-05',
    output_file='cnpj_2024_05.duckdb'
)

# Usar nome padrão (cnpj_AAAA_MM.duckdb)
processor.create_database('parquet/2024-05')

# =============================================================================
# EXEMPLO 4: Acessar Configurações
# =============================================================================

from cnpj_processor import config

# Ver todas as configurações
print(f"URL Base: {config.URL_BASE}")
print(f"Path ZIP: {config.PATH_ZIP}")
print(f"Path Parquet: {config.PATH_PARQUET}")
print(f"Número de workers: {config.NUM_WORKERS}")

# Modificar configurações (se necessário)
config.NUM_WORKERS = 8
config.SHOW_PROGRESS_BAR = True

# =============================================================================
# EXEMPLO 5: Usar Processadores Específicos
# =============================================================================

from cnpj_processor import (
    EmpresaProcessor,
    EstabelecimentoProcessor,
    SimplesProcessor,
    SocioProcessor
)

# Criar instâncias de processadores específicos
empresa_proc = EmpresaProcessor()
estabelecimento_proc = EstabelecimentoProcessor()
simples_proc = SimplesProcessor()
socio_proc = SocioProcessor()

# Cada processador herda de BaseProcessor e tem métodos específicos
# para processar seus respectivos arquivos

# =============================================================================
# EXEMPLO 6: Trabalhar com Entidades
# =============================================================================

from cnpj_processor import (
    Empresa,
    Estabelecimento,
    Simples,
    Socio,
    Painel
)

# As classes de entidades definem os schemas dos dados
# e podem ser usadas para validação e tipagem

# Exemplo: ver colunas de Empresa
print("Colunas de Empresa:", Empresa.get_columns())

# Exemplo: ver tipos de dados de Estabelecimento
print("Schema de Estabelecimento:", Estabelecimento.get_schema())

# =============================================================================
# EXEMPLO 7: Funções de Download Avançadas
# =============================================================================

import asyncio
from cnpj_processor import (
    download_multiple_files,
    get_latest_month_zip_urls,
    get_remote_folders
)

# Obter URLs de download da pasta mais recente
urls = get_latest_month_zip_urls()
print(f"URLs disponíveis: {len(urls)}")

# Obter URLs filtradas por tipo
urls_empresas = get_latest_month_zip_urls(['empresas'])

# Download assíncrono de múltiplos arquivos
async def download_example():
    result = await download_multiple_files(
        urls_empresas,
        force_download=False
    )
    return result

# Executar download
result = asyncio.run(download_example())

# =============================================================================
# EXEMPLO 8: Uso Programático Completo (Pipeline)
# =============================================================================

import asyncio
from cnpj_processor import CNPJProcessor, get_latest_month_zip_urls
from pathlib import Path

async def pipeline_completo():
    """
    Pipeline completo: Download -> Processar -> Criar DB
    """
    processor = CNPJProcessor()
    
    # 1. Identificar pasta mais recente
    latest = processor.get_latest_folder()
    print(f"Processando dados de: {latest}")
    
    # 2. Baixar apenas empresas e estabelecimentos
    print("Baixando arquivos...")
    processor.download_latest(tipos=['empresas', 'estabelecimentos'])
    
    # 3. Processar usando o main.py (via CLI)
    # Nota: O processamento completo requer execução do main.py
    # pois envolve paralelização e gerenciamento complexo
    print("Para processar, use: cnpj-processor --step process")
    
    # 4. Criar banco de dados
    parquet_folder = f'parquet/{latest}'
    if Path(parquet_folder).exists():
        print(f"Criando banco de dados de {parquet_folder}...")
        processor.create_database(parquet_folder)
        print("Banco criado com sucesso!")

# Executar pipeline
# asyncio.run(pipeline_completo())

# =============================================================================
# EXEMPLO 9: Integração com Scripts Existentes
# =============================================================================

from cnpj_processor import config, get_latest_remote_folder
import os

# Configurar ambiente
os.environ['PATH_ZIP'] = 'D:/dados/cnpj/zip'
os.environ['PATH_PARQUET'] = 'D:/dados/cnpj/parquet'

# Recarregar config (se necessário)
config.reload()  # Se implementado

# Obter pasta mais recente
latest = get_latest_remote_folder()

# Usar em seus scripts
input_folder = f"parquet/{latest}"
output_file = f"processado_{latest}.csv"

# ... seu processamento personalizado ...

# =============================================================================
# EXEMPLO 10: Uso com Variáveis de Ambiente (.env)
# =============================================================================

"""
Crie um arquivo .env na raiz do projeto:

# .env
PATH_ZIP=D:/dados/cnpj/zip
PATH_PARQUET=D:/dados/cnpj/parquet
NUM_WORKERS=8
SHOW_PROGRESS_BAR=true
MAX_RETRIES=3
TIMEOUT_SECONDS=600
"""

from dotenv import load_dotenv
from cnpj_processor import config

# Carregar variáveis de ambiente
load_dotenv()

# Usar configurações do .env
print(f"Usando {config.NUM_WORKERS} workers")
print(f"Salvando ZIPs em: {config.PATH_ZIP}")
print(f"Salvando Parquets em: {config.PATH_PARQUET}")

# =============================================================================
# EXEMPLO 11: Verificar Versão do Pacote
# =============================================================================

import cnpj_processor

# Ver versão instalada
print(f"Versão do cnpj_processor: {cnpj_processor.__version__}")
print(f"Título: {cnpj_processor.__title__}")
print(f"Autor: {cnpj_processor.__author__}")
print(f"Licença: {cnpj_processor.__license__}")

# =============================================================================
# EXEMPLO 12: Tratamento de Erros
# =============================================================================

from cnpj_processor import CNPJProcessor
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

processor = CNPJProcessor()

try:
    # Tentar obter pasta mais recente
    latest = processor.get_latest_folder()
    print(f"Sucesso: {latest}")
    
except Exception as e:
    print(f"Erro ao obter pasta: {e}")
    # Usar pasta padrão
    latest = "2024-05"

try:
    # Tentar download
    processor.download_latest(tipos=['empresas'])
    
except Exception as e:
    print(f"Erro no download: {e}")
    # Continuar com arquivos existentes

# =============================================================================
# EXEMPLO 13: Uso via Subprocess (chamando o CLI)
# =============================================================================

import subprocess

# Executar comando CLI via Python
result = subprocess.run(
    ['cnpj-processor', '--show-latest-folder'],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    latest_folder = result.stdout.strip()
    print(f"Pasta mais recente: {latest_folder}")

# Processar tipos específicos
subprocess.run([
    'cnpj-processor',
    '--tipos', 'empresas', 'estabelecimentos',
    '--step', 'process',
    '--remote-folder', '2024-05'
])

# =============================================================================
# EXEMPLO 14: Integração com Pandas/Polars
# =============================================================================

import pandas as pd
import polars as pl
from cnpj_processor import CNPJProcessor

processor = CNPJProcessor()
latest = processor.get_latest_folder()

# Ler parquets com Pandas
df_empresas = pd.read_parquet(f'parquet/{latest}/empresas.parquet')
print(f"Empresas carregadas: {len(df_empresas)}")

# Ler parquets com Polars (mais eficiente)
df_estabelecimentos = pl.read_parquet(f'parquet/{latest}/estabelecimentos.parquet')
print(f"Estabelecimentos carregados: {len(df_estabelecimentos)}")

# =============================================================================
# EXEMPLO 15: Consultas no DuckDB
# =============================================================================

import duckdb
from cnpj_processor import CNPJProcessor

processor = CNPJProcessor()
latest = processor.get_latest_folder()

# Criar banco
db_file = f'cnpj_{latest}.duckdb'
processor.create_database(f'parquet/{latest}', db_file)

# Conectar e consultar
con = duckdb.connect(db_file)

# Exemplo de consultas
empresas_ativas = con.execute("""
    SELECT COUNT(*) as total
    FROM estabelecimentos
    WHERE situacao_cadastral = 2
""").fetchone()[0]

print(f"Empresas ativas: {empresas_ativas}")

# Top 10 municípios com mais empresas
top_municipios = con.execute("""
    SELECT municipio, COUNT(*) as total
    FROM estabelecimentos
    GROUP BY municipio
    ORDER BY total DESC
    LIMIT 10
""").fetchall()

print("Top 10 municípios:")
for municipio, total in top_municipios:
    print(f"  {municipio}: {total}")

con.close()

# =============================================================================
# NOTAS IMPORTANTES
# =============================================================================

"""
1. O processamento completo (extração de ZIPs e conversão para Parquet)
   é melhor feito via CLI devido à complexidade do pipeline:
   
   $ cnpj-processor --tipos empresas estabelecimentos

2. A API é ideal para:
   - Integração em scripts maiores
   - Download automatizado
   - Criação de bancos de dados
   - Consultas e análises pós-processamento

3. Para processamento pesado, use o CLI que já tem:
   - Gerenciamento de memória
   - Paralelização otimizada
   - Circuit breaker para falhas
   - Progress tracking
   - Cache inteligente

4. Documentação completa:
   - CLI: $ cnpj-processor --help
   - Código: https://github.com/wmodanez/cnpj
"""
