from sklearn.model_selection import cross_val_predict
from sklearn.metrics import classification_report, f1_score
from joblib import dump
import json
from pathlib import Path
from DataModifying.utils.config import CONFIG
from DataModifying.MLflow.loaders import build_model
from DataModifying.modules.training.train import modeling_pipeline, create_X_y
from DataModifying.MLflow.registry_train import register

ARTIFACT = Path("ml/artifacts/genre.pkl")
METRICS_PATH = Path("ml/artifacts/genre_metrics.json")


@register("subgenre")
def run(save: bool = False):


    cfg = CONFIG["genre"]

    X, y = create_X_y(mapped=True)

    model = build_model(cfg["model"], cfg["params"])
    pipe = modeling_pipeline(model)

    print("Training...")


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
        print("\nRefitting on full data and saving model...")
        pipe.fit(X, y)
        dump(pipe, ARTIFACT)
        print("Saved to", ARTIFACT)
