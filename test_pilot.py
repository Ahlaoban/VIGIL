"""
Script de test pour 10 entreprises pilotes

Ce script teste VIGIL avec 10 profils d'entreprises réelles
pour valider la Phase 1 (POC).
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv

from src.models.competitor import ClientProfile, CompanySize
from src.models.common import GeoLocation
from src.orchestrator import VigilOrchestrator


# Configuration du logging
logger.add(
    "vigil_pilot_test.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
)


# 10 Profils d'entreprises pilotes (exemples réalistes)
PILOT_COMPANIES = [
    {
        "company_name": "TechSolutions SAS",
        "naf_code": "6201Z",
        "industry_sector": "Software Development",
        "company_size": CompanySize.SME,
        "headquarters": {"country": "France", "city": "Lyon"},
        "target_markets": ["France", "Belgique", "Suisse"],
        "products_services": ["Plateforme SaaS de gestion de projet", "Application mobile"],
        "value_proposition": "Solution de gestion de projet simple pour PME",
        "target_segments": ["PME B2B", "Startups"],
        "annual_revenue": 2_500_000,
        "employees_count": 45
    },
    {
        "company_name": "DataCorp",
        "naf_code": "6202A",
        "industry_sector": "IT Consulting",
        "company_size": CompanySize.SME,
        "headquarters": {"country": "France", "city": "Paris"},
        "target_markets": ["France", "Europe"],
        "products_services": ["Conseil BI", "Data Analytics"],
        "value_proposition": "Expert en transformation data",
        "target_segments": ["Grandes entreprises", "ETI"],
        "annual_revenue": 5_000_000,
        "employees_count": 80
    },
    {
        "company_name": "CloudFirst",
        "naf_code": "6201Z",
        "industry_sector": "Cloud Computing",
        "company_size": CompanySize.STARTUP,
        "headquarters": {"country": "France", "city": "Toulouse"},
        "target_markets": ["France"],
        "products_services": ["Infrastructure Cloud", "Migration Cloud"],
        "value_proposition": "Cloud accessible pour PME",
        "target_segments": ["PME", "Startups"],
        "annual_revenue": 800_000,
        "employees_count": 15
    },
    {
        "company_name": "SecureIT Pro",
        "naf_code": "6202A",
        "industry_sector": "Cybersecurity",
        "company_size": CompanySize.SME,
        "headquarters": {"country": "France", "city": "Nantes"},
        "target_markets": ["France", "Belgique"],
        "products_services": ["Audit sécurité", "SOC managé"],
        "value_proposition": "Cybersécurité pour PME",
        "target_segments": ["PME", "ETI"],
        "annual_revenue": 3_200_000,
        "employees_count": 55
    },
    {
        "company_name": "MarketBoost",
        "naf_code": "7311Z",
        "industry_sector": "Digital Marketing",
        "company_size": CompanySize.SME,
        "headquarters": {"country": "France", "city": "Bordeaux"},
        "target_markets": ["France", "Espagne"],
        "products_services": ["SEO/SEM", "Social Media Management"],
        "value_proposition": "Marketing digital performance",
        "target_segments": ["E-commerce", "Services B2B"],
        "annual_revenue": 1_800_000,
        "employees_count": 35
    },
    {
        "company_name": "FinTech Innov",
        "naf_code": "6201Z",
        "industry_sector": "Financial Technology",
        "company_size": CompanySize.STARTUP,
        "headquarters": {"country": "France", "city": "Paris"},
        "target_markets": ["France"],
        "products_services": ["Plateforme de paiement", "API bancaire"],
        "value_proposition": "Paiements simplifiés pour PME",
        "target_segments": ["E-commerce", "Startups"],
        "annual_revenue": 1_200_000,
        "employees_count": 28
    },
    {
        "company_name": "EduTech Solutions",
        "naf_code": "6201Z",
        "industry_sector": "EdTech",
        "company_size": CompanySize.SME,
        "headquarters": {"country": "France", "city": "Lille"},
        "target_markets": ["France", "Belgique"],
        "products_services": ["LMS", "Formation en ligne"],
        "value_proposition": "Plateforme e-learning corporate",
        "target_segments": ["Grandes entreprises", "Organismes formation"],
        "annual_revenue": 2_900_000,
        "employees_count": 48
    },
    {
        "company_name": "GreenEnergy Tech",
        "naf_code": "7112B",
        "industry_sector": "CleanTech",
        "company_size": CompanySize.SME,
        "headquarters": {"country": "France", "city": "Grenoble"},
        "target_markets": ["France", "Suisse"],
        "products_services": ["Monitoring énergie", "IoT solaire"],
        "value_proposition": "Optimisation énergétique intelligente",
        "target_segments": ["Industrie", "Tertiaire"],
        "annual_revenue": 4_100_000,
        "employees_count": 62
    },
    {
        "company_name": "HealthCare AI",
        "naf_code": "6201Z",
        "industry_sector": "HealthTech",
        "company_size": CompanySize.STARTUP,
        "headquarters": {"country": "France", "city": "Montpellier"},
        "target_markets": ["France"],
        "products_services": ["IA diagnostic", "Télémédecine"],
        "value_proposition": "IA au service de la santé",
        "target_segments": ["Hôpitaux", "Cabinets médicaux"],
        "annual_revenue": 950_000,
        "employees_count": 18
    },
    {
        "company_name": "LogiChain Pro",
        "naf_code": "6201Z",
        "industry_sector": "Supply Chain Tech",
        "company_size": CompanySize.SME,
        "headquarters": {"country": "France", "city": "Marseille"},
        "target_markets": ["France", "Italie"],
        "products_services": ["TMS", "Optimisation logistique"],
        "value_proposition": "Supply chain intelligente",
        "target_segments": ["Transporteurs", "E-commerce"],
        "annual_revenue": 3_600_000,
        "employees_count": 58
    }
]


async def test_single_company(orchestrator: VigilOrchestrator, company_data: dict, index: int) -> dict:
    """Test VIGIL pour une seule entreprise"""

    print(f"\n{'='*80}")
    print(f"Test {index}/10 : {company_data['company_name']}")
    print(f"{'='*80}")

    # Créer le profil
    client_profile = ClientProfile(
        company_name=company_data["company_name"],
        naf_code=company_data["naf_code"],
        industry_sector=company_data["industry_sector"],
        company_size=company_data["company_size"],
        headquarters=GeoLocation(**company_data["headquarters"]),
        target_markets=company_data["target_markets"],
        products_services=company_data["products_services"],
        value_proposition=company_data["value_proposition"],
        target_segments=company_data["target_segments"],
        annual_revenue=company_data.get("annual_revenue"),
        employees_count=company_data.get("employees_count")
    )

    # Lancer l'analyse
    try:
        report = await orchestrator.run_full_analysis(
            client_profile=client_profile,
            client_revenue=company_data.get("annual_revenue"),
            client_employees=company_data.get("employees_count"),
            max_competitors=5  # Limiter à 5 pour accélérer les tests
        )

        # Afficher résumé
        print(f"\n✅ Analyse terminée pour {company_data['company_name']}")
        print(f"   - Concurrents identifiés: {report['summary']['total_competitors_identified']}")
        print(f"   - Données financières: {report['summary']['data_quality']['financial_data_collected']}")
        print(f"   - Données marketing: {report['summary']['data_quality']['marketing_data_collected']}")
        print(f"   - Temps d'exécution: {report['metadata']['execution_time_seconds']:.1f}s")

        if report['competitors']:
            print(f"\n   Top 3 concurrents:")
            for i, comp in enumerate(report['competitors'][:3], 1):
                print(f"   {i}. {comp['name']} (score: {comp['similarity_score']:.2f})")

        return {
            "company": company_data["company_name"],
            "status": "SUCCESS",
            "report": report
        }

    except Exception as e:
        print(f"\n❌ Erreur pour {company_data['company_name']}: {str(e)}")
        logger.error(f"Error testing {company_data['company_name']}: {e}", exc_info=True)
        return {
            "company": company_data["company_name"],
            "status": "ERROR",
            "error": str(e)
        }


async def run_pilot_tests():
    """Execute les tests sur les 10 entreprises pilotes"""

    print("\n" + "="*80)
    print("VIGIL - TEST PILOTE - 10 ENTREPRISES")
    print("="*80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Nombre d'entreprises: {len(PILOT_COMPANIES)}")
    print("="*80)

    # Charger la config
    load_dotenv()

    orchestrator = VigilOrchestrator()
    results = []

    start_time = datetime.now()

    # Tester chaque entreprise
    for i, company in enumerate(PILOT_COMPANIES, 1):
        result = await test_single_company(orchestrator, company, i)
        results.append(result)

        # Pause entre chaque test pour respecter les rate limits
        if i < len(PILOT_COMPANIES):
            print("\n⏳ Pause de 5s avant le prochain test...")
            await asyncio.sleep(5)

    # Statistiques globales
    total_time = (datetime.now() - start_time).total_seconds()
    success_count = len([r for r in results if r["status"] == "SUCCESS"])
    error_count = len([r for r in results if r["status"] == "ERROR"])

    print("\n" + "="*80)
    print("RÉSULTATS GLOBAUX")
    print("="*80)
    print(f"✅ Succès: {success_count}/{len(PILOT_COMPANIES)}")
    print(f"❌ Erreurs: {error_count}/{len(PILOT_COMPANIES)}")
    print(f"⏱️  Temps total: {total_time:.1f}s")
    print(f"📊 Temps moyen/entreprise: {total_time/len(PILOT_COMPANIES):.1f}s")

    # Sauvegarder les résultats
    output_dir = Path("pilot_test_results")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Sauvegarder chaque rapport
    for result in results:
        if result["status"] == "SUCCESS":
            filename = f"{result['company'].replace(' ', '_')}_{timestamp}.json"
            filepath = output_dir / filename
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(result["report"], f, indent=2, ensure_ascii=False, default=str)
            print(f"📄 Rapport sauvegardé: {filepath}")

    # Sauvegarder le résumé
    summary_file = output_dir / f"summary_{timestamp}.json"
    summary = {
        "test_date": datetime.now().isoformat(),
        "total_companies": len(PILOT_COMPANIES),
        "success_count": success_count,
        "error_count": error_count,
        "total_time_seconds": total_time,
        "average_time_seconds": total_time / len(PILOT_COMPANIES),
        "results": [
            {
                "company": r["company"],
                "status": r["status"],
                "competitors_found": r["report"]["summary"]["total_competitors_identified"] if r["status"] == "SUCCESS" else 0,
                "error": r.get("error")
            }
            for r in results
        ]
    }

    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\n📊 Résumé global sauvegardé: {summary_file}")
    print("\n" + "="*80)
    print("✨ Test pilote terminé !")
    print("="*80)

    return summary


if __name__ == "__main__":
    # Exécuter les tests
    asyncio.run(run_pilot_tests())
