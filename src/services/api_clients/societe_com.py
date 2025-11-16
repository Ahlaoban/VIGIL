"""
Client pour l'API Pappers (anciennement Société.com)
Documentation: https://www.pappers.fr/api/documentation
"""

from typing import Optional, Dict, Any, List
from loguru import logger

from .base_client import BaseAPIClient
from ...config import settings


class SocieteComClient(BaseAPIClient):
    """
    Client pour l'API Pappers.
    Utilisé pour récupérer les informations légales et financières des entreprises françaises.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            base_url="https://api.pappers.fr/v2",
            api_key=api_key or settings.PAPPERS_API_KEY
        )

    async def search_companies(
        self,
        query: str,
        departement: Optional[str] = None,
        code_naf: Optional[str] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Recherche d'entreprises françaises.

        Args:
            query: Nom ou SIRET de l'entreprise
            departement: Code département (ex: "75" pour Paris)
            code_naf: Code NAF pour filtrer par secteur

        Returns:
            Liste d'entreprises trouvées
        """
        params = {
            "api_token": self.api_key,
            "q": query,
            "par_page": kwargs.get("limit", 20)
        }

        if departement:
            params["departement"] = departement
        if code_naf:
            params["code_naf"] = code_naf

        response = await self.get("/recherche", params=params)

        if not response:
            logger.warning(f"No results from Pappers for query: {query}")
            return []

        resultats = response.get("resultats", [])
        logger.info(f"Found {len(resultats)} companies on Pappers for '{query}'")

        return resultats

    async def get_company_details(self, siren: str) -> Optional[Dict[str, Any]]:
        """
        Récupère les détails complets d'une entreprise par son SIREN.

        Args:
            siren: Numéro SIREN (9 chiffres)

        Returns:
            Détails de l'entreprise ou None
        """
        params = {"api_token": self.api_key}
        response = await self.get(f"/entreprise", params={**params, "siren": siren})

        if not response:
            logger.warning(f"No details found for SIREN: {siren}")
            return None

        return response

    async def get_financials(self, siren: str) -> Optional[Dict[str, Any]]:
        """
        Récupère les données financières d'une entreprise.

        Args:
            siren: Numéro SIREN

        Returns:
            Données financières ou None
        """
        company = await self.get_company_details(siren)

        if not company:
            return None

        # Les données financières sont dans les bilans
        bilans = company.get("finances", {}).get("bilans", [])

        if not bilans:
            logger.warning(f"No financial data for SIREN: {siren}")
            return None

        # Retourne le bilan le plus récent
        return bilans[0] if bilans else None

    async def search_by_naf(
        self,
        code_naf: str,
        departement: Optional[str] = None,
        min_effectif: Optional[int] = None,
        max_effectif: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Recherche d'entreprises par code NAF.

        Args:
            code_naf: Code NAF (ex: "6201Z")
            departement: Code département
            min_effectif: Effectif minimum
            max_effectif: Effectif maximum

        Returns:
            Liste d'entreprises
        """
        params = {
            "api_token": self.api_key,
            "code_naf": code_naf,
            "par_page": 50
        }

        if departement:
            params["departement"] = departement
        if min_effectif:
            params["effectif_min"] = min_effectif
        if max_effectif:
            params["effectif_max"] = max_effectif

        response = await self.get("/recherche", params=params)

        if not response:
            return []

        return response.get("resultats", [])

    async def get_company_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Récupère une entreprise par son nom (recherche exacte).

        Args:
            name: Nom de l'entreprise

        Returns:
            Détails de l'entreprise ou None
        """
        results = await self.search_companies(query=name, limit=1)

        if not results:
            return None

        # Prendre le premier résultat et récupérer les détails complets
        first_result = results[0]
        siren = first_result.get("siren")

        if not siren:
            return first_result

        return await self.get_company_details(siren)
