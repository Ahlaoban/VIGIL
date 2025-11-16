"""
Client pour l'API Crunchbase
Documentation: https://data.crunchbase.com/docs
"""

from typing import Optional, Dict, Any, List
from loguru import logger

from .base_client import BaseAPIClient
from ...config import settings


class CrunchbaseClient(BaseAPIClient):
    """
    Client pour l'API Crunchbase.
    Utilisé pour identifier les concurrents, startups, levées de fonds.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            base_url="https://api.crunchbase.com/api/v4",
            api_key=api_key or settings.CRUNCHBASE_API_KEY
        )

    def _get_default_headers(self) -> Dict[str, str]:
        """Override pour le format d'authentification Crunchbase"""
        headers = super()._get_default_headers()
        if self.api_key:
            # Crunchbase utilise un query parameter pour l'API key
            headers.pop("Authorization", None)
        return headers

    async def search_companies(
        self,
        query: str,
        location: Optional[str] = None,
        categories: Optional[List[str]] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Recherche d'entreprises sur Crunchbase.

        Args:
            query: Terme de recherche
            location: Localisation (ex: "Paris, France")
            categories: Liste de catégories (ex: ["SaaS", "Enterprise Software"])

        Returns:
            Liste d'entreprises trouvées
        """
        params = {
            "user_key": self.api_key,
            "query": query,
        }

        # Filtres optionnels
        if location:
            params["location_uuids"] = location
        if categories:
            params["category_uuids"] = ",".join(categories)

        # Limite de résultats
        params["limit"] = kwargs.get("limit", 20)

        response = await self.get("/searches/organizations", params=params)

        if not response:
            logger.warning(f"No results from Crunchbase for query: {query}")
            return []

        entities = response.get("entities", [])
        logger.info(f"Found {len(entities)} companies on Crunchbase for '{query}'")

        return entities

    async def get_company_details(self, company_id: str) -> Optional[Dict[str, Any]]:
        """
        Récupère les détails complets d'une entreprise.

        Args:
            company_id: UUID Crunchbase de l'entreprise

        Returns:
            Détails de l'entreprise ou None
        """
        params = {"user_key": self.api_key}
        response = await self.get(f"/entities/organizations/{company_id}", params=params)

        if not response:
            logger.warning(f"No details found for company ID: {company_id}")
            return None

        return response.get("properties", {})

    async def get_funding_rounds(self, company_id: str) -> List[Dict[str, Any]]:
        """
        Récupère les levées de fonds d'une entreprise.

        Args:
            company_id: UUID Crunchbase de l'entreprise

        Returns:
            Liste des levées de fonds
        """
        params = {"user_key": self.api_key}
        response = await self.get(
            f"/entities/organizations/{company_id}/funding_rounds",
            params=params
        )

        if not response:
            return []

        return response.get("entities", [])

    async def search_by_category(
        self,
        category: str,
        location: Optional[str] = None,
        min_employees: Optional[int] = None,
        max_employees: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Recherche d'entreprises par catégorie avec filtres.

        Args:
            category: Catégorie (ex: "SaaS", "Enterprise Software")
            location: Localisation
            min_employees: Nombre minimum d'employés
            max_employees: Nombre maximum d'employés

        Returns:
            Liste d'entreprises
        """
        params = {
            "user_key": self.api_key,
            "category_uuids": category,
            "limit": 50
        }

        if location:
            params["location_uuids"] = location
        if min_employees:
            params["num_employees_min"] = min_employees
        if max_employees:
            params["num_employees_max"] = max_employees

        response = await self.get("/searches/organizations", params=params)

        if not response:
            return []

        return response.get("entities", [])
