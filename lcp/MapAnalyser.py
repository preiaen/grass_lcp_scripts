from grass.pygrass.raster import RasterRow
from grass.pygrass.vector import VectorTopo


class AnalysisData(object):
    length = 0
    cost = 0


class MapAnalyser(object):
    def analyseLcpMap(self, rast_map_name, vect_map_name):
        result = AnalysisData()

        self._readCost(rast_map_name, result)

        self._readLength(result, vect_map_name)

        return result

    def _readLength(self, result, vect_map_name):
        v_lcp = VectorTopo(vect_map_name)
        if v_lcp.exist():
            v_lcp.open(mode='r')
            result.length = v_lcp.read(1).length()
            v_lcp.close()

    def _readCost(self, rast_map_name, result):
        lcp = RasterRow(rast_map_name)
        if lcp.exist():
            lcp.open()
            result.cost = lcp.info.range[1]
            lcp.close()