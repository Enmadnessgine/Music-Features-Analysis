from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
from DataModifying.modules.preprocessing.genre_mapping import mapping
from DataModifying.modules.preprocessing.clip import clip_outliers_iqr
from sklearn.preprocessing import StandardScaler
import pandas as pd


def create_X_y(mapped=False, df: DataFrame = None) -> tuple:
    r""" creates X and y from feature path and mapping them
    (initially dropping 'genre' and 'genre_mapped' columns).
    :param path: feature path
    :return: X, y
    :rtype: tuple
    """
    if df is not None:
        pass
    else:
        df = pd.read_csv('DataModifying/data/features/features.csv')
    df = df.drop_duplicates()
    X = df.drop(['genre',  'key', 'mode'], axis=1)
    clip_cols = ['tempo', 'speechiness', 'liveness']
    X[clip_cols] = clip_outliers_iqr(X[clip_cols], clip_cols)

    if mapped:
        y = mapping(df)
    else:
        y = df['genre']
    return X, y


def col_transformer(X):
    r""" Transforms data by specific way: log columns 'tempo', 'speechiness', 'liveness';
    clipping all columns;
     remainder = "drop".
    :param X: features
    :return: column transformer ready to go
    :rtype: ColumnTransformer
    """
    log_cols = ['tempo', 'speechiness', 'liveness']
    clip_cols = X.drop(['tempo', 'speechiness', 'liveness', 'key', 'mode'], axis=1).columns
    log_transformer = FunctionTransformer(np.log1p, validate=True)
    clip_transformer = FunctionTransformer(clip_outliers_iqr, kw_args={"cols": clip_cols})
    clip_transformer_log = FunctionTransformer(clip_outliers_iqr, kw_args={"cols": log_cols})

    column_transformer = ColumnTransformer(transformers=[
        ('clip_log', Pipeline(steps=[
        ("clip", clip_transformer_log),
        ("log", log_transformer),]
        ), log_cols),
        ('clip_others', clip_transformer, clip_cols),
        ],
        remainder="drop",
        verbose_feature_names_out=False
    )
    return column_transformer



def modeling_pipeline(model) -> Pipeline:
    r""" Using model and column transformer to make pipeline
    :return: Pipeline ready to fit
    :rtype: Pipeline
    """

    pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", model)
    ])
    return pipe


def train_pipeline(pipeline: Pipeline, X, y, tune=-1) -> tuple:
    """Check tuning func in tuning.py
    :return: model, classification report, best params
    :rtype tuple"""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )
    if tune != -1:
        model, params = tune(pipeline, X_train, y_train)
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)
        return model, report, params
    else:
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)
        return pipeline, report, -1, -1
