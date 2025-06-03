#!/usr/bin/env bash

poetry add pycryptodome cryptography zstd pyyaml pandas numpy scikit-learn xgboost lightgbm shap lime optuna zstd pyyaml pandas numpy joblib boruta seaborn matplotlib umap-learn  'distributed' 'ray[default]' 'psycopg[binary]' 'asyncpg' 'alembic' 'sqlalchemy[asyncio]' 'pydantic' 'sqlmodel'

poetry add --dev pytest black pre-commit pytest-mock pytest-cov pytest-random-order pytest-xdist tox
