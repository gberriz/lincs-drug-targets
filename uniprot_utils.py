from bioservices import UniProt
import lazydict as ld

_UP = UniProt(verbose=False)

def _fetch_name(uniprot):
    ret = _UP.search(uniprot, columns='entry name').splitlines()[1:]
    assert len(ret) == 1
    return ret[0]


def fetch_name(uniprot=None, _memo=ld.LazyDict(), _reset=False):
    if _reset:
        assert uniprot is None
        return _memo.clear()
    return _memo.setdefault(uniprot, lambda: _fetch_name(uniprot))
