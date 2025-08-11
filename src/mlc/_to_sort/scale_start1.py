"""
 Distributed XGBoost

You can run distributed XGBoost using:

    Dask (dask-xgboost)

    Spark (xgboost4j-spark)

    Ray
"""

from dask.distributed import Client
from dask_ml.model_selection import train_test_split
import dask.dataframe as dd
import xgboost as xgb
from dask import array as da

client = Client("scheduler-address:port")

dask_df = dd.read_csv("bigdata.csv")
X = dask_df.drop("target", axis=1)
y = dask_df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y)

dtrain = xgb.dask.DaskDMatrix(client, X_train, y_train)
params = {"objective": "binary:logistic", "eval_metric": "auc"}
output = xgb.dask.train(client, params, dtrain, num_boost_round=100)
