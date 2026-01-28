"""
Funções relacionadas à manipulação de arquivos locais.

Responsabilidades deste módulo:
- Verificação de espaço em disco
- Extração paralela de arquivos ZIP (file_extractor)
- Remoção de arquivos (file_delete)
- Estimativa de tamanho de arquivos compactados
- Gerenciamento de ciclo de vida de ZIPs (delete_zip_after_extraction)
- Wrapper de alto nível para extração (extract_zip_files)

Para download de arquivos remotos, use src.utils.network.ensure_files_downloaded()
"""
import glob
import logging
import os
import shutil
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

# Importações locais do projeto
from ..config import config

logger = logging.getLogger(__name__)


def check_disk_space(path: str, required_mb: int) -> Tuple[bool, float]:
    """
    Verifica se há espaço suficiente em disco.
    
    Args:
        path: Caminho do diretório para verificar
        required_mb: Espaço mínimo necessário em MB
        
    Returns:
        Tupla (bool, float): Indica se há espaço suficiente e quanto espaço está disponível em MB
    """
    try:
        # Garante que o diretório existe
        os.makedirs(path, exist_ok=True)

        # Obtém informações de espaço do disco
        disk_usage = shutil.disk_usage(path)
        available_mb = disk_usage.free / (1024 * 1024)  # Converte bytes para MB

        # Verifica se há espaço suficiente
        if available_mb < required_mb:
            logger.warning(f"Espaço em disco insuficiente: {available_mb:.2f}MB disponível, {required_mb}MB necessário")
            return False, available_mb

        logger.info(f"Espaço em disco verificado: {available_mb:.2f}MB disponível, {required_mb}MB necessário")
        return True, available_mb
    except Exception as e:
        logger.error(f"Erro ao verificar espaço em disco: {str(e)}")
        return False, 0


def file_extractor(folder_ori: str, folder_dest: str, filename: str = '*.*') -> None:
    """Extrai arquivos ZIP usando processamento paralelo."""
    zip_file_list: List[str] = list(glob.glob(os.path.join(folder_ori, filename)))

    def extract_file(zip_path: str) -> None:
        try:
            logger.info(f'Descompactando: {zip_path}')
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(folder_dest)
        except Exception as e:
            logger.error(f'Erro ao descompactar {zip_path}: {str(e)}')

    # Usa ThreadPoolExecutor para extrair arquivos em paralelo
    with ThreadPoolExecutor(max_workers=config.n_workers) as executor:
        executor.map(extract_file, zip_file_list)


def file_delete(folder: str, filename: str = '*') -> None:
    """Remove arquivos usando processamento paralelo."""
    file_list: List[str] = list(glob.glob(os.path.join(folder, filename)))

    def delete_file(file_path: str) -> None:
        try:
            os.remove(file_path)
            logger.debug(f'Arquivo removido: {file_path}')
        except Exception as e:
            logger.error(f'Erro ao remover arquivo {file_path}: {str(e)}')

    # Usa ThreadPoolExecutor para remover arquivos em paralelo
    with ThreadPoolExecutor(max_workers=config.n_workers) as executor:
        executor.map(delete_file, file_list)


def estimate_zip_extracted_size(zip_path: str) -> float:
    """
    Estima o tamanho que um arquivo ZIP ocupará quando extraído.
    
    Args:
        zip_path: Caminho para o arquivo ZIP
        
    Returns:
        float: Tamanho estimado em MB
    """
    try:
        total_size = 0
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for info in zip_ref.infolist():
                # O tamanho do arquivo descompactado está disponível em file_size
                total_size += info.file_size

        # Converte para MB
        total_size_mb = total_size / (1024 * 1024)

        # Adiciona uma margem de segurança (arquivos CSV podem expandir quando carregados)
        estimated_size_mb = total_size_mb * 1.1

        logger.info(f"Tamanho estimado do ZIP extraído {os.path.basename(zip_path)}: {estimated_size_mb:.2f}MB")
        return estimated_size_mb

    except zipfile.BadZipFile as e:
        logger.error(f"Arquivo ZIP corrompido ou inválido {zip_path}: {str(e)}")
        return 0
    except Exception as e:
        logger.error(f"Erro ao estimar tamanho do ZIP {zip_path}: {str(e)}")
        # Em caso de erro, retorna uma estimativa grande para forçar uma verificação cuidadosa
        return 10000  # 10GB como valor seguro


def delete_zip_after_extraction(zip_path: str, extracted_dir: str, verify_extraction: bool = True) -> bool:
    """
    Deleta um arquivo ZIP com segurança após verificar que foi extraído corretamente.
    
    Args:
        zip_path: Caminho para o arquivo ZIP
        extracted_dir: Diretório onde os arquivos foram extraídos
        verify_extraction: Se True, verifica se a extração foi bem-sucedida antes de deletar
        
    Returns:
        bool: True se o ZIP foi deletado com sucesso, False caso contrário
    """
    try:
        if verify_extraction:
            # Verificar se o arquivo ZIP é válido e tem conteúdo
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_files = zip_ref.namelist()
                
                if not zip_files:
                    logger.warning(f"Arquivo ZIP vazio, não deletando: {os.path.basename(zip_path)}")
                    return False
                
                # Verificar se pelo menos alguns arquivos foram extraídos
                extracted_files = []
                for root, dirs, files in os.walk(extracted_dir):
                    extracted_files.extend(files)
                
                if not extracted_files:
                    logger.warning(f"Nenhum arquivo foi extraído, não deletando ZIP: {os.path.basename(zip_path)}")
                    return False
                
                # Verificação básica: se há arquivos extraídos, consideramos a extração bem-sucedida
                logger.debug(f"Verificação de extração bem-sucedida para {os.path.basename(zip_path)}: "
                           f"{len(zip_files)} arquivos no ZIP, {len(extracted_files)} arquivos extraídos")
        
        # Obter tamanho do arquivo antes de deletar para log
        file_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
        
        # Deletar o arquivo ZIP
        os.remove(zip_path)
        
        logger.info(f"🗑️  ZIP deletado após extração: {os.path.basename(zip_path)} ({file_size_mb:.1f}MB economizados)")
        return True
        
    except zipfile.BadZipFile:
        logger.error(f"Arquivo ZIP corrompido, não deletando: {os.path.basename(zip_path)}")
        return False
    except FileNotFoundError:
        logger.warning(f"Arquivo ZIP não encontrado para deletar: {os.path.basename(zip_path)}")
        return False
    except PermissionError:
        logger.error(f"Sem permissão para deletar ZIP: {os.path.basename(zip_path)}")
        return False
    except Exception as e:
        logger.error(f"Erro ao deletar ZIP {os.path.basename(zip_path)}: {str(e)}")
        return False


def extract_zip_files(source_zip_path: str, unzip_path: str, delete_after: bool = False) -> bool:
    """
    Extrai arquivos ZIP de uma pasta para outra.
    Função wrapper de alto nível para pipeline de processamento.
    Reutiliza file_extractor() para extração paralela.
    
    Args:
        source_zip_path: Pasta contendo arquivos ZIP
        unzip_path: Pasta de destino para extração
        delete_after: Se True, remove ZIPs após extração bem-sucedida
        
    Returns:
        bool: True se extração foi bem-sucedida
    """
    try:
        # Verificar se há ZIPs para extrair
        if not os.path.exists(source_zip_path):
            logger.error(f"Pasta de origem não existe: {source_zip_path}")
            return False
            
        zip_files = [f for f in os.listdir(source_zip_path) if f.endswith('.zip')]
        if not zip_files:
            logger.warning("Nenhum arquivo ZIP encontrado para extrair.")
            return True
        
        logger.info(f"🔄 Extraindo {len(zip_files)} arquivos ZIP...")
        os.makedirs(unzip_path, exist_ok=True)
        
        # Usar função existente de extração paralela
        extract_start = time.time()
        file_extractor(source_zip_path, unzip_path, '*.zip')
        extract_time = time.time() - extract_start
        
        logger.info(f"✅ Extração concluída em {extract_time:.2f}s")
        
        # Deletar ZIPs se solicitado usando função existente
        if delete_after:
            logger.info("🗑️ Removendo arquivos ZIP após extração...")
            for zip_file in zip_files:
                try:
                    zip_path = os.path.join(source_zip_path, zip_file)
                    delete_zip_after_extraction(zip_path, unzip_path, verify_extraction=True)
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao remover {zip_file}: {e}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Erro durante extração: {e}")
        return False
