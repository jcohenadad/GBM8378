# GBM8378

Polytechnique Montreal course "Principes d'imagerie biomédicale".

## Getting started (with Binder)

Click on the Binder badge:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jcohenadad/GBM8378/master)

Wait for Binder to finish building the environment (can take 5-10 minutes), then click on the Jupyter notebook. E.g.: under `lab3-irm/gbm8378-lab3-irm.ipynb`.

**Warning:** After 10 minutes of inactivity, binder will stop working and you will have to launch it again. [Save your work](https://discourse.jupyter.org/t/getting-your-notebook-after-your-binder-has-stopped/3268) before closing it or it will be lost !

## Getting started (on local station)

Clone this repository:
```bash
git clone https://github.com/jcohenadad/GBM8378.git
cd GBM8378
```

[Install miniconda](https://docs.conda.io/en/latest/miniconda.html)

Then, run the following to create a virtual environment and start the notebook:

```bash
conda create -n env-gbm8378 python=3.6  # Only do it once
conda activate env-gbm8378  # Do it everytime you wish to run the notebook
pip install -r requirements.txt  # Only do it once (or if there was any change in the repository)

# Start lab3 notebook:
jupyter notebook lab3-irm/gbm8378-lab3-irm.ipynb
```
**Make sure that you have the last version of the files by cloning the repo before every new lab.** Move your Notebooks elsewhere if you don't want them to be overwritten by the new clone. 

## Create PDF
While on the jupyter notebook, print the page and export/save as PDF.
