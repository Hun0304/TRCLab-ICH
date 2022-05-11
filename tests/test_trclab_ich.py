import sys
sys.path.append("../src")
from trclab_ich import TRCLabICH

def test_get_true_func():
    assert TRCLabICH.get_true() is True

