"""
Exemple d'utilisation de VIGIL - Expert Concurrence

Ce script montre comment utiliser VIGIL pour analyser la concurrence.
"""

import asyncio
import json
from loguru import logger
from dotenv import load_dotenv

from src.models.competitor import ClientProfile, CompanySize
from src.models.common import GeoLocation
from src.orchestrator import VigilOrchestrator


# Configuration du logging
logger.add(
    "vigil.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)


async def main():
    """
    Exemple d'analyse concurrentielle pour une entreprise fictive.
    """

    # Charger les variables d'environnement
    load_dotenv()

    logger.info("Starting VIGIL - Expert Concurrence (POC)")

    # ========================================================================
    # Définir le profil du client
    # ========================================================================

    client_profile = ClientProfile(
        company_name="TechSolutions SAS",
        naf_code="6201Z",  # Programmation informatique
        industry_sector="Software Development",
        company_size=CompanySize.SME,
        headquarters=GeoLocation(
            country="France",
            city="Lyon",
            region="Auvergne-Rhône-Alpes"
        ),
        target_markets=["France", "Belgique", "Suisse"],
        products_services=[
            "Plateforme SaaS de gestion de projet",
            "Application mobile de collaboration",
            "Outils de productivité en équipe"
        ],
        value_proposition="Solution de gestion de projet simple et abordable pour PME",
        target_segments=["PME B2B", "Startups", "Équipes distribuées"],
        annual_revenue=2_500_000,  # 2.5M€
        employees_count=45
    )

    logger.info(f"Client Profile: {client_profile.company_name}")
    logger.info(f"  Sector: {client_profile.industry_sector} ({client_profile.naf_code})")
    logger.info(f"  Size: {client_profile.company_size.value} - {client_profile.employees_count} employés")
    logger.info(f"  Revenue: {client_profile.annual_revenue:,.0f} €")
    logger.info(f"  Location: {client_profile.headquarters.city}, {client_profile.headquarters.country}")

    # ========================================================================
    # Exécuter l'analyse complète
    # ========================================================================

    orchestrator = VigilOrchestrator()

    try:
        report = await orchestrator.run_full_analysis(
            client_profile=client_profile,
            client_revenue=client_profile.annual_revenue,
            client_employees=client_profile.employees_count,
            max_competitors=10
        )

        # ========================================================================
        # Afficher le rapport
        # ========================================================================

        print("\n" + "=" * 80)
        print("VIGIL - RAPPORT D'ANALYSE CONCURRENTIELLE")
        print("=" * 80)

        print(f"\nClient: {report['metadata']['client']}")
        print(f"Date: {report['metadata']['analysis_date']}")
        print(f"Temps d'exécution: {report['metadata']['execution_time_seconds']:.2f}s")

        print("\n" + "-" * 80)
        print("RÉSUMÉ")
        print("-" * 80)
        summary = report['summary']
        print(f"Total concurrents identifiés: {summary['total_competitors_identified']}")
        print(f"  - Directs: {summary['breakdown']['direct']}")
        print(f"  - Indirects: {summary['breakdown']['indirect']}")
        print(f"  - Émergents: {summary['breakdown']['emerging']}")
        print(f"\nQualité des données:")
        print(f"  - Concurrents nécessitant validation: {summary['data_quality']['competitors_needing_validation']}")
        print(f"  - Données financières collectées: {summary['data_quality']['financial_data_collected']}")
        print(f"  - Données marketing collectées: {summary['data_quality']['marketing_data_collected']}")

        print("\n" + "-" * 80)
        print("TOP CONCURRENTS")
        print("-" * 80)
        for i, comp in enumerate(report['competitors'], 1):
            print(f"\n{i}. {comp['name']}")
            print(f"   Type: {comp['type']}")
            print(f"   Score de similarité: {comp['similarity_score']:.2f}")
            print(f"   Score de confiance: {comp['confidence_score']:.2f}")
            print(f"   Validation requise: {'⚠ OUI' if comp['needs_validation'] else '✓ NON'}")
            if comp['profile']['website']:
                print(f"   Site: {comp['profile']['website']}")
            print(f"   Secteur: {comp['profile']['sector']}")
            print(f"   Taille: {comp['profile']['size']}")

        print("\n" + "-" * 80)
        print("ANALYSE FINANCIÈRE")
        print("-" * 80)
        for fa in report['financial_analysis']:
            print(f"\n• {fa['competitor']} (confiance: {fa['confidence']:.2f})")
            if fa['strengths']:
                print(f"  Forces: {', '.join(fa['strengths'])}")
            if fa['weaknesses']:
                print(f"  Faiblesses: {', '.join(fa['weaknesses'])}")

        print("\n" + "-" * 80)
        print("ANALYSE MARKETING")
        print("-" * 80)
        for ma in report['marketing_analysis']:
            print(f"\n• {ma['competitor']} (confiance: {ma['confidence']:.2f})")
            if ma['strengths']:
                print(f"  Forces: {', '.join(ma['strengths'])}")
            if ma['weaknesses']:
                print(f"  Faiblesses: {', '.join(ma['weaknesses'])}")

        print("\n" + "-" * 80)
        print("RECOMMANDATIONS")
        print("-" * 80)
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"{i}. {rec}")

        print("\n" + "=" * 80)

        # ========================================================================
        # Sauvegarder le rapport en JSON
        # ========================================================================

        output_file = "vigil_report.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

        logger.info(f"Report saved to {output_file}")
        print(f"\n✓ Rapport complet sauvegardé dans {output_file}")

    except Exception as e:
        logger.error(f"Error during analysis: {e}", exc_info=True)
        print(f"\n❌ Erreur lors de l'analyse : {e}")
        print("Vérifiez les logs dans vigil.log pour plus de détails.")


if __name__ == "__main__":
    # Exécuter l'analyse
    asyncio.run(main())
