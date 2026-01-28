"""
Exemplo de uso do sistema de localização no argparse.

Este arquivo mostra como integrar o sistema de localização ao main.py.
"""

import argparse
from src.localization import get_localization, t, get_current_locale

def create_parser_with_locale():
    """
    Cria um parser com suporte a múltiplos idiomas.
    """
    loc = get_localization()
    
    parser = argparse.ArgumentParser(
        description=f"CNPJ Data Processor v4.0.9 (Locale: {loc.get_locale()})"
    )
    
    # Argumentos com suporte a localização
    parser.add_argument(
        '', '-t',
        nargs='+',
        choices=['empresas', 'estabelecimentos', 'simples', 'socios'],
        default=[],
        help=loc.get_help_text('tipos')
    )
    
    parser.add_argument(
        '--step', '-s',
        choices=['download', 'extract', 'csv', 'process', 'database', 'painel', 'all'],
        default='all',
        help=loc.get_help_text('step')
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help=loc.get_help_text('quiet')
    )
    
    parser.add_argument(
        '--verbose-ui', '-v',
        action='store_true',
        help=loc.get_help_text('verbose_ui')
    )
    
    parser.add_argument(
        '--log-level', '-l',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help=loc.get_help_text('log_level')
    )
    
    parser.add_argument(
        '--remote-folder', '-r',
        type=str,
        help=loc.get_help_text('remote_folder')
    )
    
    parser.add_argument(
        '--all-folders', '-a',
        action='store_true',
        help=loc.get_help_text('all_folders')
    )
    
    parser.add_argument(
        '--from-folder', '-f',
        type=str,
        help=loc.get_help_text('from_folder')
    )
    
    parser.add_argument(
        '--force-download', '-F',
        action='store_true',
        help=loc.get_help_text('force_download')
    )
    
    # Novos nomes em inglês para parâmetros anteriormente em português
    parser.add_argument(
        '--create-private-subset', '-E',
        action='store_true',
        dest='create_private_subset',
        help=loc.get_help_text('create_private_subset')
    )
    
    parser.add_argument(
        '--create-uf-subset', '-U',
        type=str,
        metavar='UF',
        dest='create_uf_subset',
        help=loc.get_help_text('create_uf_subset')
    )
    
    parser.add_argument(
        '--output-subfolder', '-o',
        type=str,
        help=loc.get_help_text('output_subfolder')
    )
    
    parser.add_argument(
        '--output-csv-folder',
        type=str,
        help=loc.get_help_text('output_csv_folder')
    )
    
    parser.add_argument(
        '--source-zip-folder', '-z',
        type=str,
        help=loc.get_help_text('source_zip_folder')
    )
    
    parser.add_argument(
        '--process-all-folders', '-p',
        action='store_true',
        help=loc.get_help_text('process_all_folders')
    )
    
    parser.add_argument(
        '--keep-artifacts', '-k',
        action='store_true',
        help=loc.get_help_text('keep_artifacts')
    )
    
    parser.add_argument(
        '--delete-zips-after-extract',
        action='store_true',
        dest='delete_zips_after_extract',
        help=loc.get_help_text('delete_zips_after_extract')
    )
    
    parser.add_argument(
        '--create-database', '-D',
        action='store_true',
        help=loc.get_help_text('create_database')
    )
    
    parser.add_argument(
        '--cleanup-after-db', '-c',
        action='store_true',
        help=loc.get_help_text('cleanup_after_db')
    )
    
    parser.add_argument(
        '--keep-parquet-after-db', '-K',
        action='store_true',
        help=loc.get_help_text('keep_parquet_after_db')
    )
    
    parser.add_argument(
        '--show-progress', '-B',
        action='store_true',
        help=loc.get_help_text('show_progress')
    )
    
    parser.add_argument(
        '--hide-progress', '-H',
        action='store_true',
        help=loc.get_help_text('hide_progress')
    )
    
    parser.add_argument(
        '--show-pending', '-S',
        action='store_true',
        help=loc.get_help_text('show_pending')
    )
    
    parser.add_argument(
        '--hide-pending', '-W',
        action='store_true',
        help=loc.get_help_text('hide_pending')
    )
    
    # Novos nomes em inglês para parâmetros do painel
    parser.add_argument(
        '--process-panel', '-P',
        action='store_true',
        dest='process_panel',
        help=loc.get_help_text('process_painel')
    )
    
    parser.add_argument(
        '--panel-uf',
        type=str,
        metavar='UF',
        dest='panel_uf',
        help=loc.get_help_text('painel_uf')
    )
    
    parser.add_argument(
        '--panel-status',
        type=int,
        metavar='CODE',
        dest='panel_status',
        help=loc.get_help_text('painel_situacao')
    )
    
    parser.add_argument(
        '--panel-include-inactive',
        action='store_true',
        dest='panel_include_inactive',
        help=loc.get_help_text('painel_include_inactive')
    )
    
    parser.add_argument(
        '--normalize-csv',
        action='store_true',
        help=loc.get_help_text('normalize_csv')
    )
    
    parser.add_argument(
        '--show-latest-folder', '--latest',
        action='store_true',
        dest='show_latest_folder',
        help=loc.get_help_text('show_latest_folder')
    )
    
    parser.add_argument(
        '--version', '-V',
        action='store_true',
        help=loc.get_help_text('version')
    )
    
    # Adicionar opção de locale
    parser.add_argument(
        '--locale',
        type=str,
        choices=['pt_BR', 'pt_PT', 'en_US', 'en_GB'],
        help='Language for messages (available: pt_BR, pt_PT, en_US, en_GB)'
    )
    
    return parser


# Uso no main.py:
# 
# from src.localization_example import create_parser_with_locale
# 
# parser = create_parser_with_locale()
# args = parser.parse_args()
# 
# # Se --locale for especificado, mudar locale
# if hasattr(args, 'locale') and args.locale:
#     from src.localization import set_locale
#     set_locale(args.locale)
#     print(f"Locale mudado para: {args.locale}")
