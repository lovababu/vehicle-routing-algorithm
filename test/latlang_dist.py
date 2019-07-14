# from model import machine

from service import vrpservice
from util import vrp_algorithm


def main():
    """Solve the CVRP problem."""
    vrp = vrpservice.VRPService()
    data_dict = vrp.build_dist_matrix('bangalore_pins.csv', 1)
    sol_dict = vrp_algorithm.solve(data_dict)
    print_route_map(data_dict['machines'], sol_dict)


def print_route_map(machines, sol):
    """"Printing route map. """
    for k, v in sol.items():
        print('Route for vehicle {}:\n'.format(k))
        m = []
        for i in v.route_map:
            m.append(machines[i].sNumber)

        print(' -> '.join(m))
        print("Total distance covered by {} is {}km".format(k, v.tot_distance))
        print('\n')


if __name__ == '__main__':
    main()




