#!/usr/bin/env python

import grass.script as gscript
from grass.pygrass.raster import RasterRow
from grass.pygrass.vector import VectorTopo

from lcp.MapAnalyser import MapAnalyser


def main():
    print "name,gesamt_laenge, sekunden, km, stunden, v_durchschnitt, 10_std_tag, 8_std_tag, 6_std_tag"
    # analyse_patch(prefix = 'walk_roads_ad_hydro_ox_e_')
    # analyse_patch(prefix = 'walk_roads_ad_hydro_e_')
    # analyse_patch(prefix = 'walk_roads_f1_ad_hydro_ox_e_')
    # analyse_patch(prefix = 'walk_roads_f1_ad_hydro_e_')
    analyse_single_lcp(prefix='walk_roads_ad_hydro_ox_e_')
    analyse_single_lcp(prefix='walk_roads_da_hydro_ox_e_')
    analyse_single_lcp(prefix='walk_roads_ad_hydro_e_')
    analyse_single_lcp(prefix='walk_roads_da_hydro_e_')
    analyse_single_lcp(prefix='walk_roads_f1_ad_hydro_ox_e_')
    analyse_single_lcp(prefix='walk_roads_f1_da_hydro_ox_e_')
    analyse_single_lcp(prefix='walk_roads_f1_ad_hydro_e_')
    analyse_single_lcp(prefix='walk_roads_f1_da_hydro_e_')


def analyse_patch(prefix):
    # gscript.run_command('g.region', flags='p')
    sum = 0
    sum_length = 0
    analyser = MapAnalyser()
    for i in xrange(30):
        map = prefix + str(i) + '_walk_lcp'
        v_map = 'v_' + map
        values = analyser.analyseLcpMap(map, v_map)
        sum += values.cost
        sum_length += values.length

    printResults(prefix, sum, sum_length)


def analyse_single_lcp(prefix):
    map_name = prefix + '_walk_lcp'
    v_map_name = map_name
    analyser = MapAnalyser()
    values = analyser.analyseLcpMap(map_name, v_map_name)
    printResults(prefix, values.cost, values.length)


def printResults(prefix, sum, sum_length):
    hours = sum / 3600
    km = sum_length / 1000
    v_journey = km / hours
    days_10 = hours / 10
    days_8 = hours / 8
    days_6 = hours / 6
    # print "Ergebnisse fuer " + prefix
    # print "Die Strecke ist %d Meter bzw. %d Sekunden lang" % (sum_length, sum)
    # print "Das entspricht %f km und %f Stunden" % (km, hours)
    # print "Die durchschnittliche Reisegeschwindigkeit betraegt %f km-h" % (v_journey)
    # print "Bei einer maximalen anzahl von 10 std. Gehzeit/Tag braucht man %f Tage" % (days_10)
    # print "Bei einer maximalen anzahl von 8 std. Gehzeit/Tag braucht man %f Tage" % (days_8)
    # print "Bei einer maximalen anzahl von 6 std. Gehzeit/Tag braucht man %f Tage" % (days_6)
    print prefix, ',', sum_length, ',', sum, ',', km, ',', hours, ',', v_journey, ',', days_10, ',', days_8, ',', days_6


if __name__ == '__main__':
    main()
