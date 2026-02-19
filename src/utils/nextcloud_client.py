"""
Cliente para interagir com Nextcloud público via WebDAV.

Este módulo fornece funções para acessar compartilhamentos públicos do Nextcloud
sem necessidade de JavaScript ou Selenium, usando apenas a API WebDAV.

RESPONSABILIDADES:
- Descobrir pastas e arquivos remotos disponíveis (listagem via WebDAV)
- Gerar URLs de download corretas
- Fornecer lógica centralizada de autenticação para Nextcloud público

A autenticação para downloads é reutilizada por async_downloader._get_auth_for_url()
para manter consistência.
"""

import asyncio
import logging
import re
from typing import List, Tuple, Optional
from urllib.parse import quote, urljoin
import aiohttp
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class NextcloudPublicClient:
    """Cliente para acessar compartilhamentos públicos do Nextcloud."""
    
    def __init__(self, base_url: str, share_token: str):
        """
        Inicializa o cliente Nextcloud.
        
        Args:
            base_url: URL base do Nextcloud (ex: https://arquivos.receitafederal.gov.br)
            share_token: Token do compartilhamento público (ex: gn672Ad4CF8N6TK)
        """
        self.base_url = base_url.rstrip('/')
        self.share_token = share_token
        # Para compartilhamentos públicos do Nextcloud
        # URL WebDAV: /public.php/webdav/ (SEM o token no path)
        # Token vai na autenticação básica: username=token, password=vazio
        self.webdav_url = f"{self.base_url}/public.php/webdav"
        
        # Autenticação básica para compartilhamento público do Nextcloud
        # Username = token do compartilhamento, password = vazio
        self.auth = aiohttp.BasicAuth(login=share_token, password='')
        self.requests_auth = (share_token, '')
        
        logger.info(f"Cliente Nextcloud inicializado: {self.base_url}")
        logger.debug(f"WebDAV URL: {self.webdav_url}")
        logger.debug(f"Token para autenticação: {self.share_token[:10]}...")
    
    def _get_propfind_body(self) -> str:
        """Retorna o corpo XML para requisições PROPFIND."""
        return '''<?xml version="1.0"?>
<d:propfind xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
    <d:prop>
        <d:getlastmodified />
        <d:getetag />
        <d:getcontenttype />
        <d:resourcetype />
        <d:getcontentlength />
        <oc:id />
        <oc:fileid />
        <oc:permissions />
        <oc:size />
        <d:displayname />
    </d:prop>
</d:propfind>'''
    
    async def list_directory(self, path: str = "/") -> List[dict]:
        """
        Lista o conteúdo de um diretório no Nextcloud.
        
        Args:
            path: Caminho do diretório (ex: "/", "/Dados/Cadastros/CNPJ")
            
        Returns:
            Lista de dicionários com informações dos arquivos/pastas:
            {
                'name': 'arquivo.zip',
                'path': '/Dados/arquivo.zip',
                'is_directory': False,
                'size': 1024,
                'last_modified': '2024-01-01T12:00:00Z'
            }
        """
        # Normalizar o caminho
        if not path.startswith('/'):
            path = '/' + path
        
        # Construir URL WebDAV completa
        encoded_path = quote(path.encode('utf-8'))
        url = f"{self.webdav_url}{encoded_path}"
        
        headers = {
            'Content-Type': 'application/xml',
            'Depth': '1'  # Lista apenas o nível atual
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                logger.debug(f"Fazendo requisição PROPFIND para: {url}")
                async with session.request(
                    'PROPFIND',
                    url,
                    auth=self.auth,
                    headers=headers,
                    data=self._get_propfind_body(),
                    timeout=aiohttp.ClientTimeout(total=120, connect=30)
                ) as response:
                    logger.debug(f"Status da resposta WebDAV: {response.status}")
                    if response.status == 207:  # Multi-Status (sucesso WebDAV)
                        xml_content = await response.text()
                        return self._parse_propfind_response(xml_content, path)
                    elif response.status == 401:
                        logger.error(f"❌ Autenticação falhou (HTTP 401). URL: {url}")
                        logger.error(f"❌ Verifique se o token está correto: {self.share_token}")
                        return []
                    elif response.status == 404:
                        logger.error(f"❌ Diretório não encontrado: {path}")
                        return []
                    else:
                        logger.error(f"❌ Erro ao listar diretório {path}: HTTP {response.status}")
                        logger.debug(f"   Resposta: {await response.text()}")
                        return []
        except asyncio.TimeoutError as e:
            logger.error(f"❌ Timeout ao acessar Nextcloud em {path} (limite: 120s)")
            logger.error(f"   Verifique sua conexão de rede ou tente novamente")
            return []
        except Exception as e:
            logger.error(f"❌ Erro ao acessar Nextcloud em {path}: {e}")
            import traceback
            logger.debug(f"   Traceback: {traceback.format_exc()}")
            return []
    
    def _parse_propfind_response(self, xml_content: str, base_path: str) -> List[dict]:
        """
        Parseia a resposta XML do PROPFIND.
        
        Args:
            xml_content: Conteúdo XML da resposta
            base_path: Caminho base usado na requisição
            
        Returns:
            Lista de itens parseados
        """
        items = []
        
        try:
            # Tentar primeiro lxml, se não funcionar, usar html.parser como fallback
            try:
                soup = BeautifulSoup(xml_content, 'lxml-xml')
            except:
                try:
                    soup = BeautifulSoup(xml_content, 'xml')
                except:
                    soup = BeautifulSoup(xml_content, 'html.parser')
            
            responses = soup.find_all('d:response')
            
            for response in responses:
                href_tag = response.find('d:href')
                if not href_tag:
                    continue
                
                href = href_tag.text
                
                # Extrair o caminho relativo
                # href geralmente vem como: /public.php/webdav/Dados/arquivo.zip
                if '/webdav' in href:
                    relative_path = href.split('/webdav', 1)[1]
                else:
                    relative_path = href
                
                # Pular o próprio diretório base
                if relative_path == base_path or relative_path == base_path + '/':
                    continue
                
                # Extrair propriedades
                propstat = response.find('d:propstat')
                if not propstat:
                    continue
                
                prop = propstat.find('d:prop')
                if not prop:
                    continue
                
                # Verificar se é diretório
                resourcetype = prop.find('d:resourcetype')
                is_directory = resourcetype and resourcetype.find('d:collection') is not None
                
                # Tamanho do arquivo
                size_tag = prop.find('d:getcontentlength')
                size = int(size_tag.text) if size_tag and size_tag.text else 0
                
                # Data de modificação
                lastmod_tag = prop.find('d:getlastmodified')
                last_modified = lastmod_tag.text if lastmod_tag else None
                
                # Nome do arquivo/diretório
                name = relative_path.rstrip('/').split('/')[-1]
                
                item = {
                    'name': name,
                    'path': relative_path,
                    'is_directory': is_directory,
                    'size': size,
                    'last_modified': last_modified
                }
                
                items.append(item)
                logger.debug(f"Item encontrado: {name} ({'DIR' if is_directory else 'FILE'}, {size} bytes)")
            
            logger.info(f"Encontrados {len(items)} itens em {base_path}")
            return items
            
        except Exception as e:
            logger.error(f"Erro ao parsear resposta PROPFIND: {e}")
            return []
    
    def get_download_url(self, file_path: str) -> str:
        """
        Gera a URL de download direto para um arquivo.
        
        Args:
            file_path: Caminho do arquivo (ex: "/Dados/arquivo.zip")
            
        Returns:
            URL completa para download
        """
        # Normalizar o caminho
        if not file_path.startswith('/'):
            file_path = '/' + file_path
        
        # URL de download usando WebDAV
        encoded_path = quote(file_path.encode('utf-8'))
        download_url = f"{self.webdav_url}{encoded_path}"
        
        logger.debug(f"URL de download gerada: {download_url}")
        return download_url
    
    async def get_folders_by_pattern(self, base_path: str, pattern: str = r'\d{4}-\d{2}') -> List[str]:
        """
        Busca pastas que correspondem a um padrão regex.
        
        Args:
            base_path: Caminho base onde buscar (ex: "/Dados/Cadastros/CNPJ")
            pattern: Padrão regex (padrão: pastas no formato AAAA-MM)
            
        Returns:
            Lista de nomes de pastas que correspondem ao padrão, ordenadas
        """
        items = await self.list_directory(base_path)
        
        folders = []
        regex = re.compile(pattern)
        
        for item in items:
            if item['is_directory'] and regex.fullmatch(item['name']):
                folders.append(item['name'])
                logger.debug(f"Pasta encontrada: {item['name']}")
        
        # Ordenar em ordem decrescente (mais recente primeiro)
        folders.sort(reverse=True)
        
        logger.info(f"Encontradas {len(folders)} pastas correspondentes ao padrão '{pattern}' em {base_path}")
        return folders
    
    async def get_zip_files(self, directory_path: str) -> List[Tuple[str, int]]:
        """
        Lista todos os arquivos .zip em um diretório com seus tamanhos.
        
        Args:
            directory_path: Caminho do diretório
            
        Returns:
            Lista de tuplas (url_download, tamanho_bytes)
        """
        items = await self.list_directory(directory_path)
        
        zip_files = []
        for item in items:
            if not item['is_directory'] and item['name'].lower().endswith('.zip'):
                download_url = self.get_download_url(item['path'])
                zip_files.append((download_url, item['size']))
                logger.debug(f"Arquivo ZIP: {item['name']} ({item['size']} bytes)")
        
        logger.info(f"Encontrados {len(zip_files)} arquivos ZIP em {directory_path}")
        return zip_files


def parse_nextcloud_url(url: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Extrai base_url, token e path de uma URL de compartilhamento público do Nextcloud.
    
    Args:
        url: URL completa do Nextcloud
            Ex: https://arquivos.receitafederal.gov.br/index.php/s/gn672Ad4CF8N6TK?dir=/Dados
    
    Returns:
        Tupla (base_url, share_token, initial_path) ou (None, None, None) se inválida
    """
    try:
        # Padrão para URLs de compartilhamento público do Nextcloud
        # Formato: https://domain/index.php/s/{TOKEN}?dir={PATH}
        pattern = r'(https?://[^/]+)/index\.php/s/([^/?]+)(?:\?dir=([^&]+))?'
        match = re.match(pattern, url)
        
        if match:
            base_url = match.group(1)
            share_token = match.group(2)
            initial_path = match.group(3) if match.group(3) else '/'
            
            logger.info(f"URL parseada: base={base_url}, token={share_token}, path={initial_path}")
            return base_url, share_token, initial_path
        else:
            logger.error(f"URL não corresponde ao formato esperado do Nextcloud: {url}")
            return None, None, None
            
    except Exception as e:
        logger.error(f"Erro ao parsear URL do Nextcloud: {e}")
        return None, None, None


async def test_nextcloud_connection(base_url: str, share_token: str) -> bool:
    """
    Testa a conexão com o Nextcloud.
    
    Args:
        base_url: URL base do Nextcloud
        share_token: Token do compartilhamento público
        
    Returns:
        True se a conexão foi bem-sucedida
    """
    try:
        client = NextcloudPublicClient(base_url, share_token)
        items = await client.list_directory('/')
        
        if items is not None:
            logger.info(f"✅ Conexão com Nextcloud bem-sucedida! Encontrados {len(items)} itens na raiz.")
            return True
        else:
            logger.error("❌ Falha ao conectar com Nextcloud")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro ao testar conexão Nextcloud: {e}")
        return False
