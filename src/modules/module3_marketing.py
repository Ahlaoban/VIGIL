"""
Module 3 : Analyse Marketing Comparative (Version POC)

Ce module analyse et compare le positionnement et les stratégies marketing.
Version POC : Focus sur scraping web basique et métriques SEO simplifiées.
"""

import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime
from loguru import logger
import httpx
from bs4 import BeautifulSoup

from ..models.competitor import Competitor
from ..models.marketing import (
    MarketingData,
    MarketingComparison,
    SEOMetrics,
    SocialMediaMetrics,
    ReputationMetrics,
    PricingTier
)
from ..models.common import DataQuality, DataQualityType
from ..modules.module6_zero_hallucination import ZeroHallucinationValidator
from ..config import settings


class MarketingAnalysisModule:
    """
    Module 3 : Analyse Marketing Comparative

    Processus (Version POC) :
    1. Scraping web pour proposition de valeur et tarifs
    2. Métriques SEO basiques (si API disponible)
    3. Présence réseaux sociaux
    4. Benchmarking avec le client
    """

    def __init__(self):
        self.validator = ZeroHallucinationValidator()
        self.client: Optional[httpx.AsyncClient] = None

    async def analyze_competitors_marketing(
        self,
        competitors: List[Competitor]
    ) -> List[MarketingData]:
        """
        Analyse marketing de tous les concurrents.

        Args:
            competitors: Liste des concurrents à analyser

        Returns:
            Liste des données marketing collectées
        """
        logger.info(f"Analyzing marketing for {len(competitors)} competitors")

        async with httpx.AsyncClient(
            timeout=30.0,
            headers={"User-Agent": settings.USER_AGENT},
            follow_redirects=True
        ) as client:
            self.client = client

            # Analyse en parallèle avec limitation
            tasks = [
                self._analyze_competitor_marketing(comp)
                for comp in competitors
            ]
            results = await asyncio.gather(*tasks)

        # Filtrer les résultats None
        marketing_data = [r for r in results if r is not None]

        logger.info(
            f"Successfully collected marketing data for "
            f"{len(marketing_data)}/{len(competitors)} competitors"
        )

        return marketing_data

    async def compare_marketing(
        self,
        competitor_marketing: MarketingData,
        client_data: Optional[Dict[str, Any]] = None
    ) -> MarketingComparison:
        """
        Compare les métriques marketing d'un concurrent avec le client.

        Args:
            competitor_marketing: Données marketing du concurrent
            client_data: Données marketing du client (optionnel pour POC)

        Returns:
            Comparaison détaillée
        """
        strengths = []
        weaknesses = []

        # Analyser la proposition de valeur
        if competitor_marketing.value_proposition and competitor_marketing.value_proposition.is_available():
            strengths.append("Proposition de valeur claire et identifiée")

        # Analyser la tarification
        pricing_comparison = None
        if competitor_marketing.pricing_available:
            pricing_comparison = f"Grille tarifaire publique avec {len(competitor_marketing.pricing_tiers)} plans"
            strengths.append("Transparence tarifaire")
        else:
            weaknesses.append("Tarification non disponible publiquement")

        # Analyser SEO (si disponible)
        seo_comparison = None
        if competitor_marketing.seo_metrics:
            seo = competitor_marketing.seo_metrics
            if seo.monthly_visits and seo.monthly_visits.is_available():
                visits = seo.monthly_visits.value
                seo_comparison = f"Trafic web estimé : {visits:,} visites/mois"
                if visits > 100000:
                    strengths.append("Trafic web très important")

        # Analyser réseaux sociaux
        social_comparison = None
        if competitor_marketing.social_metrics:
            social = competitor_marketing.social_metrics
            if social.linkedin_followers and social.linkedin_followers.is_available():
                followers = social.linkedin_followers.value
                social_comparison = f"Présence LinkedIn : {followers:,} followers"
                if followers > 10000:
                    strengths.append("Forte présence LinkedIn")

        # Analyser réputation
        reputation_comparison = None
        if competitor_marketing.reputation_metrics:
            rep = competitor_marketing.reputation_metrics
            if rep.average_score:
                reputation_comparison = f"Note moyenne : {rep.average_score:.1f}/5"
                if rep.average_score >= 4.0:
                    strengths.append("Excellente réputation client")
                elif rep.average_score < 3.5:
                    weaknesses.append("Réputation client à améliorer")

        return MarketingComparison(
            competitor_name=competitor_marketing.competitor_name,
            traffic_comparison=seo_comparison,
            seo_comparison=seo_comparison,
            social_comparison=social_comparison,
            reputation_comparison=reputation_comparison,
            pricing_comparison=pricing_comparison,
            strengths=strengths,
            weaknesses=weaknesses,
            confidence=competitor_marketing.confidence
        )

    async def _analyze_competitor_marketing(
        self,
        competitor: Competitor
    ) -> Optional[MarketingData]:
        """Analyse marketing d'un concurrent spécifique"""
        try:
            logger.debug(f"Analyzing marketing for {competitor.profile.name}")

            # Scraper le site web si disponible
            value_prop = None
            pricing_available = False
            pricing_tiers = []

            if competitor.profile.website:
                website_data = await self._scrape_website(str(competitor.profile.website))
                if website_data:
                    value_prop = website_data.get("value_proposition")
                    pricing_tiers = website_data.get("pricing_tiers", [])
                    pricing_available = len(pricing_tiers) > 0

            # Métriques sociales basiques
            social_metrics = await self._get_social_metrics(competitor)

            # Score de confiance
            sources = []
            if value_prop and value_prop.source:
                sources.append(value_prop.source)
            if social_metrics:
                # Ajouter les sources des métriques sociales
                pass

            confidence = self.validator.aggregate_confidence_scores(
                sources if sources else [],
                len(sources)
            ) if sources else self.validator.aggregate_confidence_scores([], 0)

            return MarketingData(
                competitor_name=competitor.profile.name,
                value_proposition=value_prop,
                target_segments=competitor.profile.target_segments,
                pricing_available=pricing_available,
                pricing_tiers=pricing_tiers,
                social_metrics=social_metrics,
                confidence=confidence
            )

        except Exception as e:
            logger.error(f"Error analyzing marketing for {competitor.profile.name}: {e}")
            return None

    async def _scrape_website(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape basique du site web pour extraire :
        - Proposition de valeur
        - Tarifs (si page /pricing existe)
        """
        try:
            # Délai anti-scraping
            await asyncio.sleep(settings.SCRAPING_DELAY)

            # Requête homepage
            response = await self.client.get(url)

            if response.status_code != 200:
                logger.warning(f"Failed to scrape {url}: {response.status_code}")
                return None

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extraire la proposition de valeur (heuristique basique)
            # Chercher dans les h1, h2, meta description
            value_prop_text = None

            # Essayer meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                value_prop_text = meta_desc.get('content')[:200]

            # Sinon, prendre le premier h1
            if not value_prop_text:
                h1 = soup.find('h1')
                if h1:
                    value_prop_text = h1.get_text().strip()[:200]

            value_proposition = None
            if value_prop_text:
                value_proposition = self.validator.create_data_quality(
                    value=value_prop_text,
                    source_name="Site web",
                    source_url=url,
                    quality_type=DataQualityType.FACT,
                    reliability_score=0.75
                )

            # Tentative de récupération des tarifs (très basique pour POC)
            pricing_tiers = []
            # Essayer /pricing
            try:
                pricing_url = f"{url.rstrip('/')}/pricing"
                pricing_response = await self.client.get(pricing_url)
                if pricing_response.status_code == 200:
                    # Parsing basique (à améliorer)
                    logger.info(f"Found pricing page for {url}")
                    # Pour le POC, juste noter que ça existe
            except:
                pass

            return {
                "value_proposition": value_proposition,
                "pricing_tiers": pricing_tiers
            }

        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None

    async def _get_social_metrics(
        self,
        competitor: Competitor
    ) -> Optional[SocialMediaMetrics]:
        """
        Récupère les métriques des réseaux sociaux (version POC simplifiée).
        Pour une version complète, utiliser les APIs LinkedIn, Twitter, etc.
        """
        try:
            # Pour le POC, on peut juste vérifier l'existence de la page LinkedIn
            linkedin_followers = None

            if competitor.profile.linkedin_url:
                # Dans une version complète, utiliser l'API LinkedIn
                # Pour le POC, créer une DataQuality "Non disponible"
                linkedin_followers = self.validator.create_data_quality(
                    value=None,
                    source_name="LinkedIn",
                    source_url=str(competitor.profile.linkedin_url),
                    quality_type=DataQualityType.UNAVAILABLE,
                    reliability_score=0.0
                )

            # Si on n'a aucune métrique, retourner None
            if not linkedin_followers or not linkedin_followers.is_available():
                return None

            return SocialMediaMetrics(
                linkedin_followers=linkedin_followers
            )

        except Exception as e:
            logger.error(f"Error getting social metrics: {e}")
            return None
