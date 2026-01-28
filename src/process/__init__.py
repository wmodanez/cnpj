"""
Módulo de processamento de dados do CNPJ.

Este módulo contém implementações para processar os diferentes tipos de 
arquivos do CNPJ (empresas, estabelecimentos, sócios, etc.).

Implementado com suporte à paralelização usando Polars.
"""
from typing import Dict, Any
from src.process.base.factory import ProcessorFactory

__all__ = ['ProcessorFactory', 'setup_processing']

def setup_processing(npartitions: int = 4) -> Dict[str, Any]:
    """
    Configuração comum para processamento de dados.
    Não configura o Dask diretamente, apenas retorna parâmetros comuns.
    
    Args:
        npartitions: Número de partições padrão
        
    Returns:
        Dict com configurações comuns
    """
    return {
        'npartitions': npartitions,
        'compute': False  # Lazy evaluation por padrão
    }