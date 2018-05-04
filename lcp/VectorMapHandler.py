from grass.pygrass.vector import VectorTopo
from grass.pygrass.vector.table import DBlinks, Link


class VectorMapHandler(object):
    sMapName = ""
    oMap = None
    oDBLink = None
    oTableLink = None

    def __init__(self, sMapName):
        self.sMapName = sMapName

    def open_map_dblink(self):
        self.oMap = VectorTopo(self.sMapName)
        self.oMap.open(mode='r')
        self.oDBLink = DBlinks(self.oMap.c_mapinfo)

    def open_table_cursor(self, layer_id):
        if not isinstance(self.oDBLink, DBlinks):
            self.open_map_dblink()
        self.oTableLink = self.oDBLink[layer_id].table()

    def check_open_table(self):
        if not isinstance(self.oTableLink, Link):
            self.open_table_cursor(0)

    def read_sorted_cats(self, sort='ASC'):
        self.check_open_table()
        self.oTableLink.filters.select('cat').order_by('sort_order ' + sort)

        return self.oTableLink.execute()

    def read_non_ancient_cats(self):
        self.check_open_table()
        self.oTableLink.filters.select('cat').where('ancient = 0').order_by('sort_order ASC')

        return self.oTableLink.execute()