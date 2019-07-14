"""Vehicles Routing Problem (VRP)."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


class VRPSolution:
    tot_distance = 0
    route_map = []

    def __init__(self, distance, map):
        self.tot_distance = distance
        self.route_map = map


def build_solution(data, manager, routing, solution):
    """Prints solution on console."""
    sol_dict = {}
    max_route_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        # plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        index_route_map = []
        while not routing.IsEnd(index):
            index_route_map.append(manager.IndexToNode(index))
            # plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        index_route_map.append(manager.IndexToNode(index))
        """" solution """
        sol_dict['Fuel Truck-{}'.format(vehicle_id)] = VRPSolution(route_distance, index_route_map)

        # plan_output += '{}\n'.format(manager.IndexToNode(index))
        # plan_output += 'Distance of the route: {}km\n'.format(route_distance)
        # print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    # print('Maximum of the route distances: {}km'.format(max_route_distance))
    return sol_dict


def solve(data):
    """Solve the CVRP problem."""

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        return build_solution(data, manager, routing, solution)
    else:
        return {}