from dask.distributed import Client, LocalCluster
import dask.dataframe as dd
import lightgbm as lgb
from lightgbm.dask import DaskDMatrix, train as dask_train
from sklearn.metrics import accuracy_score, roc_auc_score

# Start a local Dask cluster (or connect to remote)
cluster = LocalCluster(n_workers=4, threads_per_worker=2, memory_limit="4GB")
client = Client(cluster)

# Load large CSV as Dask DataFrame
ddf = dd.read_csv("large_dataset.csv")  # Replace with your large CSV file
ddf = ddf.persist()

# Split features and label
X = ddf.drop(columns=["target"])
y = ddf["target"]

# Create DaskDMatrix
dtrain = DaskDMatrix(client, X, y)

# LightGBM parameters
params = {"objective": "binary", "metric": "auc", "verbosity": -1}

# Train model
output = dask_train(client, params, dtrain, num_boost_round=100)
model = output["booster"]  # trained booster

# Predict on the same data (for demo)
preds = model.predict(X.compute())
preds_label = (preds > 0.5).astype(int)

# Evaluate
y_true = y.compute()
print("Accuracy:", accuracy_score(y_true, preds_label))
print("ROC AUC:", roc_auc_score(y_true, preds))
