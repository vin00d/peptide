"""fastai style imports.py to import all required libs."""

import warnings, yaml, h5py, random, os
import torch, esm

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from collections import Counter  # , OrderedDict
from abc import ABC, abstractmethod
from pathlib import Path
from addict import Dict

from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    recall_score,
    precision_score,
    f1_score,
    classification_report,
    silhouette_score,
)
from sklearn.model_selection import GridSearchCV
from sklearn.cluster import KMeans
from sklearn.semi_supervised import LabelSpreading

from xgboost import XGBClassifier

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from tqdm import tqdm
import random
