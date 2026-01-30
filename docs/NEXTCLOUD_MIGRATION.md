# 🔄 Migração para Nextcloud da Receita Federal

## 📋 Resumo

A Receita Federal migrou seu sistema de compartilhamento de arquivos CNPJ para **Nextcloud**. Este documento explica as mudanças implementadas no código para suportar essa nova infraestrutura.

## 🎯 Problema Resolvido

**Antes:** A Receita Federal disponibilizava os arquivos através de listagem HTTP simples.

**Agora:** Os arquivos estão hospedados em um Nextcloud que requer:

- Token de acesso público
- API WebDAV para listagem de diretórios e arquivos
- Autenticação básica com o token

## ✅ Solução Implementada

### 1. **Cliente Nextcloud via WebDAV** (`src/utils/nextcloud_client.py`)

Implementamos um cliente Python puro que **não requer JavaScript, Selenium ou n8n**, utilizando:

- **WebDAV** para comunicação com Nextcloud
- **Autenticação Basic Auth** com token público
- **Requisições HTTP** assíncronas (aiohttp)

### 2. **Funcionalidades**

#### `NextcloudPublicClient`

```python
client = NextcloudPublicClient(
    base_url="https://arquivos.receitafederal.gov.br",
    share_token="gn672Ad4CF8N6TK"
)

# Listar diretórios
folders = await client.get_folders_by_pattern("/Dados/Cadastros/CNPJ", r'\d{4}-\d{2}')

# Listar arquivos ZIP
zip_files = await client.get_zip_files("/Dados/Cadastros/CNPJ/2026-01")

# Gerar URL de download
url = client.get_download_url("/Dados/Cadastros/CNPJ/2026-01/Empresas0.zip")
```

#### Funções Utilitárias

- `parse_nextcloud_url()`: Extrai base_url, token e path de URLs Nextcloud
- `test_nextcloud_connection()`: Testa conectividade com o servidor

### 3. **Compatibilidade Retroativa**

O código **detecta automaticamente** se a URL é do Nextcloud ou tradicional:

```python
# URL Nextcloud (nova)
BASE_URL=https://arquivos.receitafederal.gov.br/index.php/s/gn672Ad4CF8N6TK?dir=/Dados/Cadastros/CNPJ

# URL tradicional (ainda suportada)
BASE_URL=https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/
```

### 4. **Integração Transparente**

As funções existentes continuam funcionando sem alterações:

```python
# Buscar pastas disponíveis
folders = await get_remote_folders(base_url)  # ['2026-01', '2025-12', ...]

# Buscar arquivos ZIP da pasta mais recente
zip_urls, folder = get_latest_month_zip_urls(base_url)
```

## 📦 Dependências Adicionadas

```txt
lxml>=4.9.0  # Para parsing de respostas XML do WebDAV
```

Todas as outras dependências já existiam no projeto:

- `beautifulsoup4` - Parsing HTML/XML
- `aiohttp` - Requisições HTTP assíncronas
- `requests` - Requisições HTTP síncronas

## 🚀 Como Usar

### 1. Atualizar o `.env`

```bash
# URL completa do compartilhamento Nextcloud
BASE_URL=https://arquivos.receitafederal.gov.br/index.php/s/gn672Ad4CF8N6TK?dir=/Dados/Cadastros/CNPJ
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Testar a Conexão

```bash
python test_nextcloud.py
```

### 4. Usar Normalmente

O código existente continua funcionando:

```bash
# Download automático
python main.py

# CLI
cnpj-processor -s csv -t empresas
```

## 🧪 Testes

Execute o script de teste para validar:

```bash
python test_nextcloud.py
```

**Saída esperada:**

```list
✅ URL parseada com sucesso!
✅ Conexão com Nextcloud bem-sucedida! 
✅ Encontradas 33 pastas
✅ Encontrados 37 arquivos ZIP (6.79 GB)
✅ Arquivo acessível!
🎉 O sistema está pronto para baixar arquivos do Nextcloud
```

## 📊 Estrutura do Nextcloud

```folder
/Dados/Cadastros/CNPJ/
├── 2026-01/
│   ├── Cnaes.zip
│   ├── Empresas0.zip
│   ├── Empresas1.zip
│   ├── Estabelecimentos0.zip
│   ├── Simples.zip
│   └── Socios0.zip
├── 2025-12/
│   └── ...
└── 2025-11/
    └── ...
```

## 🔧 Detalhes Técnicos

### Protocolo WebDAV

O Nextcloud suporta WebDAV através do endpoint:

```url
https://arquivos.receitafederal.gov.br/public.php/webdav
```

### Autenticação

```http
Authorization: Basic base64(token:)
```

Onde `token` é o compartilhamento público (ex: `gn672Ad4CF8N6TK`)

### Operações PROPFIND

Listagem de diretórios usando método HTTP `PROPFIND`:

```xml
<?xml version="1.0"?>
<d:propfind xmlns:d="DAV:">
    <d:prop>
        <d:getcontentlength />
        <d:getlastmodified />
        <d:resourcetype />
    </d:prop>
</d:propfind>
```

### Download de Arquivos

URLs geradas seguem o formato:
```
https://arquivos.receitafederal.gov.br/public.php/webdav/{path_completo}
```

Com autenticação Basic Auth usando o token.

## ⚠️ Observações Importantes

1. **Token Público**: O token `gn672Ad4CF8N6TK` é público e está no código. Se a Receita Federal mudar o token, basta atualizar o `.env`.

2. **Rate Limiting**: O Nextcloud pode ter limites de requisições. O código já implementa retry automático e controle de concorrência.

3. **Tamanho dos Arquivos**: A pasta mais recente (2026-01) tem **6.79 GB** em 37 arquivos ZIP.

4. **Pastas Disponíveis**: Atualmente há **33 pastas** disponíveis, de 2023-05 até 2026-01.

## 🐛 Troubleshooting

### Erro: "Couldn't find a tree builder with the features you requested: xml"

**Solução:** Instale lxml
```bash
pip install lxml
```

### Erro: "Autenticação falhou"

**Solução:** Verifique se o token está correto no `.env`:
```bash
BASE_URL=https://arquivos.receitafederal.gov.br/index.php/s/gn672Ad4CF8N6TK?dir=/Dados/Cadastros/CNPJ
```

### Erro: "Nenhuma pasta encontrada"

**Solução:** Verifique se o path está correto. O path deve ser `/Dados/Cadastros/CNPJ`.

## 📚 Referências

- [Nextcloud WebDAV Documentation](https://docs.nextcloud.com/server/latest/developer_manual/client_apis/WebDAV/basic.html)
- [RFC 4918 - WebDAV](https://tools.ietf.org/html/rfc4918)
- [Dados Abertos - Receita Federal](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/dados-publicos-cnpj)

## 🎉 Resultado

✅ **Sistema 100% funcional** com Nextcloud
✅ **Sem dependência de JavaScript ou Selenium**
✅ **Compatibilidade retroativa** mantida
✅ **Downloads funcionando** perfeitamente
✅ **Testes automatizados** passando

---

**Autor:** GitHub Copilot  
**Data:** Janeiro 2026  
**Versão:** 1.0
