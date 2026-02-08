from sklearn.model_selection import cross_val_predict, GridSearchCV, train_test_split
from sklearn.metrics import classification_report, f1_score
from joblib import dump
import json
from pathlib import Path
from DataModifying.utils.config import CONFIG
from DataModifying.MLflow.loaders import build_model
from DataModifying.modules.training.train import modeling_pipeline, create_X_y
from DataModifying.MLflow.registry_train import register

ARTIFACT = Path("DataModifying/models/artifacts/genre.pkl")
METRICS_PATH = Path("DataModifying/MLflow/metrics/genre_metrics.json")



@register("genre")
def run(grid: bool = False, save: bool = False):

    cfg = CONFIG["genre"]

    X, y = create_X_y()

    model = build_model(cfg["model"], cfg["params"])
    pipe = modeling_pipeline(model)

    print("Training...")

    if grid:

        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=0.2,
            stratify=y,
            random_state=42
        )

        param_grid = {f"model__{k}": v for k, v in cfg["grid"].items()}

        model = GridSearchCV(
            estimator=pipe,
            param_grid=param_grid,
            cv=cfg["cv"]["folds"],
            scoring='accuracy'
        )
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)
        f1 = f1_score(y_test, y_pred, average="macro")

        print("\nClassification report:\n")
        print(classification_report(y_test, y_pred))
        print(f"Macro F1 (grid) = {f1:.4f}")
        with open(METRICS_PATH, "w") as f:
            json.dump(report, f, indent=2)
        if save:
            print("\nSaving model...")
            dump(model, ARTIFACT)
            print("Saved to", ARTIFACT)
    else:
        y_pred = cross_val_predict(
            pipe,
            X,
            y,
            cv=cfg["cv"]["folds"]
        )
        report = classification_report(y, y_pred, output_dict=True)
        f1 = f1_score(y, y_pred, average="macro")

        print("\nClassification report:\n")
        print(classification_report(y, y_pred))
        print(f"Macro F1 = {f1:.4f}")
        with open(METRICS_PATH, "w") as f:
            json.dump(report, f, indent=2)
        if save:
            print("\nRefitting and saving model...")
            pipe.fit(X, y)
            dump(pipe, ARTIFACT)
            print("Saved to", ARTIFACT)

