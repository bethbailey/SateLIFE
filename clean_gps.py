import gpxpy 
import gpxpy.gpx 
import os
import xml.etree.ElementTree

# AUTHOR: Cooper Nederhood, all code original
''' CODE PURPOSE: 
    The main platform/data source of satellite imagery, Google Earth Engine, does not include geometries to designate
    neighborhoods within Kinshasa. These ARE available in OpenStreetMaps as .gpx files (an XML schema used by OpenStreetMaps).
    The below programs parse the .gpx files, create a txt file containing code compatable with Google Earth Engine, 
    which must then be pasted into the Google Earth Engine code editor, which uses javascript
'''

# hardcoded path is temporary
PATH = "/home/cooper/Documents/SateLIFE/data/"

DECODE = {
 'Kasa-Vubu': 1,
 'Nsele': 2,
 'Kintambo': 3,
 'Ngaliema': 4,
 'Bumbu': 5,
 'Mont-Ngafula': 6,
 'Maluku': 7,
 'Masina': 8,
 'Lemba': 9,
 'Gombe': 10,
 'Selembao': 11,
 'Ngiri-Ngiri': 12,
 'Kimbanseke': 13,
 'Ngaba': 14,
 'Kinshasa': 15,
 'Bandalungwa': 16,
 'Makala': 17,
 'Kalamu': 18,
 'Matete': 19,
 'Ndjili': 20,
 'Lingwala': 21,
 'Kisenso': 22,
 'Barumbu': 23,
 'Limete': 24,

 }

def clean_OSM_API(file, code):
    '''
    Given a .xml file from an OpenStreetMaps API query, parses
    the file and returns the long, lat boundaries
    '''

    e = xml.etree.ElementTree.parse(PATH+"osm_API/"+file).getroot()
    country = file

    l = []

    for atype in e.findall('node'):
        print("Long: ", atype.get('lon'))
        print("Lat: ", atype.get('lat'))
        l.append(str(atype.get('lon')))
        l.append(str(atype.get('lat')))

    all_pts = ",".join(l)
    output_string = "ee.Feature(ee.Geometry.Polygon( {} ), {{ name:'{}', code:{} }}) ".format(all_pts, country, code)

    return output_string

def clean_city_gps(file, code):
    '''
    Given a string filename of a shape file
    containing coordinates defining a neighborhood
    in Kinshasa
    '''

    gpx_file = open(PATH + "geojson/"+file, 'r')
    country = file.replace(".gpx", "")

    gpx = gpxpy.parse(gpx_file)

    route = gpx.routes[0]
    assert len(gpx.routes) == 1

    points = route.points
    output_string = ""

    l = []

    for p in points:
        l.append(str(p.longitude))
        l.append(str(p.latitude))

    all_pts = ",".join(l)
    output_string = "ee.Feature(ee.Geometry.Polygon( {} ), {{ name:'{}', code:{} }}) ".format(all_pts, country, code)

    return output_string


def create_earth_engine_code(country_code_map, output_filename):
    '''
    Loops over all .gpx files in the global PATH directory,
    creating the google Earth Engine code to define the corresponding
    geometry. Figures out the numeric code using the country_code_map

    Writes a string to an output file, and this output file can
    then be run in Google Earth Engine's Code Editor API
    '''

    f = open(output_filename, 'w')
    f.write('INSTRUCTIONS: below is code that can be pasted into Google Earth Engine to create boundaries for Kinshasa')
    f.write('\t The code creates a list of Earth Engine geometries which can then be aggregated and cast as a raster file for export')
    f.write('\n\n\n')
    f.write('var features = [')
    f.write('\n\n')

    gpx_files = [x for x in os.listdir(PATH) if ".gpx" in x]
    command_list = []

    for file in gpx_files:
        country = file.replace(".gpx", "")
        s = clean_city_gps(file, code=country_code_map[country])
        command_list.append(s)


    command_str = ", \n".join(command_list)

    f.write(command_str)
    f.write("\n ] \n")
    f.write("\n END OF GOOGLE EARTH ENGINE CODE")
    f.close()

    return command_str 

