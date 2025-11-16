"""
Module 2 : Analyse Financière Comparative (Version POC)

Ce module collecte et compare les données financières des concurrents.
Version POC : 2-3 métriques clés (CA, croissance, effectifs).
"""

import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime
from loguru import logger

from ..models.competitor import Competitor
from ..models.financial import (
    FinancialData,
    FinancialMetrics,
    FinancialComparison,
    MetricComparison,
    ComparisonResult,
    FundingRound
)
from ..models.common import DataQuality, DataQualityType
from ..services.api_clients.societe_com import SocieteComClient
from ..modules.module6_zero_hallucination import ZeroHallucinationValidator


class FinancialAnalysisModule:
    """
    Module 2 : Analyse Financière Comparative

    Processus (Version POC) :
    1. Identifier le type de société (cotée/non cotée/startup)
    2. Collecter CA, croissance, effectifs
    3. Benchmarking avec le client
    4. Identification forces/faiblesses
    """

    def __init__(self):
        self.societe_client: Optional[SocieteComClient] = None
        self.validator = ZeroHallucinationValidator()

    async def analyze_competitors_financials(
        self,
        competitors: List[Competitor],
        client_revenue: Optional[float] = None,
        client_employees: Optional[int] = None
    ) -> List[FinancialData]:
        """
        Analyse les données financières de tous les concurrents.

        Args:
            competitors: Liste des concurrents à analyser
            client_revenue: CA du client (pour comparaison)
            client_employees: Effectifs du client (pour comparaison)

        Returns:
            Liste des données financières collectées
        """
        logger.info(f"Analyzing financials for {len(competitors)} competitors")

        async with SocieteComClient() as societe:
            self.societe_client = societe

            # Analyse en parallèle
            tasks = [
                self._analyze_competitor_financial(comp)
                for comp in competitors
            ]
            results = await asyncio.gather(*tasks)

        # Filtrer les résultats None
        financial_data = [r for r in results if r is not None]

        logger.info(
            f"Successfully collected financial data for "
            f"{len(financial_data)}/{len(competitors)} competitors"
        )

        return financial_data

    async def compare_financials(
        self,
        competitor_financials: FinancialData,
        client_revenue: Optional[float],
        client_employees: Optional[int],
        client_growth: Optional[float] = None
    ) -> FinancialComparison:
        """
        Compare les métriques financières d'un concurrent avec le client.

        Args:
            competitor_financials: Données financières du concurrent
            client_revenue: CA client
            client_employees: Effectifs client
            client_growth: Croissance client (%)

        Returns:
            Comparaison détaillée
        """
        metrics = competitor_financials.metrics

        # Comparaison CA
        comp_revenue = metrics.revenue.value if metrics.revenue.is_available() else None
        revenue_comparison = self._compare_metric(
            "Chiffre d'affaires",
            client_revenue,
            comp_revenue,
            unit="€",
            interpretation_template="CA {} suggère {}"
        )

        # Comparaison croissance
        comp_growth = metrics.revenue_growth.value if metrics.revenue_growth and metrics.revenue_growth.is_available() else None
        growth_comparison = self._compare_metric(
            "Croissance CA",
            client_growth,
            comp_growth,
            unit="%",
            interpretation_template="Croissance {} indique {}"
        ) if client_growth and comp_growth else None

        # Comparaison effectifs
        comp_employees = metrics.employees.value if metrics.employees and metrics.employees.is_available() else None
        size_comparison = self._compare_metric(
            "Effectifs",
            client_employees,
            comp_employees,
            unit="employés",
            interpretation_template="Taille {} suggère {}"
        ) if client_employees and comp_employees else None

        # Identifier forces et faiblesses
        strengths, weaknesses = self._identify_strengths_weaknesses(
            revenue_comparison,
            growth_comparison,
            size_comparison
        )

        return FinancialComparison(
            competitor_name=competitor_financials.competitor_name,
            revenue_comparison=revenue_comparison,
            growth_comparison=growth_comparison,
            size_comparison=size_comparison,
            strengths=strengths,
            weaknesses=weaknesses,
            confidence=competitor_financials.confidence
        )

    async def _analyze_competitor_financial(
        self,
        competitor: Competitor
    ) -> Optional[FinancialData]:
        """Analyse financière d'un concurrent spécifique"""
        try:
            logger.debug(f"Analyzing financials for {competitor.profile.name}")

            # Pour les entreprises françaises, utiliser Pappers
            if competitor.profile.siret:
                return await self._get_financials_from_pappers(competitor)

            # Pour les autres, données limitées (à implémenter avec d'autres APIs)
            logger.warning(
                f"No SIRET for {competitor.profile.name}, "
                "financial analysis limited"
            )
            return None

        except Exception as e:
            logger.error(f"Error analyzing financials for {competitor.profile.name}: {e}")
            return None

    async def _get_financials_from_pappers(
        self,
        competitor: Competitor
    ) -> Optional[FinancialData]:
        """Récupère les données financières depuis Pappers"""
        if not competitor.profile.siret:
            return None

        # Extraire le SIREN du SIRET
        siren = competitor.profile.siret[:9]

        # Récupérer les données
        company_data = await self.societe_client.get_company_details(siren)

        if not company_data:
            logger.warning(f"No financial data for SIREN {siren}")
            return None

        # Extraire les métriques
        finances = company_data.get("finances", {})
        bilans = finances.get("bilans", [])

        if not bilans:
            logger.warning(f"No bilans for SIREN {siren}")
            return None

        # Prendre le bilan le plus récent
        latest_bilan = bilans[0]
        year = latest_bilan.get("annee_cloture")

        # Créer les DataQuality pour chaque métrique
        revenue = self.validator.create_data_quality(
            value=latest_bilan.get("chiffre_affaires"),
            source_name="Pappers",
            source_url=f"https://www.pappers.fr/entreprise/{siren}",
            quality_type=DataQualityType.FACT,
            reliability_score=0.90
        )

        # Calculer la croissance si possible
        revenue_growth = None
        if len(bilans) >= 2:
            prev_revenue = bilans[1].get("chiffre_affaires")
            curr_revenue = latest_bilan.get("chiffre_affaires")

            if prev_revenue and curr_revenue and prev_revenue > 0:
                growth_pct = ((curr_revenue - prev_revenue) / prev_revenue) * 100
                revenue_growth = self.validator.create_data_quality(
                    value=round(growth_pct, 2),
                    source_name="Pappers (calculé)",
                    source_url=f"https://www.pappers.fr/entreprise/{siren}",
                    quality_type=DataQualityType.ESTIMATE,
                    reliability_score=0.85
                )

        # Effectifs
        employees_data = self.validator.create_data_quality(
            value=company_data.get("effectif"),
            source_name="Pappers",
            source_url=f"https://www.pappers.fr/entreprise/{siren}",
            quality_type=DataQualityType.FACT,
            reliability_score=0.88
        )

        # Résultat net
        net_income = self.validator.create_data_quality(
            value=latest_bilan.get("resultat_net"),
            source_name="Pappers",
            source_url=f"https://www.pappers.fr/entreprise/{siren}",
            quality_type=DataQualityType.FACT,
            reliability_score=0.90
        )

        # Créer les métriques
        metrics = FinancialMetrics(
            revenue=revenue,
            revenue_growth=revenue_growth,
            net_income=net_income,
            employees=employees_data,
            fiscal_year=year or datetime.now().year
        )

        # Score de confiance
        sources = [s for s in [revenue.source, employees_data.source] if s]
        confidence = self.validator.aggregate_confidence_scores(sources, 3)

        return FinancialData(
            competitor_name=competitor.profile.name,
            company_type=competitor.profile.company_type.value if competitor.profile.company_type else "Inconnu",
            metrics=metrics,
            confidence=confidence
        )

    def _compare_metric(
        self,
        metric_name: str,
        client_value: Optional[float],
        competitor_value: Optional[float],
        unit: str = "",
        interpretation_template: str = "{} {}"
    ) -> MetricComparison:
        """Compare une métrique spécifique"""
        # Déterminer le résultat de comparaison
        comparison_result = MetricComparison.compare_values(client_value, competitor_value)

        # Calculer la différence en %
        percentage_diff = None
        if client_value and competitor_value and client_value != 0:
            percentage_diff = ((competitor_value - client_value) / client_value) * 100

        # Générer l'interprétation
        interpretation = self._generate_interpretation(
            metric_name,
            comparison_result,
            percentage_diff,
            unit
        )

        return MetricComparison(
            metric_name=metric_name,
            client_value=client_value,
            competitor_value=competitor_value,
            comparison_result=comparison_result,
            percentage_diff=percentage_diff,
            interpretation=interpretation
        )

    def _generate_interpretation(
        self,
        metric_name: str,
        result: ComparisonResult,
        diff_pct: Optional[float],
        unit: str
    ) -> str:
        """Génère une interprétation textuelle de la comparaison"""
        if result == ComparisonResult.UNAVAILABLE:
            return f"{metric_name} non comparable (données manquantes)"

        interpretations = {
            ComparisonResult.MUCH_HIGHER: (
                f"{metric_name} très supérieur{f' (+{diff_pct:.0f}%)' if diff_pct else ''}, "
                "suggère position de marché dominante"
            ),
            ComparisonResult.HIGHER: (
                f"{metric_name} supérieur{f' (+{diff_pct:.0f}%)' if diff_pct else ''}, "
                "indique meilleure traction"
            ),
            ComparisonResult.SIMILAR: (
                f"{metric_name} similaire, positionnement équivalent"
            ),
            ComparisonResult.LOWER: (
                f"{metric_name} inférieur{f' ({diff_pct:.0f}%)' if diff_pct else ''}, "
                "opportunité de rattrapage"
            ),
            ComparisonResult.MUCH_LOWER: (
                f"{metric_name} très inférieur{f' ({diff_pct:.0f}%)' if diff_pct else ''}, "
                "écart significatif à combler"
            ),
        }

        return interpretations.get(result, "Comparaison non disponible")

    def _identify_strengths_weaknesses(
        self,
        revenue_comp: MetricComparison,
        growth_comp: Optional[MetricComparison],
        size_comp: Optional[MetricComparison]
    ) -> tuple[List[str], List[str]]:
        """Identifie les forces et faiblesses du concurrent"""
        strengths = []
        weaknesses = []

        # Analyser chaque métrique
        for comp, metric_name in [
            (revenue_comp, "CA"),
            (growth_comp, "Croissance"),
            (size_comp, "Taille")
        ]:
            if not comp:
                continue

            if comp.comparison_result in [ComparisonResult.MUCH_HIGHER, ComparisonResult.HIGHER]:
                strengths.append(f"{metric_name} {comp.comparison_result.value.lower()}")
            elif comp.comparison_result in [ComparisonResult.LOWER, ComparisonResult.MUCH_LOWER]:
                weaknesses.append(f"{metric_name} {comp.comparison_result.value.lower()}")

        return strengths, weaknesses
