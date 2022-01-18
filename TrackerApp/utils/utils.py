import json

from configparser import ConfigParser

def config(filename='', section=''):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section 
    config = {}
    
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0].upper()] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        
    return config

def convert_lon_lat(lon_lat):
    #this function receives lon_lat as string in format (1234, -5678)
    #and returns string in format { lat : 1234, lng -5678 } which is used in JS
    ll = lon_lat.replace('(','').replace(')','').split(',')
    return "{ lat: " + ll[0] + ", lng: " + ll[1] + " }"

class Marker():

    current_loc = ""
    current_dest = ""
    label_nrs = ["e400", "e401", "e3fb", "e3fd", "e3fe", "e3ff"  ]
    label_destination = "e177"
    label_transit = "e569"
    label_car = "e62c"
    label_list = []
    text_list = []
    loc_list = []
    length = 0

    def __init__(self):
        self.current_loc = ""
        self.current_dest = ""
        self.label_list = []
        self.text_list = []
        self.loc_list = []
        self.length = 0
        
