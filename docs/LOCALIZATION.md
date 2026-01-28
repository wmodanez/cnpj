# 🌍 Sistema de Localização (i18n)

> **CNPJ Processor v4.0.9** - Suporte completo a múltiplos idiomas com detecção automática de locale

## Visão Geral

O CNPJ Processor agora suporta um sistema completo de localização que permite que as descrições de parâmetros e mensagens apareçam em português ou inglês, dependendo do seu locale do sistema ou preferência explícita.

## 🌐 Idiomas Suportados

- **Português Brasileiro** (`pt_BR`) - Padrão para sistemas em português
- **Português Europeu** (`pt_PT`) - Variação europeia
- **Inglês Americano** (`en_US`) - Padrão para sistemas em inglês
- **Inglês Britânico** (`en_GB`) - Usa `en_US` como fallback

## 🔍 Detecção Automática

O sistema detecta automaticamente o locale do seu sistema operacional usando a seguinte prioridade:

1. **Variável de Ambiente `LANG`** (mais alta prioridade)

   ```bash
   export LANG=pt_BR.UTF-8
   python main.py --help
   ```

2. **Variável de Ambiente `LANGUAGE`**

   ```bash
   export LANGUAGE=pt_BR
   python main.py --help
   ```

3. **Locale do Sistema Operacional**
   - Windows: Configurações de Região e Idioma
   - Linux/macOS: Locale do sistema (locale -a)

4. **Padrão: Inglês (`en_US`)**

## 📝 Uso

### Detecção Automática

```bash
# Sistema em português? Mensagens em português automaticamente
python main.py --help

# Sistema em inglês? Mensagens em inglês automaticamente
python main.py --help
```

### Especificar Locale Explicitamente

```bash
# Forçar português
python main.py --locale pt_BR --help

# Forçar português europeu
python main.py --locale pt_PT --help

# Forçar inglês
python main.py --locale en_US --help
```

### Via Variável de Ambiente

```bash
# Linux/macOS
export LANG=pt_BR.UTF-8
python main.py --help

# Windows PowerShell
$env:LANG="pt_BR.UTF-8"
python main.py --help

# Windows CMD
set LANG=pt_BR.UTF-8
python main.py --help
```

## 📚 Exemplos

### Exemplo 1: Ajuda em Português

```bash
export LANG=pt_BR.UTF-8
python main.py --help
```

Resultado:
```
uso: main.py [-h] [--types {...}] [--step {...}] ...

Sistema de Processamento de Dados CNPJ v4.0.9 (Locale: pt_BR)

opcionais de argumentos:
  --types, -t               Tipos de dados a processar. Se não especificado,
                            processa todos...
  --step, -s                Etapa a ser executada. Padrão: all
  --quiet, -q               Modo silencioso - reduz drasticamente as saídas
                            no console
  ...
```

### Exemplo 2: Ajuda em Inglês

```bash
export LANG=en_US.UTF-8
python main.py --help
```

Resultado:

```terminal
usage: main.py [-h] [--types {...}] [--step {...}] ...

CNPJ Data Processor v4.0.9 (Locale: en_US)

optional arguments:
  --types, -t               Types of data to process. If not specified,
                            processes all...
  --step, -s                Step to be executed. Default: all
  --quiet, -q               Silent mode - drastically reduces console output
  ...
```

### Exemplo 3: Forçar Locale Específico

```bash
# Português, independente do locale do sistema
python main.py --locale pt_BR --help

# Inglês, independente do locale do sistema
python main.py --locale en_US --help
```

## 🔧 Integração em Código

### Usar Traduções em Código Python

```python
from src.localization import get_localization, t, get_current_locale

# Obter locale atual
locale = get_current_locale()
print(f"Locale atual: {locale}")

# Traduzir chave
message = t('processing_complete')
print(message)

# Ou usar a instância diretamente
loc = get_localization()
help_text = loc.get_help_text('tipos')
```

### Adicionar Nova Tradução

Edite `src/localization.py` e adicione a chave ao dicionário `TRANSLATIONS`:

```python
TRANSLATIONS = {
    'en_US': {
        'my_new_key': 'Translation in English',
        ...
    },
    'pt_BR': {
        'my_new_key': 'Tradução em Português',
        ...
    },
    ...
}
```

Depois use em código:

```python
from src.localization import t

message = t('my_new_key')
```

## 📋 Locales Disponíveis

```bash
python -c "from src.localization import get_localization; print(get_localization().get_available_locales())"
```

Resultado:
```
['en_US', 'pt_BR', 'pt_PT']
```

## 🚀 Detecção Automática de Sistema

### Windows

O locale é detectado automaticamente das Configurações de Região e Idioma:

**Para Português:**

1. Abra Configurações → Hora e Idioma → Idioma
2. Adicione "Português (Brasil)" ou "Português (Portugal)"
3. Execute o programa

**Para Inglês:**

1. Abra Configurações → Hora e Idioma → Idioma
2. Adicione "English (United States)"
3. Execute o programa

### Linux/macOS

O locale é detectado da variável de ambiente `LANG`:

```bash
# Ver locale atual
locale

# Listar locales disponíveis
locale -a

# Definir para português
export LANG=pt_BR.UTF-8

# Definir para inglês
export LANG=en_US.UTF-8
```

## ⚡ Dicas

1. **Preferência de Locale:** Use `--locale` para sobrescrever a detecção automática
2. **Compatibilidade:** Parâmetros antigos em português continuam funcionando
3. **Performance:** Detecção acontece uma única vez no startup
4. **Extensibilidade:** Fácil adicionar novos idiomas ao `TRANSLATIONS`

## 📖 Migração de Código

Se você usava parâmetros em português, recomendamos migrar para os novos nomes em inglês:

### Antes

```bash
python main.py --criar-empresa-privada --painel-uf SP --processar-painel
```

### Depois

```bash
python main.py --create-private-subset --panel-uf SP --process-panel
```

As mensagens de ajuda aparecerão automaticamente no seu idioma!

## 🐛 Troubleshooting

### Mensagens em Inglês Quando Esperado Português

1. Verifique o locale do sistema:

   ```bash
   locale
   ```

2. Force o locale português:

   ```bash
   python main.py --locale pt_BR --help
   ```

3. Defina a variável de ambiente:

   ```bash
   export LANG=pt_BR.UTF-8
   python main.py --help
   ```

### Locale Não Reconhecido

Execute para ver locales disponíveis:

```bash
python main.py --help | grep "Language for messages"
```

Use um dos locales listados com `--locale`.

---

**Versão:** 4.0.12  
**Data:** Janeiro 2026  
**Linguagens:** English, Português Brasileiro, Português Europeu
