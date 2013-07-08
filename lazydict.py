class LazyDict(dict):
    def get(self, key, thunk=None):
        return (self[key] if key in self else
                thunk() if callable(thunk) else
                thunk)


    def setdefault(self, key, thunk=None, _setdefault=dict.setdefault):
        return (self[key] if key in self else
                _setdefault(self, key,
                            thunk() if callable(thunk) else
                            thunk))
