"""
Exemplos de Uso da API CNPJProcessor

Instalação:
    pip install cnpj-processor

Este arquivo demonstra como usar a API programática do cnpj-processor,
que replica todas as funcionalidades disponíveis via linha de comando.
"""

from cnpj_processor import CNPJProcessor

# ============================================================================
# EXEMPLO 1: Consultar Pastas Disponíveis
# ============================================================================

def exemplo_consultar_pastas():
    """Consultar pastas remotas disponíveis."""
    processor = CNPJProcessor()
    
    # Obter pasta mais recente
    latest = processor.get_latest_folder()
    print(f"📅 Pasta mais recente: {latest}")
    
    # Listar todas as pastas disponíveis
    folders = processor.get_available_folders()
    print(f"📂 Pastas disponíveis: {', '.join(folders)}")
    
    return latest, folders

# ============================================================================
# EXEMPLO 2: Pipeline Completo (Download + Processamento + Banco de Dados)
# ============================================================================

def exemplo_pipeline_completo():
    """Executa o pipeline completo de processamento."""
    processor = CNPJProcessor()
    
    # Processar tudo (dados mais recentes)
    success, folder = processor.run()
    
    if success:
        print(f"✅ Pipeline concluído com sucesso! Dados em: {folder}")
    else:
        print("❌ Falha no pipeline")
    
    return success

# ============================================================================
# EXEMPLO 3: Download Apenas
# ============================================================================

def exemplo_download():
    """Baixar apenas os arquivos sem processar."""
    processor = CNPJProcessor()
    
    # Baixar apenas empresas e estabelecimentos de uma pasta específica
    success, folder = processor.run(
        step='download',
        tipos=['empresas', 'estabelecimentos'],
        remote_folder='2026-01',
        force_download=False  # Não redownload se já existir
    )
    
    return success

# ============================================================================
# EXEMPLO 4: Processamento de Arquivos Já Baixados
# ============================================================================

def exemplo_processar_existentes():
    """Processar arquivos ZIP que já foram baixados."""
    processor = CNPJProcessor()
    
    # Processar ZIPs de uma pasta específica
    success, folder = processor.run(
        step='process',
        source_zip_folder='./dados-abertos-zip/2026-01',
        output_subfolder='processados_2026_01',
        tipos=['empresas', 'estabelecimentos']
    )
    
    return success

# ============================================================================
# EXEMPLO 5: Criar Apenas o Banco de Dados
# ============================================================================

def exemplo_criar_banco():
    """Criar banco DuckDB a partir de parquets já processados."""
    processor = CNPJProcessor()
    
    # Criar banco a partir de parquets existentes
    success, folder = processor.run(
        step='database',
        output_subfolder='processados_2026_01'
    )
    
    return success

# ============================================================================
# EXEMPLO 6: Processamento com Economia de Espaço
# ============================================================================

def exemplo_economia_espaco():
    """Pipeline com máxima economia de espaço em disco."""
    processor = CNPJProcessor()
    
    # Pipeline que remove ZIPs após extração e parquets após criar banco
    success, folder = processor.run(
        step='all',
        delete_zips_after_extract=True,  # Remove ZIPs após extração
        cleanup_all_after_db=True,       # Remove parquets E ZIPs após banco
        quiet=True                       # Modo silencioso
    )
    
    return success

# ============================================================================
# EXEMPLO 7: Processamento do Painel Consolidado
# ============================================================================

def exemplo_painel_basico():
    """Processar painel consolidado sem filtros."""
    processor = CNPJProcessor()
    
    # Processar painel completo
    success, folder = processor.run(
        step='painel',
        remote_folder='2026-01'
    )
    
    return success

def exemplo_painel_filtrado():
    """Processar painel com filtros por UF e situação."""
    processor = CNPJProcessor()
    
    # Painel apenas de empresas ativas (situação=2) de São Paulo
    success, folder = processor.run(
        step='painel',
        remote_folder='2026-01',
        painel_uf='SP',
        painel_situacao=2,  # 1=Nula, 2=Ativa, 3=Suspensa, 4=Inapta, 8=Baixada
        output_subfolder='painel_sp_ativas'
    )
    
    return success

# ============================================================================
# EXEMPLO 8: Pipeline Completo com Painel
# ============================================================================

def exemplo_pipeline_com_painel():
    """Pipeline completo incluindo processamento do painel."""
    processor = CNPJProcessor()
    
    # Processar tudo + painel filtrado por UF
    success, folder = processor.run(
        step='all',
        tipos=['empresas', 'estabelecimentos', 'simples'],
        processar_painel=True,
        painel_uf='GO',
        painel_situacao=2,
        cleanup_after_db=True  # Remove apenas parquets após banco
    )
    
    return success

# ============================================================================
# EXEMPLO 9: Criar Subconjuntos Especializados
# ============================================================================

def exemplo_subset_empresas_privadas():
    """Criar subconjunto apenas de empresas privadas."""
    processor = CNPJProcessor()
    
    success, folder = processor.run(
        step='all',
        tipos=['empresas'],
        criar_empresa_privada=True,
        output_subfolder='empresas_privadas'
    )
    
    return success

def exemplo_subset_uf():
    """Criar subconjunto de estabelecimentos por UF."""
    processor = CNPJProcessor()
    
    # Processar apenas estabelecimentos de Goiás
    success, folder = processor.run(
        step='all',
        tipos=['estabelecimentos'],
        criar_subset_uf='GO',
        output_subfolder='estabelecimentos_go'
    )
    
    return success

# ============================================================================
# EXEMPLO 10: Processamento com Logging Customizado
# ============================================================================

def exemplo_logging_customizado():
    """Processar com nível de log específico."""
    processor = CNPJProcessor()
    
    # Debug detalhado
    success, folder = processor.run(
        step='all',
        tipos=['empresas'],
        log_level='DEBUG',
        quiet=False
    )
    
    return success

# ============================================================================
# EXEMPLO 11: Processar Múltiplos Períodos
# ============================================================================

def exemplo_multiplos_periodos():
    """Processar dados de múltiplos períodos."""
    processor = CNPJProcessor()
    
    pastas = ['2025-12', '2026-01']
    resultados = []
    
    for pasta in pastas:
        print(f"\n🔄 Processando {pasta}...")
        success, folder = processor.run(
            step='all',
            remote_folder=pasta,
            output_subfolder=f'dados_{pasta.replace("-", "_")}',
            tipos=['empresas', 'estabelecimentos']
        )
        resultados.append((pasta, success))
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DO PROCESSAMENTO:")
    for pasta, success in resultados:
        status = "✅ SUCESSO" if success else "❌ FALHA"
        print(f"{pasta}: {status}")
    
    return resultados

# ============================================================================
# EXEMPLO 12: Pipeline Conservador (Mínimo Download)
# ============================================================================

def exemplo_pipeline_conservador():
    """Pipeline que baixa apenas o necessário e economiza espaço."""
    processor = CNPJProcessor()
    
    # Baixar e processar apenas o essencial
    success, folder = processor.run(
        step='all',
        tipos=['empresas', 'estabelecimentos'],  # Apenas o essencial
        force_download=False,                     # Não redownload
        delete_zips_after_extract=True,          # Remove ZIPs
        cleanup_after_db=True,                    # Remove parquets
        quiet=True                                # Menos verboso
    )
    
    return success

# ============================================================================
# EXEMPLO 13: Tratamento de Erros
# ============================================================================

def exemplo_com_tratamento_erros():
    """Exemplo com tratamento de erros adequado."""
    processor = CNPJProcessor()
    
    try:
        success, folder = processor.run(
            step='all',
            tipos=['empresas'],
            remote_folder='2026-01'
        )
        
        if success:
            print(f"✅ Processamento concluído com sucesso!")
            print(f"📁 Dados salvos em: {folder}")
            return True
        else:
            print("⚠️ Processamento concluído com erros")
            print("📝 Verifique os logs para mais detalhes")
            return False
            
    except KeyboardInterrupt:
        print("\n🛑 Processamento interrompido pelo usuário")
        return False
    except Exception as e:
        print(f"❌ Erro durante processamento: {e}")
        return False

# ============================================================================
# MAIN: Executar Exemplos
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("EXEMPLOS DE USO DA API CNPJProcessor")
    print("=" * 60)
    
    # Descomente o exemplo que deseja executar:
    
    # exemplo_pipeline_completo()
    # exemplo_download()
    # exemplo_processar_existentes()
    # exemplo_criar_banco()
    # exemplo_economia_espaco()
    # exemplo_painel_basico()
    # exemplo_painel_filtrado()
    # exemplo_pipeline_com_painel()
    # exemplo_subset_empresas_privadas()
    # exemplo_subset_uf()
    exemplo_consultar_pastas()
    # exemplo_logging_customizado()
    # exemplo_multiplos_periodos()
    # exemplo_pipeline_conservador()
    # exemplo_com_tratamento_erros()
