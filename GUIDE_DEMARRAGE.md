# 🚀 Guide de Démarrage Rapide - VIGIL

## 📍 Où est le Code ?

Le code est dans le repository **VIGIL** sur la branche :
```
claude/claude-md-mi1wmcculuxsuapp-01E25WBTqfakzJVERY5rEpSU
```

**Structure :**
```
VIGIL/
├── src/                    # Code source principal
│   ├── models/            # Modèles de données
│   ├── modules/           # Modules 1, 2, 3, 6
│   ├── services/          # APIs et scrapers
│   └── orchestrator.py    # Orchestrateur
├── main.py                # Exemple simple
├── test_pilot.py          # Test 10 entreprises ⭐
├── requirements.txt       # Dépendances
└── .env.example          # Configuration
```

---

## ⚡ Installation Express (5 minutes)

### 1. Cloner le Repository

```bash
# Si pas encore cloné
git clone https://github.com/Ahlaoban/VIGIL.git
cd VIGIL

# Vérifier la branche
git checkout claude/claude-md-mi1wmcculuxsuapp-01E25WBTqfakzJVERY5rEpSU
```

### 2. Créer l'Environnement Virtuel

```bash
# Créer venv
python3 -m venv venv

# Activer
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Vérifier
which python  # doit pointer vers venv/bin/python
```

### 3. Installer les Dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configuration des Clés API

```bash
# Copier le template
cp .env.example .env

# Éditer avec vos clés
nano .env  # ou vim, code, etc.
```

**Clés API à obtenir :**

#### Option A : Avec APIs (recommandé)

```env
# Crunchbase (identification concurrents)
# 👉 https://www.crunchbase.com/api
CRUNCHBASE_API_KEY=votre_cle_ici

# Pappers (données entreprises françaises)
# 👉 https://www.pappers.fr/api
PAPPERS_API_KEY=votre_cle_ici
```

#### Option B : Mode Test (sans APIs)

Si vous n'avez pas les clés API, VIGIL fonctionnera en mode dégradé avec des données limitées.

```env
# Laisser vide ou commenter
# CRUNCHBASE_API_KEY=
# PAPPERS_API_KEY=
```

---

## 🧪 Tester avec 10 Entreprises

### Test Automatique (Recommandé)

J'ai créé un script `test_pilot.py` qui teste automatiquement 10 profils d'entreprises :

```bash
# Lancer le test pilote
python test_pilot.py
```

**Ce script va :**
1. ✅ Tester 10 profils d'entreprises différentes
2. ✅ Identifier 5 concurrents pour chacune
3. ✅ Analyser les données financières et marketing
4. ✅ Générer 10 rapports JSON
5. ✅ Créer un résumé global

**Résultats sauvegardés dans :**
```
pilot_test_results/
├── TechSolutions_SAS_20251116_143052.json
├── DataCorp_20251116_143102.json
├── ...
└── summary_20251116_143500.json
```

**Temps estimé :** ~15-20 minutes pour les 10 entreprises

---

### Test Manuel (1 Entreprise)

Pour tester rapidement avec une seule entreprise :

```bash
python main.py
```

Ou créez votre propre test :

```python
# test_my_company.py
import asyncio
from src.models.competitor import ClientProfile, CompanySize
from src.models.common import GeoLocation
from src.orchestrator import VigilOrchestrator

async def main():
    # Votre entreprise
    client = ClientProfile(
        company_name="Ma Société SAS",
        naf_code="6201Z",
        industry_sector="Software Development",
        company_size=CompanySize.SME,
        headquarters=GeoLocation(country="France", city="Paris"),
        target_markets=["France"],
        products_services=["SaaS CRM"],
        value_proposition="CRM simple pour PME",
        target_segments=["PME B2B"],
        annual_revenue=2_000_000,
        employees_count=35
    )

    # Analyser
    orchestrator = VigilOrchestrator()
    report = await orchestrator.run_full_analysis(
        client_profile=client,
        client_revenue=2_000_000,
        client_employees=35
    )

    # Résultats
    print(f"Concurrents trouvés: {report['summary']['total_competitors_identified']}")
    for comp in report['competitors']:
        print(f"- {comp['name']}")

asyncio.run(main())
```

---

## 📊 Analyser les Résultats

### Résumé Global

```bash
# Voir le résumé du test pilote
cat pilot_test_results/summary_*.json | jq '.'
```

**Exemple de résumé :**
```json
{
  "success_count": 8,
  "error_count": 2,
  "total_time_seconds": 1234.5,
  "average_time_seconds": 123.4,
  "results": [
    {
      "company": "TechSolutions SAS",
      "status": "SUCCESS",
      "competitors_found": 5
    },
    ...
  ]
}
```

### Rapport Détaillé

```bash
# Voir un rapport complet
cat pilot_test_results/TechSolutions_SAS_*.json | jq '.'
```

**Structure du rapport :**
```json
{
  "metadata": {
    "client": "TechSolutions SAS",
    "execution_time_seconds": 45.3
  },
  "summary": {
    "total_competitors_identified": 5,
    "breakdown": {"direct": 3, "indirect": 1, "emerging": 1}
  },
  "competitors": [
    {
      "name": "Concurrent A",
      "similarity_score": 0.88,
      "confidence_score": 0.85,
      "needs_validation": false
    }
  ],
  "recommendations": [...]
}
```

---

## 🐛 Dépannage

### Erreur : Module not found

```bash
# Vérifier que vous êtes dans venv
which python

# Réinstaller
pip install -r requirements.txt
```

### Erreur : API key invalid

```bash
# Vérifier .env
cat .env | grep API_KEY

# Les clés doivent être sans guillemets
# ✅ PAPPERS_API_KEY=abc123
# ❌ PAPPERS_API_KEY="abc123"
```

### Erreur : Rate limit exceeded

```bash
# Augmenter les délais dans .env
SCRAPING_DELAY=5.0  # au lieu de 2.0
API_RATE_LIMIT_PER_MINUTE=10  # au lieu de 30
```

### Pas de concurrents trouvés

**Causes possibles :**
1. Clés API manquantes → Mode dégradé
2. Code NAF trop spécifique → Élargir le secteur
3. Rate limit atteint → Attendre quelques minutes

**Solution :**
```python
# Dans test_pilot.py, réduire max_competitors
max_competitors=3  # au lieu de 5
```

---

## 📈 Métriques de Validation (Phase 1)

Pour valider le POC, vérifier que :

✅ **90%** des concurrents identifiés sont pertinents
✅ **80%** des données financières/marketing sont correctes
✅ **0** hallucination (toujours citer les sources)
✅ **< 10 min** par analyse complète

---

## 🎯 Prochaines Actions

1. **Obtenir les clés API** (Crunchbase + Pappers)
2. **Lancer le test pilote** : `python test_pilot.py`
3. **Analyser les résultats** dans `pilot_test_results/`
4. **Valider la pertinence** des concurrents identifiés
5. **Remonter les bugs** ou ajustements nécessaires

---

## 💡 Conseils

- 🚀 Commencez par **1-2 entreprises** pour valider l'installation
- ⏱️ Le test pilote complet prend **15-20 min**
- 📊 Analysez le fichier `summary_*.json` en premier
- 🔍 Les logs détaillés sont dans `vigil_pilot_test.log`
- 💾 Tous les rapports JSON sont réutilisables

---

## 🆘 Support

- **Logs** : `vigil_pilot_test.log`
- **Documentation** : `README.md`
- **CDC** : `VIGIL_CDC.md`

**Besoin d'aide ?** Partagez le contenu de `vigil_pilot_test.log` !
