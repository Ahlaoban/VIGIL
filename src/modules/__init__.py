"""
Modules fonctionnels de VIGIL
"""

from .module1_identification import CompetitorIdentificationModule
from .module6_zero_hallucination import ZeroHallucinationValidator

__all__ = [
    "CompetitorIdentificationModule",
    "ZeroHallucinationValidator",
]
