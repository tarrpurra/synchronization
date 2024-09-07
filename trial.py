import traci
import time

# Constants for traffic light phases
GREEN_DURATION = 30  # Duration of green phase in seconds

def adjust_traffic_lights(tls_ids, edge_ids, threshold=10):
    existing_tls_ids = traci.trafficlight.getIDList()
    print("Existing traffic lights:", existing_tls_ids)
    
    for tls_id in tls_ids:
        if tls_id in existing_tls_ids:
            for edge_id in edge_ids:
                if traci.edge.exists(edge_id):
                    vehicle_count = traci.edge.getLastStepVehicleNumber(edge_id)
                    if vehicle_count > threshold:
                        try:
                            traci.trafficlight.setPhaseDuration(tls_id, GREEN_DURATION + 10)  # Extend green phase
                            print(f"Adjusted green phase duration for {tls_id} based on vehicle count.")
                        except traci.exceptions.TraCIException as e:
                            print(f"Error adjusting traffic light {tls_id}: {e}")
                    else:
                        try:
                            traci.trafficlight.setPhaseDuration(tls_id, GREEN_DURATION)
                            print(f"Set default green phase duration for {tls_id}.")
                        except traci.exceptions.TraCIException as e:
                            print(f"Error adjusting traffic light {tls_id}: {e}")
                else:
                    print(f"Edge {edge_id} is not known.")
        else:
            print(f"Traffic light {tls_id} is not known.")

def main():
    # Start SUMO simulation
    sumoCmd = ["sumo-gui", "-c", "trial.sumocfg"]  # Adjust the command as necessary
    traci.start(sumoCmd)

    start_time = time.time()

    # Define edge-to-traffic-light mappings
    edge_mapping = {
        "tls_1": [":J33_0", ":J34_0"],
        "tls_2": [":J35_0", ":J36_0"],
        # Add more mappings as needed
    }
    
    # Run the simulation
    step = 0
    tls_ids = traci.trafficlight.getIDList()  # Get all traffic light IDs in the network

    while step < 1000:  # Simulate for 1000 steps
        traci.simulationStep()
        
        # Adjust traffic light durations based on vehicle counts
        for tls_id, edge_ids in edge_mapping.items():
            adjust_traffic_lights([tls_id], edge_ids)
        
        step += 1
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Simulation completed in {total_time:.2f} seconds.")
    # Close the simulation
    traci.close()

if __name__ == '__main__':
    main()
