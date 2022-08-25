# peptide
> An ML library for peptide classification using pre-trained embeddings.


This project aims to build a series of classifiers that can predict whether a given amino acid sequence is one or more of the 3 target peptides.<br>
Additionally, this project will compare models built with vastly different approaches ranging from classic ML models with feature engineering by experts to large transformer-based models.

**Classification Tasks:** Given a sequence of amino acids (NLP equivalent = ‘words’), classify whether the resulting peptide (NLP equivalent = ‘sentence’) is one or many of the following targets (multi-task classification not multi-class i.e. 3 sigmoids not 1 softmax).
- Anticancer peptide (ACP)
- DNA-binding protein
- Antimicrobial peptide (AMP).

**Multiple Models:** Develop multiple models for the above classification tasks
- Supervised ML model(s) with hand engineered features from bio-experts
- Supervised ML model(s) using pre-trained embeddings with feature-space reduced using the following unsupervised techniques
    - Principal Component Analysis (PCA)
    - Autoencoders & its variants
    - K-Means Clustering
- Deep Learning Transformer models using pre-trained embeddings

**Model Scoring System:** Develop a system that produces accuracy scores 
- By running any given (labeled) dataset
- Through the multiple models listed above 
- And display / return accuracies on the classification tasks for each model.


## Install

### peptide
1. Git clone the repo.
    - https://github.com/vin00d/peptide.git
2. Create a new conda env using the environment.yml file.
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
    - Create conda env and install dependencies.

### ESM
To create Transformer embeddings ..
1. Clone the ESM repo
    - https://github.com/facebookresearch/esm.git
2. Install ESM and its dependesncies [detailed on their repo](https://github.com/facebookresearch/esm#usage-), one option summarized below.
    - Create new conda env with python 3.9
    - In that conda env pip install `torch` and `fair-esm==0.5.0`

## How to use

1. Read through the quick start guides and run cell by cell

# References

This library is created using the awesome [nbdev v1](https://nbdev1.fast.ai/), soon to be upgraded to [nbdev v2](https://www.fast.ai/2022/07/28/nbdev-v2/).

Pretrained embeddings used in this library are from the following papers

1. LSTM - Protein Sequence Embeddings (**ProSE**) - Multi-task and masked language model-based protein sequence embedding models - [GitHub](https://github.com/tbepler/prose)
> Bepler, T., Berger, B. Learning the protein language:evolution, structure, and function. Cell Systems 12, 6 (2021). https://doi.org/10.1016/j.cels.2021.05.017> Bepler, T., Berger, B. Learning protein sequence embeddings using information from structure. International Conference on Learning Representations (2019). https://openreview.net/pdf?id=SygLehCqtm
2. Transformer - Evolutionary Scale Modeling (**ESM**) - [GitHub](https://github.com/facebookresearch/esm)
> Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences Alexander Rives, Joshua Meier, Tom Sercu, Siddharth Goyal, Zeming Lin, Jason Liu, Demi Guo, Myle Ott, C. Lawrence Zitnick, Jerry Ma, Rob Fergus
    > bioRxiv 622803; doi:https://doi.org/10.1101/622803
