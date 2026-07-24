import pytest 

@pytest.mark.parametrize("a, b, c", [
    (2, 3, 5),
    (3, 5, 8)
])
def test_add(a, b, c):
    assert a + b == c

def test_multiply():
    assert 3 == 3


def demo():
    assert 3 == 3