#!/usr/bin/env python3
"""
Script de Monitoramento e Validação de Compliance - CNPJ Data Processor

Este script demonstra praticamente como implementar:
1. Monitoramento do processo de atualização
2. Verificação e validação de dados
3. Automação do pipeline
4. Geração de relatórios de compliance

Usage:
    python compliance_monitor.py --mode full-validation
    python compliance_monitor.py --mode quick-check
    python compliance_monitor.py --mode health-check
    python compliance_monitor.py --mode generate-report
"""

import argparse
import asyncio
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from Entity.validation.validator import EntityValidator
from process.base.resource_monitor import ResourceMonitor
from utils.progress_tracker import ProgressTracker
from utils.logging import setup_logging


class ComplianceMonitor:
    """Monitor de compliance para o processador de dados CNPJ"""
    
    def __init__(self):
        self.resource_monitor = ResourceMonitor()
        self.progress_tracker = ProgressTracker()
        self.validators = {}
        self.setup_validators()
        
    def setup_validators(self):
        """Configura validadores para cada tipo de entidade"""
        entity_types = ['empresa', 'estabelecimento', 'socio', 'simples']
        for entity_type in entity_types:
            self.validators[entity_type] = EntityValidator(entity_type)
    
    async def health_check(self) -> Dict[str, Any]:
        """Executa health check completo do sistema"""
        print("🔍 Executando health check do sistema...")
        
        health_data = {
            "timestamp": datetime.now().isoformat(),
            "system_status": "checking",
            "checks": {}
        }
        
        try:
            # Verificar recursos do sistema
            resources = self.resource_monitor.get_system_resources_dict()
            health_data["checks"]["resources"] = {
                "status": "ok" if resources["cpu_percent"] < 90 else "warning",
                "cpu_percent": resources["cpu_percent"],
                "memory_percent": resources["memory_percent"],
                "disk_free_gb": resources["disk_free_gb"]
            }
            
            # Verificar validadores
            health_data["checks"]["validators"] = {
                "status": "ok",
                "count": len(self.validators),
                "types": list(self.validators.keys())
            }
            
            # Verificar estrutura de diretórios
            required_dirs = ["data", "output", "logs"]
            dirs_status = {}
            for dir_name in required_dirs:
                dir_path = Path(dir_name)
                dirs_status[dir_name] = {
                    "exists": dir_path.exists(),
                    "writable": dir_path.exists() and os.access(dir_path, os.W_OK)
                }
            
            health_data["checks"]["directories"] = dirs_status
            
            # Status geral
            all_ok = all(check["status"] == "ok" for check in health_data["checks"].values())
            health_data["system_status"] = "healthy" if all_ok else "degraded"
            
        except Exception as e:
            health_data["system_status"] = "unhealthy"
            health_data["error"] = str(e)
            
        return health_data
    
    async def validate_sample_data(self, sample_size: int = 1000) -> Dict[str, Any]:
        """Valida amostra de dados para verificar consistência"""
        print(f"📊 Validando amostra de {sample_size} registros...")
        
        validation_results = {
            "timestamp": datetime.now().isoformat(),
            "sample_size": sample_size,
            "entity_results": {}
        }
        
        # Criar dados de teste simulados
        test_data = self._generate_test_data(sample_size)
        
        for entity_type, data in test_data.items():
            if entity_type in self.validators:
                validator = self.validators[entity_type]
                
                # Validar dados
                result = validator.validate_dataframe(data)
                validation_results["entity_results"][entity_type] = {
                    "total_rows": result["total_rows"],
                    "valid_rows": result["valid_rows"],
                    "invalid_rows": result["invalid_rows"],
                    "success_rate": result["success_rate"],
                    "most_common_errors": result.get("most_common_errors", [])
                }
        
        return validation_results
    
    def _generate_test_data(self, sample_size: int) -> Dict[str, Any]:
        """Gera dados de teste simulados para validação"""
        import polars as pl
        
        return {
            "empresa": pl.DataFrame({
                "cnpj_basico": [12345678] * sample_size,
                "razao_social": ["EMPRESA TESTE LTDA"] * sample_size,
                "natureza_juridica": [2038] * sample_size,
                "qualificacao_responsavel": [10] * sample_size,
                "capital_social": [100000.0] * sample_size,
                "porte_empresa": [2] * sample_size,
                "ente_federativo_responsavel": ["SP"] * sample_size
            }),
            "estabelecimento": pl.DataFrame({
                "cnpj_basico": [12345678] * sample_size,
                "cnpj_ordem": [0001] * sample_size,
                "cnpj_dv": [01] * sample_size,
                "identificador_matriz_filial": [1] * sample_size,
                "nome_fantasia": ["FILIAL TESTE"] * sample_size,
                "situacao_cadastral": [2] * sample_size,
                "data_situacao_cadastral": ["20240101"] * sample_size,
                "motivo_situacao_cadastral": [0] * sample_size,
                "nome_cidade_exterior": [None] * sample_size,
                "pais": [None] * sample_size,
                "data_inicio_atividade": ["20240101"] * sample_size,
                "cnae_fiscal_principal": ["4711301"] * sample_size,
                "cep": ["01310000"] * sample_size
            }),
            "socio": pl.DataFrame({
                "cnpj_basico": [12345678] * sample_size,
                "identificador_socio": [1] * sample_size,
                "nome_socio": ["SOCIO TESTE"] * sample_size,
                "cpf_cnpj_socio": ["12345678901"] * sample_size,
                "qualificacao_socio": [10] * sample_size,
                "data_entrada_sociedade": ["20240101"] * sample_size,
                "pais": ["BR"] * sample_size,
                "representante_legal": [None] * sample_size,
                "nome_representante": [None] * sample_size,
                "qualificacao_representante": [None] * sample_size,
                "faixa_etaria": [4] * sample_size
            }),
            "simples": pl.DataFrame({
                "cnpj_basico": [12345678] * sample_size,
                "opcao_simples": ["S"] * sample_size,
                "data_opcao_simples": ["20240101"] * sample_size,
                "data_exclusao_simples": [None] * sample_size,
                "opcao_mei": ["N"] * sample_size,
                "data_opcao_mei": [None] * sample_size,
                "data_exclusao_mei": [None] * sample_size
            })
        }
    
    async def generate_compliance_report(self) -> Dict[str, Any]:
        """Gera relatório completo de compliance"""
        print("📋 Gerando relatório de compliance...")
        
        report = {
            "report_id": f"compliance_{int(time.time())}",
            "generated_at": datetime.now().isoformat(),
            "system_info": {
                "python_version": sys.version,
                "platform": sys.platform,
                "working_directory": str(Path.cwd())
            },
            "health_check": await self.health_check(),
            "validation_results": await self.validate_sample_data(),
            "compliance_status": "pending"
        }
        
        # Determinar status geral de compliance
        health_status = report["health_check"]["system_status"]
        validation_rates = [
            result["success_rate"]
            for result in report["validation_results"]["entity_results"].values()
        ]
        
        if health_status == "healthy" and all(rate >= 95 for rate in validation_rates):
            report["compliance_status"] = "compliant"
        elif health_status in ["healthy", "degraded"] and all(rate >= 90 for rate in validation_rates):
            report["compliance_status"] = "conditionally_compliant"
        else:
            report["compliance_status"] = "non_compliant"
        
        return report
    
    def save_report(self, report: Dict[str, Any], filename: str = None):
        """Salva relatório em arquivo JSON"""
        if filename is None:
            filename = f"compliance_report_{report['report_id']}.json"
        
        reports_dir = Path("compliance_reports")
        reports_dir.mkdir(exist_ok=True)
        
        filepath = reports_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Relatório salvo em: {filepath}")
        return filepath


async def main():
    """Função principal do monitor de compliance"""
    parser = argparse.ArgumentParser(description="Monitor de Compliance - CNPJ Data Processor")
    parser.add_argument("--mode", choices=["health-check", "validation", "full", "generate-report"], 
                       default="health-check", help="Modo de operação")
    parser.add_argument("--sample-size", type=int, default=1000, help="Tamanho da amostra para validação")
    parser.add_argument("--output", type=str, help="Arquivo de saída para o relatório")
    
    args = parser.parse_args()
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    monitor = ComplianceMonitor()
    
    print("🚀 Iniciando monitor de compliance...")
    print("=" * 60)
    
    try:
        if args.mode == "health-check":
            result = await monitor.health_check()
            print("\n📊 Health Check Result:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif args.mode == "validation":
            result = await monitor.validate_sample_data(args.sample_size)
            print("\n📋 Validation Results:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif args.mode == "full":
            result = await monitor.generate_compliance_report()
            filepath = monitor.save_report(result, args.output)
            print(f"\n✅ Compliance check completed!")
            print(f"Status: {result['compliance_status']}")
            print(f"Report saved: {filepath}")
            
        elif args.mode == "generate-report":
            # Modo para gerar relatório sem execução
            dummy_report = {
                "report_id": "template_compliance",
                "generated_at": datetime.now().isoformat(),
                "template": True,
                "description": "Template para relatórios de compliance",
                "usage": "Execute 'python compliance_monitor.py --mode full' para relatório real"
            }
            filepath = monitor.save_report(dummy_report, args.output or "compliance_template.json")
            print(f"📋 Template report generated: {filepath}")
            
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)