"""
Modèles pour l'analyse marketing (Module 3)
"""

from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, HttpUrl

from .common import DataQuality, ConfidenceScore


class PricingTier(BaseModel):
    """Niveau de tarification"""
    name: str = Field(..., description="Nom du plan (ex: Basic, Pro, Enterprise)")
    price: Optional[float] = Field(None, description="Prix mensuel (€)")
    billing_period: str = Field(default="monthly", description="Période de facturation")
    features: List[str] = Field(default_factory=list, description="Fonctionnalités incluses")


class SEOMetrics(BaseModel):
    """
    Métriques SEO/SEM.
    Collectées via APIs (SimilarWeb, SEMrush).
    """
    # Trafic
    monthly_visits: Optional[DataQuality] = Field(None, description="Visites mensuelles")
    traffic_sources: Optional[Dict[str, float]] = Field(None, description="Sources de trafic (%)")
    bounce_rate: Optional[DataQuality] = Field(None, description="Taux de rebond (%)")

    # SEO
    organic_keywords: Optional[DataQuality] = Field(None, description="Nombre de mots-clés organiques")
    domain_authority: Optional[DataQuality] = Field(None, description="Autorité de domaine (0-100)")
    backlinks: Optional[DataQuality] = Field(None, description="Nombre de backlinks")

    # SEM
    paid_keywords: Optional[DataQuality] = Field(None, description="Nombre de mots-clés payants")
    estimated_ad_spend: Optional[DataQuality] = Field(None, description="Budget publicitaire estimé (€/mois)")

    # Top mots-clés
    top_keywords: List[str] = Field(default_factory=list, description="Top 10 mots-clés")

    class Config:
        json_schema_extra = {
            "example": {
                "monthly_visits": {
                    "value": 250000,
                    "quality_type": "Estimation",
                    "freshness_days": 7
                },
                "organic_keywords": {
                    "value": 1500,
                    "quality_type": "Fait",
                    "freshness_days": 7
                },
                "top_keywords": ["crm software", "sales management", "customer tracking"]
            }
        }


class SocialMediaMetrics(BaseModel):
    """
    Métriques des réseaux sociaux.
    Collectées via APIs ou scraping.
    """
    # LinkedIn
    linkedin_followers: Optional[DataQuality] = Field(None, description="Followers LinkedIn")
    linkedin_engagement: Optional[DataQuality] = Field(None, description="Taux d'engagement LinkedIn (%)")

    # Twitter/X
    twitter_followers: Optional[DataQuality] = Field(None, description="Followers Twitter/X")

    # Facebook
    facebook_likes: Optional[DataQuality] = Field(None, description="Likes Facebook")

    # Instagram
    instagram_followers: Optional[DataQuality] = Field(None, description="Followers Instagram")

    # Engagement global
    overall_engagement_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=10.0,
        description="Score d'engagement global (0-10)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "linkedin_followers": {
                    "value": 15000,
                    "quality_type": "Fait",
                    "freshness_days": 1
                },
                "linkedin_engagement": {
                    "value": 3.5,
                    "quality_type": "Estimation",
                    "freshness_days": 7
                },
                "overall_engagement_score": 7.2
            }
        }


class ReputationMetrics(BaseModel):
    """
    Métriques de réputation.
    Collectées via scraping (Trustpilot, G2, Capterra).
    """
    # Trustpilot
    trustpilot_score: Optional[DataQuality] = Field(None, description="Note Trustpilot (/5)")
    trustpilot_reviews: Optional[DataQuality] = Field(None, description="Nombre d'avis Trustpilot")

    # G2
    g2_score: Optional[DataQuality] = Field(None, description="Note G2 (/5)")
    g2_reviews: Optional[DataQuality] = Field(None, description="Nombre d'avis G2")

    # Capterra
    capterra_score: Optional[DataQuality] = Field(None, description="Note Capterra (/5)")
    capterra_reviews: Optional[DataQuality] = Field(None, description="Nombre d'avis Capterra")

    # Synthèse
    average_score: Optional[float] = Field(None, description="Note moyenne globale (/5)")
    total_reviews: Optional[int] = Field(None, description="Total des avis")

    class Config:
        json_schema_extra = {
            "example": {
                "trustpilot_score": {
                    "value": 4.5,
                    "quality_type": "Fait",
                    "freshness_days": 1
                },
                "trustpilot_reviews": {
                    "value": 320,
                    "quality_type": "Fait",
                    "freshness_days": 1
                },
                "average_score": 4.3,
                "total_reviews": 850
            }
        }


class MarketingData(BaseModel):
    """
    Ensemble complet des données marketing d'un concurrent.
    Sortie principale du Module 3.
    """
    competitor_name: str = Field(..., description="Nom du concurrent")

    # Positionnement
    value_proposition: Optional[DataQuality] = Field(None, description="Proposition de valeur")
    target_segments: List[str] = Field(default_factory=list, description="Segments cibles")

    # Tarification
    pricing_available: bool = Field(False, description="Grille tarifaire disponible")
    pricing_tiers: List[PricingTier] = Field(default_factory=list, description="Plans tarifaires")
    pricing_model: Optional[str] = Field(None, description="Modèle de tarification (freemium, subscription, etc.)")

    # Métriques
    seo_metrics: Optional[SEOMetrics] = Field(None, description="Métriques SEO/SEM")
    social_metrics: Optional[SocialMediaMetrics] = Field(None, description="Métriques réseaux sociaux")
    reputation_metrics: Optional[ReputationMetrics] = Field(None, description="Métriques de réputation")

    # Métadonnées
    confidence: ConfidenceScore = Field(..., description="Confiance des données")
    collected_at: datetime = Field(default_factory=datetime.now, description="Date de collecte")

    class Config:
        json_schema_extra = {
            "example": {
                "competitor_name": "TechCorp",
                "value_proposition": {
                    "value": "CRM simple et puissant pour PME",
                    "quality_type": "Fait",
                    "freshness_days": 15
                },
                "pricing_available": True,
                "pricing_tiers": [
                    {
                        "name": "Starter",
                        "price": 29.0,
                        "billing_period": "monthly",
                        "features": ["10 users", "Basic CRM"]
                    }
                ],
                "confidence": {
                    "score": 0.75,
                    "nb_sources": 3,
                    "needs_human_validation": False
                }
            }
        }


class MarketingComparison(BaseModel):
    """
    Comparaison marketing entre le client et un concurrent.
    Sortie du Module 3 (Benchmarking).
    """
    competitor_name: str = Field(..., description="Nom du concurrent")

    # Comparaisons
    traffic_comparison: Optional[str] = Field(None, description="Comparaison trafic web")
    seo_comparison: Optional[str] = Field(None, description="Comparaison SEO")
    social_comparison: Optional[str] = Field(None, description="Comparaison réseaux sociaux")
    reputation_comparison: Optional[str] = Field(None, description="Comparaison réputation")
    pricing_comparison: Optional[str] = Field(None, description="Comparaison tarification")

    # Synthèse
    strengths: List[str] = Field(default_factory=list, description="Forces marketing du concurrent")
    weaknesses: List[str] = Field(default_factory=list, description="Faiblesses marketing du concurrent")

    # Métadonnées
    confidence: ConfidenceScore = Field(..., description="Confiance de l'analyse")
    analyzed_at: datetime = Field(default_factory=datetime.now, description="Date de l'analyse")

    class Config:
        json_schema_extra = {
            "example": {
                "competitor_name": "TechCorp",
                "traffic_comparison": "Trafic web 3x supérieur (750k vs 250k visites/mois)",
                "seo_comparison": "Meilleur référencement organique (3000 vs 1500 mots-clés)",
                "strengths": [
                    "Trafic web très supérieur",
                    "Forte présence LinkedIn",
                    "Excellente réputation (4.5/5)"
                ],
                "weaknesses": [
                    "Prix plus élevés",
                    "Moins de visibilité sur les réseaux sociaux"
                ]
            }
        }
