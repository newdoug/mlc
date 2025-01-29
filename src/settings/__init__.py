"""Settings structures/objects"""

#from dataclasses import asdict, dataclass
import dataclasses as dc


@dc.dataclass
class TestData:
    val1: int
    val2: str


d = TestData(42, "abc")
print(d)
print(dir(d))
#print(dict(d))
#print(d.asdict())
print(dc.asdict(d))
