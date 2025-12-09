# 📚 Next.js Docs Scraper v1.3.0

> **Extracteur automatique et intelligent de documentation Next.js** - Clone le dépôt officiel, extrait tous les fichiers MDX et génère un dump JSON structuré pour analyse, recherche et intégration.

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Last Updated](https://img.shields.io/badge/Last%20Update-v16.0.8-orange)

---

## 📋 Table des Matières

1. [🎯 Vision & Contexte](#-vision--contexte)
2. [✨ Fonctionnalités Clés](#-fonctionnalités-clés)
3. [🏗️ Architecture](#-architecture)
4. [🛠️ Stack Technique](#-stack-technique)
5. [📂 Structure du Projet](#-structure-du-projet)
6. [🚀 Démarrage Rapide](#-démarrage-rapide)
7. [⚙️ Configuration](#-configuration)
8. [📊 Output Format](#-output-format)
9. [🔄 Workflow de Déploiement](#-workflow-de-déploiement)
10. [📚 Documentation Complémentaire](#-documentation-complémentaire)
11. [✅ Bonnes Pratiques](#-bonnes-pratiques)
12. [📄 Licence](#-licence)

---

## 🎯 Vision & Contexte

### 🌟 Objectif Stratégique

**Next.js Docs Scraper** est un outil **production-ready** conçu pour:

- ✅ **Automatiser l'extraction** de la documentation officielle Next.js depuis le dépôt GitHub
- ✅ **Détecter intelligemment** la dernière version stable (v16.0.8 actuellement)
- ✅ **Parser tous les fichiers MDX** du répertoire `/docs` avec précision
- ✅ **Générer un dump JSON structuré** exploitable pour:
  - 🔍 Moteurs de recherche documentaire
  - 🤖 Systèmes d'IA et LLMs
  - 📱 Applications mobiles et web
  - 📊 Analyses et statistiques

### 🎯 Cas d'Utilisation

| Cas d'Usage | Description |
|---|---|
| **Recherche Documentaire** | Créer un moteur de recherche full-text sur la doc Next.js |
| **Intégration IA** | Fournir du context à des LLMs pour support technique |
| **Migration Documentation** | Exporter docs Next.js vers d'autres formats (Markdown, HTML) |
| **Analyse Documentaire** | Étudier l'évolution de la doc Next.js entre versions |
| **Sauvegarde Offline** | Archive complète de la documentation pour usage hors-ligne |

### 🎨 Principes de Conception

| Principe | Implémentation |
|---|---|
| **Automatisation** | Détection auto version stable, pas de config manuelle |
| **Fiabilité** | Gestion robuste d'erreurs, logging détaillé, vérifications pré-vol |
| **Performance** | Traitement parallélisable, output JSON optimisé |
| **Maintenabilité** | Code clairement documenté, structure modulaire |
| **Reproductibilité** | Commits specifiques, hash de version dans les métadonnées |

---

## ✨ Fonctionnalités Clés

### 🤖 Détection Automatique de Version

```python
# Aucune configuration manuelle nécessaire!
get_latest_stable_version()  # Retourne: v16.0.8
```

**Logique:**
- Requête en temps réel vers `git ls-remote` sur le repo officiel
- Filtre automatique: ignore `canary`, `alpha`, `beta`, `rc`, `dev`, `experimental`
- Tri sémantique des versions (X.Y.Z) → retourne la plus récente
- Fallback intelligent si erreur

### 🔄 Clonage Intelligent

```bash
$ git clone --depth 1 --branch v16.0.8 https://github.com/vercel/next.js.git nextjs_repo_temp
```

- Clone peu profond (optimisé bande passante)
- Commit hash enregistré: `817ee56da939545d4b77cc54542f4c45a524e60a`
- Nettoyage automatique des états corrompus (`git reset --hard`, `git clean -fd`)

### 📄 Extraction MDX Complète

```
📂 docs/
├── 📄 01-app/
├── 📄 02-pages/
├── 📄 03-architecture/
└── 📄 04-community/

↓ [Parse avec python-frontmatter]

✅ 375 fichiers extraits
✅ Frontmatter (metadata) capturé
✅ Contenu pur en texte plain
```

### 💾 Export JSON Structuré

```json
{
  "pages": [
    {
      "id": 1,
      "url": "https://nextjs.org/docs/docs/01-app/...",
      "title": "...",
      "content": "...",
      "metadata": { "description": "...", "tags": [...] }
    },
    // ... 375 pages
  ],
  "statistics": {
    "source_version": "v16.0.8",
    "source_commit_hash": "817ee56da939545d4b77cc54542f4c45a524e60a",
    "total_documents_extracted": 375,
    "execution_time_seconds": 218.49,
    "timestamp": "2025-12-09T10:30:45Z"
  }
}
```

### 📝 Logging Détaillé

```
mission_log_nextjs.log  (Archivé après chaque exécution)
├── ✓ Détection versions
├── ✓ Configuration chargée
├── ✓ Clonage réussi
├── ✓ Parsing fichiers
├── ✓ Génération JSON
└── ✓ Mission terminée en 218.49s
```

---

## 🏗️ Architecture

### Diagramme de Flux

```
┌─────────────────────────────────────────────────┐
│  START: main.py exécuté                         │
└────────────────────┬────────────────────────────┘
                     │
        ┌────────────▼────────────────┐
        │  1. Load Config             │
        │  (config.json)              │
        └────────────────┬────────────┘
                         │
        ┌────────────────▼────────────────┐
        │  2. Get Latest Stable Version  │
        │  (git ls-remote + semver)      │
        │  → v16.0.8                     │
        └────────────────┬────────────────┘
                         │
        ┌────────────────▼────────────────────┐
        │  3. Clone Repository                │
        │  (git clone --branch v16.0.8)       │
        │  nextjs_repo_temp/                  │
        └────────────────┬────────────────────┘
                         │
        ┌────────────────▼──────────────────────┐
        │  4. Traverse Docs Directory           │
        │  Find all *.mdx files (375 found)     │
        └────────────────┬──────────────────────┘
                         │
        ┌────────────────▼──────────────────────┐
        │  5. Parse MDX + Extract Frontmatter   │
        │  (python-frontmatter)                 │
        └────────────────┬──────────────────────┘
                         │
        ┌────────────────▼──────────────────────┐
        │  6. Construct JSON                    │
        │  ├─ pages array (375 items)           │
        │  └─ statistics block                  │
        └────────────────┬──────────────────────┘
                         │
        ┌────────────────▼──────────────────────┐
        │  7. Write nextjs_docs_dump_v1.json    │
        │  (~5-8 MB file)                       │
        └────────────────┬──────────────────────┘
                         │
        ┌────────────────▼──────────────────────┐
        │  8. Cleanup & Log                     │
        │  ├─ mission_log_nextjs.log            │
        │  └─ Total: 218.49 seconds             │
        └──────────────┬─────────────────────────┘
                       │
            ┌──────────▼──────────┐
            │  SUCCESS ✓          │
            │  Output ready       │
            └─────────────────────┘
```

### Modules Clés

| Module | Responsabilité |
|---|---|
| `load_config()` | Charge et valide `config.json` |
| `get_latest_stable_version()` | Détection auto version stable (semver) |
| `setup_logging()` | Configure logging file + console |
| `clone_repo()` | Clone Git avec gestion erreurs |
| `parse_mdx_files()` | Itère et parse tous les `.mdx` |
| `extract_frontmatter()` | Extrait metadata avec python-frontmatter |
| `generate_json()` | Construit structure JSON finale |

---

## 🛠️ Stack Technique

### Langage & Runtime

| Component | Version | Purpose |
|---|---|---|
| **Python** | 3.8+ | Langage principal |
| **pip** | Latest | Package manager |
| **venv** | Built-in | Virtual environment |

### Dépendances Principales

```toml
[dependencies]
python-frontmatter = "*"          # Parser YAML/Markdown frontmatter
packaging = "*"                    # Semantic versioning (X.Y.Z)
```

### Outils Systèmes

| Outil | Usage |
|---|---|
| **git** | Clonage repo, tags, commits |
| **bash/sh** | Exécution scripts système |
| **grep** | Recherche/filtrage (log parsing) |

### Format de Données

| Format | Usage |
|---|---|
| **JSON** | Output principal (`nextjs_docs_dump_v1.json`) |
| **YAML** | Frontmatter dans `.mdx` files |
| **Markdown** | Contenu des fichiers MDX |
| **Plain Text** | Contenu strippé (dans JSON) |

---

## 📂 Structure du Projet

```
Nextjs_docs_Scraper/
├── 📄 main.py                          # Script principal (287 lignes)
│   ├── setup_logging()
│   ├── load_config()
│   ├── get_latest_stable_version()     # ⭐ Cœur intelligent
│   ├── clone_repo()
│   ├── traverse_docs()
│   ├── parse_mdx_files()
│   └── generate_json()
│
├── 📄 config.json                      # Configuration (répertoires, URLs)
│   ├── repo_url: "https://github.com/vercel/next.js.git"
│   ├── docs_path: "docs"
│   ├── temp_clone_dir: "nextjs_repo_temp"
│   └── output_filename: "nextjs_docs_dump_v1.json"
│
├── 📄 requirements.txt                 # Dépendances Python
│   ├── python-frontmatter
│   └── packaging
│
├── 📄 README.md                        # Cette documentation
│
├── 📄 .gitignore                       # Exclusions Git
│   ├── nextjs_repo_temp/               # Dossier clone (temporaire)
│   ├── *.json (sauf config)            # Outputs (trop volumineux)
│   ├── mission_log*.log                # Logs
│   └── venv/                           # Virtual environment
│
├── 📄 nextjs_docs_dump_v1.json         # OUTPUT: Dump documentaire (5-8 MB)
│   └── Format: {"pages": [...], "statistics": {...}}
│
├── 📄 mission_log_nextjs.log           # OUTPUT: Logs exécution détaillés
│   └── Généré après chaque run
│
└── 📂 nextjs_repo_temp/                # TEMPORAIRE: Clone du repo
    └── Supprimé/Régénéré à chaque exécution
    ├── docs/
    │   ├── 01-app/
    │   ├── 02-pages/
    │   ├── 03-architecture/
    │   └── 04-community/
    ├── package.json
    ├── lerna.json
    └── ... (autres fichiers)
```

### Fichiers Clés Expliqués

**`main.py`** (287 lignes)
- Cœur du scraper
- Logique auto-détection version
- Orchestration complète du pipeline

**`config.json`**
- Centralisé toute la configuration
- URLs, chemins, extensions fichiers
- Modifiable sans toucher au code

**`.gitignore`**
- Ignore clone temporaire (trop volumineux)
- Ignore JSON output (5-8 MB)
- Ignore environnement local (venv)

---

## 🚀 Démarrage Rapide

### Prérequis

```bash
# Vérifier Python
python3 --version              # Doit être >= 3.8

# Vérifier Git
git --version                  # Doit être installé

# Vérifier pip
pip3 --version                 # Doit être installé
```

### Installation

```bash
# 1. Cloner ce repository
git clone git@github.com:jackjosias/NEXTJS_DOCS_SCRAPER_STABLE_VERSION.git
cd NEXTJS_DOCS_SCRAPER_STABLE_VERSION

# 2. Créer et activer virtual environment
python3 -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

### Exécution

```bash
# Mode standard (détection auto version v16.0.8)
python3 main.py

# ✅ Résultat:
# - nextjs_docs_dump_v1.json (généré)
# - mission_log_nextjs.log (généré)
# - nextjs_repo_temp/ (crée puis nettoyé)
```

### Output

```
✓ Dernière version stable détectée : v16.0.8
✓ Clonage du dépôt...
✓ 375 fichiers MDX trouvés
✓ Parsing et extraction complète
✓ JSON généré: nextjs_docs_dump_v1.json (6.2 MB)
✓ SUCCÈS FINAL ! Execution: 218.49 secondes
```

### Vérification de l'Output

```bash
# Vérifier le JSON généré
ls -lh nextjs_docs_dump_v1.json   # Doit être ~5-8 MB

# Vérifier le nombre de pages extraites
grep -o '"id":' nextjs_docs_dump_v1.json | wc -l   # Doit être ~375

# Vérifier la version source
grep "source_commit_hash" nextjs_docs_dump_v1.json  # Doit être 817ee56...
```

---

## ⚙️ Configuration

### Fichier `config.json`

```json
{
  "repo_url": "https://github.com/vercel/next.js.git",
  "branch": "main",
  "docs_path": "docs",
  "temp_clone_dir": "nextjs_repo_temp",
  "output_filename": "nextjs_docs_dump_v1.json",
  "file_extensions": [".mdx"]
}
```

**Paramètres:**

| Clé | Description | Exemple |
|---|---|---|
| `repo_url` | URL du dépôt Git | `https://github.com/vercel/next.js.git` |
| `branch` | Branche par défaut | `main` (remplacée auto par tag version) |
| `docs_path` | Chemin du dossier docs | `docs` |
| `temp_clone_dir` | Dossier clone temporaire | `nextjs_repo_temp` |
| `output_filename` | Nom du JSON final | `nextjs_docs_dump_v1.json` |
| `file_extensions` | Extensions à parser | `[".mdx"]` |

### Variables d'Environnement (Optionnelles)

```bash
# Aucune variable d'env obligatoire
# Toute la config passe par config.json

# Pour debug avancé (futur):
export DEBUG_SCRAPER=true       # (Non implémenté actuellement)
export LOG_LEVEL=DEBUG          # (Non implémenté actuellement)
```

### Modifier le Comportement

**Changer la version ciblée** (manuel):
```python
# Dans main.py, ligne ~75, remplacer:
version_to_use = get_latest_stable_version()  # Auto

# Par:
version_to_use = "v15.1.0"  # Manual
```

**Changer le répertoire output:**
```json
// config.json
{
  "output_filename": "my_custom_dump.json"
}
```

---

## 📊 Output Format

### Structure JSON Complète

```json
{
  "pages": [
    {
      "id": 1,
      "url": "https://nextjs.org/docs/docs/01-app/01-building-your-application/01-routing",
      "title": "Routing",
      "content": "# Routing\n\nThe page...",
      "metadata": {
        "description": "...",
        "tags": ["routing", "navigation"],
        "sidebar_position": 1
      }
    },
    // ... (items 2-375)
  ],
  "statistics": {
    "source_version": "v16.0.8",
    "source_commit_hash": "817ee56da939545d4b77cc54542f4c45a524e60a",
    "source_timestamp": "2025-12-09T10:30:45Z",
    "total_documents_extracted": 375,
    "total_content_bytes": 6241234,
    "execution_time_seconds": 218.49,
    "scraper_version": "1.3.0",
    "python_version": "3.12.1"
  }
}
```

### Champs par Page

| Champ | Type | Description |
|---|---|---|
| `id` | Integer | ID unique (0-375) |
| `url` | String | URL NextJS docs originale |
| `title` | String | Titre de la page |
| `content` | String | Contenu markdown/text pur |
| `metadata` | Object | Frontmatter YAML parsé |

### Bloc Statistiques

| Clé | Description |
|---|---|
| `source_version` | Version cible (ex: v16.0.8) |
| `source_commit_hash` | Commit Git exact utilisé |
| `source_timestamp` | Date/heure de l'extraction |
| `total_documents_extracted` | Nombre total pages |
| `total_content_bytes` | Taille totale du contenu |
| `execution_time_seconds` | Durée totale exécution |
| `scraper_version` | Version du scraper |
| `python_version` | Python utilisé |

### Tailles Typiques

```
Python script:        ~10 KB
Config:              ~1 KB
JSON output:         ~6-8 MB (375 pages × ~20 KB avg)
Log file:            ~100-200 KB
Total:               ~6-8 MB
```

---

## 🔄 Workflow de Déploiement

### Pour Déployer sur GitHub

```bash
# 1. Initialiser Git (si pas déjà fait)
cd NEXTJS_DOCS_SCRAPER_STABLE_VERSION
git init

# 2. Configurer utilisateur Git
git config user.name "Jack Josias"
git config user.email "jackjosias@github.com"

# 3. Ajouter les fichiers
git add main.py requirements.txt config.json .gitignore README.md

# 4. Commit initial
git commit -m "Initial commit: Next.js v16.0.8 docs scraper with auto-version detection

- Automatic stable version detection (v16.0.8)
- Full MDX parsing (375 files)
- Structured JSON output with metadata
- Comprehensive logging
- Production-ready error handling"

# 5. Créer branche principale
git branch -M main

# 6. Ajouter remote
git remote add origin git@github.com:jackjosias/NEXTJS_DOCS_SCRAPER_STABLE_VERSION.git

# 7. Push vers GitHub
git push -u origin main
```

### Vérifier le Déploiement

```bash
# Vérifier remote est configuré
git remote -v
# origin	git@github.com:jackjosias/NEXTJS_DOCS_SCRAPER_STABLE_VERSION.git (fetch)
# origin	git@github.com:jackjosias/NEXTJS_DOCS_SCRAPER_STABLE_VERSION.git (push)

# Vérifier l'historique
git log --oneline
# [Latest commit] Initial commit: Next.js v16.0.8 docs scraper...

# Vérifier les fichiers poussés
git ls-tree -r HEAD
```

### Mise à Jour Future

```bash
# Quand vous mettez à jour le code:
git add .
git commit -m "feat: [description changement]"
git push origin main

# Format commit recommandé:
# feat: New feature
# fix: Bug fix
# docs: Documentation update
# refactor: Code reorganization
# perf: Performance improvement
```

---

## 📚 Documentation Complémentaire

### Fichiers de Référence

| Fichier | Contenu |
|---|---|
| `main.py` | Source code complet (~287 lignes) |
| `config.json` | Configuration centralisée |
| `requirements.txt` | Dépendances exactes |
| `mission_log_nextjs.log` | Logs d'exécution (généré) |

### Ressources Externes

- **[Next.js Official Repository](https://github.com/vercel/next.js)** - Repo source
- **[Next.js Releases](https://github.com/vercel/next.js/releases)** - Changelog version
- **[python-frontmatter Docs](https://python-frontmatter.readthedocs.io/)** - Parser YAML
- **[packaging Library](https://packaging.pydata.org/)** - Versioning sémantique

### Debugging & Troubleshooting

**Le JSON n'est pas généré:**
```bash
# 1. Vérifier les logs
cat mission_log_nextjs.log

# 2. Vérifier Git est installé
git --version

# 3. Vérifier perms dossier
ls -la nextjs_repo_temp/

# 4. Vérifier espace disque
df -h
```

**Git clone échoue:**
```bash
# 1. Tester la connexion
git ls-remote https://github.com/vercel/next.js.git

# 2. Nettoyer repo corrompu
rm -rf nextjs_repo_temp/
python3 main.py
```

**Parsing échoue:**
```bash
# 1. Vérifier python-frontmatter
python3 -c "import frontmatter; print(frontmatter.__version__)"

# 2. Vérifier fichiers MDX existent
find nextjs_repo_temp/docs -name "*.mdx" | head
```

---

## ✅ Bonnes Pratiques

### Avant d'Exécuter

- ✅ Vérifier Git est installé: `git --version`
- ✅ Vérifier Python 3.8+: `python3 --version`
- ✅ Vérifier espace disque (~1-2 GB pour clone + output)
- ✅ Vérifier connexion Internet stable (clone ~100 MB repo)
- ✅ Vérifier config.json valide: `python3 -m json.tool config.json`

### Pendant l'Exécution

- ✅ Ne pas interrompre avec Ctrl+C (peut corrompre l'état)
- ✅ Monitorer mission_log_nextjs.log en temps réel: `tail -f mission_log_nextjs.log`
- ✅ Vérifier l'utilisation CPU/RAM ne dépasse pas limite système

### Après l'Exécution

- ✅ Vérifier nextjs_docs_dump_v1.json n'est pas vide:
  ```bash
  wc -c nextjs_docs_dump_v1.json  # Doit être > 5MB
  ```
- ✅ Valider JSON généré: `python3 -m json.tool nextjs_docs_dump_v1.json | head`
- ✅ Archiver les logs: `cp mission_log_nextjs.log logs/mission_log_$(date +%s).log`
- ✅ Nettoyer clone temporaire si besoin: `rm -rf nextjs_repo_temp/`

### Pour la Maintenance

- 📌 **Version Locking**: Toujours enregistrer la version exacte utilisée (dans `statistics`)
- 📌 **Versioning**: Créer une nouvelle version de output si breaking changes (v2, v3)
- 📌 **Backup**: Archiver les dumps précédents avant nouvelle exécution
- 📌 **Monitoring**: Parser les logs pour détecter erreurs/avertissements

---

## 📄 Licence

Ce projet est sous licence **MIT** - Libre d'utilisation, modification et redistribution.

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...

See LICENSE file for full text.
```

### Crédits

- **Auteur Principal**: Jack Josias (@jackjosias)
- **Documentation Originale**: Next.js Team (Vercel)
- **Librairies**: 
  - `python-frontmatter` (MIT License)
  - `packaging` (Apache 2.0 License)

---

## 🔗 Liens Rapides

| Ressource | Lien |
|---|---|
| **GitHub Repo** | [NEXTJS_DOCS_SCRAPER_STABLE_VERSION](https://github.com/jackjosias/NEXTJS_DOCS_SCRAPER_STABLE_VERSION) |
| **Latest Release** | [v16.0.8](https://github.com/vercel/next.js/releases/tag/v16.0.8) |
| **Source Commit** | [817ee56](https://github.com/vercel/next.js/commit/817ee56da939545d4b77cc54542f4c45a524e60a) |
| **Next.js Docs** | [nextjs.org/docs](https://nextjs.org/docs) |

---

## 💬 Support & Questions

Pour des questions ou issues:

1. Vérifier la section [Troubleshooting](#debugging--troubleshooting)
2. Consulter les logs: `cat mission_log_nextjs.log`
3. Ouvrir une GitHub Issue avec les détails complets

---

**Last Updated**: 2025-12-09 | **Scraper Version**: v1.3.0 | **Target Version**: v16.0.8 | **Files Extracted**: 375
