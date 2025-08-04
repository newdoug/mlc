import os

from mlc.anal.oeis import OEIS_SEQ_BASE_DIR, OeisSequence
from mlc.utils.loading import get_all_filenames


def test_all_files_are_valid():
    """Gets every .seq file and creates OeisSequence with it. Nothing should raise an exception"""
    for filename in get_all_filenames(OEIS_SEQ_BASE_DIR):
        seq_id = os.path.splitext(os.path.basename(filename))[0]
        seq = OeisSequence(seq_id)
        assert seq.seq_id == seq_id
        assert seq.seq_filename.samefile(filename)
        assert len(seq.seq_values) > 0
