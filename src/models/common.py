"""
Modèles communs et utilitaires pour la garantie "Zéro Hallucination"
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl


class DataQualityType(str, Enum):
    """Type de qualité de la donnée"""
    FACT = "Fait"  # Source primaire vérifiée
    ESTIMATE = "Estimation"  # Calculée à partir de faits
    HYPOTHESIS = "Hypothèse"  # Inférée ou supposée
    UNAVAILABLE = "Non disponible"  # Donnée introuvable


class DataSource(BaseModel):
    """
    Représente une source de données pour garantir la traçabilité.
    Implémentation du Module 6 : Garantie "Zéro Hallucination"
    """
    name: str = Field(..., description="Nom de la source (ex: Crunchbase, Societe.com)")
    url: Optional[HttpUrl] = Field(None, description="URL de la source si disponible")
    collected_at: datetime = Field(default_factory=datetime.now, description="Date de collecte")
    quality_type: DataQualityType = Field(..., description="Type de qualité de la donnée")
    reliability_score: float = Field(..., ge=0.0, le=1.0, description="Score de fiabilité (0-1)")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Crunchbase",
                "url": "https://www.crunchbase.com/organization/example",
                "collected_at": "2025-11-16T10:30:00",
                "quality_type": "Fait",
                "reliability_score": 0.95
            }
        }


class ConfidenceScore(BaseModel):
    """
    Score de confiance global pour une analyse ou un concurrent.
    Implémentation du seuil de 70% du Module 6.
    """
    score: float = Field(..., ge=0.0, le=1.0, description="Score de confiance global (0-1)")
    nb_sources: int = Field(..., ge=0, description="Nombre de sources utilisées")
    sources: List[DataSource] = Field(default_factory=list, description="Liste des sources")
    needs_human_validation: bool = Field(False, description="True si score < 0.70")

    def __init__(self, **data):
        super().__init__(**data)
        # Auto-calcul de la nécessité de validation humaine
        self.needs_human_validation = self.score < 0.70

    class Config:
        json_schema_extra = {
            "example": {
                "score": 0.85,
                "nb_sources": 3,
                "sources": [],
                "needs_human_validation": False
            }
        }


class DataQuality(BaseModel):
    """
    Encapsule une donnée avec ses métadonnées de qualité.
    Permet de respecter la règle "Il vaut mieux dire 'Je ne sais pas' que d'inventer"
    """
    value: Optional[str | int | float] = Field(None, description="Valeur de la donnée")
    quality_type: DataQualityType = Field(..., description="Type de qualité")
    source: Optional[DataSource] = Field(None, description="Source de la donnée")
    freshness_days: Optional[int] = Field(None, description="Âge de la donnée en jours")

    def is_available(self) -> bool:
        """Vérifie si la donnée est disponible"""
        return self.value is not None and self.quality_type != DataQualityType.UNAVAILABLE

    def get_display_value(self) -> str:
        """Retourne la valeur formatée pour affichage"""
        if not self.is_available():
            return "Non disponible"
        return str(self.value)

    class Config:
        json_schema_extra = {
            "example": {
                "value": 15000000,
                "quality_type": "Fait",
                "source": {
                    "name": "Pappers",
                    "url": "https://www.pappers.fr/...",
                    "collected_at": "2025-11-16T10:30:00",
                    "quality_type": "Fait",
                    "reliability_score": 0.90
                },
                "freshness_days": 30
            }
        }


class GeoLocation(BaseModel):
    """Localisation géographique"""
    country: str = Field(..., description="Pays")
    city: Optional[str] = Field(None, description="Ville")
    region: Optional[str] = Field(None, description="Région")


class TimeRange(BaseModel):
    """Période temporelle"""
    start_date: datetime = Field(..., description="Date de début")
    end_date: datetime = Field(..., description="Date de fin")

    def duration_days(self) -> int:
        """Calcule la durée en jours"""
        return (self.end_date - self.start_date).days
