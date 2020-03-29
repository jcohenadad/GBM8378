# GBM8378

Polytechnique Montreal course "Principes d'imagerie biomédicales".

## Getting started (with Binder)

Click on the Binder badge:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jcohenadad/GBM8378/master)

Wait for Binder to build (can take 5-10 minutes), then click on the Jupyter notebook. E.g.: under `lab3-irm/gbm8378-lab3-irm.ipynb`.

## Getting started (on local station)

Clone this repository:
```bash
git clone https://github.com/jcohenadad/GBM8378.git
cd GBM8378
```

[Install miniconda](https://docs.conda.io/en/latest/miniconda.html)

Then, run the following to create virtual environment and start the notebook:

```bash
conda create -n env-gbm8378 python=3.6  # Only do it once
conda activate env-gbm8378  # Do it everytime you wish to run the notebook
pip install -r requirements.txt  # Only do it once (or if there was any change in the repository)

# Start lab3 notebook:
jupyter notebook lab3-irm/gbm8378-lab3-irm.ipynb
```
