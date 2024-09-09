import traci

# Threshold for number of vehicles to trigger green light
VEHICLE_THRESHOLD = 8

def is_vehicle_near_signal(edge_id, distance_threshold=50):
    """
    Check if any vehicle is within a certain distance from the traffic light signal on the specified edge.
    """
    vehicle_ids = traci.edge.getLastStepVehicleIDs(edge_id)
    
    stopped_vehicles = 0
    for vehicle_id in vehicle_ids:
        # Get the position and speed of the vehicle on the edge
        vehicle_position = traci.vehicle.getLanePosition(vehicle_id)
        vehicle_speed = traci.vehicle.getSpeed(vehicle_id)

        # Check if the vehicle is within the distance threshold and is stopped
        if vehicle_position <= distance_threshold and vehicle_speed == 0:
            stopped_vehicles += 1
    
    return stopped_vehicles

def synchronization(tls_id, edge_mapping):
    """
    Synchronize traffic light if the number of stopped vehicles exceeds the threshold.
    """
    for tls, edges in edge_mapping.items():
        # Get the total number of stopped vehicles near the traffic light
        total_stopped_vehicles = sum(is_vehicle_near_signal(edge) for edge in edges)
        
        # If the number of stopped vehicles exceeds the threshold, switch to green
        if total_stopped_vehicles >= VEHICLE_THRESHOLD:
            # Set the traffic light to green for this traffic light
            traci.trafficlight.setPhase(tls_id, 0)  # Phase 0 is usually green, adjust if needed
            print(f"Setting traffic light {tls_id} to green. Stopped vehicles: {total_stopped_vehicles}")
        else:
            print(f"Traffic light {tls_id} stays on current phase. Stopped vehicles: {total_stopped_vehicles}")

def main():
    sumoCmd = ["sumo-gui", "-c", "trial.sumocfg"]  # Adjust the command as necessary
    traci.start(sumoCmd)
    
    # Define edge-to-traffic-light mappings
    edge_mapping = {
        "J33": [':J33_0', ':J34_0', ':J38_0', ':J39_0'],
        "J34": [':J34_0', ':J35_0', ':J36_0', ':J33_0', ':J37_0'],
        "J35": [':J35_0', ':J41_0', ':J40_0', ':J34_0'],
        "J36": [':J36_0', ':J40_0', ':J39_0', ':J34_0'],
        "J37": [':J37_0', ':J38_0']
    }

    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:  # Run simulation for 1000 steps
        traci.simulationStep()
        
        # Get all traffic light IDs
        tls_ids = traci.trafficlight.getIDList()    

        # Synchronize the traffic lights based on vehicle counts
        for tls_id in tls_ids:
            synchronization(tls_id, edge_mapping)
        
        step += 1
    
    # Close the simulation
    traci.close()

if __name__ == '__main__':
    main()
