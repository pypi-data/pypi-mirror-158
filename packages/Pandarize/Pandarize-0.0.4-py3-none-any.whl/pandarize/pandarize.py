import pandas as pd
from pandarize import _util

class Pandarizer:
    def __init__(self):
        self.raw = None
        self.df = None

    def load(self, source=None):
        '''Loads data from the source

        TODO: source type inference
        '''

        self.raw = _util.url_loader(url=source)

    def fit(self, kind='bib'):
        '''Method that infers data structure (in the future)
        '''
        if kind == 'bib':
            self.df = _util.bib_parser(raw=self.raw)

