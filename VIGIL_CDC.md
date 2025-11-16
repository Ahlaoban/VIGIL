# Cahier des Charges (CdC) - VIGIL - Module "Expert Concurrence"

- **Version :** 1.0
- **Date :** 16 novembre 2025
- **Auteur :** Manus
- **Statut :** Finalisé pour développement

---

## Table des Matières

1.  [Introduction et Contexte du Projet](#1-introduction-et-contexte-du-projet)
    - [1.1. Présentation Générale du Projet VIGIL](#11-présentation-générale-du-projet-vigil)
    - [1.2. Problématique Adressée](#12-problématique-adressée)
    - [1.3. Vision et Objectifs du Module "Expert Concurrence"](#13-vision-et-objectifs-du-module-expert-concurrence)
    - [1.4. Publics Cibles](#14-publics-cibles)
2.  [Périmètre et Spécifications Fonctionnelles](#2-périmètre-et-spécifications-fonctionnelles)
    - [2.1. Vue d'Ensemble des Fonctionnalités](#21-vue-densemble-des-fonctionnalités)
    - [2.2. Module 1 : Identification des Concurrents](#22-module-1--identification-des-concurrents)
    - [2.3. Module 2 : Analyse Financière Comparative](#23-module-2--analyse-financière-comparative)
    - [2.4. Module 3 : Analyse Marketing Comparative](#24-module-3--analyse-marketing-comparative)
    - [2.5. Module 4 : Détection des Mouvements Stratégiques](#25-module-4--détection-des-mouvements-stratégiques)
    - [2.6. Module 5 : Intégration aux Prévisions et Recommandations](#26-module-5--intégration-aux-prévisions-et-recommandations)
    - [2.7. Module 6 : Garantie "Zéro Hallucination" (Exigence Transversale)](#27-module-6--garantie-zéro-hallucination-exigence-transversale)
    - [2.8. Interface Utilisateur (Dashboard)](#28-interface-utilisateur-dashboard)
3.  [Spécifications Techniques](#3-spécifications-techniques)
    - [3.1. Architecture Globale](#31-architecture-globale)
    - [3.2. Technologies et Environnement](#32-technologies-et-environnement)
    - [3.3. Sources de Données (APIs & Scraping)](#33-sources-de-données-apis--scraping)
    - [3.4. Modèles de Données et Formats d'Échange (JSON)](#34-modèles-de-données-et-formats-déchange-json)
4.  [Feuille de Route (Roadmap) et Livrables](#4-feuille-de-route-roadmap-et-livrables)
    - [4.1. Phase 1 : Preuve de Concept (POC) - 3 mois](#41-phase-1--preuve-de-concept-poc---3-mois)
    - [4.2. Phase 2 : Industrialisation - 6 mois](#42-phase-2--industrialisation---6-mois)
    - [4.3. Phase 3 : Évolution Continue - 12-24 mois](#43-phase-3--évolution-continue---12-24-mois)
5.  [Risques, Contraintes et Mitigations](#5-risques-contraintes-et-mitigations)
    - [5.1. Risques Techniques](#51-risques-techniques)
    - [5.2. Risques Business](#52-risques-business)
    - [5.3. Contraintes Légales](#53-contraintes-légales)
6.  [Critères de Succès et de Validation](#6-critères-de-succès-et-de-validation)

---

## 1. Introduction et Contexte du Projet

### 1.1. Présentation Générale du Projet VIGIL
VIGIL est une plateforme d'intelligence stratégique conçue pour aider les entreprises à naviguer dans des environnements complexes. Sa mission principale est de détecter les signaux faibles, d'anticiper les tendances de marché et d'identifier les ruptures potentielles pour permettre une prise de décision proactive.

### 1.2. Problématique Adressée
Les analyses concurrentielles traditionnelles, souvent réalisées par des cabinets de conseil, souffrent de défauts majeurs :
- **Coût élevé :** 15k€ à 30k€ pour une analyse ponctuelle.
- **Obsolescence rapide :** Les données deviennent caduques en moins de 3 mois.
- **Manque de profondeur :** Utilisation de frameworks génériques (Porter, BCG) sans données réelles et granulaires.
- **Biais :** Analyses orientées pour confirmer les hypothèses du client.
- **Manque de continuité :** Absence de suivi et d'alertes en temps réel.

### 1.3. Vision et Objectifs du Module "Expert Concurrence"
Le module "Expert Concurrence" a pour objectif de transformer VIGIL en une plateforme d'intelligence concurrentielle complète.

**Promesse de valeur :** *Fournir une analyse concurrentielle ultra-précise, factuelle (zéro hallucination), et mise à jour en continu qui identifie les vrais concurrents d'une entreprise et leurs forces/faiblesses réelles, et non supposées.*

**Objectifs clés :**
1.  **Automatiser** l'identification et l'analyse des concurrents.
2.  **Garantir** la factualité et la traçabilité de chaque donnée ("Zéro Hallucination").
3.  **Surveiller** en continu les mouvements stratégiques des concurrents.
4.  **Intégrer** l'intelligence concurrentielle dans le processus de recalibrage des scénarios prospectifs de VIGIL.

### 1.4. Publics Cibles
- **B2C :** Dirigeants de PME/ETI et consultants en stratégie.
- **B2B :** Grandes entreprises avec des équipes dédiées à la stratégie, au marketing et à l'intelligence économique.

---

## 2. Périmètre et Spécifications Fonctionnelles

### 2.1. Vue d'Ensemble des Fonctionnalités
Le module est composé de 6 sous-modules interconnectés qui assurent le cycle complet de l'intelligence concurrentielle.

### 2.2. Module 1 : Identification des Concurrents
- **Objectif :** Identifier automatiquement 5 à 10 concurrents principaux (directs, indirects, émergents).
- **Inputs :** Profil du client (secteur d'activité via code NAF, produits/services, marchés géographiques, taille, segments cibles).
- **Processus :**
    1.  **Recherche de concurrents directs :** Critères stricts (même secteur, marché, taille comparable).
    2.  **Recherche de concurrents indirects :** Critères plus larges (secteur adjacent, même problème résolu).
    3.  **Recherche de concurrents émergents :** Startups récentes, levées de fonds significatives, croissance rapide.
    4.  **Scoring & Classement :** Chaque concurrent candidat est évalué selon un score de pertinence (similarité secteur, taille, géographie, produits) et un niveau de confiance (nombre et qualité des sources).
    5.  **Validation :** Les concurrents avec un score de confiance < 70% sont marqués comme nécessitant une "validation humaine".

### 2.3. Module 2 : Analyse Financière Comparative
- **Objectif :** Collecter, analyser et comparer les données financières des concurrents identifiés.
- **Processus :**
    1.  **Identification du type de société :** Cotée, non cotée, startup.
    2.  **Collecte automatisée :** Via APIs financières et scraping de rapports annuels.
    3.  **Métriques collectées :** CA, croissance, EBITDA, résultat net, effectifs, levées de fonds, valorisation.
    4.  **Benchmarking :** Comparaison systématique de chaque métrique du concurrent avec celle du client (+/- 20% = équilibre).
    5.  **Identification des forces/faiblesses :** Génération d'interprétations textuelles (ex: "Croissance très supérieure, suggère meilleure traction marché").

### 2.4. Module 3 : Analyse Marketing Comparative
- **Objectif :** Analyser et comparer le positionnement et les stratégies marketing.
- **Processus :**
    1.  **Scraping des sites web :** Extraction de la proposition de valeur, des segments cibles et des grilles tarifaires.
    2.  **Analyse SEO/SEM :** Via APIs (SimilarWeb, SEMrush) pour obtenir le trafic, les mots-clés et les budgets publicitaires estimés.
    3.  **Analyse des réseaux sociaux :** Collecte du nombre de followers et de l'engagement.
    4.  **Analyse de la réputation :** Collecte des notes et avis sur Trustpilot, G2, etc.
    5.  **Benchmarking :** Comparaison de toutes les métriques marketing avec le client.

### 2.5. Module 4 : Détection des Mouvements Stratégiques
- **Objectif :** Surveiller en continu les actions stratégiques des concurrents et alerter le client.
- **Processus :**
    1.  **Boucle de surveillance (toutes les heures) :** Scan des sources d'actualités, communiqués de presse, LinkedIn, Product Hunt.
    2.  **Événements surveillés :** Levées de fonds, acquisitions, lancements de produits, recrutements clés (CEO, CTO, etc.).
    3.  **Scoring d'impact (0-10) :** Chaque mouvement est noté en fonction de son type, de son ampleur, de sa pertinence pour le client et de son urgence.
    4.  **Génération d'alertes critiques :** Si impact ≥ 8/10, une alerte est envoyée.

### 2.6. Module 5 : Intégration aux Prévisions et Recommandations
- **Objectif :** Utiliser l'intelligence concurrentielle pour enrichir l'analyse stratégique.
- **Processus :**
    1.  **Impact sur les scénarios :** Les mouvements stratégiques détectés (Module 4) et les forces/faiblesses identifiées (Modules 2 & 3) sont utilisés comme inputs pour recalibrer les probabilités des scénarios prospectifs de VIGIL.
    2.  **Génération de recommandations :** Le système génère des actions stratégiques différenciées (court, moyen, long terme) avec une justification basée sur l'analyse concurrentielle.

### 2.7. Module 6 : Garantie "Zéro Hallucination" (Exigence Transversale)
- **Règle d'or :** "Il vaut mieux dire 'Je ne sais pas' que d'inventer."
- **Exigences :**
    1.  **Jamais d'invention :** Si une donnée est introuvable, afficher "Non disponible".
    2.  **Citation systématique :** Chaque donnée doit être accompagnée de sa source, de sa date de collecte et d'une URL si possible.
    3.  **Qualification de la donnée :** Chaque information doit être étiquetée comme "Fait" (source primaire), "Estimation" (calculée) ou "Hypothèse" (inférée).
    4.  **Indication de la fraîcheur :** La date de la donnée doit toujours être visible.
    5.  **Validation humaine :** Tout résultat avec une confiance globale < 70% doit déclencher une recommandation de validation manuelle.

### 2.8. Interface Utilisateur (Dashboard)
Le dashboard VIGIL sera enrichi d'un quatrième onglet : **"Concurrence"**.
- **Contenu :**
    - Liste des 5-10 concurrents identifiés avec leur score de pertinence.
    - Tableau de bord comparatif (financier et marketing).
    - Timeline visuelle des mouvements stratégiques critiques des concurrents.
    - Graphiques d'évolution (ex: parts de marché estimées).

---

## 3. Spécifications Techniques

### 3.1. Architecture Globale
- **Architecture Parallèle (v2.0) :**
    - **Branche MACRO :** Le flux VIGIL existant qui analyse les signaux macro-environnementaux et sectoriels.
    - **Branche MICRO :** Le nouveau module "Expert Concurrence" qui fonctionne en parallèle.
    - **Hub de Convergence :** L'Expert "Scénarii" est modifié pour accepter les inputs des deux branches (MACRO + MICRO) afin de produire un recalibrage enrichi.
- **Orchestration :** L'orchestrateur principal de VIGIL doit être refactorisé pour lancer les deux branches en parallèle (`asyncio.gather`) et attendre leurs résultats avant de les passer à l'Expert Scénarii.

### 3.2. Technologies et Environnement
- **Langage :** Python (version 3.10+).
- **Librairies clés :** `asyncio` pour la concurrence, `httpx` ou `aiohttp` pour les appels API, `BeautifulSoup4` ou `Scrapy` pour le scraping, `Pydantic` ou `dataclasses` pour la modélisation des données.
- **Base de données :** Une base de données (ex: PostgreSQL ) est requise pour stocker les données concurrentielles collectées, afin de permettre le caching et l'analyse historique.

### 3.3. Sources de Données (APIs & Scraping)
- **Entreprises :** Crunchbase, PitchBook, Societe.com, Infogreffe, LinkedIn Company Pages.
- **Finances :** Pappers API, Financial Modeling Prep API, Alpha Vantage API, Yahoo Finance API.
- **Marketing & SEO :** SimilarWeb API, SEMrush API, Ahrefs API.
- **Réputation :** Scraping de Trustpilot, G2, Capterra.
- **Actualités & Mouvements :** TechCrunch, Les Échos (via flux RSS ou APIs), Product Hunt, scraping des pages "News" des sites concurrents.

### 3.4. Modèles de Données et Formats d'Échange (JSON)
Des `dataclasses` Python seront utilisées pour représenter chaque entité. Les outputs de chaque module devront se conformer à un schéma JSON strict. Les exemples fournis dans le document de spécifications initiales serviront de référence.

---

## 4. Feuille de Route (Roadmap) et Livrables

### 4.1. Phase 1 : Preuve de Concept (POC) - 3 mois
- **Objectif :** Valider la faisabilité technique et la valeur pour le client.
- **Livrables :**
    - Implémentation du **Module 1** (Identification Concurrents) avec les APIs Crunchbase et Societe.com.
    - Implémentation partielle des **Modules 2 & 3** (Analyse Financière & Marketing) pour 2-3 métriques clés.
    - Workflow de validation humaine.
    - Tests avec 10 entreprises pilotes pour valider la pertinence des concurrents identifiés.

### 4.2. Phase 2 : Industrialisation - 6 mois
- **Objectif :** Construire une version robuste, scalable et complète du module.
- **Livrables :**
    - Refactoring de l'orchestrateur VIGIL en architecture parallèle.
    - Implémentation complète des 6 modules.
    - Mise en place du caching des données et de l'optimisation des appels API.
    - Développement du dashboard "Concurrence".
    - API publique pour l'export des données.

### 4.3. Phase 3 : Évolution Continue - 12-24 mois
- **Objectif :** Ajouter des fonctionnalités d'analyse prédictive et avancée.
- **Livrables :**
    - Modèle de Machine Learning pour prédire les prochains mouvements concurrents.
    - Analyse de sentiment (NLP) sur les avis clients.
    - Module de veille sur les brevets.
    - Module de "war gaming" pour simuler des scénarios concurrentiels.

---

## 5. Risques, Contraintes et Mitigations

### 5.1. Risques Techniques
- **Risque 1 : Coûts des APIs élevés.**
    - **Mitigation :** Mettre en place un cache agressif (données valables 90 jours), traiter les données par lots (batch processing), négocier des tarifs préférentiels avec les fournisseurs.
- **Risque 2 : Scraping bloqué ou instable.**
    - **Mitigation :** Développer des scrapers robustes avec des fallbacks, diversifier les sources de données pour ne pas dépendre d'une seule, monitorer les erreurs de scraping.
- **Risque 3 : Qualité des données variable.**
    - **Mitigation :** Mettre en œuvre le protocole "Zéro Hallucination", croiser les sources pour valider les données, utiliser le score de confiance pour indiquer la fiabilité.

### 5.2. Risques Business
- **Risque 4 : Adoption lente (prix perçu élevé).**
    - **Mitigation :** Proposer un essai gratuit d'un mois, créer des études de cas démontrant le ROI par rapport au consulting, communiquer clairement sur la valeur ajoutée (données fraîches et continues).
- **Risque 5 : Concurrence d'outils similaires (ex: Crayon, Kompyte).**
    - **Mitigation :** Mettre en avant la différenciation unique : l'intégration avec la veille prospective (VIGIL) et le dialogue stratégique (Min&Maï), ainsi que la garantie "Zéro Hallucination".

### 5.3. Contraintes Légales
- **Risque 6 : Complexité légale (RGPD, scraping).**
    - **Mitigation :** Scraper uniquement les données publiques, respecter scrupuleusement les fichiers `robots.txt`, consulter un conseil juridique pour valider les pratiques de collecte de données.

---

## 6. Critères de Succès et de Validation

### Pour le POC (Phase 1) :
- **Qualité de l'identification :** 90% des concurrents identifiés sont jugés pertinents par les clients pilotes.
- **Qualité des données :** 80% des données financières/marketing collectées sont correctes (vérification manuelle).
- **Fiabilité :** 0 hallucination détectée sur un audit de 100 analyses.
- **Satisfaction client :** NPS (Net Promoter Score) des clients pilotes ≥ 9/10.

### Pour le Produit Final (Phase 2) :
- **Performance :** Le temps d'exécution d'un cycle d'analyse complet (Macro + Micro) est inférieur à 10 minutes.
- **Adoption :** 40% des clients VIGIL existants adoptent le module "Expert Concurrence" dans les 24 mois suivant son lancement.
- **Rentabilité :** Le module atteint son seuil de rentabilité (couverture des coûts d'API et de compute additionnels) avec 2 clients B2C ou 1 client B2B.
