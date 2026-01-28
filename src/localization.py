"""
Sistema de Localização (i18n) para CNPJ Processor

Suporta múltiplos idiomas com detecção automática baseada no locale do sistema.
Suporte para português (pt_BR, pt_PT) e inglês (en_US, en_GB).
"""

import locale
import os
from typing import Dict, Optional

# Dicionário de traduções completo
TRANSLATIONS = {
    'en_US': {
        # Argumentos principais
        'tipos_help': 'Types of data to process. If not specified, processes all (relevant for steps "process" and "all").',
        'step_help': 'Step to be executed. Default: all',
        'quiet_help': 'Silent mode - drastically reduces console output',
        'verbose_ui_help': 'More complete visual interface - only works with interactive UI',
        'log_level_help': 'Logging level. Default: INFO',
        'remote_folder_help': 'Use a specific server folder (format AAAA-MM). Example: 2024-05',
        'all_folders_help': 'Download from all available server folders. Overrides --remote-folder',
        'from_folder_help': 'Start download/processing from a specific folder (format AAAA-MM)',
        'force_download_help': 'Force download even if file already exists',
        'create_private_subset_help': 'Create private companies subset (companies only)',
        'create_uf_subset_help': 'Create subset by UF (establishments only). Ex: --create-private-subset SP',
        'output_subfolder_help': 'Name of subfolder where to save parquet files. Use "." for root folder',
        'output_csv_folder_help': 'Folder to save normalized CSVs (default: dados-abertos). For step csv',
        'source_zip_folder_help': 'Source folder of ZIP files (for step "process")',
        'process_all_folders_help': 'Process all date folders (format AAAA-MM) in PATH_ZIP',
        'keep_artifacts_help': 'Keep ZIP and decompressed files (by default removed to save space)',
        'delete_zips_after_extract_help': 'Delete ZIP files after extraction (default)',
        'create_database_help': 'Create DuckDB database after processing (optional)',
        'cleanup_after_db_help': 'Delete parquet files after database creation (only works with --create-database)',
        'keep_parquet_after_db_help': 'Keep parquet files after database creation (only works with --create-database)',
        'show_progress_help': 'Force progress bar display (overrides config)',
        'hide_progress_help': 'Force progress bar hidden (overrides config)',
        'show_pending_help': 'Force pending files list display (overrides config)',
        'hide_pending_help': 'Force pending files list hidden (overrides config)',
        'process_painel_help': 'Process panel data (combines establishments + simples + companies)',
        'painel_uf_help': 'Filter panel by specific UF (ex: SP, GO, MG)',
        'painel_situacao_help': 'Filter by registration status (1=Null, 2=Active, 3=Suspended, 4=Unfit, 8=Deleted)',
        'painel_include_inactive_help': 'Include inactive establishments in panel',
        'normalize_csv_help': 'Generate normalized CSV files (with same standardization rules as parquets)',
        'show_latest_folder_help': 'Show the most recent available remote folder and exit',
        'version_help': 'Display cnpj-processor version and exit',
        
        # Mensagens gerais
        'loading_env': 'Loading environment variables...',
        'env_loaded_success': 'Environment variables loaded successfully',
        'env_load_error': 'Error loading environment variables. Check .env file',
        'processors_initialized': 'Refactored architecture initialized successfully',
        'processors_init_error': 'Failed to initialize new architecture. Check logs.',
        'network_offline': '⚠️ No network connectivity. Some features may be limited.',
        'disk_space_warning': '⚠️ Limited disk space. Monitoring resources during execution.',
        'step_completed': 'Step completed',
        'step_failed': 'Step failed',
        'processing_complete': 'Processing completed',
        'total_execution_time': 'TOTAL EXECUTION TIME:',
        'final_status': 'FINAL STATUS:',
        'success': 'SUCCESS',
        'failure': 'FAILURE',
    },
    'pt_BR': {
        # Argumentos principais
        'tipos_help': 'Tipos de dados a processar. Se não especificado, processa todos (relevante para steps "process" e "all").',
        'step_help': 'Etapa a ser executada. Padrão: all',
        'quiet_help': 'Modo silencioso - reduz drasticamente as saídas no console',
        'verbose_ui_help': 'Interface visual mais completa - só funciona com UI interativo',
        'log_level_help': 'Nível de logging. Padrão: INFO',
        'remote_folder_help': 'Usar uma pasta específica do servidor (formato AAAA-MM). Exemplo: 2024-05',
        'all_folders_help': 'Baixar de todas as pastas disponíveis do servidor. Sobrescreve --remote-folder',
        'from_folder_help': 'Iniciar download/processamento a partir de uma pasta específica (formato AAAA-MM)',
        'force_download_help': 'Forçar download mesmo que arquivo já exista',
        'create_private_subset_help': 'Criar subconjunto de empresas privadas (apenas para empresas)',
        'create_uf_subset_help': 'Criar subconjunto por UF (apenas para estabelecimentos). Ex: --create-private-subset SP',
        'output_subfolder_help': 'Nome da subpasta onde salvar os arquivos parquet. Use "." para pasta raiz',
        'output_csv_folder_help': 'Pasta onde salvar CSVs normalizados (padrão: dados-abertos). Para step csv',
        'source_zip_folder_help': 'Pasta de origem dos arquivos ZIP (para step "process")',
        'process_all_folders_help': 'Processar todas as pastas de data (formato AAAA-MM) em PATH_ZIP',
        'keep_artifacts_help': 'Manter arquivos ZIP e descompactados (por padrão são removidos para economizar espaço)',
        'delete_zips_after_extract_help': 'Deletar arquivos ZIP após extração (padrão)',
        'create_database_help': 'Criar banco de dados DuckDB após processamento (opcional)',
        'cleanup_after_db_help': 'Deletar arquivos parquet após criação do banco DuckDB (só funciona com --create-database)',
        'keep_parquet_after_db_help': 'Manter arquivos parquet após criação do banco (só funciona com --create-database)',
        'show_progress_help': 'Forçar exibição da barra de progresso (sobrescreve config)',
        'hide_progress_help': 'Forçar ocultação da barra de progresso (sobrescreve config)',
        'show_pending_help': 'Forçar exibição da lista de arquivos pendentes (sobrescreve config)',
        'hide_pending_help': 'Forçar ocultação da lista de arquivos pendentes (sobrescreve config)',
        'process_painel_help': 'Processar dados do painel (combina estabelecimentos + simples + empresas)',
        'painel_uf_help': 'Filtrar painel por UF específica (ex: SP, GO, MG)',
        'painel_situacao_help': 'Filtrar por situação cadastral (1=Nula, 2=Ativa, 3=Suspensa, 4=Inapta, 8=Baixada)',
        'painel_include_inactive_help': 'Incluir estabelecimentos inativos no painel',
        'normalize_csv_help': 'Gerar arquivos CSV normalizados (com as mesmas regras de padronização dos parquets)',
        'show_latest_folder_help': 'Exibir a pasta remota mais recente disponível e sair',
        'version_help': 'Exibir a versão do cnpj-processor e sair',
        
        # Mensagens gerais
        'loading_env': 'Carregando variáveis de ambiente...',
        'env_loaded_success': 'Variáveis de ambiente carregadas com sucesso',
        'env_load_error': 'Erro ao carregar variáveis de ambiente. Verifique o arquivo .env',
        'processors_initialized': 'Arquitetura refatorada inicializada com sucesso',
        'processors_init_error': 'Falha ao inicializar nova arquitetura. Verifique os logs.',
        'network_offline': '⚠️ Sem conectividade de rede. Algumas funcionalidades podem estar limitadas.',
        'disk_space_warning': '⚠️ Espaço em disco limitado. Monitorando recursos durante execução.',
        'step_completed': 'Etapa concluída',
        'step_failed': 'Etapa falhou',
        'processing_complete': 'Processamento concluído',
        'total_execution_time': 'TEMPO TOTAL DE EXECUÇÃO:',
        'final_status': 'STATUS FINAL:',
        'success': 'SUCESSO',
        'failure': 'FALHA',
    },
    'pt_PT': {  # Portuguese (Portugal) - reuse pt_BR as base
        'tipos_help': 'Tipos de dados a processar. Se não especificado, processa todos (relevante para steps "process" e "all").',
        'step_help': 'Etapa a ser executada. Padrão: all',
        'quiet_help': 'Modo silencioso - reduz drasticamente as saídas na consola',
        'verbose_ui_help': 'Interface visual mais completa - só funciona com UI interativo',
        'log_level_help': 'Nível de logging. Padrão: INFO',
        'remote_folder_help': 'Usar uma pasta específica do servidor (formato AAAA-MM). Exemplo: 2024-05',
        'all_folders_help': 'Descarregar de todas as pastas disponíveis do servidor. Sobrescreve --remote-folder',
        'from_folder_help': 'Iniciar descarga/processamento a partir de uma pasta específica (formato AAAA-MM)',
        'force_download_help': 'Forçar descarga mesmo que ficheiro já exista',
        'create_private_subset_help': 'Criar subconjunto de empresas privadas (apenas para empresas)',
        'create_uf_subset_help': 'Criar subconjunto por UF (apenas para estabelecimentos). Ex: --create-private-subset SP',
        'output_subfolder_help': 'Nome da subpasta onde guardar os ficheiros parquet. Use "." para pasta raiz',
        'output_csv_folder_help': 'Pasta onde guardar CSVs normalizados (padrão: dados-abertos). Para step csv',
        'source_zip_folder_help': 'Pasta de origem dos ficheiros ZIP (para step "process")',
        'process_all_folders_help': 'Processar todas as pastas de data (formato AAAA-MM) em PATH_ZIP',
        'keep_artifacts_help': 'Manter ficheiros ZIP e descompactados (por padrão são removidos para economizar espaço)',
        'delete_zips_after_extract_help': 'Eliminar ficheiros ZIP após extração (padrão)',
        'create_database_help': 'Criar base de dados DuckDB após processamento (opcional)',
        'cleanup_after_db_help': 'Eliminar ficheiros parquet após criação da base de dados DuckDB (só funciona com --create-database)',
        'keep_parquet_after_db_help': 'Manter ficheiros parquet após criação da base de dados (só funciona com --create-database)',
        'show_progress_help': 'Forçar exibição da barra de progresso (sobrescreve config)',
        'hide_progress_help': 'Forçar ocultação da barra de progresso (sobrescreve config)',
        'show_pending_help': 'Forçar exibição da lista de ficheiros pendentes (sobrescreve config)',
        'hide_pending_help': 'Forçar ocultação da lista de ficheiros pendentes (sobrescreve config)',
        'process_painel_help': 'Processar dados do painel (combina estabelecimentos + simples + empresas)',
        'painel_uf_help': 'Filtrar painel por UF específica (ex: SP, GO, MG)',
        'painel_situacao_help': 'Filtrar por situação cadastral (1=Nula, 2=Ativa, 3=Suspensa, 4=Inapta, 8=Baixada)',
        'painel_include_inactive_help': 'Incluir estabelecimentos inativos no painel',
        'normalize_csv_help': 'Gerar ficheiros CSV normalizados (com as mesmas regras de padronização dos parquets)',
        'show_latest_folder_help': 'Exibir a pasta remota mais recente disponível e sair',
        'version_help': 'Exibir a versão do cnpj-processor e sair',
        
        # Mensagens gerais
        'loading_env': 'Carregando variáveis de ambiente...',
        'env_loaded_success': 'Variáveis de ambiente carregadas com sucesso',
        'env_load_error': 'Erro ao carregar variáveis de ambiente. Verifique o ficheiro .env',
        'processors_initialized': 'Arquitetura refatorada inicializada com sucesso',
        'processors_init_error': 'Falha ao inicializar nova arquitetura. Verifique os registos.',
        'network_offline': '⚠️ Sem conectividade de rede. Algumas funcionalidades podem estar limitadas.',
        'disk_space_warning': '⚠️ Espaço em disco limitado. Monitorando recursos durante execução.',
        'step_completed': 'Etapa concluída',
        'step_failed': 'Etapa falhou',
        'processing_complete': 'Processamento concluído',
        'total_execution_time': 'TEMPO TOTAL DE EXECUÇÃO:',
        'final_status': 'ESTADO FINAL:',
        'success': 'SUCESSO',
        'failure': 'FALHA',
    }
}


class Localization:
    """
    Sistema de localização para suportar múltiplos idiomas.
    
    Detecta automaticamente o locale do sistema e fornece traduções.
    Suporta português (pt_BR, pt_PT) e inglês (en_US, en_GB).
    """
    
    _instance = None
    _current_locale = None
    _translations = TRANSLATIONS
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Inicializa o sistema de localização."""
        # Tentar detectar locale do sistema
        system_locale = self._detect_system_locale()
        
        # Verificar variável de ambiente LANG ou LANGUAGE
        env_locale = os.environ.get('LANG', '').split('.')[0]
        env_language = os.environ.get('LANGUAGE', '').split(':')[0]
        
        # Prioridade: env var > system > padrão (en_US)
        detected_locale = env_locale or env_language or system_locale or 'en_US'
        
        # Normalizar locale
        self._current_locale = self._normalize_locale(detected_locale)
    
    def _detect_system_locale(self) -> Optional[str]:
        """Detecta o locale do sistema operacional."""
        try:
            system_locale, _ = locale.getlocale()
            if system_locale:
                return system_locale.replace('_', '_').split('.')[0]
        except Exception:
            pass
        return None
    
    def _normalize_locale(self, locale_str: str) -> str:
        """
        Normaliza string de locale para formato padrão.
        
        Exemplos:
            'pt' → 'pt_BR'
            'pt_BR' → 'pt_BR'
            'pt-br' → 'pt_BR'
            'en' → 'en_US'
            'en_US' → 'en_US'
        """
        if not locale_str:
            return 'en_US'
        
        # Converter para uppercase e _ separador
        normalized = locale_str.replace('-', '_').upper()
        
        # Mapeamento de variações para padrão
        mapping = {
            'PT': 'pt_BR',
            'PT_BR': 'pt_BR',
            'PT_PT': 'pt_PT',
            'EN': 'en_US',
            'EN_US': 'en_US',
            'EN_GB': 'en_US',  # Usar en_US como fallback para en_GB
        }
        
        # Tentar encontrar match exato
        for key, value in mapping.items():
            if normalized.startswith(key):
                return value
        
        # Se contém 'PT', usar pt_BR
        if 'PT' in normalized:
            return 'pt_BR'
        
        # Padrão: en_US
        return 'en_US'
    
    def set_locale(self, locale_str: str) -> None:
        """Define o locale manualmente."""
        self._current_locale = self._normalize_locale(locale_str)
    
    def get_locale(self) -> str:
        """Retorna o locale atual."""
        return self._current_locale
    
    def get_available_locales(self) -> list:
        """Retorna lista de locales disponíveis."""
        return list(self._translations.keys())
    
    def translate(self, key: str, default: Optional[str] = None) -> str:
        """
        Traduz uma chave para o idioma atual.
        
        Args:
            key: Chave da tradução
            default: Valor padrão se chave não encontrada
            
        Returns:
            Texto traduzido ou default
        """
        locale_dict = self._translations.get(self._current_locale, {})
        return locale_dict.get(key, default or key)
    
    def t(self, key: str, default: Optional[str] = None) -> str:
        """Atalho para translate()."""
        return self.translate(key, default)
    
    def get_help_text(self, param_name: str) -> str:
        """
        Obtém texto de ajuda para um parâmetro.
        
        Args:
            param_name: Nome do parâmetro (sem hífens)
            
        Returns:
            Texto de ajuda traduzido
        """
        key = f'{param_name}_help'
        return self.translate(key, '')


# Instância global singleton
_localization_instance = None

def get_localization() -> Localization:
    """Obtém instância global do sistema de localização."""
    global _localization_instance
    if _localization_instance is None:
        _localization_instance = Localization()
    return _localization_instance


def set_locale(locale_str: str) -> None:
    """Define o locale globalmente."""
    get_localization().set_locale(locale_str)


def t(key: str, default: Optional[str] = None) -> str:
    """Função global de tradução."""
    return get_localization().t(key, default)


def get_current_locale() -> str:
    """Obtém locale atual."""
    return get_localization().get_locale()
