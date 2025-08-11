# classification_pipeline.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap

from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMClassifier

from boruta import BorutaPy
import shap
import optuna
from lime.lime_tabular import LimeTabularExplainer
import joblib

# 1. Load Data
df = pd.read_csv("your_data.csv")
X = df.drop(columns=["target"])
y = df["target"]

# 2. Preprocessing
X.fillna(X.median(), inplace=True)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Feature Selection with Boruta
rf = LGBMClassifier(n_jobs=-1, max_depth=5)
boruta_selector = BorutaPy(estimator=rf, n_estimators="auto", verbose=0, random_state=42)
boruta_selector.fit(X_scaled, y.values)
X_boruta = X_scaled[:, boruta_selector.support_]
selected_features = X.columns[boruta_selector.support_]

# 4. Dimensionality Reduction (Visualization)
pca = PCA(n_components=2).fit_transform(X_boruta)
umap_reduced = umap.UMAP(n_components=2, random_state=42).fit_transform(X_boruta)
tsne = TSNE(n_components=2, random_state=42).fit_transform(X_boruta)

fig, axs = plt.subplots(1, 3, figsize=(18, 5))
for ax, data, title in zip(axs, [pca, umap_reduced, tsne], ["PCA", "UMAP", "t-SNE"]):
    sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=y, ax=ax)
    ax.set_title(title)
plt.tight_layout()
plt.savefig("dimensionality_reduction_plots.png")
plt.close()

# 5. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_boruta, y, stratify=y, test_size=0.2, random_state=42
)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)


# 6A. Optuna for LightGBM
def optuna_objective(trial):
    params = {
        "max_depth": trial.suggest_int("max_depth", 3, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
        "n_estimators": trial.suggest_int("n_estimators", 50, 300),
        "subsample": trial.suggest_float("subsample", 0.5, 1.0),
    }
    model = LGBMClassifier(**params)
    score = cross_val_score(model, X_train, y_train, cv=skf, scoring="roc_auc").mean()
    return score


study = optuna.create_study(direction="maximize")
study.optimize(optuna_objective, n_trials=30)
best_lgbm_params = study.best_params

# 6B. Logistic Regression with GridSearchCV
lr = LogisticRegression(max_iter=1000)
lr_params = {"C": [0.01, 0.1, 1, 10], "penalty": ["l1", "l2"], "solver": ["liblinear"]}
grid_search_lr = GridSearchCV(lr, lr_params, cv=skf, scoring="roc_auc", n_jobs=-1)
grid_search_lr.fit(X_train, y_train)

# 7. Final Training & Evaluation
models = {
    "LightGBM": LGBMClassifier(**best_lgbm_params),
    "Logistic Regression": grid_search_lr.best_estimator_,
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    results[name] = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "ROC AUC": roc_auc_score(y_test, y_proba),
        "Report": classification_report(y_test, y_pred, output_dict=True),
    }

# Save Results
for name, metrics in results.items():
    print(f"\nModel: {name}")
    print(f"Accuracy: {metrics['Accuracy']:.4f}")
    print(f"ROC AUC: {metrics['ROC AUC']:.4f}")
    report_df = pd.DataFrame(metrics["Report"]).T
    report_df.to_csv(f"{name.replace(' ', '_')}_classification_report.csv")
    print(report_df)

# 8. SHAP Interpretability for LightGBM
explainer = shap.Explainer(models["LightGBM"], X_train)
shap_values = explainer(X_test)
shap.plots.beeswarm(shap_values, max_display=15)
plt.savefig("shap_beeswarm.png")
plt.close()

# 9. LIME for one prediction
explainer_lime = LimeTabularExplainer(
    X_train,
    feature_names=selected_features,
    class_names=["Class 0", "Class 1"],
    mode="classification",
)
i = 0
exp = explainer_lime.explain_instance(X_test[i], models["LightGBM"].predict_proba, num_features=10)
exp.save_to_file("lime_explanation.html")

# 10. Save models
joblib.dump(models["LightGBM"], "lightgbm_model.pkl")
joblib.dump(models["Logistic Regression"], "logistic_regression_model.pkl")
