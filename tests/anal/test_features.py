import json
import os

import pytest

from mlc.anal.binary import FeatureType
from mlc.anal.features import calculate_all_binary_features


def test_doesnt_raise_exception_on_nonempty_data():
    """There are a lot of functions that execute. Make sure they generally work on nonempty data"""
    for idx in range(1, 4):
        calculate_all_binary_features(os.urandom(32 * idx))


def test_unsupported_length_data_behavior():
    """Don't really care if we don't support empty data. Not a useful use case enough for us to
    slow down every function by checking for empty data or checking for types.
    """
    with pytest.raises(Exception):
        calculate_all_binary_features(b"")
        for _ in range(255):
            calculate_all_binary_features(os.urandom(1))
        calculate_all_binary_features(os.urandom(b"\x00"))
        calculate_all_binary_features(os.urandom(b"\xff"))
        for unsupported_len in range(1, 8):
            calculate_all_binary_features(os.urandom(unsupported_len))


def test_features_dict_valid_types():
    for idx in range(1, 4):
        features = calculate_all_binary_features(os.urandom(32 * idx))
        assert isinstance(features, dict)
        for k, v in features.items():
            assert isinstance(k, str)
            assert len(k) > 0
            assert isinstance(v, FeatureType)
            assert v is not None


def test_features_dict_is_json_serializable():
    """Would be useful and isn't much to require"""
    # This is generally true assuming the types are correct, which is checked by an earlier test
    for idx in range(1, 4):
        features = calculate_all_binary_features(os.urandom(32 * idx))
        # Test that this doesn't raise an exception
        json.dumps(features)
