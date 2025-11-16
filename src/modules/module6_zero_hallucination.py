"""
Module 6 : Garantie "Zéro Hallucination"

Module transversal qui garantit la factualité et la traçabilité de toutes les données.
Règle d'or : "Il vaut mieux dire 'Je ne sais pas' que d'inventer"
"""

from typing import Any, Optional, List, Dict
from datetime import datetime, timedelta
from loguru import logger

from ..models.common import (
    DataSource,
    DataQuality,
    DataQualityType,
    ConfidenceScore
)
from ..config import settings


class ZeroHallucinationValidator:
    """
    Validateur pour garantir "Zéro Hallucination".

    Exigences :
    1. Jamais d'invention : Si donnée introuvable, afficher "Non disponible"
    2. Citation systématique : Chaque donnée avec sa source, date et URL
    3. Qualification : Chaque info étiquetée (Fait/Estimation/Hypothèse)
    4. Indication de fraîcheur : Date de la donnée toujours visible
    5. Validation humaine : Confiance < 70% déclenche recommandation
    """

    @staticmethod
    def create_data_quality(
        value: Any,
        source_name: str,
        source_url: Optional[str] = None,
        quality_type: DataQualityType = DataQualityType.FACT,
        reliability_score: float = 0.80
    ) -> DataQuality:
        """
        Crée un objet DataQuality avec toutes les métadonnées requises.

        Args:
            value: La valeur de la donnée (ou None si non disponible)
            source_name: Nom de la source
            source_url: URL de la source si disponible
            quality_type: Type de qualité (Fait/Estimation/Hypothèse)
            reliability_score: Score de fiabilité de la source (0-1)

        Returns:
            DataQuality avec métadonnées complètes
        """
        # Si pas de valeur, marquer comme "Non disponible"
        if value is None:
            quality_type = DataQualityType.UNAVAILABLE
            logger.debug(f"Data not available from {source_name}")

        # Créer la source
        source = DataSource(
            name=source_name,
            url=source_url,
            collected_at=datetime.now(),
            quality_type=quality_type,
            reliability_score=reliability_score
        )

        # Calculer la fraîcheur
        freshness_days = 0  # Données fraîches (collectées maintenant)

        return DataQuality(
            value=value,
            quality_type=quality_type,
            source=source,
            freshness_days=freshness_days
        )

    @staticmethod
    def aggregate_confidence_scores(
        sources: List[DataSource],
        data_points_count: int
    ) -> ConfidenceScore:
        """
        Agrège plusieurs sources pour calculer un score de confiance global.

        Args:
            sources: Liste des sources de données
            data_points_count: Nombre de points de données collectés

        Returns:
            ConfidenceScore global
        """
        if not sources:
            logger.warning("No sources provided for confidence calculation")
            return ConfidenceScore(
                score=0.0,
                nb_sources=0,
                sources=[],
                needs_human_validation=True
            )

        # Score basé sur :
        # 1. Nombre de sources (plus = mieux)
        # 2. Fiabilité moyenne des sources
        # 3. Complétude des données

        nb_sources = len(sources)
        avg_reliability = sum(s.reliability_score for s in sources) / nb_sources

        # Pénalité si peu de sources
        source_penalty = min(nb_sources / settings.MIN_DATA_SOURCES, 1.0)

        # Score final
        confidence_score = avg_reliability * source_penalty * 0.95  # Max 0.95 pour rester prudent

        logger.info(
            f"Confidence score: {confidence_score:.2f} "
            f"({nb_sources} sources, avg reliability: {avg_reliability:.2f})"
        )

        return ConfidenceScore(
            score=confidence_score,
            nb_sources=nb_sources,
            sources=sources,
            needs_human_validation=(confidence_score < settings.MIN_CONFIDENCE_THRESHOLD)
        )

    @staticmethod
    def validate_data_freshness(
        data_quality: DataQuality,
        max_age_days: int = 90
    ) -> bool:
        """
        Vérifie si une donnée est suffisamment fraîche.

        Args:
            data_quality: Donnée à valider
            max_age_days: Âge maximum acceptable en jours

        Returns:
            True si la donnée est fraîche, False sinon
        """
        if data_quality.freshness_days is None:
            logger.warning("No freshness information available")
            return False

        is_fresh = data_quality.freshness_days <= max_age_days

        if not is_fresh:
            logger.warning(
                f"Data is {data_quality.freshness_days} days old "
                f"(max: {max_age_days} days)"
            )

        return is_fresh

    @staticmethod
    def cross_validate_data(
        data_points: List[DataQuality],
        tolerance: float = 0.10
    ) -> Optional[DataQuality]:
        """
        Croise plusieurs sources pour valider une donnée.

        Args:
            data_points: Liste de données provenant de sources différentes
            tolerance: Tolérance de variation (10% par défaut)

        Returns:
            DataQuality validée ou None si incohérence
        """
        if not data_points:
            return None

        # Filtrer les données disponibles
        available = [dp for dp in data_points if dp.is_available()]

        if not available:
            logger.warning("No available data points for cross-validation")
            return None

        # Si une seule source, retourner telle quelle
        if len(available) == 1:
            return available[0]

        # Vérifier la cohérence des valeurs numériques
        numeric_values = []
        for dp in available:
            if isinstance(dp.value, (int, float)):
                numeric_values.append(dp.value)

        if len(numeric_values) >= 2:
            # Calculer la variation
            min_val = min(numeric_values)
            max_val = max(numeric_values)
            variation = (max_val - min_val) / min_val if min_val != 0 else 0

            if variation > tolerance:
                logger.warning(
                    f"High variation between sources: {variation:.2%} "
                    f"(tolerance: {tolerance:.2%})"
                )
                # Marquer comme nécessitant validation
                # Pour l'instant, retourner la valeur médiane
                median_value = sorted(numeric_values)[len(numeric_values) // 2]
                best_match = next(dp for dp in available if dp.value == median_value)

                # Changer le type en ESTIMATION
                return DataQuality(
                    value=best_match.value,
                    quality_type=DataQualityType.ESTIMATE,
                    source=best_match.source,
                    freshness_days=best_match.freshness_days
                )

        # Prendre la source la plus fiable
        best_source = max(available, key=lambda dp: dp.source.reliability_score)
        return best_source

    @staticmethod
    def format_for_display(data_quality: DataQuality) -> Dict[str, Any]:
        """
        Formate une DataQuality pour affichage à l'utilisateur.
        Inclut toutes les métadonnées de traçabilité.

        Args:
            data_quality: Donnée à formater

        Returns:
            Dict avec valeur et métadonnées
        """
        if not data_quality.is_available():
            return {
                "value": "Non disponible",
                "quality": "Non disponible",
                "source": None,
                "freshness": None,
                "reliable": False
            }

        # Indicateur de fraîcheur
        if data_quality.freshness_days is not None:
            if data_quality.freshness_days <= 7:
                freshness_label = "Très fraîche"
            elif data_quality.freshness_days <= 30:
                freshness_label = "Fraîche"
            elif data_quality.freshness_days <= 90:
                freshness_label = "Acceptable"
            else:
                freshness_label = "Périmée"
        else:
            freshness_label = "Inconnue"

        return {
            "value": data_quality.value,
            "quality": data_quality.quality_type.value,
            "source": {
                "name": data_quality.source.name if data_quality.source else "Inconnue",
                "url": str(data_quality.source.url) if data_quality.source and data_quality.source.url else None,
                "collected_at": data_quality.source.collected_at.isoformat() if data_quality.source else None,
            },
            "freshness": {
                "days": data_quality.freshness_days,
                "label": freshness_label
            },
            "reliable": (
                data_quality.source.reliability_score >= 0.70
                if data_quality.source else False
            )
        }

    @staticmethod
    def generate_validation_report(confidence: ConfidenceScore) -> Dict[str, Any]:
        """
        Génère un rapport de validation pour les humains.

        Args:
            confidence: Score de confiance à analyser

        Returns:
            Dict avec recommandations
        """
        report = {
            "confidence_score": confidence.score,
            "nb_sources": confidence.nb_sources,
            "needs_validation": confidence.needs_human_validation,
            "recommendations": []
        }

        # Recommandations basées sur le score
        if confidence.score < 0.50:
            report["recommendations"].append(
                "Score de confiance très faible. Validation humaine OBLIGATOIRE."
            )
        elif confidence.score < 0.70:
            report["recommendations"].append(
                "Score de confiance insuffisant. Validation humaine recommandée."
            )
        elif confidence.score < 0.85:
            report["recommendations"].append(
                "Score de confiance acceptable. Vérification ponctuelle suggérée."
            )
        else:
            report["recommendations"].append(
                "Score de confiance élevé. Données fiables."
            )

        # Recommandations basées sur le nombre de sources
        if confidence.nb_sources < 2:
            report["recommendations"].append(
                f"Seulement {confidence.nb_sources} source(s). "
                "Rechercher des sources additionnelles."
            )

        return report
