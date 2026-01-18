import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
from modules.preprocessing.genre_mapping import mapping
from tuning import tune_random_forest
from modules.preprocessing.clip import clip_outliers_iqr

def create_X_y(path: str) -> tuple:
    r""" creates X and y from feature path and mapping them
    (initially dropping 'genre' and 'genre_mapped' columns).
    :param path: feature path
    :return: X, y
    :rtype: tuple
    """
    df = pd.read_csv(path)
    mapping(df, path)
    X = df.drop(['genre', 'genre_mapped', 'y'], axis=1)
    y = df['y']
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



def modeling_pipeline_rf(column_transformer: ColumnTransformer) -> Pipeline:
    r""" Using the RandomForestClassifier with the best hypertuning for today.
    :return: Pipeline ready to fit
    :rtype: Pipeline
    """
    rf = RandomForestClassifier(max_depth= 20, max_features ='sqrt',
                        min_samples_leaf= 1, min_samples_split= 2,
                        n_estimators= 200)
    pipe = Pipeline([
    ('Preprocessor', column_transformer),
    ("rf", rf)
    ])
    return pipe


def train_pipeline(pipeline: Pipeline, X, y) -> tuple:
    """test_size = 0.2
    :return: model, classification report, best params
    :rtype tuple"""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    model, params = tune_random_forest(pipeline, X_train, y_train)

    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    return model, report, params





