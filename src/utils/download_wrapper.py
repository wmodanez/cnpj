"""
Wrapper simples para downloads que automaticamente adiciona autenticação Nextcloud quando necessário.
"""

import aiohttp
from typing import Tuple, Optional
import logging
from urllib.parse import urlparse

from src.utils.nextcloud_client import parse_nextcloud_url

logger = logging.getLogger(__name__)


def get_auth_for_url(url: str) -> Optional[aiohttp.BasicAuth]:
    """
    Detecta se uma URL precisa de autenticação Nextcloud e retorna o auth apropriado.
    
    Args:
        url: URL para verificar
        
    Returns:
        aiohttp.BasicAuth se a URL é do Nextcloud, None caso contrário
    """
    # Verificar se é uma URL do Nextcloud
    if 'public.php/webdav' in url or '/index.php/s/' in url:
        # Tentar extrair o token da URL
        # URL típica: https://domain/public.php/webdav/path/to/file
        # Precisamos encontrar o token compartilhado
        
        # Se a URL contém public.php/webdav, o token deve estar nas configurações
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        base_url = os.getenv('BASE_URL', '')
        if base_url:
            parsed_base, parsed_token, _ = parse_nextcloud_url(base_url)
            if parsed_token:
                logger.debug(f"Autenticação Nextcloud detectada para {url}")
                return aiohttp.BasicAuth(login=parsed_token, password='')
    
    return None


# Versão melhorada da função de download que detecta automaticamente autenticação
async def download_file_with_auto_auth(session: aiohttp.ClientSession, url: str, destination_path: str,
                                       semaphore, progress, task_id, force_download=False):
    """
    Wrapper que detecta automaticamente se precisa de autenticação Nextcloud.
    """
    from src.async_downloader import download_file
    
    # Detectar se precisa autenticação
    auth = get_auth_for_url(url)
    
    if auth:
        logger.debug(f"Usando autenticação Nextcloud para {url}")
    
    # Chamar função original com auth
    return await download_file(
        session=session,
        url=url,
        destination_path=destination_path,
        semaphore=semaphore,
        progress=progress,
        task_id=task_id,
        force_download=force_download,
        auth=auth
    )
