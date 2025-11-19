# Cahier des Charges (CdC) - VIGIL - Module "Expert Concurrence"

- **Version :** 2.0 (Optimisée)
- **Date :** 18 novembre 2025
- **Auteur :** Manus (v1.0) - Optimisé par Claude AI (v2.0)
- **Statut :** Optimisé et prêt pour développement

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
        - [2.8.1. Architecture du Dashboard](#281-architecture-du-dashboard)
        - [2.8.2. Page "Concurrence" - Wireframe Détaillé](#282-page-concurrence---wireframe-détaillé)
        - [2.8.3. Page Détails d'un Concurrent](#283-page-détails-dun-concurrent)
        - [2.8.4. Fonctionnalités Interactives](#284-fonctionnalités-interactives)
        - [2.8.5. Principes UX](#285-principes-ux)
3.  [Spécifications Techniques](#3-spécifications-techniques)
    - [3.1. Architecture Globale](#31-architecture-globale)
        - [3.1.1. Vue d'Ensemble - Architecture Parallèle v2.0](#311-vue-densemble---architecture-parallèle-v20)
        - [3.1.2. Architecture Détaillée - Module Expert Concurrence](#312-architecture-détaillée---module-expert-concurrence)
        - [3.1.3. Flux de Données et Communications](#313-flux-de-données-et-communications)
        - [3.1.4. Stack Technique Détaillée](#314-stack-technique-détaillée)
    - [3.2. Technologies et Environnement](#32-technologies-et-environnement)
    - [3.3. API REST - Spécifications des Endpoints](#33-api-rest---spécifications-des-endpoints)
        - [3.3.1. API Publique VIGIL - Module Concurrence](#331-api-publique-vigil---module-concurrence)
        - [3.3.2. Webhooks](#332-webhooks)
    - [3.4. Sources de Données (APIs & Scraping)](#34-sources-de-données-apis--scraping)
    - [3.5. Modèles de Données et Formats d'Échange (JSON)](#35-modèles-de-données-et-formats-déchange-json)
    - [3.6. Scalabilité et Performance](#36-scalabilité-et-performance)
        - [3.6.1. Stratégie de Scalabilité](#361-stratégie-de-scalabilité)
        - [3.6.2. Plan de Montée en Charge](#362-plan-de-montée-en-charge)
    - [3.7. Stratégie de Tests et Qualité](#37-stratégie-de-tests-et-qualité)
        - [3.7.1. Tests Unitaires et d'Intégration](#371-tests-unitaires-et-dintégration)
        - [3.7.2. Tests de Scraping](#372-tests-de-scraping)
        - [3.7.3. Tests de Charge et de Performance](#373-tests-de-charge-et-de-performance)
        - [3.7.4. Tests de Qualité des Données](#374-tests-de-qualité-des-données)
    - [3.8. Budget et Coûts Estimés](#38-budget-et-coûts-estimés)
        - [3.8.1. Coûts des APIs et Services Externes](#381-coûts-des-apis-et-services-externes)
        - [3.8.2. Coûts de Développement](#382-coûts-de-développement)
        - [3.8.3. Budget Total et ROI](#383-budget-total-et-roi)
    - [3.9. Sécurité et Conformité RGPD](#39-sécurité-et-conformité-rgpd)
        - [3.9.1. Classification des Données](#391-classification-des-données)
        - [3.9.2. Conformité RGPD](#392-conformité-rgpd)
        - [3.9.3. Pratiques de Scraping Éthique](#393-pratiques-de-scraping-éthique)
        - [3.9.4. Sécurité de l'Infrastructure](#394-sécurité-de-linfrastructure)
    - [3.10. Monitoring et Observabilité](#310-monitoring-et-observabilité)
        - [3.10.1. Métriques Applicatives (APM)](#3101-métriques-applicatives-apm)
        - [3.10.2. Métriques Infrastructure](#3102-métriques-infrastructure)
        - [3.10.3. Alerting](#3103-alerting)
        - [3.10.4. Dashboards Opérationnels](#3104-dashboards-opérationnels)
4.  [Feuille de Route (Roadmap) et Livrables](#4-feuille-de-route-roadmap-et-livrables)
    - [4.1. Phase 1 : Preuve de Concept (POC) - 3 mois](#41-phase-1--preuve-de-concept-poc---3-mois)
    - [4.2. Phase 2 : Industrialisation - 6 mois](#42-phase-2--industrialisation---6-mois)
    - [4.3. Phase 3 : Évolution Continue - 12-24 mois](#43-phase-3--évolution-continue---12-24-mois)
    - [4.4. Documentation et Formation](#44-documentation-et-formation)
        - [4.4.1. Documentation Technique](#441-documentation-technique)
        - [4.4.2. Documentation Utilisateur](#442-documentation-utilisateur)
        - [4.4.3. Vidéos Tutorielles](#443-vidéos-tutorielles)
        - [4.4.4. Formation des Équipes Clients](#444-formation-des-équipes-clients)
        - [4.4.5. Support Utilisateur](#445-support-utilisateur)
        - [4.4.6. Release Notes et Communication](#446-release-notes-et-communication)
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

#### 2.8.1. Architecture du Dashboard

Le dashboard VIGIL sera enrichi d'un **quatrième onglet : "Concurrence"**.

**Navigation principale:**
```
┌────────────────────────────────────────────────────────────┐
│  VIGIL                    [Client: MonEntreprise SAS]      │
├────────────────────────────────────────────────────────────┤
│  [Vue d'ensemble] [Scénarios] [Recommandations] [CONCURRENCE] │
└────────────────────────────────────────────────────────────┘
```

#### 2.8.2. Page "Concurrence" - Wireframe Détaillé

**Layout général:**
```
┌─────────────────────────────────────────────────────────────────┐
│ CONCURRENCE                           [⟳ Actualiser] [⚙ Config]│
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ ALERTES CRITIQUES (3)                           [Voir tout] ││
│ ├─────────────────────────────────────────────────────────────┤│
│ │ 🔴 [Il y a 2h] Concurrent A : Levée de fonds Série B 15M€  ││
│ │ 🟠 [Hier] Concurrent C : Lancement nouveau produit Analytics││
│ │ 🟠 [Il y a 3j] Concurrent B : Recrutement d'un ex-VP Google││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌───────────────────────────────────────────────────────────┐ │
│ │ VOS CONCURRENTS PRINCIPAUX (8)                            │ │
│ ├───────────────────────────────────────────────────────────┤ │
│ │ [Liste] [Grille] [Comparatif]                             │ │
│ ├───────────────────────────────────────────────────────────┤ │
│ │ ┌────┬──────────────┬──────┬────────┬────────┬─────────┐ │ │
│ │ │ #  │ Nom          │ Type │ Score  │ CA 2024│ Actions │ │ │
│ │ ├────┼──────────────┼──────┼────────┼────────┼─────────┤ │ │
│ │ │ 1  │ Concurrent A │ Dir. │ 95/100 │ 12.5M€ │ [Voir]  │ │ │
│ │ │    │ 🟢 Forte croissance │ 🔴 CA supérieur          │ │ │
│ │ ├────┼──────────────┼──────┼────────┼────────┼─────────┤ │ │
│ │ │ 2  │ Concurrent B │ Dir. │ 88/100 │ 8.2M€  │ [Voir]  │ │ │
│ │ │    │ 🔴 Pricing agressif │ 🟢 Trafic faible         │ │ │
│ │ ├────┼──────────────┼──────┼────────┼────────┼─────────┤ │ │
│ │ │ 3  │ Startup X    │ Émerg│ 75/100 │ 1.2M€  │ [Voir]  │ │ │
│ │ │    │ ⚠️ Levée de fonds récente (5M€)                  │ │ │
│ │ └────┴──────────────┴──────┴────────┴────────┴─────────┘ │ │
│ └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────┐ ┌─────────────────────────────────────┐│
│ │ BENCHMARKS CLÉS     │ │ TIMELINE MOUVEMENTS STRATÉGIQUES    ││
│ ├─────────────────────┤ ├─────────────────────────────────────┤│
│ │                     │ │ Nov ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ ││
│ │ CA Moyen: 9.8M€     │ │  16│ 🔴 Concurrent A: Levée 15M€    ││
│ │ Vous: 10.2M€        │ │  12│ 🟡 Concurrent D: Acquisition   ││
│ │ ✅ +4%              │ │   8│ 🟢 Concurrent B: Produit       ││
│ │                     │ │ Oct│ 🟡 Startup X: Partenariat AWS  ││
│ │ Croissance Moy: 28% │ │  │                                 ││
│ │ Vous: 32%           │ │ [Filtrer par type] [Export PDF]     ││
│ │ ✅ +4pts            │ │                                     ││
│ │                     │ │                                     ││
│ │ Trafic Web Moy:     │ │                                     ││
│ │ 320k/mois           │ │                                     ││
│ │ Vous: 180k/mois     │ │                                     ││
│ │ ⚠️ -44%              │ │                                     ││
│ └─────────────────────┘ └─────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

#### 2.8.3. Page Détails d'un Concurrent

```
┌─────────────────────────────────────────────────────────────────┐
│ < Retour            CONCURRENT A                    Score: 95/100│
├─────────────────────────────────────────────────────────────────┤
│ ┌─ IDENTITÉ ─────────────────────────────────────────────────┐ │
│ │ Nom: Concurrent A SAS        │ Site: concurrenta.com       │ │
│ │ Secteur: SaaS Analytics      │ Géo: France, Belgique       │ │
│ │ Type: Concurrent Direct      │ Effectifs: 75 personnes     │ │
│ │ Confiance: 87%               │ MAJ: il y a 2 jours         │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ [📊 Financier] [📈 Marketing] [📰 Actualités] [💡 Insights]     │
│                                                                 │
│ ┌─ DONNÉES FINANCIÈRES (2024) ────────────────────────────────┐│
│ │                                                              ││
│ │ Chiffre d'Affaires: 12.5M€               ┌─────────────────┐││
│ │ • +35% vs 2023                           │   📊 Graphique  │││
│ │ • +25% vs vous (10M€)                    │   CA évolution  │││
│ │ Source: Pappers (2j) ✓ Fait              │   2020-2024     │││
│ │                                           └─────────────────┘││
│ │ EBITDA: 2.1M€ (17% marge)                                   ││
│ │ • Rentable depuis 2022                                      ││
│ │ Source: Pappers (2j) ✓ Fait                                 ││
│ │                                                              ││
│ │ Levées de fonds:                                            ││
│ │ • 2025-11: Série B - 15M€ (Accel Partners) ⚡ NOUVEAU       ││
│ │ • 2023-03: Série A - 5M€ (Partech)                          ││
│ │ Source: Crunchbase (2h) ✓ Fait                              ││
│ │                                                              ││
│ │ 💡 Interprétation:                                          ││
│ │ Concurrent A montre une forte dynamique de croissance       ││
│ │ (+35%) et vient de lever 15M€. Risque de guerre des prix   ││
│ │ et d'accélération du recrutement à court terme.             ││
│ └──────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─ DONNÉES MARKETING ──────────────────────────────────────────┐│
│ │ Trafic Web: 450k visites/mois (+18% MoM)                    ││
│ │ Source: SimilarWeb (3j) ⚠️ Estimation (75% confiance)       ││
│ │                                                              ││
│ │ Top 3 Keywords:                                             ││
│ │ 1. "analytics saas" - Pos. 3 - 8100 vol.                    ││
│ │ 2. "business intelligence" - Pos. 7 - 12000 vol.            ││
│ │ 3. "data visualization" - Pos. 5 - 6500 vol.                ││
│ │                                                              ││
│ │ Pricing: À partir de 49€/mois (vs vous: 79€/mois)          ││
│ │ ⚠️ Prix 38% plus bas - pression concurrentielle             ││
│ │ Source: Site web (1j) ✓ Fait                                ││
│ │                                                              ││
│ │ Réputation:                                                 ││
│ │ • Trustpilot: 4.3/5 (234 avis)                              ││
│ │ • G2: 4.5/5 (89 avis) - Leader dans catégorie Analytics    ││
│ └──────────────────────────────────────────────────────────────┘│
│                                                                 │
│ [📥 Exporter en PDF] [🔔 Configurer alertes]                   │
└─────────────────────────────────────────────────────────────────┘
```

#### 2.8.4. Fonctionnalités Interactives

**Filtres et Recherche:**
- Filtrer par type de concurrent (Direct / Indirect / Émergent)
- Filtrer par pays / région
- Recherche par nom
- Tri par score de pertinence, CA, croissance, trafic web

**Alertes Configurables:**
- Seuil d'impact pour notifications (ex: uniquement impact ≥ 7/10)
- Types d'événements à surveiller (levées de fonds, lancements, recrutements)
- Canaux de notification (email, SMS, webhook)

**Exports:**
- PDF: Rapport concurrentiel complet
- CSV: Données brutes pour analyse
- API: Accès programmatique via endpoints REST

**Comparaisons:**
- Vue côte-à-côte de 2-3 concurrents
- Radar chart des forces/faiblesses
- Matrices de positionnement (prix vs features, CA vs croissance)

#### 2.8.5. Principes UX

**Transparence et Confiance:**
- Affichage systématique de la source et de la date de collecte
- Indicateur visuel du type de donnée (Fait ✓ / Estimation ⚠️ / Hypothèse ?)
- Score de confiance visible
- Message "Non disponible" si donnée manquante (jamais d'invention)

**Accessibilité:**
- Contraste WCAG AA minimum
- Navigation au clavier
- Lecteurs d'écran supportés
- Responsive design (desktop, tablet, mobile)

**Performance:**
- Lazy loading des graphiques
- Pagination des listes de concurrents
- Cache côté client pour navigation fluide
- Skeleton screens pendant chargement

---

## 3. Spécifications Techniques

### 3.1. Architecture Globale

#### 3.1.1. Vue d'Ensemble - Architecture Parallèle v2.0

```
┌─────────────────────────────────────────────────────────────────┐
│                    VIGIL ORCHESTRATEUR                          │
│                   (asyncio.gather)                              │
└────────────┬────────────────────────────────────┬───────────────┘
             │                                    │
             ▼                                    ▼
┌────────────────────────┐          ┌────────────────────────────┐
│  BRANCHE MACRO         │          │  BRANCHE MICRO             │
│  (Existant)            │          │  (Expert Concurrence)      │
│                        │          │                            │
│  - Signaux faibles     │          │  - Identification          │
│  - Tendances secteur   │          │  - Analyse financière      │
│  - Ruptures            │          │  - Analyse marketing       │
│  - PESTEL/Porter       │          │  - Mouvements stratégiques │
└────────────┬───────────┘          └───────────┬────────────────┘
             │                                  │
             │          ┌───────────────────────┘
             │          │
             ▼          ▼
     ┌──────────────────────────┐
     │  HUB DE CONVERGENCE      │
     │  Expert "Scénarii"       │
     │  (Modifié)               │
     │                          │
     │  Inputs:                 │
     │  - Signaux MACRO         │
     │  + Forces/Faiblesses     │
     │    concurrents (MICRO)   │
     │  + Mouvements critiques  │
     └──────────┬───────────────┘
                │
                ▼
     ┌──────────────────────────┐
     │  DASHBOARD VIGIL         │
     │  (4 onglets)             │
     │                          │
     │  1. Vue d'ensemble       │
     │  2. Scénarios            │
     │  3. Recommandations      │
     │  4. Concurrence (NEW)    │
     └──────────────────────────┘
```

#### 3.1.2. Architecture Détaillée - Module Expert Concurrence

```
┌────────────────────────────────────────────────────────────────┐
│                 EXPERT CONCURRENCE - PIPELINE                  │
└────────────────────────────────────────────────────────────────┘

INPUT: Profil Client (secteur NAF, produits, géo, taille)
   │
   ▼
┌──────────────────────────────────────────────────────────┐
│  MODULE 1: IDENTIFICATION CONCURRENTS                    │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐         │
│  │ Directs    │  │ Indirects  │  │ Émergents  │         │
│  │ (Crunchbase│  │ (Secteur   │  │ (Product   │         │
│  │ Societe.com│  │ adjacent)  │  │  Hunt)     │         │
│  └────────────┘  └────────────┘  └────────────┘         │
│         │               │               │                │
│         └───────────────┴───────────────┘                │
│                         ▼                                │
│              ┌──────────────────────┐                    │
│              │ Scoring & Ranking    │                    │
│              │ (Pertinence 0-100)   │                    │
│              └──────────────────────┘                    │
└─────────────────────────┬────────────────────────────────┘
                          │
         OUTPUT: Liste 5-10 concurrents + scores
                          │
          ┌───────────────┴───────────────┐
          │                               │
          ▼                               ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│ MODULE 2: ANALYSE       │   │ MODULE 3: ANALYSE       │
│ FINANCIÈRE              │   │ MARKETING               │
│                         │   │                         │
│ APIs:                   │   │ APIs:                   │
│ - Pappers               │   │ - SimilarWeb            │
│ - Financial Modeling    │   │ - SEMrush               │
│ - Yahoo Finance         │   │                         │
│                         │   │ Scraping:               │
│ Métriques:              │   │ - Trustpilot            │
│ - CA, croissance        │   │ - G2 / Capterra         │
│ - EBITDA, effectifs     │   │ - LinkedIn              │
│ - Levées de fonds       │   │ - Sites web             │
│                         │   │                         │
│ Output: Benchmarks      │   │ Output: Positionnement  │
└─────────┬───────────────┘   └─────────┬───────────────┘
          │                             │
          └──────────────┬──────────────┘
                         ▼
         ┌───────────────────────────────────┐
         │ CACHE / DATABASE (PostgreSQL)     │
         │ Rétention: 90 jours               │
         │ - competitor_profiles             │
         │ - financial_metrics               │
         │ - marketing_metrics               │
         │ - strategic_moves                 │
         └───────────────┬───────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────┐
│  MODULE 4: SURVEILLANCE MOUVEMENTS STRATÉGIQUES            │
│                                                            │
│  Boucle: Toutes les heures                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ News/RSS     │  │ LinkedIn     │  │ Product Hunt │   │
│  │ (Les Échos,  │  │ (Recrutements│  │ (Lancements) │   │
│  │ TechCrunch)  │  │ clés)        │  │              │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│         │                  │                 │            │
│         └──────────────────┴─────────────────┘            │
│                            ▼                              │
│              ┌──────────────────────────┐                 │
│              │ Détection d'événements   │                 │
│              │ - Levées de fonds        │                 │
│              │ - Acquisitions           │                 │
│              │ - Lancements produits    │                 │
│              └──────────┬───────────────┘                 │
│                         ▼                                 │
│              ┌──────────────────────────┐                 │
│              │ Scoring Impact (0-10)    │                 │
│              │ + Urgence (L/M/H/C)      │                 │
│              └──────────┬───────────────┘                 │
└─────────────────────────┼──────────────────────────────────┘
                          │
              Impact ≥ 8/10 ?
                    │   │
                    │   └─ Non → Stockage uniquement
                    │
                    └─ Oui → ALERTE CRITIQUE
                              │
                              ▼
                    ┌──────────────────────┐
                    │ Notification Client  │
                    │ (Email + Dashboard)  │
                    └──────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  MODULE 5: INTÉGRATION AUX PRÉVISIONS                      │
│                                                            │
│  Input: Forces/Faiblesses + Mouvements stratégiques       │
│         ▼                                                  │
│  ┌──────────────────────────────────────────┐            │
│  │ Recalibrage des Scénarios VIGIL          │            │
│  │ (Ajustement des probabilités)            │            │
│  └──────────────────────────────────────────┘            │
│         ▼                                                  │
│  ┌──────────────────────────────────────────┐            │
│  │ Génération de Recommandations            │            │
│  │ - Court terme (0-6 mois)                 │            │
│  │ - Moyen terme (6-18 mois)                │            │
│  │ - Long terme (18-36 mois)                │            │
│  └──────────────────────────────────────────┘            │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  MODULE 6: GARANTIE "ZÉRO HALLUCINATION"                  │
│  (Transversal - appliqué à tous les modules)              │
│                                                            │
│  Pour chaque donnée:                                      │
│  ✓ Source + URL                                           │
│  ✓ Date de collecte                                       │
│  ✓ Type (Fait / Estimation / Hypothèse)                  │
│  ✓ Score de confiance (0-100%)                           │
│  ✓ "Non disponible" si donnée introuvable                │
│                                                            │
│  Si confiance < 70% → Flag "Validation humaine requise"  │
└────────────────────────────────────────────────────────────┘
```

#### 3.1.3. Flux de Données et Communications

```
┌─────────────────────┐
│  APIs Externes      │
│  - Crunchbase       │───┐
│  - Pappers          │   │
│  - SimilarWeb       │   │
│  - SEMrush          │   │
└─────────────────────┘   │
                          │ HTTPS/REST
┌─────────────────────┐   │
│  Scraping Targets   │   │
│  - Trustpilot       │───┤
│  - LinkedIn         │   │
│  - News sites       │   │
│  - Company websites │   │
└─────────────────────┘   │
                          │
                          ▼
              ┌───────────────────────┐
              │  API Gateway          │
              │  - Rate limiting      │
              │  - Retry logic        │
              │  - Cost tracking      │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  Expert Concurrence   │
              │  (Python Workers)     │
              │  - Celery tasks       │
              │  - asyncio            │
              └───────────┬───────────┘
                          │
                ┌─────────┴─────────┐
                │                   │
                ▼                   ▼
    ┌──────────────────┐   ┌──────────────────┐
    │  Cache (Redis)   │   │  DB (PostgreSQL) │
    │  - API responses │   │  - Historique    │
    │  - TTL: 24h      │   │  - Métriques     │
    └──────────────────┘   └─────────┬────────┘
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │  API REST VIGIL      │
                          │  (FastAPI)           │
                          │  - GET /competitors  │
                          │  - GET /analysis     │
                          │  - POST /refresh     │
                          └──────────┬───────────┘
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │  Frontend Dashboard  │
                          │  (React/Vue)         │
                          └──────────────────────┘
```

#### 3.1.4. Stack Technique Détaillée

**Backend:**
- **Langage:** Python 3.11+
- **Framework API:** FastAPI (async, typage, auto-doc OpenAPI)
- **Orchestration:** Celery + Redis (tasks asynchrones)
- **HTTP Client:** httpx (async, HTTP/2)
- **Scraping:** Scrapy + BeautifulSoup4 + Playwright (pour sites JS)
- **Data Validation:** Pydantic v2 (validation + serialization)
- **ORM:** SQLAlchemy 2.0 (async mode)

**Data & Storage:**
- **Database:** PostgreSQL 15+ (avec extension TimescaleDB pour séries temporelles)
- **Cache:** Redis 7+ (cache API + queue Celery)
- **Object Storage:** S3-compatible (stockage rapports PDF, captures d'écran)

**Infrastructure:**
- **Containerisation:** Docker + Docker Compose (dev) / Kubernetes (prod)
- **Proxy Management:** Bright Data ou Oxylabs (rotation IP)
- **CI/CD:** GitHub Actions
- **Cloud Provider:** AWS (EC2, RDS, ElastiCache) ou GCP (recommandé pour coûts)

**Frontend:**
- **Framework:** React 18+ avec TypeScript
- **UI Library:** Tailwind CSS + shadcn/ui
- **Charts:** Recharts ou Apache ECharts
- **State Management:** Zustand ou React Query

**Monitoring:**
- **APM:** Datadog (recommandé) ou New Relic
- **Logs:** Loki + Grafana ou ELK Stack
- **Métriques:** Prometheus + Grafana
- **Alerting:** Alertmanager + PagerDuty

### 3.2. Technologies et Environnement
Voir section 3.1.4 pour le stack technique détaillé.

### 3.3. API REST - Spécifications des Endpoints

#### 3.3.1. API Publique VIGIL - Module Concurrence

**Base URL:** `https://api.vigil.io/v2`
**Authentification:** Bearer Token (JWT) dans header `Authorization`
**Format:** JSON (Content-Type: application/json)
**Rate Limiting:** 100 requêtes/minute par client

#### Endpoints Principaux

**1. POST /api/v2/competitors/identify**
Identifier les concurrents d'une entreprise.

**Request:**
```json
{
  "company_profile": {
    "name": "MonEntreprise SAS",
    "naf_code": "6201Z",
    "sector": "Développement logiciel",
    "products": ["SaaS Analytics", "BI Platform"],
    "geography": ["France", "Belgique"],
    "size": "50-200",
    "website": "https://example.com"
  },
  "options": {
    "max_competitors": 10,
    "include_indirect": true,
    "include_emerging": true,
    "min_relevance_score": 60
  }
}
```

**Response 200:**
```json
{
  "request_id": "uuid",
  "status": "completed",
  "execution_time_ms": 8420,
  "competitors": [
    {
      "id": "comp_abc123",
      "name": "Concurrent A",
      "website": "https://concurrenta.com",
      "type": "direct",
      "relevance_score": 92.5,
      "confidence_level": 87.3,
      "match_criteria": {
        "sector_match": true,
        "geography_match": true,
        "size_match": true,
        "product_similarity": 0.85
      },
      "sources": [
        {"type": "crunchbase", "url": "...", "date": "2025-11-15"},
        {"type": "societe.com", "url": "...", "date": "2025-11-16"}
      ]
    }
  ],
  "validation_required": false,
  "metadata": {
    "direct_competitors": 5,
    "indirect_competitors": 3,
    "emerging_competitors": 2
  }
}
```

**2. GET /api/v2/competitors/{competitor_id}/financial**
Récupérer l'analyse financière d'un concurrent.

**Query Parameters:**
- `years`: Années à inclure (ex: `2023,2024`)
- `include_benchmarks`: Comparer avec le client (true/false)

**Response 200:**
```json
{
  "competitor_id": "comp_abc123",
  "competitor_name": "Concurrent A",
  "financial_data": [
    {
      "year": 2024,
      "revenue": {
        "value": 12500000,
        "currency": "EUR",
        "type": "fact",
        "source": "https://pappers.fr/...",
        "collected_at": "2025-11-16T10:00:00Z",
        "freshness_days": 2
      },
      "growth_rate": {
        "value": 0.35,
        "type": "estimate",
        "source": "calculated",
        "confidence": 85.0
      },
      "ebitda": {
        "value": 2100000,
        "currency": "EUR",
        "type": "fact",
        "source": "https://pappers.fr/...",
        "collected_at": "2025-11-16T10:00:00Z"
      },
      "employees": {
        "value": 75,
        "type": "fact",
        "source": "https://linkedin.com/...",
        "collected_at": "2025-11-14T15:30:00Z",
        "freshness_days": 4
      }
    }
  ],
  "benchmarks": {
    "revenue_vs_client": {
      "comparison": "superior",
      "difference_percent": 25.3,
      "interpretation": "Le concurrent a un CA 25% supérieur, indiquant une meilleure pénétration marché"
    },
    "growth_vs_client": {
      "comparison": "equivalent",
      "difference_percent": 3.2,
      "interpretation": "Croissances comparables"
    }
  },
  "overall_confidence": 85.5
}
```

**3. GET /api/v2/competitors/{competitor_id}/marketing**
Récupérer l'analyse marketing d'un concurrent.

**Response 200:**
```json
{
  "competitor_id": "comp_abc123",
  "marketing_metrics": {
    "website_traffic": {
      "monthly_visits": 450000,
      "type": "estimate",
      "source": "SimilarWeb API",
      "collected_at": "2025-11-15T09:00:00Z",
      "confidence": 75.0
    },
    "top_keywords": [
      {"keyword": "analytics saas", "position": 3, "volume": 8100},
      {"keyword": "business intelligence", "position": 7, "volume": 12000}
    ],
    "social_media": {
      "linkedin_followers": 12500,
      "twitter_followers": 4300,
      "engagement_rate": 0.042
    },
    "reputation": {
      "trustpilot_score": 4.3,
      "trustpilot_reviews": 234,
      "g2_score": 4.5,
      "g2_reviews": 89
    },
    "pricing": {
      "model": "subscription",
      "starting_price": 49,
      "currency": "EUR",
      "billing_period": "monthly",
      "source": "scraped_website",
      "confidence": 95.0
    }
  },
  "positioning": {
    "value_proposition": "Plateforme analytics temps réel pour PME",
    "target_segments": ["PME 10-200 salariés", "Retail", "E-commerce"],
    "source": "scraped_website"
  }
}
```

**4. GET /api/v2/strategic-moves**
Récupérer les mouvements stratégiques récents de tous les concurrents.

**Query Parameters:**
- `since`: Date de début (ISO 8601, ex: `2025-11-01`)
- `min_impact`: Score d'impact minimum (0-10, défaut: 5)
- `competitor_ids`: Filtrer par concurrents (optionnel)
- `types`: Types d'événements (funding,acquisition,product_launch,key_hire,partnership)

**Response 200:**
```json
{
  "strategic_moves": [
    {
      "id": "move_xyz789",
      "competitor_id": "comp_abc123",
      "competitor_name": "Concurrent A",
      "type": "funding",
      "title": "Levée de fonds Série B de 15M€",
      "description": "Concurrent A annonce une levée de 15M€ menée par Accel Partners pour accélérer son expansion européenne",
      "impact_score": 9,
      "urgency": "critical",
      "detected_at": "2025-11-16T08:30:00Z",
      "event_date": "2025-11-15",
      "source": "https://techcrunch.com/...",
      "confidence": 95.0,
      "implications": [
        "Capacité d'investissement accrue en R&D",
        "Accélération du recrutement attendue",
        "Possible guerre des prix à venir"
      ]
    }
  ],
  "total_moves": 12,
  "critical_alerts": 3
}
```

**5. POST /api/v2/analysis/full**
Lancer une analyse concurrentielle complète (asynchrone).

**Request:**
```json
{
  "company_profile": { /* ... */ },
  "modules": ["identification", "financial", "marketing", "strategic"],
  "webhook_url": "https://client.com/webhook"
}
```

**Response 202 Accepted:**
```json
{
  "job_id": "job_12345",
  "status": "queued",
  "estimated_completion_time": "2025-11-16T11:45:00Z",
  "status_url": "/api/v2/jobs/job_12345"
}
```

**6. GET /api/v2/jobs/{job_id}**
Vérifier le statut d'une analyse asynchrone.

**Response 200:**
```json
{
  "job_id": "job_12345",
  "status": "completed",
  "progress": 100,
  "started_at": "2025-11-16T11:35:00Z",
  "completed_at": "2025-11-16T11:42:00Z",
  "result_url": "/api/v2/results/job_12345"
}
```

**Codes d'erreur:**
- `400 Bad Request`: Paramètres invalides
- `401 Unauthorized`: Token manquant ou invalide
- `403 Forbidden`: Quota dépassé
- `404 Not Found`: Ressource introuvable
- `422 Unprocessable Entity`: Validation échouée (détails dans response body)
- `429 Too Many Requests`: Rate limit dépassé
- `500 Internal Server Error`: Erreur serveur
- `503 Service Unavailable`: Service temporairement indisponible

#### 3.3.2. Webhooks

Les clients peuvent configurer des webhooks pour recevoir des notifications en temps réel.

**Événements supportés:**
- `strategic_move.detected`: Nouveau mouvement stratégique critique détecté
- `analysis.completed`: Analyse complète terminée
- `data.updated`: Données d'un concurrent mises à jour

**Payload exemple:**
```json
{
  "event": "strategic_move.detected",
  "timestamp": "2025-11-16T08:30:00Z",
  "data": {
    "move_id": "move_xyz789",
    "competitor_name": "Concurrent A",
    "impact_score": 9,
    "urgency": "critical",
    "summary": "Levée de fonds Série B de 15M€"
  }
}
```

### 3.4. Sources de Données (APIs & Scraping)
- **Entreprises :** Crunchbase, PitchBook, Societe.com, Infogreffe, LinkedIn Company Pages.
- **Finances :** Pappers API, Financial Modeling Prep API, Alpha Vantage API, Yahoo Finance API.
- **Marketing & SEO :** SimilarWeb API, SEMrush API, Ahrefs API.
- **Réputation :** Scraping de Trustpilot, G2, Capterra.
- **Actualités & Mouvements :** TechCrunch, Les Échos (via flux RSS ou APIs), Product Hunt, scraping des pages "News" des sites concurrents.

### 3.5. Modèles de Données et Formats d'Échange (JSON)
Des `dataclasses` Python seront utilisées pour représenter chaque entité. Les outputs de chaque module devront se conformer à un schéma JSON strict. Les exemples fournis dans le document de spécifications initiales serviront de référence.

#### Exemples de Structures de Données

**CompetitorProfile:**
```json
{
  "id": "uuid",
  "name": "string",
  "sector": "string",
  "naf_code": "string",
  "country": "string",
  "website": "url",
  "relevance_score": "float (0-100)",
  "confidence_level": "float (0-100)",
  "competitor_type": "direct|indirect|emerging",
  "identified_at": "datetime",
  "sources": ["url1", "url2"]
}
```

**FinancialMetrics:**
```json
{
  "competitor_id": "uuid",
  "year": "int",
  "revenue": {"value": "float", "currency": "EUR", "source": "url", "type": "fact|estimate"},
  "growth_rate": {"value": "float", "source": "url", "type": "fact|estimate"},
  "ebitda": {"value": "float", "currency": "EUR", "source": "url", "type": "fact|estimate"},
  "employees": {"value": "int", "source": "url", "type": "fact|estimate"},
  "funding": {"total_raised": "float", "currency": "EUR", "last_round": "Series A", "source": "url"},
  "collected_at": "datetime",
  "freshness_days": "int"
}
```

**StrategicMove:**
```json
{
  "id": "uuid",
  "competitor_id": "uuid",
  "type": "funding|acquisition|product_launch|key_hire|partnership",
  "title": "string",
  "description": "string",
  "impact_score": "int (0-10)",
  "urgency": "low|medium|high|critical",
  "detected_at": "datetime",
  "event_date": "datetime",
  "source": "url",
  "confidence": "float (0-100)"
}
```

### 3.6. Scalabilité et Performance

#### 3.6.1. Stratégie de Scalabilité

**Architecture Horizontale:**
- Utilisation de workers Celery pour distribuer la charge
- Auto-scaling des containers en fonction de la charge (Kubernetes HPA)
- Load balancer pour distribuer les requêtes API

**Scaling par Type de Tâche:**
| Type de Tâche | Workers Min | Workers Max | Scale Trigger |
|---------------|-------------|-------------|---------------|
| Identification concurrents | 2 | 10 | Queue > 50 jobs |
| Analyse financière | 3 | 15 | Queue > 100 jobs |
| Scraping | 5 | 20 | Queue > 200 jobs |
| Surveillance temps réel | 2 (permanent) | 5 | Event rate > 100/min |

**Optimisations Performance:**
1. **Caching Agressif:**
   - Cache Redis avec TTL intelligent (24h pour trafic web, 90j pour données financières)
   - Cache CDN pour les assets frontend
   - Mémoization des calculs coûteux (scoring, benchmarks)

2. **Batch Processing:**
   - Regroupement des requêtes API par fournisseur (ex: 10 entreprises → 1 appel Crunchbase)
   - Collecte des données en parallèle avec `asyncio.gather()`

3. **Database Optimization:**
   - Index sur les colonnes fréquemment requêtées (competitor_id, date, confidence_score)
   - Partitionnement des tables par date (TimescaleDB)
   - Utilisation de vues matérialisées pour les benchmarks pré-calculés

4. **Rate Limiting Intelligent:**
   - File d'attente avec priorités (clients B2B > B2C)
   - Throttling adaptatif basé sur les quotas API restants
   - Circuit breaker pour éviter de saturer les APIs externes en cas de panne

**Métriques de Performance Cibles:**
| Métrique | Cible Phase 1 (POC) | Cible Phase 2 (Prod) |
|----------|---------------------|----------------------|
| Temps d'identification (5 concurrents) | < 2 min | < 30 sec |
| Temps d'analyse financière (1 concurrent) | < 1 min | < 15 sec |
| Temps d'analyse complète (10 concurrents) | < 15 min | < 5 min |
| Throughput (analyses/heure) | 10 | 100 |
| Disponibilité (uptime) | 95% | 99.5% |

#### 3.6.2. Plan de Montée en Charge

**Scénario 1: 100 clients (M+12)**
- 100 analyses complètes/jour
- 10 000 surveillances temps réel/jour
- Infrastructure: 2 serveurs API + 5 workers
- Coût mensuel: 2 500€

**Scénario 2: 500 clients (M+18)**
- 500 analyses complètes/jour
- 50 000 surveillances temps réel/jour
- Infrastructure: 5 serveurs API + 20 workers + 2 DB replicas
- Coût mensuel: 8 000€

**Scénario 3: 1000+ clients (M+24)**
- 1000+ analyses complètes/jour
- 100 000+ surveillances temps réel/jour
- Infrastructure: Architecture Kubernetes auto-scalable
- Coût mensuel: 15 000€

### 3.7. Stratégie de Tests et Qualité

#### 3.7.1. Tests Unitaires et d'Intégration

**Coverage Cible:** 80% minimum

**Tests Unitaires (pytest):**
- Tests de chaque module (identification, analyse financière, marketing, mouvements)
- Mock des APIs externes pour éviter les coûts
- Tests des algorithmes de scoring et de ranking
- Tests de validation des données (Pydantic schemas)

**Exemple de structure:**
```
tests/
  unit/
    test_competitor_identification.py
    test_financial_analysis.py
    test_marketing_analysis.py
    test_strategic_moves.py
    test_scoring_algorithms.py
  integration/
    test_api_gateway.py
    test_scraping_pipeline.py
    test_database_operations.py
  e2e/
    test_full_analysis_flow.py
```

**Tests d'Intégration:**
- Tests des intégrations API réelles (sur environnement de test)
- Tests de la pipeline complète (bout en bout)
- Tests de la persistance en base de données
- Tests des webhooks

#### 3.7.2. Tests de Scraping

**Challenges spécifiques:**
- Sites web qui changent leur structure HTML
- Détection de bots et blocages
- Données manquantes ou incohérentes

**Stratégie:**
- Tests avec snapshots HTML archivés
- Tests de robustesse (HTML malformé, champs manquants)
- Monitoring continu du taux de succès en production
- Alertes si taux de succès < 80%

#### 3.7.3. Tests de Charge et de Performance

**Outils:** Locust ou K6

**Scénarios de Test:**
1. **Test de charge nominal:**
   - 50 utilisateurs concurrents
   - 100 requêtes/minute
   - Durée: 30 minutes
   - Objectif: 95% requêtes < 2 sec

2. **Test de pic (spike):**
   - Passage de 10 à 200 utilisateurs en 1 minute
   - Objectif: Pas de timeout, auto-scaling fonctionnel

3. **Test de stress:**
   - Augmentation progressive jusqu'à saturation
   - Identifier le point de rupture
   - Objectif: Dégradation gracieuse (pas de crash)

#### 3.7.4. Tests de Qualité des Données

**Protocole "Zéro Hallucination":**
- Audit mensuel sur échantillon de 100 analyses
- Vérification manuelle de 10 données par analyse
- Objectif: 0 hallucination détectée

**Tests de Confiance:**
- Vérification que chaque donnée a un score de confiance
- Vérification que chaque donnée a une source traçable
- Tests de régression pour éviter la dégradation de la qualité

**Tests de Fraîcheur:**
- Alerte si données > 120 jours pour > 30% des métriques
- Tests automatisés de l'actualisation des données

### 3.8. Budget et Coûts Estimés

#### 3.8.1. Coûts des APIs et Services Externes

**Phase 1 - POC (3 mois) - Pour 10 entreprises pilotes:**
| Service | Usage Estimé | Coût Mensuel | Coût Phase 1 (3 mois) |
|---------|--------------|--------------|----------------------|
| Crunchbase API | 500 requêtes/mois | 250€ | 750€ |
| Societe.com / Pappers API | 300 requêtes/mois | 150€ | 450€ |
| Financial Modeling Prep | 1000 requêtes/mois | 200€ | 600€ |
| SimilarWeb API | 200 requêtes/mois | 400€ | 1200€ |
| Scraping Infrastructure (Proxies) | 50GB bande passante | 100€ | 300€ |
| **Total APIs - Phase 1** | | **1100€/mois** | **3300€** |

**Phase 2 - Industrialisation (6 mois) - Pour 50-100 clients:**
| Service | Usage Estimé | Coût Mensuel | Coût Phase 2 (6 mois) |
|---------|--------------|--------------|----------------------|
| Crunchbase API (Plan Pro) | 5000 requêtes/mois | 1200€ | 7200€ |
| Pappers API (Plan Business) | 3000 requêtes/mois | 500€ | 3000€ |
| Financial APIs (Multi-sources) | 10000 requêtes/mois | 800€ | 4800€ |
| SimilarWeb / SEMrush API | 2000 requêtes/mois | 1500€ | 9000€ |
| Scraping Infrastructure | 500GB bande passante | 500€ | 3000€ |
| Base de données PostgreSQL (Managed) | 100GB stockage | 300€ | 1800€ |
| Serveurs de calcul (Cloud) | 4 vCPU, 16GB RAM | 400€ | 2400€ |
| **Total Infra - Phase 2** | | **5200€/mois** | **31200€** |

#### 3.8.2. Coûts de Développement

**Phase 1 - POC:**
- Développeur Backend Senior (3 mois, 50% temps) : 30 000€
- Développeur Data Engineer (3 mois, 50% temps) : 25 000€
- Designer UX/UI (1 mois, 20% temps) : 3 000€
- Chef de projet (3 mois, 20% temps) : 8 000€
- **Total Dev Phase 1:** 66 000€

**Phase 2 - Industrialisation:**
- Équipe développement (6 mois, 2 devs temps plein) : 120 000€
- Architecte Cloud (6 mois, 30% temps) : 25 000€
- Designer UX/UI (2 mois, 50% temps) : 10 000€
- DevOps Engineer (3 mois, 50% temps) : 20 000€
- QA/Testeur (3 mois, 100% temps) : 30 000€
- Chef de projet (6 mois, 50% temps) : 30 000€
- **Total Dev Phase 2:** 235 000€

#### 3.8.3. Budget Total et ROI

**Investissement Total:**
- Phase 1 (POC): 69 300€ (Dev + APIs)
- Phase 2 (Industrialisation): 266 200€ (Dev + Infra)
- **Total Phase 1+2:** 335 500€

**Modèle de Revenus Estimé:**
- Prix B2C: 500€/mois par client
- Prix B2B: 3000€/mois par client
- Objectif: 40 clients B2C + 5 clients B2B à M+24
- **Revenus Mensuels Estimés (M+24):** (40 × 500€) + (5 × 3000€) = 35 000€/mois
- **Revenus Annuels (M+24):** 420 000€/an

**Breakeven:**
- Avec un coût opérationnel récurrent de 6 000€/mois (APIs + Infra)
- Breakeven atteint avec: 12 clients B2C OU 2 clients B2B
- **Breakeven estimé:** M+9 après lancement commercial (M+12 après début projet)
- **ROI à M+24:** +250% (investissement de 335k€, revenus cumulés de 840k€ sur 2 ans)

### 3.9. Sécurité et Conformité RGPD

#### 3.9.1. Classification des Données

**Données Publiques (Niveau 1 - Vert):**
- Informations d'entreprises (raison sociale, SIREN, adresse)
- Données financières publiques (comptes déposés)
- Contenus web publics (tarifs, proposition de valeur)
- **Traitement:** Collecte autorisée, stockage sans chiffrement requis

**Données Semi-Sensibles (Niveau 2 - Orange):**
- Estimations financières calculées
- Données de trafic web agrégées
- Profils LinkedIn d'entreprises
- **Traitement:** Stockage chiffré au repos, accès tracé

**Données Sensibles (Niveau 3 - Rouge):**
- Données personnelles de dirigeants (noms, rôles)
- Informations confidentielles client (stratégie interne)
- **Traitement:** Chiffrement end-to-end, pseudonymisation, durée de rétention limitée (2 ans)

#### 3.9.2. Conformité RGPD

**Article 6 (Base légale):**
- Intérêt légitime (Article 6.1.f) pour la collecte de données publiques d'entreprises
- Consentement explicite des clients VIGIL pour le traitement de leurs données stratégiques

**Article 13-14 (Transparence):**
- Mention dans les CGU de VIGIL des sources de données utilisées
- Droit d'accès et de rectification pour les entreprises analysées (formulaire dédié)

**Article 17 (Droit à l'effacement):**
- Mécanisme de demande de suppression pour les concurrents analysés
- Délai de traitement: 30 jours

**Article 32 (Sécurité):**
- Chiffrement AES-256 pour les données au repos
- TLS 1.3 pour les données en transit
- Authentification multi-facteurs (MFA) pour les accès administrateurs
- Logs d'audit de tous les accès aux données sensibles

#### 3.9.3. Pratiques de Scraping Éthique

**Respect des robots.txt:**
- Parser systématique du fichier robots.txt avant tout scraping
- Respect des directives User-agent et Crawl-delay

**Rate Limiting:**
- Maximum 1 requête par seconde par domaine
- Pauses aléatoires (2-5 secondes) entre les requêtes
- Utilisation d'un User-Agent transparent identifiant VIGIL

**Détection et Réaction:**
- Si blocage détecté (403/429): arrêt immédiat et backoff exponentiel (1h, 4h, 24h)
- Rotation de proxies résidentiels pour éviter les bans IP
- Monitoring des erreurs: si taux d'erreur > 10%, alerte et suspension du scraper

**Stockage et Rétention:**
- Conservation des données scrappées: 90 jours (actualisation trimestrielle)
- Purge automatique des données obsolètes
- Logs de scraping conservés 1 an pour audit

#### 3.9.4. Sécurité de l'Infrastructure

**Contrôle d'Accès:**
- RBAC (Role-Based Access Control) avec 4 niveaux:
  - Admin: Accès complet
  - Analyste: Lecture seule des données concurrents
  - Client: Accès uniquement à ses propres analyses
  - API: Accès programmatique avec tokens révocables

**Isolation des Environnements:**
- Séparation stricte Dev / Staging / Production
- Données de production anonymisées en dev/staging
- Pas de données clients en environnement de développement

**Backup et Disaster Recovery:**
- Backup incrémental quotidien (rétention 30 jours)
- Backup complet hebdomadaire (rétention 12 semaines)
- RPO (Recovery Point Objective): 24h
- RTO (Recovery Time Objective): 4h

**Audit et Compliance:**
- Audit de sécurité externe annuel
- Pentesting semestriel
- Rapport de conformité RGPD trimestriel

### 3.10. Monitoring et Observabilité

#### 3.10.1. Métriques Applicatives (APM)

**Performance:**
- `competitor_analysis_duration_seconds`: Temps d'exécution complet d'une analyse concurrentielle (p50, p95, p99)
- `module_execution_time_seconds{module="identification|financial|marketing|strategic"}`: Temps par module
- `api_call_duration_seconds{provider="crunchbase|pappers|similarweb"}`: Latence des APIs externes
- **SLA:** p95 < 10 minutes pour une analyse complète

**Fiabilité:**
- `competitor_identification_accuracy_rate`: Taux de précision des concurrents identifiés (feedback clients)
- `data_freshness_days{metric="revenue|traffic|funding"}`: Fraîcheur des données (moyenne)
- `hallucination_detection_count`: Nombre d'hallucinations détectées (objectif: 0)
- `confidence_score_distribution`: Distribution des scores de confiance

**Volumétrie:**
- `analyses_completed_total`: Nombre d'analyses complétées
- `competitors_tracked_total`: Nombre total de concurrents suivis
- `strategic_moves_detected_total{urgency="low|medium|high|critical"}`: Mouvements stratégiques détectés

#### 3.10.2. Métriques Infrastructure

**Scraping:**
- `scraping_success_rate{source="trustpilot|linkedin|company_website"}`: Taux de succès par source
- `scraping_blocked_total{reason="403|429|timeout|robots_txt"}`: Nombre de blocages
- `proxy_rotation_count`: Nombre de rotations de proxies

**APIs Externes:**
- `api_quota_usage_percent{provider="crunchbase|pappers"}`: Utilisation des quotas API
- `api_error_rate{provider="..."}`: Taux d'erreur par fournisseur
- `api_cost_estimation_euros`: Coût estimé des appels API en temps réel

**Base de Données:**
- `db_query_duration_seconds{query_type="read|write"}`: Performance des requêtes
- `db_connection_pool_usage`: Utilisation du pool de connexions
- `db_storage_size_gb`: Taille de la base de données

#### 3.10.3. Alerting

**Alertes Critiques (P1 - Intervention immédiate):**
- Taux d'erreur global > 10% sur 5 minutes
- Aucune analyse complétée depuis 1 heure
- Hallucination détectée (score de confiance incohérent)
- Coût API mensuel dépasse le budget de 20%
- **Canal:** SMS + Email + PagerDuty

**Alertes Importantes (P2 - Intervention sous 1h):**
- Taux de blocage scraping > 30% sur 1 heure
- Performance p95 > 15 minutes
- Quota API atteint à 90%
- **Canal:** Email + Slack

**Alertes Mineures (P3 - Intervention sous 24h):**
- Données obsolètes (freshness > 120 jours) pour > 20% des concurrents
- Taux de validation humaine requis > 40%
- **Canal:** Email quotidien groupé

#### 3.10.4. Dashboards Opérationnels

**Dashboard "Santé Système":**
- Vue temps réel des analyses en cours
- Graphique des temps de réponse (24h)
- Taux d'erreur par module
- Statut des APIs externes (up/down)

**Dashboard "Qualité des Données":**
- Distribution des scores de confiance
- Taux de fraîcheur des données
- Top 10 des sources d'erreurs de scraping
- Évolution du taux de validation humaine requise

**Dashboard "Coûts":**
- Évolution des coûts API (jour/semaine/mois)
- Répartition par fournisseur
- Projection du coût mensuel
- Alerte si dépassement budgétaire

**Outils:**
- **APM:** Datadog ou New Relic
- **Logs:** ELK Stack (Elasticsearch, Logstash, Kibana) ou Loki
- **Métriques:** Prometheus + Grafana
- **Alerting:** Alertmanager + PagerDuty

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

### 4.4. Documentation et Formation

#### 4.4.1. Documentation Technique

**Documentation du Code (Phase 1 & 2):**
- **README.md complet:**
  - Architecture du projet
  - Prérequis et installation
  - Variables d'environnement
  - Commandes de lancement (dev, test, prod)
  - Guide de contribution

- **Documentation API (OpenAPI/Swagger):**
  - Auto-générée via FastAPI
  - Spécifications complètes de tous les endpoints
  - Exemples de requêtes/réponses
  - Codes d'erreur et leur signification
  - Guide d'authentification

- **Documentation Architecture:**
  - Diagrammes d'architecture (C4 model)
  - Schéma de base de données (ERD)
  - Flux de données et intégrations
  - Décisions d'architecture (ADR - Architecture Decision Records)

- **Guide du Développeur:**
  - Setup de l'environnement de développement
  - Standards de code (PEP8, linting avec ruff/black)
  - Guide des tests (comment écrire et lancer les tests)
  - Workflow Git et revue de code
  - Debugging et troubleshooting

**Outil recommandé:** MkDocs ou Docusaurus (hébergement sur Read the Docs ou GitHub Pages)

#### 4.4.2. Documentation Utilisateur

**Guide Utilisateur Complet (Phase 2):**
1. **Guide de Démarrage Rapide (Quick Start):**
   - Connexion à VIGIL
   - Configuration du profil entreprise
   - Lancement de la première analyse concurrentielle
   - Interprétation des résultats

2. **Manuel Utilisateur Détaillé:**
   - Navigation dans le dashboard "Concurrence"
   - Comprendre les scores de pertinence et de confiance
   - Interpréter les benchmarks financiers et marketing
   - Configurer les alertes personnalisées
   - Exporter les rapports (PDF, CSV)

3. **FAQ (Foire Aux Questions):**
   - "Pourquoi certains concurrents ont un score de confiance faible ?"
   - "Comment sont calculés les benchmarks ?"
   - "Que signifie 'Donnée Non Disponible' ?"
   - "À quelle fréquence les données sont-elles mises à jour ?"
   - "Comment ajouter manuellement un concurrent ?"

4. **Glossaire:**
   - Définitions des termes techniques (Score de pertinence, Confiance, EBITDA, etc.)
   - Explication des types de concurrents (Direct, Indirect, Émergent)
   - Catégories de mouvements stratégiques

**Format:** Base de connaissances en ligne (Notion, Confluence ou GitBook)

#### 4.4.3. Vidéos Tutorielles

**Contenu Vidéo (Phase 2):**
- **Vidéo 1 (5 min):** Introduction à VIGIL Expert Concurrence
- **Vidéo 2 (8 min):** Analyser vos concurrents - Tutoriel complet
- **Vidéo 3 (4 min):** Comprendre les alertes stratégiques critiques
- **Vidéo 4 (6 min):** Exporter et partager vos analyses
- **Vidéo 5 (10 min):** Cas d'usage : PME SaaS vs Concurrents

**Plateforme:** YouTube (chaîne VIGIL) + embed dans le dashboard

#### 4.4.4. Formation des Équipes Clients

**Programme de Formation B2B (Phase 2):**

**Formation Initiale (2h - en ligne ou présentiel):**
1. **Module 1 (30 min):** Présentation de VIGIL et du module Concurrence
   - Vision et objectifs
   - Différenciation vs outils traditionnels
   - Garantie "Zéro Hallucination"

2. **Module 2 (45 min):** Démonstration pratique
   - Configuration du profil entreprise
   - Lancement d'une analyse
   - Navigation dans le dashboard
   - Lecture et interprétation des résultats

3. **Module 3 (30 min):** Cas d'usage et bonnes pratiques
   - Comment intégrer VIGIL dans votre processus stratégique
   - Exemples d'actions déclenchées suite à une alerte
   - Collaboration en équipe (partage de rapports)

4. **Module 4 (15 min):** Q&A et certification
   - Questions des participants
   - Quiz de validation des connaissances
   - Remise de certificat de formation

**Supports de Formation:**
- Slides de présentation (PowerPoint/Google Slides)
- Environnement de démo avec données fictives
- Checklist de bonnes pratiques
- Fiche mémo (cheat sheet) imprimable

**Formation Continue:**
- Webinaires trimestriels (1h) sur les nouvelles fonctionnalités
- Newsletter mensuelle avec tips & tricks
- Sessions de Q&A mensuelles (office hours)

#### 4.4.5. Support Utilisateur

**Niveaux de Support:**

**Tier 1 - Self-Service (24/7):**
- Base de connaissances en ligne
- FAQ interactives
- Chatbot IA pour réponses basiques
- Tutoriels vidéo

**Tier 2 - Support Email (Réponse sous 24h):**
- Email: support@vigil.io
- Formulaire de contact dans le dashboard
- Tickets classés par priorité (Low, Medium, High, Critical)

**Tier 3 - Support Premium (B2B uniquement):**
- Account Manager dédié
- Support téléphonique (heures ouvrables)
- Temps de réponse: 4h pour Critical, 24h pour High
- Revue de compte trimestrielle

**Outils de Support:**
- Ticketing: Zendesk ou Freshdesk
- Chat en direct: Intercom ou Crisp
- Monitoring de satisfaction: CSAT et NPS après chaque interaction

#### 4.4.6. Release Notes et Communication

**Gestion des Releases:**
- **Changelog public:** Toutes les nouvelles fonctionnalités, améliorations et corrections de bugs
- **Release notes détaillées:** Envoyées par email avant chaque mise à jour majeure
- **Roadmap publique:** Trello ou ProductBoard pour transparence sur les fonctionnalités à venir
- **Beta testing:** Programme "early access" pour tester les nouvelles features

**Canaux de Communication:**
- Blog VIGIL (Medium ou site web dédié)
- Newsletter mensuelle
- Notifications in-app pour les changements importants
- Webinaires de lancement pour les fonctionnalités majeures

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
