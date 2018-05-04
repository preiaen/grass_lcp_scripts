from grass.script import run_command
from grass.pygrass.vector import VectorTopo
from grass.pygrass.raster import RasterRow


class CalcSettings(object):
    """Data Object for the different possible settings"""

    walk_param = "0.72,6.0,1.9998,-1.9998"
    slope_fact = -0.2125
    file_prefix = ""
    walk_direction_lable = ""
    formula = 0
    start_point = None
    stop_point = None
    move_type = "k"
    friction = "friction@PERMANENT"

    def __init__(self, file_prefix, **kwargs):
        self.file_prefix = file_prefix
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def get_file_name(self, *args, **kwargs):
        add_key_val = ""
        add = ""
        for val in args:
            add += '{}'.format(val)
        for key, value in kwargs.items():
            add_key_val += '{}_{}'.format(key, value)

        return self.file_prefix + self.walk_direction_lable + add + add_key_val


class AreaAnalyser(object):
    def __init__(self, aAreaMapNames):
        self.aMapNames = aAreaMapNames

    def analyseArea(self):

        for name in self.aMapNames:
            lcp_name = short_name = name[:-10]
            lcp_name += '_walk_lcp'
            cur_map = VectorTopo(name)
            if cur_map.exist():
                lcp_rast = RasterRow(lcp_name)
                lcp_rast.open('r')
                max = lcp_rast.info.range[1]

                lcp_vec = VectorTopo(lcp_name)
                lcp_vec.open('r')
                len = lcp_vec.read(1).length()
                cur_map.open(mode='r')

                areas = []
                for boundary in cur_map.viter('areas'):
                    areas.append(boundary.area())
                print short_name,',',reduce(lambda x,y: x+y,areas),',',str(len),',',str(max)


class ModuleController(object):
    oCalcSettings = None
    aMapNames = []

    def __init__(self, oCalcSettings):
        self.oCalcSettings = oCalcSettings
        self.aMapNames = []

    def run_walk(self, start_coor, stop_coor, id):
        prefix = self.oCalcSettings.get_file_name(id)
        out_cost = prefix + "_walk_cost"
        out_dir = prefix + "_walk_dir"

        run_command("r.walk.roads",
                    flags=self.oCalcSettings.move_type,
                    overwrite=True,
                    elevation="elevation@PERMANENT",
                    friction=self.oCalcSettings.friction,
                    output=out_cost,
                    outdir=out_dir,
                    start_coordinates=start_coor,
                    stop_coordinates=stop_coor,
                    max_cost=0,
                    memory=300,
                    formula=self.oCalcSettings.formula,
                    walk_coeff=self.oCalcSettings.walk_param,
                    slope_factor=self.oCalcSettings.slope_fact)
        return 0

    def run_drain(self, start_coor, id):
        prefix = self.oCalcSettings.get_file_name(id)
        in_cost = prefix + "_walk_cost"
        in_dir = prefix + "_walk_dir"
        out_rast = prefix + "_walk_lcp"
        out_vect = "v_" + out_rast
        run_command("r.drain",
                    flags='dc',
                    overwrite=True,
                    input=in_cost,
                    direction=in_dir,
                    output=out_rast,
                    drain=out_vect,
                    start_coordinates=start_coor)
        self.aMapNames.append(out_vect)
        return 0

    def run_walk_points(self, quite=True):
        prefix = self.oCalcSettings.get_file_name()
        out_cost = prefix + "_walk_cost"
        out_dir = prefix + "_walk_dir"
        run_command("r.walk.roads",
                    flags=self.oCalcSettings.move_type,
                    overwrite=True,
                    quiet=quite,
                    elevation="elevation@PERMANENT",
                    friction=self.oCalcSettings.friction,
                    output=out_cost,
                    outdir=out_dir,
                    start_points=self.oCalcSettings.start_point,
                    max_cost=0,
                    memory=300,
                    formula=self.oCalcSettings.formula,
                    walk_coeff=self.oCalcSettings.walk_param,
                    slope_factor=self.oCalcSettings.slope_fact)
        return 0

    def run_drain_points(self, quite=True):
        prefix = self.oCalcSettings.get_file_name()
        in_cost = prefix + "_walk_cost"
        in_dir = prefix + "_walk_dir"
        out_rast = prefix + "_walk_lcp"
        out_vect = out_rast
        run_command("r.drain",
                    flags='dc',
                    overwrite=True,
                    quiet=quite,
                    input=in_cost,
                    direction=in_dir,
                    output=out_rast,
                    drain=out_vect,
                    start_points=self.oCalcSettings.stop_point)
        self.aMapNames.append(out_vect)
        return 0

    def run_patch(self):
        prefix = self.oCalcSettings.get_file_name()
        input_maps = ','.join(self.aMapNames)
        output = prefix + "patch_lcp"
        run_command("v.patch",
                    overwrite=True,
                    input=input_maps,
                    output=output)
        self.aMapNames = []
        return 0

    def run_patch_or_area(self):
        prefix = self.oCalcSettings.get_file_name()
        input_maps = ','.join(self.aMapNames)
        input_maps += ',oinoe_road'
        output = prefix + "_area"
        run_command("v.patch",
                    overwrite=True,
                    quiet=True,
                    input=input_maps,
                    output=output)

        run_command("v.clean",
                    overwrite=True,
                    input=output,
                    quiet=True,
                    output=output + '_clean',
                    tool="snap,break,rmdupl,rmsa",
                    flags="c",
                    threshold="13.0,2.0")

        run_command("v.type",
                    overwrite=True,
                    quiet=True,
                    input=output + '_clean',
                    output=output + '_type')

        run_command("v.centroids",
                    overwrite=True,
                    quiet=True,
                    input=output + '_type',
                    output=output + '_cent')

        self.aMapNames = []
        return output + '_cent'

    def run_modules(self, aStartPoint, aStopPoint):
        """
             runs first r_walk and then r_drain
             expects both input parameters to be arrays with
             a cat as a first element
        """
        id = aStartPoint[0]
        start_p = aStartPoint[1]
        stop_p = aStopPoint[1]
        self.run_walk(start_p.coords(), stop_p.coords(), id)
        self.run_drain(stop_p.coords(), id)
        return 0
