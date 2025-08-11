from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from joblib import dump, load

# Create data
X, y = make_classification(n_samples=10000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save the model
dump(model, "logreg_model.joblib")

# Load the model
loaded_model = load("logreg_model.joblib")

# Use it
print("Accuracy:", loaded_model.score(X_test, y_test))


# Ex 2: Run a function in parallel across CPU cores

from joblib import Parallel, delayed
import math


def slow_square(x):
    return math.sqrt(x**2)


results = Parallel(n_jobs=4)(delayed(slow_square)(i) for i in range(10))
print(results)


# Caching computation
from joblib import Memory
import os

memory = Memory(location="cachedir", verbose=0)


@memory.cache
def slow_function(x):
    import time

    time.sleep(2)
    return x * 2


# First call is slow
print(slow_function(10))  # Takes ~2 seconds

# Second call is fast (cached)
print(slow_function(10))  # Instant
