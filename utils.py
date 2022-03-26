import yaml


class Config:
    def __init__(self, file):
        super().__init__()
        with open(file) as f:
            self._dict = yaml.load(f, Loader=yaml.FullLoader)

    def __getattr__(self, name):
        return self._dict[name]

    def getDict(self):
        return self._dict

    def __getstate__(self):
        return self._dict

    def __setstate__(self, state):
        self._dict = state
