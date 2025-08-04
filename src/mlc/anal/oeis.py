"""Managing OEIS (Online Encyclopedia of Integer Sequences) usage"""

from mlc.utils.constants import ROOT_DIR


OEIS_ROOT_DIR = ROOT_DIR / "oeisdata"
OEIS_SEQ_BASE_DIR = OEIS_ROOT_DIR / "seq"
# The oeisdata repo uses directories using first few characters of the A ID. E.g. "A000/A000982.seq"
SEQ_DIR_LEN = 4


class OeisSequence:
    """A single OEIS sequence"""

    def __init__(self, a_seq_id: str, autoload: bool = True):
        a_seq_id = (a_seq_id or "").upper()
        if not a_seq_id or not a_seq_id.startswith("A"):
            raise ValueError(f"Invalid OEIS sequence number '{a_seq_id}'")
        self.seq_id = a_seq_id
        self.seq_filename = OEIS_SEQ_BASE_DIR / self.seq_id[:SEQ_DIR_LEN] / f"{self.seq_id}.seq"
        self.seq_values: list[int] = []
        if autoload:
            self.load_static_info()

    def load_static_info(self) -> None:
        """.seq files from OEIS statically list the first N values of the sequence. That's what this function does."""
        seq_name = None
        seq_formula = None
        seq_values = []
        with open(self.seq_filename, "r", encoding="UTF-8") as handle:
            for line in handle.readlines():
                line = line.strip()
                # E.g., '%S A000982 ' ...
                if len(line) < 11:
                    continue
                split = line.split()
                if split[1] != self.seq_id:
                    raise ValueError(
                        f"Sequence ID in file '{self.seq_filename}' was '{split[1]}' when it "
                        f"should have been '{self.seq_id}'"
                    )

                # Static initial members of the sequence
                if split[0] in ("%S", "%T", "%U"):
                    nums_list = "".join(split[2:])
                    for num in nums_list.split(","):
                        # Empty string usually (lines sometimes end in ',')
                        if not num:
                            continue
                        seq_values.append(int(num.strip()))

                # Sequence name. May also be the formula
                if split[0] == "%N":
                    if seq_name:
                        raise ValueError(
                            f"OEIS sequence file '{self.seq_filename}' had more than one %N line"
                        )
                    seq_name = " ".join(split[2:])

                # Sequence formula. Optional and may be provided in the sequence name field
                if split[0] == "%F":
                    seq_formula = " ".join(split[2:])

        if not seq_values or not seq_name:
            raise ValueError(f"OEIS file '{self.seq_filename}' was missing required field(s)")

        self.seq_values = seq_values
        self.seq_name = seq_name
        self.seq_formula = seq_formula or seq_name

    def load_extra_members(self, desired_num_values: int) -> None:
        """Use the generic formula provided by the OEIS file and calculate the next N values of
        the sequence.
        Will likely try to use Maple, Wolphram Alpha, Mathematica, some similar library, etc.
        Unfortunately, the formula doesn't appear to be in a consistent, standard format.
        `desired_num_values` is the total number of members the caller wants in self.seq_values.
        Therefore, if self.seq_values already has <= `desired_num_values` members, this call does
        nothing.
        """
        if desired_num_values <= len(self.seq_values):
            return
        # TODO
        raise NotImplementedError()
