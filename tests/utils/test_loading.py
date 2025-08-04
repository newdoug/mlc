from mlc.utils.loading import get_all_filenames

from ..constants import RESOURCE_DIR


GET_ALL_FILENAMES_RESOURCE_DIR = RESOURCE_DIR / "get_all_filenames"


def test_multi_layers_one_empty_dir():
    """Multiple subdirectories. One is empty (no files)"""
    filenames = get_all_filenames(GET_ALL_FILENAMES_RESOURCE_DIR)
    assert len(filenames) == 3
    assert filenames == [
        str(p)
        for p in [
            GET_ALL_FILENAMES_RESOURCE_DIR / "e.txt",
            GET_ALL_FILENAMES_RESOURCE_DIR / "a" / "d.txt",
            GET_ALL_FILENAMES_RESOURCE_DIR / "a" / "b" / "c.txt",
        ]
    ]
