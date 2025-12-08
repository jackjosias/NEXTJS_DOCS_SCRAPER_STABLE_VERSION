# -*- coding: utf-8 -*-
"""
Next.js Docs Git Parser v1.3.0 (Production Ready - Auto Latest Stable Version)
Objectif: Cloner le dépôt Git de Next.js, parcourir le répertoire 'docs',
extraire le contenu des fichiers .mdx, et générer un dump JSON
conforme au format spécifié par le scraper RHF.

v1.3.0: Détection automatique de la dernière version STABLE (ignorant canary/pre-release).
v1.2.0: Ajout d'une routine de nettoyage forcé (`git reset` et `git clean`) pour
        gérer les états de dépôt corrompus suite à des échecs précédents.
v1.1.0: Ajout d'une vérification pré-vol pour 'core.longpaths' sur Windows.

Stratégie validée par l'Oracle-Engine_Channeler_77.0_Tartarus.
La perfection est la seule norme.

Dépendances:
pip install -r requirements.txt
Nécessite que 'git' soit installé et accessible dans le PATH.
"""

import os
import subprocess
import json
import re
import time
import logging
import platform
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional
from packaging import version as pkg_version

import frontmatter

# --- Configuration du Logging ---
def setup_logging() -> None:
    """Configure le logging pour la console et un fichier."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - (Next.js_Git_Parser) - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler("mission_log_nextjs.log", mode='w', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

# --- Fonctions Utilitaires et Vérifications Pré-vol ---
def load_config(config_path: str = 'config.json') -> Dict[str, Any]:
    """Charge la configuration depuis un fichier JSON."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.critical(f"CRITIQUE : Fichier de configuration '{config_path}' introuvable.")
        raise SystemExit(f"Impossible de trouver le fichier de configuration: {config_path}")
    except json.JSONDecodeError:
        logging.critical(f"CRITIQUE : Erreur de parsing du fichier JSON '{config_path}'.")
        raise SystemExit(f"Fichier de configuration JSON invalide: {config_path}")

def get_latest_stable_version() -> Optional[str]:
    """Récupère automatiquement la dernière version STABLE de Next.js (en ignorant canary/pre-release)."""
    try:
        logging.info("Détection de la dernière version stable de Next.js...")
        result = subprocess.run(
            ['git', 'ls-remote', '--tags', 'https://github.com/vercel/next.js.git'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Extraire tous les tags valides
        tags = []
        for line in result.stdout.strip().split('\n'):
            if line:
                tag = line.split('refs/tags/')[-1].replace('^{}', '')
                # Ignorer les versions canary, pre-release, et autres versions instables
                if tag and not any(x in tag.lower() for x in ['canary', 'alpha', 'beta', 'rc', 'dev', 'experimental', 'zones']):
                    # Nettoyer le tag pour avoir juste le numéro de version
                    clean_tag = tag.lstrip('v')
                    # Vérifier le format de la version (X.Y.Z)
                    if clean_tag and re.match(r'^\d+\.\d+\.\d+$', clean_tag):
                        tags.append((clean_tag, tag))  # Garder aussi le tag avec 'v'
        
        if tags:
            # Trier les versions et prendre la plus récente
            try:
                from packaging import version
                sorted_tags = sorted(tags, key=lambda x: version.parse(x[0]), reverse=True)
                latest_clean, latest_tag = sorted_tags[0]
                logging.info(f"✓ Dernière version stable détectée : {latest_tag}")
                return latest_tag
            except Exception as e:
                logging.warning(f"Impossible de parser les versions : {e}. Utilisation de la première trouvée.")
                return tags[0][1] if tags else None
        else:
            logging.warning("Aucune version stable trouvée. Utilisation de 'canary' par défaut.")
            return None
    except subprocess.CalledProcessError as e:
        logging.error(f"Erreur lors de la récupération des tags : {e}")
        logging.warning("Utilisation de 'canary' par défaut.")
        return None

def pre_flight_checks() -> None:
    """Exécute les vérifications d'environnement avant de lancer le script."""
    try:
        subprocess.run(['git', '--version'], check=True, capture_output=True)
        logging.info("Vérification pré-vol : 'git' est installé.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        logging.critical("CRITIQUE : 'git' n'est pas installé ou n'est pas dans le PATH.")
        sys.exit("'git' est requis pour cloner le dépôt. Veuillez l'installer.")

    if platform.system() == "Windows":
        logging.info("Vérification pré-vol : Système d'exploitation Windows détecté. Vérification de 'core.longpaths'.")
        try:
            result = subprocess.run(['git', 'config', '--get', 'core.longpaths'], capture_output=True, text=True)
            if result.stdout.strip().lower() != 'true':
                logging.critical("ERREUR DE CONFIGURATION GIT : La prise en charge des chemins longs n'est pas activée.")
                error_message = (
                    "\n"
                    "--------------------------------------------------------------------------\n"
                    "ERREUR D'ENVIRONNEMENT DÉTECTÉE SUR WINDOWS\n"
                    "--------------------------------------------------------------------------\n"
                    "Le dépôt 'next.js' contient des noms de fichiers très longs qui dépassent\n"
                    "la limite par défaut de Windows. Pour continuer, vous devez activer la\n"
                    "prise en charge des chemins longs dans votre configuration Git.\n\n"
                    "Veuillez exécuter la commande suivante dans votre terminal (PowerShell/CMD) :\n\n"
                    "    git config --global core.longpaths true\n\n"
                    "NOTE : Vous pourriez avoir besoin d'exécuter cette commande dans un terminal\n"
                    "ouvert avec des droits d'administrateur.\n"
                    "Après avoir exécuté la commande, relancez ce script.\n"
                    "--------------------------------------------------------------------------"
                )
                sys.exit(error_message)
            logging.info("Vérification pré-vol : 'core.longpaths' est correctement activé.")
        except Exception as e:
            logging.error(f"Impossible de vérifier la configuration Git 'core.longpaths'. Erreur : {e}")
            sys.exit("Une erreur est survenue lors de la vérification de votre configuration Git.")

# --- Phase 1: Extraction ---
def clone_or_pull_repo(repo_url: str, branch: str, clone_dir: str) -> Optional[str]:
    """Clone le dépôt s'il n'existe pas, sinon le nettoie et le met à jour pour la branche spécifiée."""
    try:
        if os.path.exists(clone_dir):
            logging.info(f"Le répertoire '{clone_dir}' existe. Nettoyage et récupération de la branche '{branch}'...")
            # Nettoyage forcé pour garantir un état propre
            logging.warning(f"AVERTISSEMENT : Nettoyage forcé du répertoire '{clone_dir}' pour éviter les conflits.")
            
            # Récupérer les infos du repo distant
            subprocess.run(['git', '-C', clone_dir, 'fetch', '--all', '--tags'], check=True, capture_output=True)
            
            # Réinitialiser la branche locale et checkout la nouvelle branche
            subprocess.run(['git', '-C', clone_dir, 'checkout', '-f', branch], check=True, capture_output=True)
            subprocess.run(['git', '-C', clone_dir, 'reset', '--hard', f'origin/{branch}'], check=True, capture_output=True)
            subprocess.run(['git', '-C', clone_dir, 'clean', '-fdx'], check=True, capture_output=True)
        else:
            logging.info(f"Clonage du dépôt '{repo_url}' (branche: {branch}) dans '{clone_dir}'...")
            subprocess.run(['git', 'clone', '--depth', '1', '--branch', branch, repo_url, clone_dir], check=True, capture_output=True)

        commit_hash_result = subprocess.run(['git', '-C', clone_dir, 'rev-parse', 'HEAD'], check=True, capture_output=True, text=True)
        commit_hash = commit_hash_result.stdout.strip()
        logging.info(f"Dépôt synchronisé. Commit HEAD actuel : {commit_hash}")
        return commit_hash
    except subprocess.CalledProcessError as e:
        logging.error(f"Erreur Git : {e.stderr.decode('utf-8').strip() if hasattr(e, 'stderr') else str(e)}")
        return None

def find_target_files(start_path: str, extensions: List[str]) -> List[str]:
    """Trouve tous les fichiers avec les extensions spécifiées dans un répertoire."""
    target_files = []
    for root, _, files in os.walk(start_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                target_files.append(os.path.join(root, file))
    logging.info(f"{len(target_files)} fichiers cibles trouvés dans '{start_path}'.")
    return target_files

# --- Phase 2: Transformation ---
def mdx_to_text(mdx_content: str) -> str:
    """Transforme le contenu MDX en texte brut en préservant les blocs de code."""
    # TODO: Améliorer le parsing pour gérer les composants JSX complexes.
    code_blocks = re.findall(r'```.*?```', mdx_content, re.DOTALL)
    content_no_code = re.sub(r'```.*?```', '___CODE_BLOCK___', mdx_content, flags=re.DOTALL)
    text_only = re.sub(r'<[^>]+>', '', content_no_code)
    text_only = re.sub(r'import .*?;', '', text_only, flags=re.DOTALL)
    text_only = re.sub(r'#+\s', '', text_only)
    text_only = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text_only)
    for block in code_blocks:
        text_only = text_only.replace('___CODE_BLOCK___', f" ``` {block.strip('` ')} ``` ", 1)
    cleaned_text = re.sub(r'\s+', ' ', text_only).strip()
    return cleaned_text

def parse_mdx_file(file_path: str, base_dir: str) -> Optional[Dict[str, Any]]:
    """Parse un fichier MDX pour extraire métadonnées et contenu."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        relative_path = os.path.relpath(file_path, base_dir)
        url_path = os.path.splitext(relative_path)[0].replace(os.path.sep, '/')
        url_path = re.sub(r'^\d+-', '', url_path)
        url_path = url_path.replace('/index', '')
        url = f"https://nextjs.org/docs/{url_path}"
        title = post.metadata.get('title', os.path.basename(file_path))
        content_cleaned = mdx_to_text(post.content)
        return {
            "url": url,
            "title": title,
            "content": content_cleaned if content_cleaned else "[Contenu Vide Apres Extraction]"
        }
    except Exception as e:
        logging.warning(f"Échec du parsing pour le fichier '{file_path}': {e}")
        return None

# --- Phase 3: Chargement ---
def generate_final_json(all_results: List[Dict[str, Any]], duration: float, commit_hash: str, config: Dict[str, Any]) -> None:
    """Génère le fichier JSON de sortie final, conforme au format RHF."""
    success_count = len(all_results)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    title_index = [f"  - ID {i}: Page '{item.get('title', 'Titre inconnu')}'" for i, item in enumerate(all_results)]
    index_str = "\\n".join(title_index)
    stats_block = {
        "report_id": f"NEXTJS-DOCS-DUMP-v1.2.0-{int(time.time())}",
        "status": "✅ Extraction terminée",
        "timestamp_utc": timestamp,
        "source_commit_hash": commit_hash,
        "total_documents_extracted": success_count,
        "execution_time_seconds": round(duration, 2),
        "llm_navigation_guide": {
            "description": "Ce bloc fournit des métadonnées pour aider les LLMs à naviguer et comprendre ce jeu de données. Chaque document possède un ID unique. L'index ci-dessous mappe les IDs aux titres des pages pour un accès rapide.",
            "content_format": "Le champ 'content' est une chaîne de caractères où les blocs de code sont encadrés par '```'.",
            "quick_access_index": f"[ {index_str} ]"
        }
    }
    final_output = {"pages": all_results, "statistics": stats_block}
    try:
        with open(config['output_filename'], 'w', encoding='utf-8') as f:
            json.dump(final_output, f, indent=2, ensure_ascii=False)
        logging.info(f"SUCCÈS FINAL ! Fichier Next.js Docs .json sauvegardé : {config['output_filename']}")
    except IOError as e:
        logging.critical(f"CRITIQUE: Impossible d'écrire dans '{config['output_filename']}': {e}")

# --- Orchestration ---
def main():
    """Fonction principale orchestrant le pipeline ETL."""
    start_time = time.time()
    setup_logging()
    logging.info("<<< Parser de Dépôt Git Next.js v1.3.0 - Initialisation >>>")
    
    pre_flight_checks()
    config = load_config()
    
    # Détection automatique de la dernière version stable
    latest_stable = get_latest_stable_version()
    if latest_stable:
        config['branch'] = latest_stable
        logging.info(f"✓ Configuration mise à jour : branche = {latest_stable}")
    else:
        logging.info(f"Utilisation de la branche par défaut : {config.get('branch', 'canary')}")

    commit_hash = clone_or_pull_repo(config['repo_url'], config['branch'], config['temp_clone_dir'])
    if not commit_hash:
        logging.critical("Arrêt du script en raison d'une erreur Git.")
        return

    docs_root_path = os.path.join(config['temp_clone_dir'], config['docs_path'])
    mdx_files = find_target_files(docs_root_path, config['file_extensions'])

    all_results = []
    for i, file_path in enumerate(mdx_files):
        logging.info(f"Traitement du fichier {i+1}/{len(mdx_files)}: {os.path.basename(file_path)}")
        parsed_data = parse_mdx_file(file_path, config['temp_clone_dir'])
        if parsed_data:
            all_results.append(parsed_data)
    
    all_results.sort(key=lambda x: x.get("url", ""))
    for i, item in enumerate(all_results):
        item['id'] = i

    duration = time.time() - start_time
    generate_final_json(all_results, duration, commit_hash, config)
    
    logging.info(f"Mission terminée en {duration:.2f} secondes.")
    logging.info("<<< Parser de Dépôt Git Next.js v1.3.0 - Protocole Terminé. >>>")

if __name__ == "__main__":
    main()