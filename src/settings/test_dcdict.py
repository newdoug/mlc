import dataclasses as dc

@dc.dataclass
class A:
    val1: int
    val2: str
    val3: int = 6
    val4: float = 6.2


a = A(2, "abc")
d = dc.asdict(a)
a2 = A(**d)
d2 = dc.asdict(a2)
print(a == a2)
print(d == d2)
