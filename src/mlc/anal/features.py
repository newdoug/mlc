from mlc.anal.binary import (
    BYTE_ARRAY_ANAL_FUNCS,
    BYTE_ARRAYS_ANAL_FUNCS,
    FeatureType,
)


def calculate_all_binary_features(data: bytes) -> dict[str, FeatureType]:
    features = {}
    for func_name, func in BYTE_ARRAY_ANAL_FUNCS.items():
        features[func_name] = func(data)
    return features


def calculate_all_binary_pair_features(data1: bytes, data2: bytes) -> dict[str, FeatureType]:
    features = {}
    for func_name, func in BYTE_ARRAYS_ANAL_FUNCS.items():
        features[func_name] = func(data1, data2)
    return features
