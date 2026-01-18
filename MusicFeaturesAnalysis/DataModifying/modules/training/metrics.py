from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pandas as pd

def metrics_rf(y_test, y_pred, pipe, X_cols):

    rf_model = pipe.named_steps["rf"]

    importances = rf_model.feature_importances_
    feature_names = X_cols
    feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False)

    result = [{'accuracy': accuracy_score(y_test, y_pred),
               'confusion_matrix': confusion_matrix(y_test, y_pred),
               'classification_report': classification_report(y_test, y_pred, output_dict=True),
               'feature_importances': feat_imp}]
    return result
