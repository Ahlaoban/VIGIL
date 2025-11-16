"""
Test Rapide VIGIL - 1 entreprise

Script minimal pour tester rapidement l'installation.
"""

import asyncio
import json
from dotenv import load_dotenv
from loguru import logger

from src.models.competitor import ClientProfile, CompanySize
from src.models.common import GeoLocation
from src.orchestrator import VigilOrchestrator


async def quick_test():
    """Test rapide avec une seule entreprise"""

    print("\n" + "="*60)
    print("🚀 VIGIL - Test Rapide")
    print("="*60)

    # Charger config
    load_dotenv()

    # Entreprise de test
    client = ClientProfile(
        company_name="TechTest SAS",
        naf_code="6201Z",
        industry_sector="Software Development",
        company_size=CompanySize.SME,
        headquarters=GeoLocation(country="France", city="Paris"),
        target_markets=["France"],
        products_services=["Logiciel SaaS"],
        value_proposition="Solution SaaS pour PME",
        target_segments=["PME"],
        annual_revenue=1_500_000,
        employees_count=25
    )

    print(f"\nEntreprise testée: {client.company_name}")
    print(f"Secteur: {client.industry_sector}")
    print(f"Taille: {client.company_size.value}")
    print("\n⏳ Lancement de l'analyse (cela peut prendre 1-2 min)...\n")

    try:
        orchestrator = VigilOrchestrator()
        report = await orchestrator.run_full_analysis(
            client_profile=client,
            client_revenue=1_500_000,
            client_employees=25,
            max_competitors=3  # Limité à 3 pour test rapide
        )

        # Affichage résultats
        print("\n" + "="*60)
        print("✅ ANALYSE TERMINÉE")
        print("="*60)
        print(f"\n📊 Résumé:")
        print(f"   - Concurrents identifiés: {report['summary']['total_competitors_identified']}")
        print(f"   - Direct: {report['summary']['breakdown']['direct']}")
        print(f"   - Indirect: {report['summary']['breakdown']['indirect']}")
        print(f"   - Émergent: {report['summary']['breakdown']['emerging']}")
        print(f"   - Temps d'exécution: {report['metadata']['execution_time_seconds']:.1f}s")

        if report['competitors']:
            print(f"\n🎯 Top concurrents:")
            for i, comp in enumerate(report['competitors'], 1):
                print(f"\n   {i}. {comp['name']}")
                print(f"      Type: {comp['type']}")
                print(f"      Score similarité: {comp['similarity_score']:.2f}")
                print(f"      Score confiance: {comp['confidence_score']:.2f}")
                print(f"      Site: {comp['profile']['website'] or 'N/A'}")

        # Sauvegarder
        with open("quick_test_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

        print(f"\n💾 Rapport sauvegardé: quick_test_report.json")
        print("\n✨ Test réussi !")

    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        print("\n💡 Vérifiez:")
        print("   1. Les clés API dans .env")
        print("   2. La connexion internet")
        print("   3. Les logs dans vigil.log")
        logger.error(f"Quick test error: {e}", exc_info=True)

    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(quick_test())
