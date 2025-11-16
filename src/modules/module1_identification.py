"""
Module 1 : Identification des Concurrents

Ce module identifie automatiquement 5 à 10 concurrents principaux
(directs, indirects, émergents) en utilisant diverses sources de données.
"""

import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime
from loguru import logger

from ..models.competitor import (
    Competitor,
    CompetitorProfile,
    CompetitorType,
    ClientProfile,
    CompetitorSimilarityScore,
    CompanySize,
    CompanyType
)
from ..models.common import DataSource, DataQualityType, ConfidenceScore, GeoLocation
from ..services.api_clients.crunchbase import CrunchbaseClient
from ..services.api_clients.societe_com import SocieteComClient
from ..config import settings


class CompetitorIdentificationModule:
    """
    Module 1 : Identification des Concurrents

    Processus :
    1. Recherche de concurrents directs (même secteur, marché, taille)
    2. Recherche de concurrents indirects (secteur adjacent)
    3. Recherche de concurrents émergents (startups récentes)
    4. Scoring & Classement
    5. Validation (score confiance < 70% = validation humaine)
    """

    def __init__(self):
        self.crunchbase_client: Optional[CrunchbaseClient] = None
        self.societe_client: Optional[SocieteComClient] = None

    async def identify_competitors(
        self,
        client_profile: ClientProfile,
        max_results: Optional[int] = None
    ) -> List[Competitor]:
        """
        Identifie les concurrents pour un profil client donné.

        Args:
            client_profile: Profil du client
            max_results: Nombre maximum de concurrents à retourner

        Returns:
            Liste de concurrents identifiés et scorés
        """
        max_competitors = max_results or settings.MAX_COMPETITORS_TO_IDENTIFY

        logger.info(f"Starting competitor identification for {client_profile.company_name}")

        # Initialiser les clients API
        async with CrunchbaseClient() as crunchbase, SocieteComClient() as societe:
            self.crunchbase_client = crunchbase
            self.societe_client = societe

            # Recherche parallèle des 3 types de concurrents
            direct_task = self._find_direct_competitors(client_profile)
            indirect_task = self._find_indirect_competitors(client_profile)
            emerging_task = self._find_emerging_competitors(client_profile)

            direct, indirect, emerging = await asyncio.gather(
                direct_task,
                indirect_task,
                emerging_task
            )

        # Combiner et dédupliquer
        all_competitors = direct + indirect + emerging
        all_competitors = self._deduplicate_competitors(all_competitors)

        # Trier par score de pertinence
        all_competitors.sort(
            key=lambda c: c.similarity_score.overall_score,
            reverse=True
        )

        # Limiter au nombre max
        top_competitors = all_competitors[:max_competitors]

        logger.info(
            f"Identified {len(top_competitors)} competitors: "
            f"{len([c for c in top_competitors if c.competitor_type == CompetitorType.DIRECT])} direct, "
            f"{len([c for c in top_competitors if c.competitor_type == CompetitorType.INDIRECT])} indirect, "
            f"{len([c for c in top_competitors if c.competitor_type == CompetitorType.EMERGING])} emerging"
        )

        return top_competitors

    async def _find_direct_competitors(self, client_profile: ClientProfile) -> List[Competitor]:
        """
        Recherche de concurrents directs.
        Critères stricts : même secteur, marché, taille comparable.
        """
        logger.info("Searching for direct competitors...")
        competitors = []

        # Recherche sur Pappers (entreprises françaises)
        if client_profile.headquarters.country.lower() == "france":
            pappers_results = await self.societe_client.search_by_naf(
                code_naf=client_profile.naf_code,
                departement=None,  # Toute la France
                min_effectif=self._get_min_employees(client_profile.company_size),
                max_effectif=self._get_max_employees(client_profile.company_size)
            )

            for result in pappers_results[:15]:  # Limiter à 15 résultats
                competitor = await self._build_competitor_from_pappers(
                    result,
                    client_profile,
                    CompetitorType.DIRECT
                )
                if competitor:
                    competitors.append(competitor)

        # Recherche sur Crunchbase (international)
        crunchbase_results = await self.crunchbase_client.search_companies(
            query=client_profile.industry_sector,
            location=client_profile.headquarters.country,
            categories=[client_profile.industry_sector]
        )

        for result in crunchbase_results[:15]:
            competitor = await self._build_competitor_from_crunchbase(
                result,
                client_profile,
                CompetitorType.DIRECT
            )
            if competitor:
                competitors.append(competitor)

        logger.info(f"Found {len(competitors)} direct competitors")
        return competitors

    async def _find_indirect_competitors(self, client_profile: ClientProfile) -> List[Competitor]:
        """
        Recherche de concurrents indirects.
        Critères plus larges : secteur adjacent, même problème résolu.
        """
        logger.info("Searching for indirect competitors...")
        competitors = []

        # Pour l'instant, recherche basique sur mots-clés des produits/services
        # Dans une version avancée, utiliser du NLP pour identifier les problèmes résolus

        for product in client_profile.products_services[:3]:  # Top 3 produits
            results = await self.crunchbase_client.search_companies(
                query=product,
                limit=10
            )

            for result in results:
                competitor = await self._build_competitor_from_crunchbase(
                    result,
                    client_profile,
                    CompetitorType.INDIRECT
                )
                if competitor:
                    competitors.append(competitor)

        logger.info(f"Found {len(competitors)} indirect competitors")
        return competitors

    async def _find_emerging_competitors(self, client_profile: ClientProfile) -> List[Competitor]:
        """
        Recherche de concurrents émergents.
        Critères : startups récentes, levées de fonds significatives, croissance rapide.
        """
        logger.info("Searching for emerging competitors...")
        competitors = []

        # Recherche de startups récentes dans le secteur
        # Crunchbase est idéal pour ça
        results = await self.crunchbase_client.search_by_category(
            category=client_profile.industry_sector,
            location=client_profile.headquarters.country,
            max_employees=250  # Limiter aux petites structures
        )

        for result in results[:10]:
            # Vérifier si c'est vraiment une startup émergente
            # (fondée récemment, a levé des fonds, etc.)
            competitor = await self._build_competitor_from_crunchbase(
                result,
                client_profile,
                CompetitorType.EMERGING
            )
            if competitor:
                competitors.append(competitor)

        logger.info(f"Found {len(competitors)} emerging competitors")
        return competitors

    async def _build_competitor_from_pappers(
        self,
        data: Dict[str, Any],
        client_profile: ClientProfile,
        competitor_type: CompetitorType
    ) -> Optional[Competitor]:
        """Construit un objet Competitor à partir des données Pappers"""
        try:
            # Extraction des données de base
            name = data.get("nom_entreprise", "")
            siren = data.get("siren", "")

            if not name or not siren:
                return None

            # Créer le profil
            profile = CompetitorProfile(
                name=name,
                legal_name=data.get("denomination", name),
                website=data.get("site_internet"),
                naf_code=data.get("code_naf"),
                industry_sector=data.get("libelle_code_naf", client_profile.industry_sector),
                company_size=self._map_employees_to_size(data.get("effectif")),
                company_type=CompanyType.PRIVATE,
                headquarters=GeoLocation(
                    country="France",
                    city=data.get("ville"),
                    region=data.get("region")
                ),
                siret=data.get("siege", {}).get("siret"),
            )

            # Calculer le score de similarité
            similarity = self._calculate_similarity(profile, client_profile)

            # Créer la source de données
            source = DataSource(
                name="Pappers",
                url=f"https://www.pappers.fr/entreprise/{siren}",
                quality_type=DataQualityType.FACT,
                reliability_score=0.90
            )

            # Score de confiance
            confidence = ConfidenceScore(
                score=0.85,  # Score moyen pour Pappers
                nb_sources=1,
                sources=[source]
            )

            return Competitor(
                profile=profile,
                competitor_type=competitor_type,
                similarity_score=similarity,
                confidence=confidence
            )

        except Exception as e:
            logger.error(f"Error building competitor from Pappers data: {e}")
            return None

    async def _build_competitor_from_crunchbase(
        self,
        data: Dict[str, Any],
        client_profile: ClientProfile,
        competitor_type: CompetitorType
    ) -> Optional[Competitor]:
        """Construit un objet Competitor à partir des données Crunchbase"""
        try:
            properties = data.get("properties", {})
            name = properties.get("name", "")
            cb_id = properties.get("uuid", "")

            if not name:
                return None

            # Créer le profil
            profile = CompetitorProfile(
                name=name,
                legal_name=properties.get("legal_name", name),
                website=properties.get("website_url"),
                industry_sector=", ".join(properties.get("categories", [])),
                company_size=self._map_employees_to_size(properties.get("num_employees_enum")),
                founded_year=properties.get("founded_on", {}).get("year") if properties.get("founded_on") else None,
                crunchbase_id=cb_id,
                headquarters=GeoLocation(
                    country=properties.get("location_identifiers", [{}])[0].get("country_code", "Unknown")
                    if properties.get("location_identifiers") else "Unknown",
                    city=properties.get("location_identifiers", [{}])[0].get("city", None)
                    if properties.get("location_identifiers") else None
                )
            )

            # Calculer le score de similarité
            similarity = self._calculate_similarity(profile, client_profile)

            # Source
            source = DataSource(
                name="Crunchbase",
                url=f"https://www.crunchbase.com/organization/{cb_id}",
                quality_type=DataQualityType.FACT,
                reliability_score=0.95
            )

            # Confiance
            confidence = ConfidenceScore(
                score=0.88,
                nb_sources=1,
                sources=[source]
            )

            return Competitor(
                profile=profile,
                competitor_type=competitor_type,
                similarity_score=similarity,
                confidence=confidence
            )

        except Exception as e:
            logger.error(f"Error building competitor from Crunchbase data: {e}")
            return None

    def _calculate_similarity(
        self,
        competitor_profile: CompetitorProfile,
        client_profile: ClientProfile
    ) -> CompetitorSimilarityScore:
        """
        Calcule le score de similarité entre un concurrent et le client.
        """
        # Similarité sectorielle
        sector_sim = 1.0 if competitor_profile.naf_code == client_profile.naf_code else 0.7

        # Similarité de taille
        size_sim = 1.0 if competitor_profile.company_size == client_profile.company_size else 0.6

        # Similarité géographique
        geo_sim = 1.0 if competitor_profile.headquarters and \
                        competitor_profile.headquarters.country == client_profile.headquarters.country else 0.5

        # Similarité produits (basique pour POC)
        product_sim = 0.7  # Valeur par défaut, nécessiterait du NLP pour être précis

        similarity = CompetitorSimilarityScore(
            sector_similarity=sector_sim,
            size_similarity=size_sim,
            geo_similarity=geo_sim,
            product_similarity=product_sim,
            overall_score=0.0
        )

        similarity.calculate_overall()

        return similarity

    def _deduplicate_competitors(self, competitors: List[Competitor]) -> List[Competitor]:
        """Déduplique les concurrents par nom"""
        seen = set()
        unique = []

        for comp in competitors:
            name_lower = comp.profile.name.lower().strip()
            if name_lower not in seen:
                seen.add(name_lower)
                unique.append(comp)

        return unique

    def _get_min_employees(self, size: CompanySize) -> Optional[int]:
        """Retourne le nombre min d'employés pour une taille"""
        mapping = {
            CompanySize.STARTUP: 0,
            CompanySize.SME: 50,
            CompanySize.MIDCAP: 250,
            CompanySize.LARGE: 5000
        }
        return mapping.get(size)

    def _get_max_employees(self, size: CompanySize) -> Optional[int]:
        """Retourne le nombre max d'employés pour une taille"""
        mapping = {
            CompanySize.STARTUP: 49,
            CompanySize.SME: 249,
            CompanySize.MIDCAP: 4999,
            CompanySize.LARGE: None
        }
        return mapping.get(size)

    def _map_employees_to_size(self, employees: Optional[Any]) -> Optional[CompanySize]:
        """Convertit un nombre d'employés en CompanySize"""
        if employees is None:
            return None

        # Gérer les strings de Crunchbase (ex: "51-100")
        if isinstance(employees, str):
            if "-" in employees:
                min_emp = int(employees.split("-")[0])
                employees = min_emp
            else:
                try:
                    employees = int(employees)
                except:
                    return None

        if isinstance(employees, int):
            if employees < 50:
                return CompanySize.STARTUP
            elif employees < 250:
                return CompanySize.SME
            elif employees < 5000:
                return CompanySize.MIDCAP
            else:
                return CompanySize.LARGE

        return None
