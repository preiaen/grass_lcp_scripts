from . import ModuleController
from . import VectorMapHandler


class LcpCalculator(object):
    oMapHandler = None # type: VectorMapHandler
    oModuleController = None # type: ModuleController
    aSortedCats = None

    def __init__(self, oMapHandler, oModuleController):
        self.oMapHandler = oMapHandler
        self.oModuleController = oModuleController
        self.aSortedCats = oMapHandler.read_sorted_cats()

    def get_point(self, cat):
        return [ cat[0],  self.oMapHandler.oMap.read(cat[0]) ]

    def get_next_point(self):
        cat = self.aSortedCats.fetchone()
        return self.get_point(cat)

    def run_calc(self, mode='f'):
        if mode == 'r':
            self.aSortedCats = self.oMapHandler.read_sorted_cats('DESC')
        if mode == 'na':
            self.aSortedCats = self.oMapHandler.read_non_ancient_cats()
        start_point = self.get_next_point()
        end_point = self.get_next_point()
        for cat in self.aSortedCats:
            self.oModuleController.run_modules(start_point, end_point)
            start_point = end_point
            end_point = self.get_point(cat)


        self.oModuleController.run_modules(start_point, end_point)
        self.oModuleController.run_patch()