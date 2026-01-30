# 🚀 Guia de Atalhos - cnpj-processor

> Referência curta com os atalhos principais e exemplos de uso. Este arquivo é um resumo rápido — para detalhes completos, veja `README.md` e `README_Painel_Processor.md`.

## ⭐ Atalhos mais úteis

```bash
-t  # --types (empresas, estabelecimentos, simples, socios)
-s  # --step (download, extract, csv, process, database, painel, all)
-q  # --quiet (modo silencioso)
-a  # --all-folders (baixar todas as pastas)
-f  # --from-folder (pasta inicial AAAA-MM)
-o  # --output-subfolder (subpasta de saída)
-d  # --delete-zips-after-extract (economizar espaço)
-c  # --cleanup-after-db (limpar após DB)
-F  # --force-download (forçar download)
-P  # --process-panel (gerar painel consolidado)
```

---

## 📋 Referência rápida de argumentos

### Principais

| Atalho | Argumento | Descrição |
| -------- | ----------- | ----------- |
| `-t` | `--types` | Tipos de dados (empresas, estabelecimentos, simples, socios) |
| `-s` | `--step` | Etapa a executar (download, extract, csv, process, database, painel, all) |
| `-q` | `--quiet` | Modo silencioso (remove barras e saídas extras) |
| `-v` | `--verbose-ui` | Modo verboso de interface |
| `-l` | `--log-level` | Nível de logging (DEBUG, INFO, WARNING, ERROR) |

### Downloads e pastas

| Atalho | Argumento | Descrição |
| -------- | ----------- | ----------- |
| `-r` | `--remote-folder` | Pasta remota específica (AAAA-MM) |
| `-a` | `--all-folders` | Baixar todas as pastas disponíveis |
| `-f` | `--from-folder` | Iniciar em uma pasta específica (AAAA-MM) |
| `-F` | `--force-download` | Forçar re-download mesmo que exista localmente |
| `-z` | `--source-zip-folder` | Pasta de origem dos ZIPs (usado em `--step process`) |
| `-o` | `--output-subfolder` | Subpasta para salvar Parquets |

### Processamento / Subsets

| Atalho | Argumento | Descrição |
| -------- | ----------- | ----------- |
| `-E` | `--create-private-subset` | Criar subconjunto de empresas privadas |
| `-U` | `--create-uf-subset` | Criar subconjunto por UF (ex: `--create-uf-subset SP`) |
| `-p` | `--process-all-folders` | Processar todas as pastas locais de ZIP |

### Limpeza e DB

| Atalho | Argumento | Descrição |
| -------- | ----------- | ----------- |
| `-d` | `--delete-zips-after-extract` | Deletar ZIPs após extração |
| `-c` | `--cleanup-after-db` | Deletar Parquets após criar DB (`--create-database`) |
| `-D` | `--create-database` | Criar banco DuckDB |
| `-K` | `--keep-parquet-after-db` | Manter Parquets após criar DB |

### Interface (atalhos)

| Atalho | Argumento | Descrição |
| -------- | ----------- | ----------- |
| `-B` | `--show-progress` | Forçar exibição da barra de progresso |
| `-H` | `--hide-progress` | Ocultar barra de progresso |
| `-S` | `--show-pending` | Forçar exibição da lista de pendentes |
| `-W` | `--hide-pending` | Ocultar lista de pendentes |

### Painel consolidado

| Atalho | Argumento | Descrição |
| -------- | ----------- | ----------- |
| `-P` | `--process-panel` | Processar dados do painel (empresas + estabelecimentos + simples) |
| (sem) | `--panel-uf` | Filtrar painel por UF (ex: `--panel-uf SP`) |
| (sem) | `--panel-status` | Filtrar painel por situação cadastral (ex: `--panel-status 2`) |
| (sem) | `--panel-include-inactive` | Incluir estabelecimentos inativos no painel |

---

## 🔥 Comandos essenciais (exemplos)

### Download básico

```bash
python main.py -t empresas -q                     # Empresas, modo silencioso
python main.py -a -f 2023-01                      # Todas as pastas desde 2023-01
python main.py -r 2024-03 -F                      # Pasta específica, forçando download
```

### Processamento por steps

```bash
python main.py -s download -t empresas            # Apenas download
python main.py -s extract -z dados-abertos-zip/2024-01 # Apenas extração
python main.py -s csv -t socios                   # Gerar CSVs normalizados
python main.py -s process -t empresas -o resultado# Processar para parquet
python main.py -s database -o resultado           # Criar banco DuckDB
```

### Painel

```bash
python main.py -P                                # Processar painel completo
python main.py -P --panel-include-inactive       # Painel incluindo inativos
python main.py -P --panel-uf SP                  # Painel apenas SP
python main.py -P --panel-uf GO --panel-status 2 # Painel GO, empresas ativas
```

### Economia de espaço

```bash
python main.py -t empresas -d                     # Deletar ZIPs após extração
python main.py -D -c                              # Criar DB + limpar Parquets
```

---

## 💡 Dicas rápidas

- Use `python main.py --help` para ver a lista completa de argumentos.
- O passo `csv` gera CSVs normalizados — útil para análise manual.
- `--step process` requer `--source-zip-folder` (`-z`) quando os ZIPs não estão no padrão.
- `--create-database` (`-D`) pode ser usado junto com `--cleanup-after-db` (`-c`) para economizar espaço.

### Download Básico (Exemplos)

```bash
python main.py -t empresas -q                    # Empresas silencioso
python main.py -a -f 2023-01                     # Todas desde 2023-01
python main.py -r 2024-03 -F                     # Específica forçada
```

### Processamento por Steps

```bash
python main.py -s download -t empresas           # 1. Apenas download
python main.py -s extract -z dados-zip/2024-01   # 2. Apenas extração
python main.py -s csv -t socios                  # 3. Gerar CSVs normalizados
python main.py -s process -t empresas -o resultado  # 4. Processar para parquet
python main.py -s database -o resultado          # 5. Criar banco DuckDB
```

### Processamento com Painel

```bash
python main.py -P                                # Painel COMPLETO
python main.py -P --painel-incluir-inativos      # Painel + inativos
python main.py -P --painel-uf SP                 # Painel apenas SP
python main.py -P --painel-uf GO --painel-situacao 2  # Painel GO ativas
```

### Economia de Espaço

```bash
python main.py -t empresas -d                    # Deletar ZIPs após
python main.py -D -c                             # Criar DB + limpar parquets
python main.py -P --painel-uf SP -c              # Painel + economia máxima
```

---

## 💡 Exemplos Práticos Completos

### Download Sequencial Otimizado

```bash
python main.py -a -f 2023-01 -q -d -o dados_2023_completos
```

### Processamento Específico com Limpeza

```bash
python main.py -s process -t empresas estabelecimentos -d -c -o processados
```

### Painel São Paulo com Máxima Economia

```bash
python main.py -P --painel-uf SP --painel-situacao 2 -D -c -q
```

### Painel Histórico Otimizado

```bash
python main.py -a -f 2023-01 -P --painel-uf MG -q
```

### Painel COMPLETO com Máxima Economia

```bash
python main.py -P -D -c -q
```

### Debug Completo

```bash
python main.py -l DEBUG -v -B -S -t empresas
```

### Produção Limpa

```bash
python main.py -a -f 2022-01 -q -d -D -c -o producao_completa
```

### Painel Estabelecimentos Suspensos + Inativos

```bash
python main.py -P --painel-situacao 3 --painel-incluir-inativos -q
```

---

## 🎯 Combinações Power User (Guia Avançado)

### Workflow Completo por Etapas (Exemplos)

```bash
# 1. Download inicial
python main.py -s download -a -f 2023-01 -q

# 2. Extração
python main.py -s extract -z dados-abertos-zip/2023-01

# 3. Gerar CSVs normalizados (se necessário)
python main.py -s csv -t socios

# 4. Processamento para parquet
python main.py -s process -z dados-abertos-zip/2023-01 -o processados

# 5. Criar banco de dados
python main.py -s database -o processados -c

# 6. Gerar painel (opcional)
python main.py -s painel -P --painel-uf GO
```

### Download + Processamento Tradicional

```bash
# Tudo junto (pipeline completo)
python main.py -t empresas estabelecimentos -d -D -c -q
```

### Análise Regional Específica

```bash
# Empresas privadas de São Paulo
python main.py -t empresas -E -U SP -o empresas_sp_privadas

# Painel completo de Goiás
python main.py -P --painel-uf GO -o painel_goias
```

### Máxima Economia de Espaço

```bash
# Estratégia 1: Apenas banco final (~15 GB)
python main.py -D -c -q

# Estratégia 2: Painel específico (~10 GB)
python main.py -P --painel-uf SP -D -c -q
```

---

## 📊 Comparativo: Antes vs Agora

### Download Básico

```bash
# ANTES (78 caracteres):
python main.py --types empresas --step download --quiet --remote-folder 2024-01

# AGORA (36 caracteres - 54% mais curto):
python main.py -t empresas -s download -q -r 2024-01
```

### Processamento com Economia

```bash
# ANTES (132 caracteres):
python main.py --types estabelecimentos --step process --delete-zips-after-extract --cleanup-after-db --quiet --output-subfolder resultado

# AGORA (47 caracteres - 64% mais curto):
python main.py -t estabelecimentos -s process -d -c -q -o resultado
```

### Download Sequencial

```bash
# ANTES (89 caracteres):
python main.py --all-folders --from-folder 2023-01 --quiet --delete-zips-after-extract

# AGORA (29 caracteres - 67% mais curto):
python main.py -a -f 2023-01 -q -d
```

---

## 💡 Dicas de Uso

### Combinações Úteis por Cenário

**Download Rápido:**

```bash
-a -f 2023-01 -q  # Todas as pastas desde 2023-01 em modo silencioso
```

**Processamento Econômico:**

```bash
-s process -d -c  # Processar deletando ZIPs e parquets
```

**Debug Completo:**

```bash
-l DEBUG -v -B -S  # Logging detalhado com interface completa
```

**Produção Limpa:**

```bash
-q -H -W  # Interface mínima para logs limpos
```

**Painel Analítico:**

```bash
-P --painel-uf GO --painel-situacao 2 -q  # Painel GO empresas ativas, silencioso
```

### Sequências Recomendadas

#### Para Desenvolvimento

```bash
1. python main.py -s download -r 2024-01 -q
2. python main.py -s extract -z dados-zip/2024-01
3. python main.py -s process -t empresas -z dados-zip/2024-01 -o teste
```

#### Para Produção

```bash
python main.py -a -f 2023-01 -d -D -c -q -o producao
```

#### Para Análise Específica

```bash
python main.py -P --painel-uf SP --painel-situacao 2 -o analise_sp
```

---

## 🎓 Atalhos por Categoria

### Essenciais

`-t`, `-s`, `-q`, `-v`

### Downloads

`-r`, `-a`, `-f`, `-F`

### Processamento

`-E`, `-U`, `-p`, `-d`, `-z`

### Otimização

`-c`, `-k`, `-D`, `-K`, `-o`

### Interface

`-B`, `-H`, `-S`, `-W`

### Painel

`-P`, `--painel-uf`, `--painel-situacao`, `--painel-incluir-inativos`

---

**💡 Lembre-se:**

- Use `python main.py --help` para ver todos os argumentos
- Todos os atalhos podem ser combinados livremente
- O step `csv` gera CSVs normalizados (útil para análise manual)
- O step `painel` requer dados já processados (parquets)

**📖 Veja também:**

- [README.md](README.md) - Documentação completa do sistema
- [README_Painel_Processor.md](README_Painel_Processor.md) - Detalhes do processador de painel
python main.py -l DEBUG -v -B -S -t empresas

### Produção Limpa (exemplo)

```bash
python main.py -a -f 2022-01 -q -d -D -c -o producao_completa
```

### Painel Estabelecimentos Suspensos + Inativos 🆕

```bash
python main.py -P --painel-situacao 3 --painel-incluir-inativos -q
```

---

## 🎯 Combinações Power User

### Workflow Completo por Etapas

```bash
# 1. Download inicial
python main.py -s download -a -f 2023-01 -q

# 2. Extração
python main.py -s extract -z dados-abertos-zip/2023-01

# 3. Gerar CSVs normalizados (se necessário)
python main.py -s csv -t socios

# 4. Processamento para parquet
python main.py -s process -z dados-abertos-zip/2023-01 -o processados

# 5. Criar banco de dados
python main.py -s database -o processados -c

# 6. Gerar painel (opcional)
python main.py -s painel -P --painel-uf GO
```

### Download + Processamento Tradicional (exemplo)

```bash
# Tudo junto (pipeline completo)
python main.py -t empresas estabelecimentos -d -D -c -q
```

### Análise Regional Específica (exemplo)

```bash
# Empresas privadas de Goiás
python main.py -t empresas -E -U GO -o empresas_go_privadas

# Painel completo de Goiás
python main.py -P --painel-uf GO -o painel_goias
```

### Máxima Economia de Espaço (exemplo)

```bash
# Estratégia 1: Apenas banco final (~15 GB)
python main.py -D -c -q

# Estratégia 2: Painel específico (~10 GB)
python main.py -P --painel-uf SP -D -c -q
```

---

## 📊 Comparativo: Antes vs Agora

### Download Básico

```bash
# ANTES (78 caracteres):
python main.py --types empresas --step download --quiet --remote-folder 2024-01

# AGORA (36 caracteres - 54% mais curto):
python main.py -t empresas -s download -q -r 2024-01
```

### Processamento com Economia

```bash
# ANTES (132 caracteres):
python main.py --types estabelecimentos --step process --delete-zips-after-extract --cleanup-after-db --quiet --output-subfolder resultado

# AGORA (47 caracteres - 64% mais curto):
python main.py -t estabelecimentos -s process -d -c -q -o resultado
```

### Download Sequencial

```bash
# ANTES (89 caracteres):
python main.py --all-folders --from-folder 2023-01 --quiet --delete-zips-after-extract

# AGORA (29 caracteres - 67% mais curto):
python main.py -a -f 2023-01 -q -d
```

---

## 💡 Dicas de Uso

### Combinações Úteis por Cenário

**Download Rápido:**

```bash
-a -f 2023-01 -q  # Todas as pastas desde 2023-01 em modo silencioso
```

**Processamento Econômico:**

```bash
-s process -d -c  # Processar deletando ZIPs e parquets
```

**Debug Completo:**

```bash
-l DEBUG -v -B -S  # Logging detalhado com interface completa
```

**Produção Limpa:**

```bash
-q -H -W  # Interface mínima para logs limpos
```

**Painel Analítico:**

```bash
-P --painel-uf GO --painel-situacao 2 -q  # Painel GO empresas ativas, silencioso
```

### Sequências Recomendadas

#### Para Desenvolvimento

```bash
1. python main.py -s download -r 2024-01 -q
2. python main.py -s extract -z dados-zip/2024-01
3. python main.py -s process -t empresas -z dados-zip/2024-01 -o teste
```

#### Para Produção

```bash
python main.py -a -f 2023-01 -d -D -c -q -o producao
```

#### Para Análise Específica

```bash
python main.py -P --painel-uf SP --painel-situacao 2 -o analise_sp
```

---

## 🎓 Atalhos por Categoria

### Essenciais

`-t`, `-s`, `-q`, `-v`

### Downloads

`-r`, `-a`, `-f`, `-F`

### Processamento

`-E`, `-U`, `-p`, `-d`, `-z`

### Otimização

`-c`, `-k`, `-D`, `-K`, `-o`

### Interface

`-B`, `-H`, `-S`, `-W`

### Painel

`-P`, `--painel-uf`, `--painel-situacao`, `--painel-incluir-inativos`

---

**💡 Lembre-se:**

- Use `python main.py --help` para ver todos os argumentos
- Todos os atalhos podem ser combinados livremente
- O step `csv` gera CSVs normalizados (útil para análise manual)
- O step `painel` requer dados já processados (parquets)

**📖 Veja também:**

- [README.md](README.md) - Documentação completa do sistema
- [README_Painel_Processor.md](README_Painel_Processor.md) - Detalhes do processador de painel
python main.py -t empresas -q

# Processar apenas estabelecimentos da pasta 2024-01

python main.py -s process -t estabelecimentos -z dados-zip/2024-01

# Download de todas as pastas desde 2023-01

python main.py -a -f 2023-01

```

### Comandos com Otimização de Espaço
```bash
# Download + processamento deletando ZIPs após extração
python main.py -t empresas -d

# Processamento completo com limpeza máxima
python main.py -t estabelecimentos -C

# Download conservador de espaço
python main.py -a -f 2023-01 -d -c
```

### Comandos com Subsets Específicos

```bash
# Empresas privadas apenas
python main.py -t empresas -E -o apenas_privadas

# Estabelecimentos de São Paulo
python main.py -t estabelecimentos -U SP -o estabelecimentos_sp

# Múltiplos tipos com subset
python main.py -t empresas estabelecimentos -E -U RJ -o empresas_estab_rj
```

### Comandos com Interface Personalizada

```bash
# Modo verboso com todas as barras visuais
python main.py -v -P -S

# Modo ultra-silencioso (sem nenhuma interface visual)
python main.py -q -H -W

# Apenas barras de progresso, sem lista de pendentes
python main.py -P -W
```

### Comandos Avançados Combinados

```bash
# Download sequencial com economia máxima de espaço
python main.py -a -f 2022-01 -q -d -C

# Processamento específico com logging detalhado
python main.py -s process -t empresas socios -l DEBUG -v -z dados/2024-01 -o empresas_socios_2024

# Download forçado com interface mínima
python main.py -r 2024-03 -F -q -H -o redownload_2024_03

# Processamento de todas as pastas locais com limpeza
python main.py -s process -p -f 2023-01 -d -c -o processamento_completo
```

## 💡 Dicas de Uso

### Combinações Úteis

- **Download rápido:** `-a -f 2023-01 -q` (todas as pastas desde 2023-01 em modo silencioso)
- **Processamento econômico:** `-s process -d -c` (processar deletando ZIPs e parquets)
- **Debug completo:** `-l DEBUG -v -P -S` (logging detalhado com interface completa)
- **Produção limpa:** `-q -H -W` (interface mínima para logs limpos)

### Sequências Comuns

```bash
# 1. Download inicial
python main.py -a -q -o dados_completos

# 2. Processamento específico  
python main.py -s process -t empresas estabelecimentos -z dados_completos -o processados

# 3. Criação de banco com limpeza
python main.py -s database -o processados -c
```

### Atalhos por Categoria

**Essenciais:** `-t`, `-s`, `-q`, `-v`  
**Downloads:** `-r`, `-a`, `-f`, `-F`  
**Processamento:** `-E`, `-U`, `-p`, `-d`  
**Otimização:** `-c`, `-C`, `-o`, `-z`  
**Interface:** `-P`, `-H`, `-S`, `-W`  

---

**💡 Lembre-se:** Todos os atalhos podem ser combinados livremente para criar comandos personalizados conforme sua necessidade!
