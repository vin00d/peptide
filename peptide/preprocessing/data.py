# AUTOGENERATED! DO NOT EDIT! File to edit: 01_preprocessing_data.ipynb (unless otherwise specified).

__all__ = ['ProteinDataset', 'ACPDataset', 'AMPDataset', 'DNABindDataset']

# Cell
from ..basics import *

from collections import Counter
from abc import ABC, abstractmethod

import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt
import seaborn as sns


# Cell


class ProteinDataset(ABC):
    """Abstract base class for prtein datasets"""

    def __init__(self, location: str, max_seq_len: int = None):
        self.location = location
        self.max_seq_len = max_seq_len

    @abstractmethod
    def clean_data(self):
        pass

    def extract_features_labels(
        self, df: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame, np.array]:
        """Extract features and separate labels"""

        df["sequence"] = df["sequence"].apply(lambda x: list(x))
        df["length"] = df["sequence"].apply(lambda x: len(x))

        features = pd.DataFrame(df["sequence"].to_list())
        if self.max_seq_len:
            features = features.loc[:, : self.max_seq_len - 1]

        label_cols = [lbl for lbl in df.columns if "label" in lbl]
        labels = pd.DataFrame(df[label_cols])

        return df, features, np.ravel(labels.to_numpy())


# Cell


class ACPDataset(ProteinDataset):
    """Anticancer Peptide Dataset"""

    def __init__(self, location: str, max_seq_len: int = None):
        """Load, clean ,extract labels & features for ACP train and test"""
        super().__init__(location, max_seq_len)

        train_df, test_df = self.clean_data()
        self.train, self.X_train, self.y_train = self.extract_features_labels(train_df)
        self.test, self.X_test, self.y_test = self.extract_features_labels(test_df)

    def clean_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Load, clean and return ACP train and test dataframes"""
        acp_train_df = pd.read_csv(f"{self.location}/acp/train_data.csv")
        acp_test_df = pd.read_csv(f"{self.location}/acp/test_data.csv")

        acp_train_df.rename(
            columns={"sequences": "sequence", "label": "label_acp"}, inplace=True
        )
        acp_test_df.rename(
            columns={"sequences": "sequence", "label": "label_acp"}, inplace=True
        )

        return acp_train_df, acp_test_df


# Cell


class AMPDataset(ProteinDataset):
    """Antimicrobial Peptide Dataset"""

    def __init__(
        self, location: str, max_seq_len: int = 150, test_pct: float = 0.2, seed=1234
    ):
        """Load, clean ,extract labels & features for AMP train and test"""
        super().__init__(location, max_seq_len)
        self.test_pct = test_pct
        self.seed = seed

        train_df, test_df = self.clean_data(self.test_pct, self.seed)
        self.train, self.X_train, self.y_train = self.extract_features_labels(train_df)
        self.test, self.X_test, self.y_test = self.extract_features_labels(test_df)

    def clean_data(
        self, test_pct: float = 0.2, seed: int = 1234
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Load, clean, split and return AMP train and test dataframes"""
        amp_df = pd.read_csv(f"{self.location}/amp/all_data.csv")

        amp_df.drop(columns=["PDBs_code"], inplace=True)
        amp_df.rename(
            columns={"SequenceID": "sequence", "label": "label_amp"}, inplace=True
        )

        amp_test_df = amp_df.sample(frac=test_pct, random_state=seed)
        amp_train_df = amp_df.drop(amp_test_df.index)

        amp_train_df.reset_index(inplace=True)
        amp_test_df.reset_index(inplace=True)

        return amp_train_df, amp_test_df


# Cell


class DNABindDataset(ProteinDataset):
    """DNA Binding Protein Dataset"""

    def __init__(self, location: str, max_seq_len: int = 300):
        """Load, clean ,extract labels & features for ACP train and test"""
        super().__init__(location, max_seq_len)

        train_df, test_df = self.clean_data()
        self.train, self.X_train, self.y_train = self.extract_features_labels(train_df)
        self.test, self.X_test, self.y_test = self.extract_features_labels(test_df)

    def clean_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Load, clean and return DNABind train and test dataframes"""

        dna_bind_train_df = pd.read_csv(f"{self.location}/dna_binding/train.csv")
        dna_bind_test_df = pd.read_csv(f"{self.location}/dna_binding/test.csv")

        dna_bind_train_df.drop(columns=["code", "origin"], inplace=True)
        dna_bind_test_df.drop(columns=["code", "origin"], inplace=True)

        dna_bind_train_df.rename(columns={"label": "label_dna_bind"}, inplace=True)
        dna_bind_test_df.rename(columns={"label": "label_dna_bind"}, inplace=True)

        return dna_bind_train_df, dna_bind_test_df
