"""
Modèles de données pour VIGIL
"""

from .common import DataSource, DataQuality, ConfidenceScore
from .competitor import Competitor, CompetitorProfile, CompetitorType
from .financial import FinancialData, FinancialMetrics, FinancialComparison
from .marketing import MarketingData, SEOMetrics, SocialMediaMetrics, ReputationMetrics

__all__ = [
    "DataSource",
    "DataQuality",
    "ConfidenceScore",
    "Competitor",
    "CompetitorProfile",
    "CompetitorType",
    "FinancialData",
    "FinancialMetrics",
    "FinancialComparison",
    "MarketingData",
    "SEOMetrics",
    "SocialMediaMetrics",
    "ReputationMetrics",
]
