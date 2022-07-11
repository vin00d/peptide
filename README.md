# peptide
> An open source library for peptide classification using Machine Learning and Deep Learning.


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

With conda
- `conda install -c conda-forge peptide`

With pip
- `pip install peptide`

## How to use

Fill me in please! Don't forget code examples:

```
1+1
```




    2


