import csv
from model import machine


class DataLoader:

    @staticmethod
    def load_machine_details(csv_file_name):
        machines = []
        """" assume data is getting loaded from respective data store. """
        with open('{}\\{}'.format('C:\\Users\\padaldl\\workspace\\practice\\FriInnov2019\\datastore', csv_file_name),
                  'rt') as f:
            data = csv.DictReader(f)
            for row in data:
                m = machine.Machine(serial_number=row.get('SerialNumber'),
                                    machine_type=row.get('Type'),
                                    latitude=row.get('Latitude'),
                                    longitude=row.get('Longitude'),
                                    fuel_level=row.get('Fuel'))
                machines.append(m)

        return machines
