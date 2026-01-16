"""
Exemplo de importação e uso do pacote cnpj-processor

Após instalação via pip:
  pip install cnpj-processor

Ou em modo desenvolvimento:
  pip install -e .

O pacote é importado como 'cnpj_processor'
"""

# Importar versão e metadados
from cnpj_processor import __version__, __title__, get_version

print(f"Pacote: {__title__}")
print(f"Versão: {__version__}")
print(f"Versão (função): {get_version()}")

# Importar configuração
from cnpj_processor import Config, config

print(f"\nConfig class: {Config}")
print(f"Config instance: {config}")
print(f"base_cache_dir: {config.cache.base_cache_dir}")
print(f"n_workers: {config.n_workers}")

# Importar funções de database
from cnpj_processor import create_duckdb_file, verify_parquet_file

print(f"\nFunções disponíveis:")
print(f"- create_duckdb_file: {create_duckdb_file}")
print(f"- verify_parquet_file: {verify_parquet_file}")

# Importar entidades diretamente
from cnpj_processor.Entity.Empresa import Empresa
from cnpj_processor.Entity.Estabelecimento import Estabelecimento
from cnpj_processor.Entity.Socio import Socio
from cnpj_processor.Entity.Simples import Simples

print(f"\nEntidades:")
print(f"- Empresa: {Empresa}")
print(f"- Estabelecimento: {Estabelecimento}")
print(f"- Socio: {Socio}")
print(f"- Simples: {Simples}")

# Importar schemas
from cnpj_processor.Entity.schemas.empresa import EmpresaSchema
from cnpj_processor.Entity.schemas.estabelecimento import EstabelecimentoSchema
from cnpj_processor.Entity.schemas.socio import SocioSchema
from cnpj_processor.Entity.schemas.simples import SimplesSchema

print(f"\nSchemas Pydantic:")
print(f"- EmpresaSchema: {EmpresaSchema}")
print(f"- EstabelecimentoSchema: {EstabelecimentoSchema}")
print(f"- SocioSchema: {SocioSchema}")
print(f"- SimplesSchema: {SimplesSchema}")

# Exemplo de uso de schema
print(f"\n--- Exemplo de criação de objeto com schema ---")
empresa_data = {
    "cnpj_basico": 12345678,
    "razao_social": "EMPRESA EXEMPLO LTDA",
    "natureza_juridica": 2062,
    "qualificacao_responsavel": 50,
    "capital_social": 100000.00,
    "porte_empresa": 3,
    "ente_federativo_responsavel": None
}

empresa = EmpresaSchema(**empresa_data)
print(f"\nEmpresa criada:")
print(f"- CNPJ: {empresa.cnpj_basico}")
print(f"- Razão Social: {empresa.razao_social}")
print(f"- Capital Social: R$ {empresa.capital_social:,.2f}")
print(f"- Porte: {empresa.porte_empresa}")

# Converter para dict
print(f"\nEmpresa como dict:")
print(empresa.model_dump())

print("\n✅ Importações funcionando corretamente!")
