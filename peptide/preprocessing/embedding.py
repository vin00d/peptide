# AUTOGENERATED! DO NOT EDIT! File to edit: 02_preprocessing_embedding.ipynb (unless otherwise specified).

__all__ = ['one_hot_encode']

# Cell
import numpy as np
import pandas as pd

from .data import *
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder

# Cell

def one_hot_encode(df):
    '''Create and return one-hot encoded features'''

    df = df.copy()
    df['seq_list'] = df['sequence'].apply(lambda x: list(x))
    df['lenghts'] = df['sequence'].apply(lambda x: len(x))
    features_df = pd.DataFrame(df['seq_list'].to_list())

    ohe = OneHotEncoder(sparse=True)
    transformed_data = ohe.fit_transform(features_df)
    transformed_df = pd.DataFrame(transformed_data, index=features_df.index)

    # features_ohe = pd.get_dummies(features_df, sparse=True)
    return ohe, transformed_df, features_df, df