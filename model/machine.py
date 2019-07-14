from math import radians, sin, cos, acos


class Machine:
    sNumber = ""
    mType = ""
    fLevel = 0
    fEconomy = 0
    lat = 0.0
    lon = 0.0

    def __init__(self, serial_number, machine_type, latitude, longitude, fuel_level, fuel_economy=0.0):
        self.sNumber = serial_number
        self.mType = machine_type
        self.fLevel = fuel_level
        self.fEconomy = fuel_economy
        self.lat = latitude
        self.lon = longitude

    def distance(self, dest):
        slat = radians(float(self.lat))
        slon = radians(float(self.lon))
        elat = radians(float(dest.lat))
        elon = radians(float(dest.lon))
        dist = round(6371.01 * acos(sin(slat) * sin(elat) + cos(slat) * cos(elat) * cos(slon - elon)), 2)
        return dist
