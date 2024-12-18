# GBM8378

Cours "Principes d'imagerie biomédicale" à Polytechnique Montréal.

Ce répertoire contient le matériel de laboratoire pour ce cours.

## Documentation et ressources

Pour débuter avec Python, on recommande [cet excellent ](https://www.youtube.com/playlist?list=PLnzBBbvhjz4X3htDbNF0aJEDVtny48GI0) tutoriel par Guillaume Sheehy.

## Mise en route (sur poste informatique local)
#### 1) [Installer miniconda](https://docs.conda.io/en/latest/miniconda.html) pour préparer l'environnement python.
**Note:** Pour MacOS avec la puce M1/M2/M3, installer la version `x86_64.pkg` (version Intel).

Sur la page d'[installation](https://docs.anaconda.com/miniconda/install/#installing-miniconda), choisir, `MacOS/Linux installation --> MacOS terminal Installer --> Intel`
#### 2) Cloner ce répertoire GitHub sur votre ordinateur et sélectionner la dernière version:
```bash
git clone https://github.com/jcohenadad/GBM8378.git
cd GBM8378
git checkout r20241218
```
- Pour les usagers Windows, vous devrez peut-être [installer git](https://git-scm.com/downloads) avant de cloner ce répertoire GitHub.
- Si `git clone` ne fonctionne pas, vous pouvez télécharger directement la [dernière version](https://github.com/jcohenadad/GBM8378/releases) de ce répertoire sur votre ordinateur.

#### 3) Une fois que miniconda est installée et que ce répertoire est cloné, lancez les commandes suivantes pour créer votre environnement virtuel et lancez jupyter notebook:

Après, lancez les commandes suivantes pour créer l'environnement virtuel et ouvrir le notebook.

**⚠️ Note**: Ne pas utiliser le notebook dans VScode, certaines images n'afficheront pas.

```bash
conda env create -f environment.yml # Seulement pour créer l'environnement (peut prendre quelques minutes)

# Lancer le jupyter notebook:
conda activate env-GBM8378  # À faire à chaque fois que vous voulez lancer le notebook
jupyter notebook  
```
- Assurez-vous que sur votre terminal, vous êtes bien dans le dossier `GBM8378` lorsque vous appelez le fichier `environment.yml`
- Pour les usagers Windows, vous devrez peut-être écrire ces commandes dans `Anaconda Prompt` si `cmd`ne reconnait pas `conda`.

**Assurez-vous d'avoir la dernière version des fichiers en effectuant un `git pull` du répertoire avant chaque nouveau laboratoire**. Déplacez vos Notebooks ailleurs si vous ne voulez pas qu'ils soient écrasés par la dernière version.

## Créer PDF
Sur le jupyter notebook, imprimez la page et exporter/enregistrer au format PDF.

## Mise en route (avec Binder)
Cliquez sur l'icône Binder:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jcohenadad/GBM8378/HEAD?urlpath=%2Ftree%2F)

Attendre que Binder termine de créer l'environnement (peut prendre 5-10 minutes), après cliquez sur le Jupyter notebook. Ex.: sous `lab3-irm/GBM8378-lab3-IRM.ipynb`.

**Attention:** Après 10 d'inactivité, Binder va s'arrêter et vous devrez le relancer à nouveau. [Enregistrez votre travail](https://discourse.jupyter.org/t/getting-your-notebook-after-your-binder-has-stopped/3268) avant de fermer le notebook ou il sera perdu.
