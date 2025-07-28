import json
import os

from .features import calculate_all_binary_features


def main():
    for idx in range(1, 4):
        features = calculate_all_binary_features(os.urandom(32 * idx))
        print(json.dumps(features, indent=2))


if __name__ == "__main__":
    main()
