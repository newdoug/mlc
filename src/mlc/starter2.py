import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap

from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from boruta import BorutaPy
import shap
import optuna
from lime.lime_tabular import LimeTabularExplainer


# Load and pre-process data

df = pd.read_csv("your_data.csv")
X = df.drop(columns=["target"])
y = df["target"]

X.fillna(X.median(), inplace=True)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# Feature Selection using Boruta with Random Forest
rf_boruta = RandomForestClassifier(n_jobs=-1, class_weight='balanced', max_depth=5)
boruta = BorutaPy(estimator=rf_boruta, n_estimators='auto', verbose=0, random_state=42)
boruta.fit(X_scaled, y.values)

X_boruta = X_scaled[:, boruta.support_]
selected_features = X.columns[boruta.support_]


# Dimensionality Reduction (PCA / UMAP / t-SNE)

pca = PCA(n_components=2).fit_transform(X_boruta)
umap_reduced = umap.UMAP(n_components=2, random_state=42).fit_transform(X_boruta)
tsne = TSNE(n_components=2, random_state=42).fit_transform(X_boruta)

fig, axs = plt.subplots(1, 3, figsize=(18, 5))
for ax, data, title in zip(axs, [pca, umap_reduced, tsne], ['PCA', 'UMAP', 't-SNE']):
    sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=y, ax=ax)
    ax.set_title(title)
plt.show()


# Train/Test Split & Stratified K-Fold

X_train, X_test, y_train, y_test = train_test_split(X_boruta, y, stratify=y, test_size=0.2, random_state=42)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)


# Hyperparameter Tuning: Optuna + GridSearchCV (example with XGBoost)
# A. Optuna

def objective(trial):
    params = {
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'n_estimators': trial.suggest_int('n_estimators', 50, 300),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0)
    }
    model = XGBClassifier(**params, use_label_encoder=False, eval_metric='logloss')
    score = cross_val_score(model, X_train, y_train, cv=skf, scoring='roc_auc').mean()
    return score

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=30)
best_params = study.best_params

# B. GridSearchCV (Alternative)

param_grid = {
    'max_depth': [4, 6, 8],
    'n_estimators': [100, 200],
}
grid_search = GridSearchCV(XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
                           param_grid, cv=skf, scoring='roc_auc', n_jobs=-1)
grid_search.fit(X_train, y_train)


# Final Model Training & Evaluation

model = XGBClassifier(**best_params, use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("Accuracy:", accuracy_score(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, y_proba))
print("Classification Report:")
print(classification_report(y_test, y_pred))


# Model Interpretability (SHAP + LIME)
# SHAP (Tree Explainer for XGBoost/LightGBM)

explainer = shap.Explainer(model, X_train, feature_names=selected_features)
shap_values = explainer(X_test)

shap.plots.beeswarm(shap_values, max_display=15)
shap.plots.bar(shap_values, max_display=15)

# LIME

explainer_lime = LimeTabularExplainer(X_train, feature_names=selected_features,
                                      class_names=["Class 0", "Class 1"], mode='classification')
i = 0
exp = explainer_lime.explain_instance(X_test[i], model.predict_proba, num_features=10)
exp.show_in_notebook()



