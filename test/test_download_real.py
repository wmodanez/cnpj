"""
Teste rápido de download de um arquivo pequeno do Nextcloud.
"""

import asyncio
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from dotenv import load_dotenv
from src.async_downloader import download_file
import aiohttp
from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn

load_dotenv()


async def test_real_download():
    """Testa download real de um arquivo pequeno."""
    
    print("\n" + "=" * 80)
    print("🧪 TESTE DE DOWNLOAD REAL DO NEXTCLOUD")
    print("=" * 80)
    
    # Obter URL e configurar cliente
    base_url = os.getenv('BASE_URL')
    
    from src.utils.nextcloud_client import parse_nextcloud_url, NextcloudPublicClient
    
    parsed_base, parsed_token, parsed_path = parse_nextcloud_url(base_url)
    
    if not parsed_base or not parsed_token:
        print("❌ Erro ao parsear URL")
        return False
    
    # Criar cliente
    client = NextcloudPublicClient(parsed_base, parsed_token)
    
    # Buscar pasta mais recente
    folders = await client.get_folders_by_pattern(parsed_path, r'\d{4}-\d{2}')
    if not folders:
        print("❌ Nenhuma pasta encontrada")
        return False
    
    latest_folder = folders[0]
    folder_path = f"{parsed_path.rstrip('/')}/{latest_folder}"
    
    # Buscar arquivos
    zip_files = await client.get_zip_files(folder_path)
    if not zip_files:
        print("❌ Nenhum arquivo encontrado")
        return False
    
    # Pegar o menor arquivo (Cnaes.zip é geralmente o menor, ~20KB)
    zip_files_sorted = sorted(zip_files, key=lambda x: x[1])
    test_url, test_size = zip_files_sorted[0]
    test_filename = test_url.split('/')[-1].split('?')[0]
    
    print(f"\n📥 Arquivo selecionado para teste: {test_filename}")
    print(f"📊 Tamanho: {test_size / 1024:.2f} KB")
    print(f"🔗 URL: {test_url[:80]}...")
    
    # Criar diretório de destino temporário
    test_dir = Path("temp_test_download")
    test_dir.mkdir(exist_ok=True)
    destination = test_dir / test_filename
    
    # Remover arquivo se já existir
    if destination.exists():
        destination.unlink()
    
    print(f"\n⏬ Iniciando download...")
    
    # Fazer download
    semaphore = asyncio.Semaphore(1)
    
    # Criar autenticação
    auth = aiohttp.BasicAuth(login=parsed_token, password='')
    
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        DownloadColumn(),
        TransferSpeedColumn(),
    ) as progress:
        task_id = progress.add_task(f"Baixando {test_filename}", total=test_size)
        
        async with aiohttp.ClientSession() as session:
            result_filename, error, skip_reason = await download_file(
                session=session,
                url=test_url,
                destination_path=str(destination),
                semaphore=semaphore,
                progress=progress,
                task_id=task_id,
                force_download=True,
                auth=auth  # Passar autenticação Nextcloud
            )
    
    # Verificar resultado
    if error:
        print(f"\n❌ Erro no download: {error}")
        return False
    
    if skip_reason:
        print(f"\n⚠️  Download pulado: {skip_reason}")
    
    if destination.exists():
        downloaded_size = destination.stat().st_size
        print(f"\n✅ Download concluído com sucesso!")
        print(f"📁 Arquivo salvo em: {destination}")
        print(f"📊 Tamanho baixado: {downloaded_size / 1024:.2f} KB")
        
        # Verificar integridade
        if downloaded_size == test_size:
            print(f"✅ Tamanho correto! ({downloaded_size} bytes)")
        else:
            print(f"⚠️  Tamanho diferente: esperado {test_size}, obtido {downloaded_size}")
        
        # Limpar arquivo de teste
        print(f"\n🧹 Limpando arquivo de teste...")
        destination.unlink()
        test_dir.rmdir()
        print(f"✅ Limpeza concluída")
        
        return True
    else:
        print(f"\n❌ Arquivo não foi criado")
        return False


if __name__ == "__main__":
    print("\n🚀 Iniciando teste de download real...\n")
    
    try:
        success = asyncio.run(test_real_download())
        
        if success:
            print("\n" + "=" * 80)
            print("🎉 TESTE DE DOWNLOAD CONCLUÍDO COM SUCESSO!")
            print("=" * 80)
            print("\n✅ O sistema está pronto para downloads em produção!")
            sys.exit(0)
        else:
            print("\n" + "=" * 80)
            print("❌ TESTE DE DOWNLOAD FALHOU")
            print("=" * 80)
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n💥 Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
