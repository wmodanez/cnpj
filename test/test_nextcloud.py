"""
Script de teste para validar a integração com Nextcloud da Receita Federal.

Este script testa:
1. Parsing da URL do Nextcloud
2. Conexão com o servidor
3. Listagem de pastas AAAA-MM
4. Listagem de arquivos ZIP
5. Geração de URLs de download
"""

import asyncio
import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from dotenv import load_dotenv
from src.utils.nextcloud_client import (
    NextcloudPublicClient,
    parse_nextcloud_url,
    test_nextcloud_connection
)

# Carregar variáveis de ambiente
load_dotenv()


async def test_nextcloud_integration():
    """Testa a integração completa com Nextcloud."""
    
    print("=" * 80)
    print("🧪 TESTE DE INTEGRAÇÃO COM NEXTCLOUD DA RECEITA FEDERAL")
    print("=" * 80)
    
    # Obter URL do .env
    base_url = os.getenv('BASE_URL')
    if not base_url:
        print("❌ BASE_URL não definida no arquivo .env")
        return False
    
    print(f"\n📍 URL configurada: {base_url}")
    
    # Teste 1: Parsing da URL
    print("\n" + "=" * 80)
    print("1️⃣ TESTE: Parsing da URL do Nextcloud")
    print("=" * 80)
    
    parsed_base, parsed_token, parsed_path = parse_nextcloud_url(base_url)
    
    if parsed_base and parsed_token:
        print(f"✅ URL parseada com sucesso!")
        print(f"   • Base: {parsed_base}")
        print(f"   • Token: {parsed_token}")
        print(f"   • Path: {parsed_path}")
    else:
        print(f"❌ Falha ao parsear URL. Verifique o formato.")
        return False
    
    # Teste 2: Conexão com o servidor
    print("\n" + "=" * 80)
    print("2️⃣ TESTE: Conexão com o servidor Nextcloud")
    print("=" * 80)
    
    connection_ok = await test_nextcloud_connection(parsed_base, parsed_token)
    
    if not connection_ok:
        print("❌ Falha na conexão com o servidor")
        return False
    
    # Teste 3: Listagem de pastas AAAA-MM
    print("\n" + "=" * 80)
    print("3️⃣ TESTE: Listagem de pastas no formato AAAA-MM")
    print("=" * 80)
    
    client = NextcloudPublicClient(parsed_base, parsed_token)
    
    folders = await client.get_folders_by_pattern(parsed_path, r'\d{4}-\d{2}')
    
    if folders:
        print(f"✅ Encontradas {len(folders)} pastas:")
        for i, folder in enumerate(folders[:10], 1):
            print(f"   {i}. {folder}")
        if len(folders) > 10:
            print(f"   ... e mais {len(folders) - 10} pastas")
    else:
        print(f"❌ Nenhuma pasta encontrada em {parsed_path}")
        return False
    
    # Teste 4: Listagem de arquivos ZIP na pasta mais recente
    print("\n" + "=" * 80)
    print("4️⃣ TESTE: Listagem de arquivos ZIP na pasta mais recente")
    print("=" * 80)
    
    latest_folder = folders[0]
    folder_path = f"{parsed_path.rstrip('/')}/{latest_folder}"
    
    print(f"📁 Buscando arquivos em: {folder_path}")
    
    zip_files = await client.get_zip_files(folder_path)
    
    if zip_files:
        print(f"✅ Encontrados {len(zip_files)} arquivos ZIP:")
        
        # Mostrar primeiros 5 arquivos com detalhes
        for i, (url, size) in enumerate(zip_files[:5], 1):
            filename = url.split('/')[-1].split('?')[0]
            size_mb = size / (1024 * 1024)
            print(f"   {i}. {filename} ({size_mb:.2f} MB)")
        
        if len(zip_files) > 5:
            print(f"   ... e mais {len(zip_files) - 5} arquivos")
        
        # Calcular tamanho total
        total_size = sum(size for _, size in zip_files)
        total_size_gb = total_size / (1024 ** 3)
        print(f"\n📊 Tamanho total: {total_size_gb:.2f} GB")
        
    else:
        print(f"❌ Nenhum arquivo ZIP encontrado em {folder_path}")
        return False
    
    # Teste 5: Geração de URL de download
    print("\n" + "=" * 80)
    print("5️⃣ TESTE: Geração de URL de download")
    print("=" * 80)
    
    if zip_files:
        first_file_url, first_file_size = zip_files[0]
        filename = first_file_url.split('/')[-1].split('?')[0]
        
        print(f"📥 URL de download gerada para: {filename}")
        print(f"   {first_file_url[:100]}...")
        print(f"✅ URL gerada com sucesso!")
    
    # Teste 6: Teste de download (apenas headers)
    print("\n" + "=" * 80)
    print("6️⃣ TESTE: Verificação de download (HEAD request)")
    print("=" * 80)
    
    import aiohttp
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(
                first_file_url,
                auth=aiohttp.BasicAuth(login=parsed_token, password=''),
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    content_length = response.headers.get('Content-Length')
                    content_type = response.headers.get('Content-Type')
                    
                    print(f"✅ Arquivo acessível!")
                    print(f"   • Status: {response.status}")
                    print(f"   • Content-Type: {content_type}")
                    if content_length:
                        size_mb = int(content_length) / (1024 * 1024)
                        print(f"   • Tamanho: {size_mb:.2f} MB")
                else:
                    print(f"⚠️  Status inesperado: {response.status}")
                    
    except Exception as e:
        print(f"❌ Erro ao verificar download: {e}")
        return False
    
    # Resumo final
    print("\n" + "=" * 80)
    print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
    print("=" * 80)
    print("\n🎉 O sistema está pronto para baixar arquivos do Nextcloud da Receita Federal")
    print(f"📁 Pasta mais recente disponível: {latest_folder}")
    print(f"📦 Total de arquivos disponíveis: {len(zip_files)}")
    print(f"💾 Tamanho total para download: {total_size_gb:.2f} GB")
    
    return True


async def test_integration_with_async_downloader():
    """Testa as funções de alto nível do async_downloader."""
    
    print("\n" + "=" * 80)
    print("7️⃣ TESTE: Integração com async_downloader.py")
    print("=" * 80)
    
    from src.async_downloader import get_remote_folders, get_latest_month_zip_urls
    
    base_url = os.getenv('BASE_URL')
    
    # Testar get_remote_folders
    print("\n🔍 Testando get_remote_folders()...")
    folders = await get_remote_folders(base_url)
    
    if folders:
        print(f"✅ Encontradas {len(folders)} pastas:")
        for i, folder in enumerate(folders[:5], 1):
            print(f"   {i}. {folder}")
        if len(folders) > 5:
            print(f"   ... e mais {len(folders) - 5} pastas")
    else:
        print("❌ Falha ao buscar pastas")
        return False
    
    # Testar get_latest_month_zip_urls
    print("\n🔍 Testando get_latest_month_zip_urls()...")
    zip_urls, folder_name = get_latest_month_zip_urls(base_url)
    
    if zip_urls and folder_name:
        print(f"✅ Pasta: {folder_name}")
        print(f"✅ Encontrados {len(zip_urls)} arquivos ZIP")
        
        # Mostrar primeiros 3 arquivos
        for i, url in enumerate(zip_urls[:3], 1):
            filename = url.split('/')[-1].split('?')[0]
            print(f"   {i}. {filename}")
        
        if len(zip_urls) > 3:
            print(f"   ... e mais {len(zip_urls) - 3} arquivos")
    else:
        print("❌ Falha ao buscar arquivos ZIP")
        return False
    
    print("\n✅ Integração com async_downloader funcionando!")
    return True


if __name__ == "__main__":
    print("\n🚀 Iniciando testes de integração Nextcloud...\n")
    
    # Executar testes
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Teste básico
        success = loop.run_until_complete(test_nextcloud_integration())
        
        if success:
            # Teste de integração com async_downloader
            success = loop.run_until_complete(test_integration_with_async_downloader())
        
        if success:
            print("\n" + "=" * 80)
            print("🎊 TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
            print("=" * 80)
            sys.exit(0)
        else:
            print("\n" + "=" * 80)
            print("❌ ALGUNS TESTES FALHARAM")
            print("=" * 80)
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Testes interrompidos pelo usuário")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n💥 Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        loop.close()
