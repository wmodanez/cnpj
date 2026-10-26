# TODO — CNPJ Processor (análise da v4.4.5)

## Problemas identificados

- [ ] **Sem testes automatizados**: não existe `tests/`, só scripts de exemplo. Risco alto para um pipeline que transforma dados em larga escala.
- [ ] **Arquivos grandes demais**:
  - `main.py` (2.014 linhas): `_async_main_impl` tem ~1.000 linhas e usa `global overall_success`.
  - `src/async_downloader.py` (2.882 linhas).
  - `src/process/processors/painel_processor.py` (1.491 linhas).
- [ ] **Tratamento de erros**: 27 arquivos com `except Exception`; `except: pass` em `main.py` (apontado em `docs/ANALISE_MELHORIAS.md`).
- [ ] **Dependências inconsistentes**: `setuptools==67.6.1`, `requests==2.31.0`, `aiofiles==23.2.1` fixos e antigos; `polars`, `duckdb`, `aiohttp` com `>=`. Sem lockfile, builds irreproduzíveis.
- [ ] **Arquivos de ambiente versionados**: `.env.hom` e `.env.local` estão no git. Verificar se contêm segredos ou caminhos pessoais.
- [ ] **Binários e duplicações no repositório**: `parquet/base/*.parquet`, PDF/MD de apresentação, e docs de compliance duplicados em `docs/compliance/` e `scripts/compliance/`.
- [ ] **Versão inconsistente na documentação**: README diz 4.3.0, `docs/ANALISE_MELHORIAS.md` analisa a 4.3.1, versão atual é 4.4.5. Histórico com vários commits de bump e correções de `.env`/`MANIFEST.in` indica release frágil.

## Sugestões (por prioridade)

1. [ ] Criar `tests/` com pytest, começando por validação de entidades, transformações dos processadores e parsing do Nextcloud.
2. [ ] Quebrar `_async_main_impl` em funções por etapa e eliminar o `global`.
3. [ ] Fixar dependências com lockfile e atualizar as pinagens antigas.
4. [ ] Revisar os `.env.*` versionados e remover do git o que for local.
5. [ ] Automatizar a versão (fonte única) e a checagem dos docs no CI.
