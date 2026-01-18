from sklearn.model_selection import GridSearchCV, StratifiedKFold


def tune_random_forest(pipeline, X, y):
    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    params = {
        "clf__n_estimators": [200, 400],
        "clf__max_depth": [None, 10, 20],
        "clf__min_samples_split": [2, 5, 10],
        "clf__min_samples_leaf": [1, 2, 4],
        "clf__max_features": ["sqrt", "log2"]
    }

    grid = GridSearchCV(
        pipeline,
        params,
        cv=cv,
        scoring="f1_macro",
        n_jobs=-1,
        verbose=1
    )

    grid.fit(X, y)

    return grid.best_estimator_, grid.best_params_
