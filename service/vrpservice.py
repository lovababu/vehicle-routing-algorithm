from repository import dataload


def print_matrix(matrix):
    print("*" * 10 + " Distance Matrix Start " + "*" * 10)
    for row in matrix:
        row = ' | '.join(map(str, row))
        print('-' * len(row))
        print(row)

    print("*" * 10 + "  Distance Matrix End  " + "*" * 10)


class VRPService:

    def build_dist_matrix(self, csv_file_name, no_of_fuel_tanks):
        data = {'depot': 0}
        machines = dataload.DataLoader.load_machine_details(csv_file_name)
        data['num_vehicles'] = no_of_fuel_tanks
        data['distance_matrix'] = self.__prep_dist_matrix(machines)
        data['machines'] = machines
        # print_matrix(data['distance_matrix'])
        return data

    @staticmethod
    def __prep_dist_matrix(machine_list):
        no_of_machines = len(machine_list)
        matrix = []
        for i in range(0, no_of_machines):  # inclusive
            row_y = []
            for j in range(0, no_of_machines):
                if i == j:
                    row_y.append(0)
                else:
                    dist = machine_list[i].distance(machine_list[j])
                    row_y.append(dist)

            matrix.append(row_y)

        return matrix

