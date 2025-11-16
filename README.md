# VIGIL - Expert Concurrence

**Version 1.0 - Phase 1 (POC)**

Plateforme d'intelligence concurrentielle automatisée avec garantie "Zéro Hallucination".

---

## 🎯 Vue d'Ensemble

VIGIL est une solution d'intelligence stratégique qui identifie, analyse et compare automatiquement vos concurrents en utilisant des données factuelles provenant de sources multiples.

### Promesse de Valeur

> *Fournir une analyse concurrentielle ultra-précise, factuelle (zéro hallucination), et mise à jour en continu qui identifie les vrais concurrents d'une entreprise et leurs forces/faiblesses réelles, et non supposées.*

### Avantages par rapport aux analyses traditionnelles

- ✅ **Coût réduit** : Automatisation vs 15-30k€ pour un cabinet de conseil
- ✅ **Toujours à jour** : Analyse continue vs analyse ponctuelle obsolète en 3 mois
- ✅ **Données réelles** : Métriques factuelles vs frameworks génériques (Porter, BCG)
- ✅ **Zéro biais** : Analyse objective avec traçabilité des sources
- ✅ **Alertes temps réel** : Détection des mouvements stratégiques

---

## 📋 Modules Implémentés (Phase 1 - POC)

### ✅ Module 1 : Identification des Concurrents

Identifie automatiquement 5 à 10 concurrents principaux :

- **Concurrents directs** : Même secteur, marché, taille comparable
- **Concurrents indirects** : Secteur adjacent, même problème résolu
- **Concurrents émergents** : Startups récentes, croissance rapide

**Scoring & Classement** :
- Score de pertinence (similarité secteur, taille, géo, produits)
- Score de confiance (nombre et qualité des sources)
- Validation humaine si confiance < 70%

### ✅ Module 2 : Analyse Financière (POC)

Collecte et compare les données financières :

- **Métriques clés** (POC) :
  - Chiffre d'affaires
  - Croissance CA
  - Effectifs
  - Résultat net (si disponible)

- **Benchmarking** : Comparaison systématique avec le client
- **Forces/Faiblesses** : Génération d'interprétations textuelles

### ✅ Module 3 : Analyse Marketing (POC)

Analyse le positionnement et les stratégies marketing :

- **Scraping web** : Proposition de valeur, grille tarifaire
- **Réseaux sociaux** : Présence LinkedIn (POC)
- **Comparaison** : Benchmarking avec le client

### ✅ Module 6 : Garantie "Zéro Hallucination"

Système transversal garantissant la factualité :

- **Règle d'or** : "Il vaut mieux dire 'Je ne sais pas' que d'inventer"
- **Citation systématique** : Source, date, URL pour chaque donnée
- **Qualification** : Fait / Estimation / Hypothèse / Non disponible
- **Fraîcheur** : Indication de l'âge des données
- **Validation** : Recommandation si confiance < 70%

---

## 🏗️ Architecture Technique

### Technologies

- **Langage** : Python 3.10+
- **Async** : `asyncio` pour la concurrence
- **HTTP** : `httpx`, `aiohttp`
- **Scraping** : `BeautifulSoup4`, `Scrapy`, `Playwright`
- **Données** : `Pydantic` pour validation
- **Logs** : `loguru`

### Structure du Projet

```
vigil/
├── src/
│   ├── models/              # Modèles de données (Pydantic)
│   │   ├── common.py        # DataSource, DataQuality, ConfidenceScore
│   │   ├── competitor.py    # Competitor, ClientProfile, CompetitorType
│   │   ├── financial.py     # FinancialData, FinancialMetrics
│   │   └── marketing.py     # MarketingData, SEOMetrics
│   ├── modules/             # Modules fonctionnels
│   │   ├── module1_identification.py
│   │   ├── module2_financial.py
│   │   ├── module3_marketing.py
│   │   └── module6_zero_hallucination.py
│   ├── services/            # Services externes
│   │   └── api_clients/
│   │       ├── base_client.py
│   │       ├── crunchbase.py
│   │       └── societe_com.py
│   ├── orchestrator.py      # Orchestrateur principal
│   └── config.py            # Configuration
├── tests/
├── main.py                  # Exemple d'utilisation
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Installation

### 1. Prérequis

- Python 3.10 ou supérieur
- Compte et clés API pour :
  - [Crunchbase](https://www.crunchbase.com/api) (identification concurrents)
  - [Pappers](https://www.pappers.fr/api) (données entreprises françaises)

### 2. Installation

```bash
# Cloner le repository
git clone https://github.com/your-org/vigil.git
cd vigil

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configuration

Copier le fichier de configuration et renseigner vos clés API :

```bash
cp .env.example .env
nano .env  # ou votre éditeur préféré
```

**Variables obligatoires pour le POC** :
```env
# API Keys
CRUNCHBASE_API_KEY=your_crunchbase_api_key_here
PAPPERS_API_KEY=your_pappers_api_key_here

# Base de données (optionnel pour POC)
DATABASE_URL=postgresql://user:password@localhost:5432/vigil_db
```

---

## 💻 Utilisation

### Exemple Basique

```python
import asyncio
from src.models.competitor import ClientProfile, CompanySize
from src.models.common import GeoLocation
from src.orchestrator import VigilOrchestrator

async def main():
    # Définir le profil client
    client_profile = ClientProfile(
        company_name="Ma Startup SaaS",
        naf_code="6201Z",
        industry_sector="Software Development",
        company_size=CompanySize.SME,
        headquarters=GeoLocation(country="France", city="Paris"),
        target_markets=["France", "Europe"],
        products_services=["CRM SaaS", "Automation Tools"],
        value_proposition="CRM simple pour PME",
        target_segments=["PME B2B"],
        annual_revenue=1_500_000,
        employees_count=25
    )

    # Lancer l'analyse
    orchestrator = VigilOrchestrator()
    report = await orchestrator.run_full_analysis(
        client_profile=client_profile,
        client_revenue=1_500_000,
        client_employees=25,
        max_competitors=10
    )

    # Afficher les résultats
    print(f"Concurrents identifiés : {report['summary']['total_competitors_identified']}")
    for comp in report['competitors']:
        print(f"- {comp['name']} (score: {comp['similarity_score']:.2f})")

asyncio.run(main())
```

### Lancer l'exemple complet

```bash
python main.py
```

Le rapport sera sauvegardé dans `vigil_report.json`.

---

## 📊 Format du Rapport

Le rapport JSON généré contient :

```json
{
  "metadata": {
    "client": "TechSolutions SAS",
    "analysis_date": "2025-11-16T10:30:00",
    "execution_time_seconds": 45.3
  },
  "summary": {
    "total_competitors_identified": 10,
    "breakdown": {"direct": 6, "indirect": 3, "emerging": 1},
    "data_quality": {
      "competitors_needing_validation": 2,
      "financial_data_collected": 7,
      "marketing_data_collected": 8
    }
  },
  "competitors": [
    {
      "name": "Concurrent A",
      "type": "Direct",
      "similarity_score": 0.88,
      "confidence_score": 0.85,
      "needs_validation": false,
      "profile": {...}
    }
  ],
  "financial_analysis": [...],
  "marketing_analysis": [...],
  "insights": {...},
  "recommendations": [...]
}
```

---

## 🔧 Configuration Avancée

### Seuils de Confiance

Dans `.env` :

```env
MIN_CONFIDENCE_THRESHOLD=0.70  # Seuil pour validation humaine
MIN_DATA_SOURCES=2              # Nombre minimum de sources
```

### Rate Limiting

```env
API_RATE_LIMIT_PER_MINUTE=30    # Limite API
SCRAPING_RATE_LIMIT_PER_MINUTE=10
```

### Cache

```env
CACHE_TTL_DAYS=90               # Durée de validité du cache
ENABLE_CACHE=true
```

---

## 🧪 Tests

```bash
# Lancer tous les tests
pytest

# Tests avec couverture
pytest --cov=src --cov-report=html

# Tests d'un module spécifique
pytest tests/test_module1.py
```

---

## 📈 Roadmap

### ✅ Phase 1 - POC (Actuel)
- Module 1 : Identification concurrents
- Module 2 : Analyse financière (métriques de base)
- Module 3 : Analyse marketing (scraping web)
- Module 6 : Garantie "Zéro Hallucination"

### 🚧 Phase 2 - Industrialisation (6 mois)
- [ ] Module 4 : Détection des mouvements stratégiques (veille)
- [ ] Module 5 : Intégration aux prévisions et recommandations
- [ ] Architecture parallèle (MACRO + MICRO)
- [ ] Dashboard web interactif
- [ ] API publique d'export
- [ ] Optimisations (caching, batch processing)

### 🔮 Phase 3 - Évolution (12-24 mois)
- [ ] ML pour prédiction des mouvements concurrents
- [ ] Analyse de sentiment (NLP) sur avis clients
- [ ] Veille brevets
- [ ] Module "War Gaming" (simulation scénarios)

---

## 🛡️ Garantie "Zéro Hallucination"

Chaque donnée respecte le protocole suivant :

1. **Jamais d'invention** : Si donnée introuvable → "Non disponible"
2. **Citation systématique** : Source + Date + URL
3. **Qualification** :
   - `Fait` : Source primaire vérifiée
   - `Estimation` : Calculée à partir de faits
   - `Hypothèse` : Inférée
   - `Non disponible` : Données introuvables
4. **Indication de fraîcheur** : Âge de la donnée en jours
5. **Validation humaine** : Si confiance < 70%

### Exemple de DataQuality

```python
{
  "value": 15000000,
  "quality_type": "Fait",
  "source": {
    "name": "Pappers",
    "url": "https://www.pappers.fr/entreprise/...",
    "collected_at": "2025-11-16T10:30:00",
    "reliability_score": 0.90
  },
  "freshness_days": 30
}
```

---

## 📝 Sources de Données

### Entreprises & Identification
- [Crunchbase](https://www.crunchbase.com) - Startups, levées de fonds
- [Pappers](https://www.pappers.fr) - Entreprises françaises (SIRET, bilans)
- LinkedIn Company Pages - Profils entreprises

### Finances
- [Financial Modeling Prep](https://financialmodelingprep.com) - Données boursières
- [Alpha Vantage](https://www.alphavantage.co) - Données financières

### Marketing & SEO (Phase 2)
- [SimilarWeb](https://www.similarweb.com) - Trafic web
- [SEMrush](https://www.semrush.com) - Mots-clés, SEO
- Trustpilot, G2, Capterra - Réputation

---

## ⚠️ Limitations du POC

Cette version POC a les limitations suivantes :

1. **Géographie** : Optimisé pour entreprises françaises (Pappers API)
2. **Données limitées** : 2-3 métriques financières seulement
3. **Pas de veille temps réel** : Analyse ponctuelle (Module 4 non implémenté)
4. **Scraping basique** : Parsing web simplifié
5. **Pas d'API publique** : Utilisation via script Python uniquement

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour les guidelines.

---

## 📄 Licence

Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour plus de détails.

---

## 📞 Support

- **Documentation** : [docs.vigil.io](https://docs.vigil.io)
- **Issues** : [GitHub Issues](https://github.com/your-org/vigil/issues)
- **Email** : support@vigil.io

---

## 🙏 Remerciements

Développé par **Manus** dans le cadre du projet VIGIL.

**Technologies utilisées** :
- Python, asyncio, Pydantic
- Crunchbase API, Pappers API
- BeautifulSoup4, httpx
- loguru

---

**Version** : 1.0.0-POC
**Date** : 16 novembre 2025
**Statut** : Phase 1 (Preuve de Concept)
