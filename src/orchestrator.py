"""
Orchestrateur principal de VIGIL

Coordonne l'exécution de tous les modules d'analyse concurrentielle.
"""

import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
from loguru import logger

from .models.competitor import ClientProfile, Competitor
from .models.financial import FinancialData, FinancialComparison
from .models.marketing import MarketingData, MarketingComparison
from .modules.module1_identification import CompetitorIdentificationModule
from .modules.module2_financial import FinancialAnalysisModule
from .modules.module3_marketing import MarketingAnalysisModule
from .modules.module6_zero_hallucination import ZeroHallucinationValidator
from .config import settings


class VigilOrchestrator:
    """
    Orchestrateur principal de VIGIL.

    Workflow :
    1. Module 1 : Identification des concurrents
    2. Modules 2 & 3 en parallèle : Analyses financière et marketing
    3. Génération du rapport final avec recommandations
    """

    def __init__(self):
        self.identification_module = CompetitorIdentificationModule()
        self.financial_module = FinancialAnalysisModule()
        self.marketing_module = MarketingAnalysisModule()
        self.validator = ZeroHallucinationValidator()

    async def run_full_analysis(
        self,
        client_profile: ClientProfile,
        client_revenue: Optional[float] = None,
        client_employees: Optional[int] = None,
        max_competitors: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Exécute l'analyse complète de la concurrence.

        Args:
            client_profile: Profil du client
            client_revenue: CA du client (optionnel)
            client_employees: Effectifs du client (optionnel)
            max_competitors: Nombre max de concurrents (défaut: config)

        Returns:
            Rapport complet d'analyse
        """
        logger.info("=" * 80)
        logger.info(f"Starting VIGIL analysis for {client_profile.company_name}")
        logger.info("=" * 80)

        start_time = datetime.now()

        try:
            # ====================================================================
            # ÉTAPE 1 : Identification des Concurrents
            # ====================================================================
            logger.info("\n[STEP 1/3] Identifying competitors...")
            competitors = await self.identification_module.identify_competitors(
                client_profile=client_profile,
                max_results=max_competitors
            )

            if not competitors:
                logger.warning("No competitors identified. Aborting analysis.")
                return self._generate_empty_report(client_profile, "No competitors found")

            logger.info(f"✓ Identified {len(competitors)} competitors")

            # Filtrer les concurrents nécessitant validation
            needs_validation = [c for c in competitors if c.requires_validation()]
            if needs_validation:
                logger.warning(
                    f"⚠ {len(needs_validation)} competitors require human validation "
                    f"(confidence < {settings.MIN_CONFIDENCE_THRESHOLD})"
                )

            # ====================================================================
            # ÉTAPE 2 : Analyses Financière et Marketing (en parallèle)
            # ====================================================================
            logger.info("\n[STEP 2/3] Running financial and marketing analyses in parallel...")

            financial_task = self.financial_module.analyze_competitors_financials(
                competitors=competitors,
                client_revenue=client_revenue,
                client_employees=client_employees
            )

            marketing_task = self.marketing_module.analyze_competitors_marketing(
                competitors=competitors
            )

            financial_data, marketing_data = await asyncio.gather(
                financial_task,
                marketing_task
            )

            logger.info(f"✓ Financial data collected for {len(financial_data)} competitors")
            logger.info(f"✓ Marketing data collected for {len(marketing_data)} competitors")

            # ====================================================================
            # ÉTAPE 3 : Benchmarking et Comparaisons
            # ====================================================================
            logger.info("\n[STEP 3/3] Generating comparisons and insights...")

            financial_comparisons = []
            for fd in financial_data:
                if client_revenue or client_employees:
                    comp = await self.financial_module.compare_financials(
                        competitor_financials=fd,
                        client_revenue=client_revenue,
                        client_employees=client_employees
                    )
                    financial_comparisons.append(comp)

            marketing_comparisons = []
            for md in marketing_data:
                comp = await self.marketing_module.compare_marketing(
                    competitor_marketing=md
                )
                marketing_comparisons.append(comp)

            # ====================================================================
            # Génération du Rapport Final
            # ====================================================================
            execution_time = (datetime.now() - start_time).total_seconds()

            report = self._generate_report(
                client_profile=client_profile,
                competitors=competitors,
                financial_data=financial_data,
                marketing_data=marketing_data,
                financial_comparisons=financial_comparisons,
                marketing_comparisons=marketing_comparisons,
                execution_time=execution_time
            )

            logger.info("\n" + "=" * 80)
            logger.info(f"✓ VIGIL analysis completed in {execution_time:.2f}s")
            logger.info("=" * 80)

            return report

        except Exception as e:
            logger.error(f"Error during analysis: {e}", exc_info=True)
            return self._generate_error_report(client_profile, str(e))

    def _generate_report(
        self,
        client_profile: ClientProfile,
        competitors: List[Competitor],
        financial_data: List[FinancialData],
        marketing_data: List[MarketingData],
        financial_comparisons: List[FinancialComparison],
        marketing_comparisons: List[MarketingComparison],
        execution_time: float
    ) -> Dict[str, Any]:
        """Génère le rapport final d'analyse"""

        # Calcul des statistiques
        total_competitors = len(competitors)
        direct = len([c for c in competitors if c.competitor_type.value == "Direct"])
        indirect = len([c for c in competitors if c.competitor_type.value == "Indirect"])
        emerging = len([c for c in competitors if c.competitor_type.value == "Émergent"])

        needs_validation = len([c for c in competitors if c.requires_validation()])

        # Top concurrents par score de similarité
        top_competitors = sorted(
            competitors,
            key=lambda c: c.similarity_score.overall_score,
            reverse=True
        )[:5]

        # Insights globaux
        insights = self._generate_insights(
            financial_comparisons,
            marketing_comparisons
        )

        return {
            "metadata": {
                "client": client_profile.company_name,
                "analysis_date": datetime.now().isoformat(),
                "execution_time_seconds": execution_time,
                "vigil_version": settings.APP_VERSION
            },
            "summary": {
                "total_competitors_identified": total_competitors,
                "breakdown": {
                    "direct": direct,
                    "indirect": indirect,
                    "emerging": emerging
                },
                "data_quality": {
                    "competitors_needing_validation": needs_validation,
                    "financial_data_collected": len(financial_data),
                    "marketing_data_collected": len(marketing_data)
                }
            },
            "competitors": [
                {
                    "name": c.profile.name,
                    "type": c.competitor_type.value,
                    "similarity_score": round(c.similarity_score.overall_score, 2),
                    "confidence_score": round(c.confidence.score, 2),
                    "needs_validation": c.requires_validation(),
                    "profile": {
                        "website": str(c.profile.website) if c.profile.website else None,
                        "sector": c.profile.industry_sector,
                        "size": c.profile.company_size.value if c.profile.company_size else None,
                        "location": c.profile.headquarters.country if c.profile.headquarters else None
                    }
                }
                for c in top_competitors
            ],
            "financial_analysis": [
                {
                    "competitor": fc.competitor_name,
                    "strengths": fc.strengths,
                    "weaknesses": fc.weaknesses,
                    "confidence": round(fc.confidence.score, 2)
                }
                for fc in financial_comparisons[:5]
            ],
            "marketing_analysis": [
                {
                    "competitor": mc.competitor_name,
                    "strengths": mc.strengths,
                    "weaknesses": mc.weaknesses,
                    "confidence": round(mc.confidence.score, 2)
                }
                for mc in marketing_comparisons[:5]
            ],
            "insights": insights,
            "recommendations": self._generate_recommendations(insights, needs_validation)
        }

    def _generate_insights(
        self,
        financial_comparisons: List[FinancialComparison],
        marketing_comparisons: List[MarketingComparison]
    ) -> Dict[str, Any]:
        """Génère des insights à partir des comparaisons"""

        insights = {
            "financial": {
                "common_strengths": [],
                "common_weaknesses": [],
                "key_finding": None
            },
            "marketing": {
                "common_strengths": [],
                "common_weaknesses": [],
                "key_finding": None
            }
        }

        # Analyser les forces/faiblesses communes (financières)
        if financial_comparisons:
            all_strengths = []
            all_weaknesses = []
            for fc in financial_comparisons:
                all_strengths.extend(fc.strengths)
                all_weaknesses.extend(fc.weaknesses)

            # Trouver les plus fréquentes
            if all_strengths:
                insights["financial"]["common_strengths"] = list(set(all_strengths))[:3]
            if all_weaknesses:
                insights["financial"]["common_weaknesses"] = list(set(all_weaknesses))[:3]

        # Analyser les forces/faiblesses communes (marketing)
        if marketing_comparisons:
            all_strengths = []
            all_weaknesses = []
            for mc in marketing_comparisons:
                all_strengths.extend(mc.strengths)
                all_weaknesses.extend(mc.weaknesses)

            if all_strengths:
                insights["marketing"]["common_strengths"] = list(set(all_strengths))[:3]
            if all_weaknesses:
                insights["marketing"]["common_weaknesses"] = list(set(all_weaknesses))[:3]

        return insights

    def _generate_recommendations(
        self,
        insights: Dict[str, Any],
        needs_validation_count: int
    ) -> List[str]:
        """Génère des recommandations stratégiques"""

        recommendations = []

        # Recommandations basées sur la qualité des données
        if needs_validation_count > 0:
            recommendations.append(
                f"⚠ Valider manuellement {needs_validation_count} concurrent(s) "
                f"avec un score de confiance < {settings.MIN_CONFIDENCE_THRESHOLD}"
            )

        # Recommandations financières
        fin_strengths = insights.get("financial", {}).get("common_strengths", [])
        if fin_strengths:
            recommendations.append(
                f"💰 Points forts financiers récurrents chez les concurrents : "
                f"{', '.join(fin_strengths[:2])}"
            )

        # Recommandations marketing
        mkt_strengths = insights.get("marketing", {}).get("common_strengths", [])
        if mkt_strengths:
            recommendations.append(
                f"📢 Opportunités marketing identifiées : "
                f"{', '.join(mkt_strengths[:2])}"
            )

        # Recommandation générale
        recommendations.append(
            "🔄 Mettre en place une surveillance continue (Module 4) pour détecter "
            "les mouvements stratégiques des concurrents"
        )

        return recommendations

    def _generate_empty_report(
        self,
        client_profile: ClientProfile,
        reason: str
    ) -> Dict[str, Any]:
        """Génère un rapport vide en cas d'échec"""
        return {
            "metadata": {
                "client": client_profile.company_name,
                "analysis_date": datetime.now().isoformat(),
                "status": "INCOMPLETE",
                "reason": reason
            },
            "summary": {
                "total_competitors_identified": 0
            },
            "competitors": [],
            "recommendations": [
                "⚠ Aucun concurrent identifié. Vérifier les critères de recherche.",
                "💡 Élargir les critères de recherche (secteur adjacent, géographie, etc.)"
            ]
        }

    def _generate_error_report(
        self,
        client_profile: ClientProfile,
        error: str
    ) -> Dict[str, Any]:
        """Génère un rapport d'erreur"""
        return {
            "metadata": {
                "client": client_profile.company_name,
                "analysis_date": datetime.now().isoformat(),
                "status": "ERROR",
                "error": error
            },
            "summary": {
                "total_competitors_identified": 0
            },
            "competitors": [],
            "recommendations": [
                f"❌ Erreur lors de l'analyse : {error}",
                "🔧 Vérifier la configuration et les clés API"
            ]
        }
