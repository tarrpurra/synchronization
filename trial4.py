import traci

VEHICLE_THRESHOLD = 8

def adaptive_green_phase(tls_id, vehicle_count, base_duration=30, max_extension=20):
    extended_duration = min(base_duration + vehicle_count, base_duration + max_extension)
    traci.trafficlight.setPhaseDuration(tls_id, extended_duration)

def is_vehicle_near_signal(edge_id, distance_threshold=50):
    vehicle_ids = traci.edge.getLastStepVehicleIDs(edge_id)
    stopped_vehicles = 0
    for vehicle_id in vehicle_ids:
        vehicle_position = traci.vehicle.getLanePosition(vehicle_id)
        vehicle_speed = traci.vehicle.getSpeed(vehicle_id)
        if vehicle_position <= distance_threshold and vehicle_speed == 0:
            stopped_vehicles += 1
    return stopped_vehicles

def synchronize_traffic_lights(tls_ids, edge_mapping):
    for tls_id, edges in edge_mapping.items():
        total_stopped_vehicles = sum(is_vehicle_near_signal(edge) for edge in edges)
        if total_stopped_vehicles >= VEHICLE_THRESHOLD:
            adaptive_green_phase(tls_id, total_stopped_vehicles)
        # Additional green wave synchronization logic here

def main():
    sumoCmd = ["sumo-gui", "-c", "trial.sumocfg"]
    traci.start(sumoCmd)
    edge_mapping = { "J33": [':J33_0'], "J34": [':J34_0'] }
    
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        tls_ids = traci.trafficlight.getIDList()
        synchronize_traffic_lights(tls_ids, edge_mapping)

    traci.close()

if __name__ == '__main__':
    main()
