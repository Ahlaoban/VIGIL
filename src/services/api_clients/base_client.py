"""
Client API de base avec gestion du rate limiting et retry
"""

import asyncio
import time
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
import httpx
from loguru import logger

from ...config import settings


class RateLimiter:
    """Gestionnaire de rate limiting"""

    def __init__(self, max_calls_per_minute: int):
        self.max_calls = max_calls_per_minute
        self.calls = []
        self.lock = asyncio.Lock()

    async def acquire(self):
        """Attend si nécessaire pour respecter le rate limit"""
        async with self.lock:
            now = time.time()
            # Supprimer les appels plus vieux qu'une minute
            self.calls = [call_time for call_time in self.calls if now - call_time < 60]

            if len(self.calls) >= self.max_calls:
                # Attendre jusqu'à ce qu'un slot soit disponible
                sleep_time = 60 - (now - self.calls[0])
                if sleep_time > 0:
                    logger.debug(f"Rate limit atteint, attente de {sleep_time:.2f}s")
                    await asyncio.sleep(sleep_time)
                    self.calls = self.calls[1:]

            self.calls.append(now)


class BaseAPIClient(ABC):
    """
    Client API de base avec fonctionnalités communes :
    - Rate limiting
    - Retry automatique
    - Gestion des erreurs
    - Logging
    """

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        rate_limit_per_minute: Optional[int] = None
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.rate_limiter = RateLimiter(
            rate_limit_per_minute or settings.API_RATE_LIMIT_PER_MINUTE
        )
        self.client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """Context manager entry"""
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers=self._get_default_headers()
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.client:
            await self.client.aclose()

    def _get_default_headers(self) -> Dict[str, str]:
        """Retourne les headers par défaut"""
        headers = {
            "User-Agent": settings.USER_AGENT,
            "Accept": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        max_retries: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Effectue une requête HTTP avec retry et rate limiting
        """
        if not self.client:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        retries = max_retries or settings.MAX_RETRIES

        for attempt in range(retries):
            try:
                # Rate limiting
                await self.rate_limiter.acquire()

                # Requête
                logger.debug(f"API Request: {method} {url} (attempt {attempt + 1}/{retries})")
                response = await self.client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data
                )

                # Vérification du status
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:  # Too Many Requests
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"Rate limited, waiting {wait_time}s before retry")
                    await asyncio.sleep(wait_time)
                    continue
                elif response.status_code >= 500:  # Server errors
                    if attempt < retries - 1:
                        wait_time = 2 ** attempt
                        logger.warning(f"Server error {response.status_code}, retrying in {wait_time}s")
                        await asyncio.sleep(wait_time)
                        continue
                else:
                    logger.error(f"API error {response.status_code}: {response.text}")
                    return None

            except httpx.TimeoutException:
                logger.warning(f"Request timeout (attempt {attempt + 1}/{retries})")
                if attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
            except Exception as e:
                logger.error(f"Request error: {str(e)}")
                if attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue

        logger.error(f"All {retries} attempts failed for {method} {url}")
        return None

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """GET request"""
        return await self._make_request("GET", endpoint, params=params)

    async def post(self, endpoint: str, json_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """POST request"""
        return await self._make_request("POST", endpoint, json_data=json_data)

    @abstractmethod
    async def search_companies(self, query: str, **kwargs) -> list:
        """Recherche d'entreprises - à implémenter par les sous-classes"""
        pass

    @abstractmethod
    async def get_company_details(self, company_id: str) -> Optional[Dict[str, Any]]:
        """Récupère les détails d'une entreprise - à implémenter par les sous-classes"""
        pass
