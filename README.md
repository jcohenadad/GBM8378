# GBM8378

Polytechnique Montreal course "Principes d'imagerie biomédicale".

This repository includes the lab material for the course 

## Documentation and Ressource

To get started with Python, we recommend [this excellent tutorial](https://www.youtube.com/playlist?list=PLnzBBbvhjz4X3htDbNF0aJEDVtny48GI0) (in French) made by Guillaume Sheehy. 

## Getting started (with Binder)

Click on the Binder badge:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jcohenadad/GBM8378/master)

Wait for Binder to finish building the environment (can take 5-10 minutes), then click on the Jupyter notebook. E.g.: under `lab3-irm/gbm8378-lab3-irm.ipynb`.

**Warning:** After 10 minutes of inactivity, binder will stop working and you will have to launch it again. [Save your work](https://discourse.jupyter.org/t/getting-your-notebook-after-your-binder-has-stopped/3268) before closing it or it will be lost !

## Getting started (on local station)

#### 1) You will need to [install miniconda](https://docs.conda.io/en/latest/miniconda.html) in order to set-up your python environment.

#### 2) Clone this GitHub repository on your computer and select the latest release:
```bash
git clone https://github.com/jcohenadad/GBM8378.git
cd GBM8378
git checkout $(git describe --tags `git rev-list --tags --max-count=1`)
```
- For Windows user, you might need to [install git](https://git-scm.com/downloads) prior to clone the repository.
- If git clone is not working, you can download the most [recent release](https://github.com/jcohenadad/GBM8378/releases) of the repository on your computer.

#### 3) Once miniconda is installed and the repository is cloned, run the following commands in order to create your virtual environment and start the jupyter notebook:

Then, run the following to create a virtual environment and start the notebook:

```bash
conda env create -f environment.yml # Only do it once in order to create the environment (might take a few minutes)

# Start the jupyter notebooks:
conda activate env-gbm8378  # Do it everytime you wish to run the notebook
jupyter notebook  
```

- Make sure that your prompt is currently on the `GBM8378` folder when you call the `environment.yml` file.
- For Windows user, you might need to type these commands in `Anaconda Prompt` if `cmd` does not recognize `conda`.

**Make sure that you have the last version of the files by pulling the repo before every new lab** (`git pull`). Move your Notebooks elsewhere if you don't want them to be overwritten by the new clone. 

## Create PDF
While on the jupyter notebook, print the page and export/save as PDF.
