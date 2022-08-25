# peptide
> An ML library for peptide classification using pre-trained embeddings.


This library demonstrates the performance of a series of classifiers on the task of predicting whether a given amino acid sequence is one or more of the 3 target peptides.<br>
Specifically, this library compares the performance of classic ML classifiers trained on vastly different feature representations (of the amino acid sequences) - ranging from One-Hot embeddings to pre-trained embeddings from large protein language models.

**Classification Tasks:** Given a sequence of amino acids, classify whether the resulting peptide is one of the following.
- Anticancer peptide (ACP)
- DNA-binding protein
- Antimicrobial peptide (AMP)

## Install

### peptide
1. Git clone the repo.
    - https://github.com/vin00d/peptide.git
2. Create a new conda environment using the environment.yml file.
    - `cd peptide`
    - `conda env create -n peptide -f environment.yml`
3. To try things out, install this library in editable mode.
    - `pip install -e .`

### ProSE
To create LSTM embeddings ..
1. Clone the ProSE repo
    - https://github.com/tbepler/prose.git
2. Then complete setup instructions for ProSE [detailed on their repo](https://github.com/tbepler/prose#setup-instructions), also summarized below.
    - Download pre-trained embedding models.
    - Create conda environment and install dependencies.

### ESM
To create Transformer embeddings ..
1. Clone the ESM repo
    - https://github.com/facebookresearch/esm.git
2. Install ESM and its dependencies [detailed on their repo](https://github.com/facebookresearch/esm#usage-), one option summarized below.
    - Create new conda environment with python 3.9
    - In that conda environment, pip install `torch` and `fair-esm==0.5.0`

## How to use

Read through any (or all) of the following quick start guides to get a general idea. Then try running any of them as detailed below:
- Option 1: run any of the following jupyter noteboooks in the `nbs` folder.
    - `03_onehot.ipynb`
    - `04_lstm.ipynb`
    - `05_transformer.ipynb`
- Option 2: just open a jupyter notebook and copy, paste & run cell-by-cell from any of the following quick start guides.
    - [Onehot Embeddings](/peptide/onehot.html)
    - [LSTM Embeddings](/peptide/lstm.html)
    - [Transformer Embeddings](/peptide/transformer.html)

### Settings file and DATASTORE

- The steps demonstrated in these notebooks use default locations for datastore, etc as detailed in [Basics](/peptide/basics.html).
- The first cell in every notebook imports these settings for convenience.
- So if you intend to use default settings, make sure to place the datasets in the DATASTORE as detailed next.
{% include note.html content='The settings file and default folder structure will be created by either executing `from peptide.basics import *` in a cell or executing the first cell in any of the above notebooks. This will create a `DATASTORE` variable pointing to the path `~/.peptide/datasets`.' %}

### Copy Datasets Into DATASTORE

- Copy dataset directories into the location pointed to by the `DATASTORE` global variable.
    - for example `~/.peptide/datasets`
- Resulting folder structure **must** be
    - `~/.peptide/datasets/acp/train_data.csv`
    - `~/.peptide/datasets/amp/all_data.csv`
    - `~/.peptide/datasets/dna_binding/train.csv`
    

# References

This library is created using the awesome [nbdev v1](https://nbdev1.fast.ai/), soon to be upgraded to [nbdev v2](https://www.fast.ai/2022/07/28/nbdev-v2/).

Pretrained embeddings used in this library are from the following papers

1. LSTM - Protein Sequence Embeddings (**ProSE**) - Multi-task and masked language model-based protein sequence embedding models - [GitHub](https://github.com/tbepler/prose)
> Bepler, T., Berger, B. Learning the protein language:evolution, structure, and function. Cell Systems 12, 6 (2021). https://doi.org/10.1016/j.cels.2021.05.017> Bepler, T., Berger, B. Learning protein sequence embeddings using information from structure. International Conference on Learning Representations (2019). https://openreview.net/pdf?id=SygLehCqtm
2. Transformer - Evolutionary Scale Modeling (**ESM**) - [GitHub](https://github.com/facebookresearch/esm)
> Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences Alexander Rives, Joshua Meier, Tom Sercu, Siddharth Goyal, Zeming Lin, Jason Liu, Demi Guo, Myle Ott, C. Lawrence Zitnick, Jerry Ma, Rob Fergus
    > bioRxiv 622803; doi:https://doi.org/10.1101/622803
