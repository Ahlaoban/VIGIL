"""
Modèles pour l'analyse financière (Module 2)
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

from .common import DataQuality, ConfidenceScore


class FundingRound(BaseModel):
    """Détails d'une levée de fonds"""
    round_type: str = Field(..., description="Type de levée (Seed, Series A, B, etc.)")
    amount: float = Field(..., description="Montant levé (€)")
    date: datetime = Field(..., description="Date de la levée")
    investors: List[str] = Field(default_factory=list, description="Investisseurs principaux")
    valuation: Optional[float] = Field(None, description="Valorisation post-money (€)")


class FinancialMetrics(BaseModel):
    """
    Métriques financières d'une entreprise.
    Collectées par le Module 2.
    """
    # Revenus
    revenue: DataQuality = Field(..., description="Chiffre d'affaires (€)")
    revenue_growth: Optional[DataQuality] = Field(None, description="Croissance CA (%)")

    # Profitabilité
    ebitda: Optional[DataQuality] = Field(None, description="EBITDA (€)")
    ebitda_margin: Optional[DataQuality] = Field(None, description="Marge EBITDA (%)")
    net_income: Optional[DataQuality] = Field(None, description="Résultat net (€)")

    # Effectifs
    employees: Optional[DataQuality] = Field(None, description="Nombre d'employés")
    employees_growth: Optional[DataQuality] = Field(None, description="Croissance effectifs (%)")

    # Financement (startups)
    total_funding: Optional[DataQuality] = Field(None, description="Total levé (€)")
    last_funding_round: Optional[FundingRound] = Field(None, description="Dernière levée")
    valuation: Optional[DataQuality] = Field(None, description="Valorisation (€)")

    # Période
    fiscal_year: int = Field(..., description="Année fiscale")
    reporting_date: Optional[datetime] = Field(None, description="Date du rapport")

    class Config:
        json_schema_extra = {
            "example": {
                "revenue": {
                    "value": 15000000,
                    "quality_type": "Fait",
                    "freshness_days": 30
                },
                "revenue_growth": {
                    "value": 25.5,
                    "quality_type": "Estimation",
                    "freshness_days": 30
                },
                "employees": {
                    "value": 120,
                    "quality_type": "Fait",
                    "freshness_days": 15
                },
                "fiscal_year": 2024
            }
        }


class ComparisonResult(str, Enum):
    """Résultat de comparaison entre deux métriques"""
    MUCH_HIGHER = "Très supérieur"  # > +20%
    HIGHER = "Supérieur"  # +5% à +20%
    SIMILAR = "Similaire"  # -5% à +5%
    LOWER = "Inférieur"  # -20% à -5%
    MUCH_LOWER = "Très inférieur"  # < -20%
    UNAVAILABLE = "Non comparable"


class MetricComparison(BaseModel):
    """Comparaison d'une métrique spécifique"""
    metric_name: str = Field(..., description="Nom de la métrique")
    client_value: Optional[float] = Field(None, description="Valeur client")
    competitor_value: Optional[float] = Field(None, description="Valeur concurrent")
    comparison_result: ComparisonResult = Field(..., description="Résultat de la comparaison")
    percentage_diff: Optional[float] = Field(None, description="Différence en %")
    interpretation: str = Field(..., description="Interprétation textuelle")

    @staticmethod
    def compare_values(client: Optional[float], competitor: Optional[float]) -> ComparisonResult:
        """Compare deux valeurs et retourne le résultat"""
        if client is None or competitor is None or client == 0:
            return ComparisonResult.UNAVAILABLE

        diff_pct = ((competitor - client) / client) * 100

        if diff_pct > 20:
            return ComparisonResult.MUCH_HIGHER
        elif diff_pct > 5:
            return ComparisonResult.HIGHER
        elif diff_pct >= -5:
            return ComparisonResult.SIMILAR
        elif diff_pct >= -20:
            return ComparisonResult.LOWER
        else:
            return ComparisonResult.MUCH_LOWER


class FinancialComparison(BaseModel):
    """
    Comparaison financière entre le client et un concurrent.
    Sortie du Module 2 (Benchmarking).
    """
    competitor_name: str = Field(..., description="Nom du concurrent")

    # Comparaisons individuelles
    revenue_comparison: MetricComparison = Field(..., description="Comparaison CA")
    growth_comparison: Optional[MetricComparison] = Field(None, description="Comparaison croissance")
    profitability_comparison: Optional[MetricComparison] = Field(None, description="Comparaison rentabilité")
    size_comparison: Optional[MetricComparison] = Field(None, description="Comparaison taille")

    # Synthèse
    strengths: List[str] = Field(default_factory=list, description="Forces du concurrent")
    weaknesses: List[str] = Field(default_factory=list, description="Faiblesses du concurrent")

    # Métadonnées
    confidence: ConfidenceScore = Field(..., description="Confiance de l'analyse")
    analyzed_at: datetime = Field(default_factory=datetime.now, description="Date de l'analyse")

    class Config:
        json_schema_extra = {
            "example": {
                "competitor_name": "TechCorp",
                "revenue_comparison": {
                    "metric_name": "Chiffre d'affaires",
                    "client_value": 10000000,
                    "competitor_value": 15000000,
                    "comparison_result": "Supérieur",
                    "percentage_diff": 50.0,
                    "interpretation": "Le concurrent a un CA 50% supérieur, suggérant une meilleure traction marché"
                },
                "strengths": [
                    "Croissance très supérieure (+50%)",
                    "Effectifs plus importants"
                ],
                "weaknesses": [
                    "Marge EBITDA inférieure"
                ]
            }
        }


class FinancialData(BaseModel):
    """
    Ensemble complet des données financières d'un concurrent.
    Sortie principale du Module 2.
    """
    competitor_name: str = Field(..., description="Nom du concurrent")
    company_type: str = Field(..., description="Type de société")

    # Métriques
    metrics: FinancialMetrics = Field(..., description="Métriques financières")

    # Historique (optionnel pour POC)
    historical_metrics: List[FinancialMetrics] = Field(
        default_factory=list,
        description="Historique des métriques (3-5 ans)"
    )

    # Métadonnées
    confidence: ConfidenceScore = Field(..., description="Confiance des données")
    collected_at: datetime = Field(default_factory=datetime.now, description="Date de collecte")

    class Config:
        json_schema_extra = {
            "example": {
                "competitor_name": "TechCorp",
                "company_type": "Non cotée",
                "metrics": {
                    "revenue": {"value": 15000000, "quality_type": "Fait"},
                    "fiscal_year": 2024
                },
                "confidence": {
                    "score": 0.82,
                    "nb_sources": 2,
                    "needs_human_validation": False
                }
            }
        }
