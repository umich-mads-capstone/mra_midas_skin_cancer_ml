"""
Utility functions for running NLPs to lower data cardinality in the midas_location field
"""

import re
import numpy as np
import pandas as pd
from typing import Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline


def basic_clean_clinical_text(x: str) -> str:
    """
    Light text cleanup for clinical text. 
    Normalize whitespace, keep clinical tokens
    """
    if x is None: 
        return ""
    x = str(x)
    x = x.replace("\u00A0", " ")
    x = re.sub(r"\s+", " ", x).strip()
    return x

def add_note_embeddings_tfidf_svd(
    df: pd.DataFrame, 
    text_col: str, 
    out_prefix: str = "note_svd", 
    n_components: int = 50, 
    max_features: int = 200_000, 
    ngram_range=(1, 2), 
    min_df: int = 3, 
    max_df: float = 0.95, 
    random_state: int = 42, 
) -> tuple[pd.DataFrame, Pipeline]:
    """
    Converts clinical notes text column into a low-cardinality numeric
    representation using TF-IDF and TruncatedSVD (LSA). 

    Returns: (df_with_new_cols, fitted_pipeline)
    """

    if text_col not in df.columns:
        raise KeyError(f"{text_col!r} not found in df.columns")
    
    texts = df[text_col].map(basic_clean_clinical_text).fillna("")

    pipeline = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(
                max_features=max_features,
                ngram_range=ngram_range,
                min_df=min_df,
                max_df=max_df,
                lowercase=True,
                strip_accents=None,
            )),
            ("svd", TruncatedSVD(
                n_components=n_components,
                random_state=random_state,
            )),
        ]
    )

    X_reduced = pipeline.fit_transform(texts)

    df_out = df.copy()
    for i in range(n_components):
        df_out[f"{out_prefix}_{i:03d}"] = X_reduced[:, i].astype(np.float32)

    return df_out, pipeline

def svd_top_phrases(
    pipeline,
    top_n: int = 20,
    component_ids: Optional[list[int]] = None,
) -> pd.DataFrame:
    """
    Returns a tidy table of top phrases for each SVD component (positive and negative).
    Assumes pipeline has steps named 'tfidf' and 'svd'.
    """
    tfidf = pipeline.named_steps["tfidf"]
    svd = pipeline.named_steps["svd"]

    terms = tfidf.get_feature_names_out()
    comps = svd.components_  # shape: (n_components, n_terms)

    if component_ids is None:
        component_ids = list(range(comps.shape[0]))

    rows = []
    for k in component_ids:
        weights = comps[k]

        pos_idx = np.argsort(weights)[::-1][:top_n]
        neg_idx = np.argsort(weights)[:top_n]

        for rank, j in enumerate(pos_idx, 1):
            rows.append({
                "component": k,
                "direction": "positive",
                "rank": rank,
                "phrase": terms[j],
                "weight": float(weights[j]),
            })

        for rank, j in enumerate(neg_idx, 1):
            rows.append({
                "component": k,
                "direction": "negative",
                "rank": rank,
                "phrase": terms[j],
                "weight": float(weights[j]),
            })

    return pd.DataFrame(rows).sort_values(["component", "direction", "rank"])
    