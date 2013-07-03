import sys
import re
import csv
import fileinput as fi
import operator as op
import itertools as it

# operator.itemgetter, annoyingly, behaves differently according to
# whether len(items) == 1 or not, so we must roll our own...

def itemgetter(item, *args):
    return (op.itemgetter(item, *args) if (args or type(item) is slice)
            else lambda ob: (ob[item],))

KEYCOLS = (0,)
VALCOLS = (1,)
KEYS = []
COLLECT = dict()

SEP = '|'


def _complement(cols, n):
    m = len(cols)
    s = set(cols)
    assert m == len(s) < n
    return tuple([i for i in range(n) if not i in cols])


def collapse(seq, keycols=(0,), valcols=None, ncols=None):
    assert keycols or valcols
    if not (keycols and valcols):
        if ncols is None:
            first = next(seq)
            ncols = len(first)
            seq = it.chain((first,), seq)
        assert isinstance(ncols, int)

        if keycols:
            assert not valcols
            valcols = _complement(keycols, ncols)
        else:
            keycols = _complement(valcols, ncols)

    assert keycols and hasattr(keycols, '__iter__')
    assert valcols and hasattr(valcols, '__iter__')
    assert len(keycols) + len(valcols) <= ncols

    keys = []
    collect = dict()

    kig = itemgetter(*keycols)
    vig = itemgetter(*valcols)

    for rec in seq:
        key = kig(rec)
        if key in collect:
            sets = collect[key]
        else:
            sets = collect[key] = tuple([set() for _ in valcols])
            keys.append(key)

        for s, v in zip(sets, vig(rec)):
            s.add(v)

    return ([(k, collect[k]) for k in keys])


def _collapse_one(seq, _sep=SEP):
    return _sep.join(sorted(seq))

if __name__ == '__main__':
    wr = csv.writer(sys.stdout, delimiter='\t', lineterminator='\n')
    for key, vals in collapse(csv.reader(fi.input(), delimiter='\t')):
        wr.writerow(key + tuple([_collapse_one(v) for v in vals]))
