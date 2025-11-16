"""
Modèles pour les concurrents (Module 1)
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl

from .common import DataQuality, ConfidenceScore, GeoLocation


class CompetitorType(str, Enum):
    """Type de concurrent"""
    DIRECT = "Direct"  # Même secteur, marché, taille
    INDIRECT = "Indirect"  # Secteur adjacent, même problème résolu
    EMERGING = "Émergent"  # Startup récente, croissance rapide


class CompanySize(str, Enum):
    """Taille de l'entreprise"""
    STARTUP = "Startup"  # < 50 employés
    SME = "PME"  # 50-250 employés
    MIDCAP = "ETI"  # 250-5000 employés
    LARGE = "Grande Entreprise"  # > 5000 employés


class CompanyType(str, Enum):
    """Type de société pour le Module 2"""
    LISTED = "Cotée"  # Société cotée en bourse
    PRIVATE = "Non cotée"  # Société privée
    STARTUP = "Startup"  # Startup (levées de fonds)


class CompetitorProfile(BaseModel):
    """
    Profil détaillé d'un concurrent.
    Correspond aux données collectées par le Module 1.
    """
    # Identité
    name: str = Field(..., description="Nom de l'entreprise")
    legal_name: Optional[str] = Field(None, description="Raison sociale complète")
    website: Optional[HttpUrl] = Field(None, description="Site web principal")

    # Classification
    naf_code: Optional[str] = Field(None, description="Code NAF/NACE")
    industry_sector: str = Field(..., description="Secteur d'activité")
    company_size: Optional[CompanySize] = Field(None, description="Taille de l'entreprise")
    company_type: Optional[CompanyType] = Field(None, description="Type de société")

    # Localisation
    headquarters: Optional[GeoLocation] = Field(None, description="Siège social")
    markets: List[str] = Field(default_factory=list, description="Marchés géographiques")

    # Produits et services
    products_services: List[str] = Field(default_factory=list, description="Produits/services principaux")
    value_proposition: Optional[DataQuality] = Field(None, description="Proposition de valeur")
    target_segments: List[str] = Field(default_factory=list, description="Segments cibles")

    # Données de base
    founded_year: Optional[int] = Field(None, description="Année de création")
    employees_count: Optional[DataQuality] = Field(None, description="Nombre d'employés")

    # Identifiants externes
    siret: Optional[str] = Field(None, description="Numéro SIRET (France)")
    crunchbase_id: Optional[str] = Field(None, description="ID Crunchbase")
    linkedin_url: Optional[HttpUrl] = Field(None, description="Page LinkedIn")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "TechCorp",
                "legal_name": "TechCorp SAS",
                "website": "https://www.techcorp.com",
                "naf_code": "6201Z",
                "industry_sector": "Software Development",
                "company_size": "ETI",
                "company_type": "Non cotée",
                "headquarters": {"country": "France", "city": "Paris"},
                "markets": ["France", "Europe"],
                "products_services": ["SaaS Platform", "Mobile App"],
                "founded_year": 2015,
            }
        }


class CompetitorSimilarityScore(BaseModel):
    """
    Score de similarité pour le classement des concurrents.
    Utilisé dans le Module 1 pour scorer et classer les candidats.
    """
    sector_similarity: float = Field(..., ge=0.0, le=1.0, description="Similarité sectorielle")
    size_similarity: float = Field(..., ge=0.0, le=1.0, description="Similarité de taille")
    geo_similarity: float = Field(..., ge=0.0, le=1.0, description="Similarité géographique")
    product_similarity: float = Field(..., ge=0.0, le=1.0, description="Similarité produits")

    overall_score: float = Field(..., ge=0.0, le=1.0, description="Score global de pertinence")

    def calculate_overall(self, weights: Optional[dict] = None) -> float:
        """
        Calcule le score global pondéré.
        Poids par défaut : secteur=0.4, taille=0.2, géo=0.2, produit=0.2
        """
        if weights is None:
            weights = {
                "sector": 0.4,
                "size": 0.2,
                "geo": 0.2,
                "product": 0.2
            }

        self.overall_score = (
            self.sector_similarity * weights.get("sector", 0.4) +
            self.size_similarity * weights.get("size", 0.2) +
            self.geo_similarity * weights.get("geo", 0.2) +
            self.product_similarity * weights.get("product", 0.2)
        )
        return self.overall_score


class Competitor(BaseModel):
    """
    Représentation complète d'un concurrent identifié.
    Sortie principale du Module 1.
    """
    # Profil
    profile: CompetitorProfile = Field(..., description="Profil du concurrent")

    # Classification
    competitor_type: CompetitorType = Field(..., description="Type de concurrent")

    # Scores
    similarity_score: CompetitorSimilarityScore = Field(..., description="Score de similarité")
    confidence: ConfidenceScore = Field(..., description="Score de confiance")

    # Métadonnées
    identified_at: datetime = Field(default_factory=datetime.now, description="Date d'identification")
    last_updated: datetime = Field(default_factory=datetime.now, description="Dernière mise à jour")

    # Validation
    validated_by_human: bool = Field(False, description="Validé par un humain")
    validation_notes: Optional[str] = Field(None, description="Notes de validation")

    def requires_validation(self) -> bool:
        """Détermine si le concurrent nécessite une validation humaine"""
        return self.confidence.needs_human_validation or self.similarity_score.overall_score < 0.60

    class Config:
        json_schema_extra = {
            "example": {
                "profile": {
                    "name": "TechCorp",
                    "website": "https://www.techcorp.com",
                    "industry_sector": "Software Development"
                },
                "competitor_type": "Direct",
                "similarity_score": {
                    "sector_similarity": 0.95,
                    "size_similarity": 0.80,
                    "geo_similarity": 0.90,
                    "product_similarity": 0.85,
                    "overall_score": 0.88
                },
                "confidence": {
                    "score": 0.85,
                    "nb_sources": 3,
                    "sources": [],
                    "needs_human_validation": False
                }
            }
        }


class ClientProfile(BaseModel):
    """
    Profil du client pour l'identification des concurrents.
    Input du Module 1.
    """
    # Identité
    company_name: str = Field(..., description="Nom de l'entreprise cliente")

    # Classification
    naf_code: str = Field(..., description="Code NAF/NACE")
    industry_sector: str = Field(..., description="Secteur d'activité")
    company_size: CompanySize = Field(..., description="Taille de l'entreprise")

    # Localisation
    headquarters: GeoLocation = Field(..., description="Siège social")
    target_markets: List[str] = Field(..., description="Marchés géographiques cibles")

    # Produits et services
    products_services: List[str] = Field(..., description="Produits/services principaux")
    value_proposition: str = Field(..., description="Proposition de valeur")
    target_segments: List[str] = Field(..., description="Segments de clientèle cibles")

    # Contexte additionnel
    annual_revenue: Optional[float] = Field(None, description="Chiffre d'affaires annuel (€)")
    employees_count: Optional[int] = Field(None, description="Nombre d'employés")

    class Config:
        json_schema_extra = {
            "example": {
                "company_name": "Mon Entreprise",
                "naf_code": "6201Z",
                "industry_sector": "Software Development",
                "company_size": "PME",
                "headquarters": {"country": "France", "city": "Lyon"},
                "target_markets": ["France", "Belgique", "Suisse"],
                "products_services": ["SaaS CRM", "Mobile App"],
                "value_proposition": "CRM simple et abordable pour PME",
                "target_segments": ["PME B2B", "Startups"],
                "annual_revenue": 2500000,
                "employees_count": 45
            }
        }
