import traci
import time  # Import the time module to measure elapsed time

# Constants for traffic light phases
GREEN_DURATION = 30  # Duration of green phase in seconds
YELLOW_DURATION = 5  # Duration of yellow phase in seconds
RED_DURATION = 30    # Duration of red phase in seconds
CYCLE_TIME = GREEN_DURATION + YELLOW_DURATION + RED_DURATION  # Total cycle time

def synchronize_traffic_lights(tls_ids):
    current_time = traci.simulation.getTime()
    for tls_id in tls_ids:
        # Get current phase information
        current_phase = traci.trafficlight.getPhase(tls_id)
        current_duration = traci.trafficlight.getPhaseDuration(tls_id)
        
        # Calculate synchronized phase
        phase_index = int((current_time % CYCLE_TIME) / (CYCLE_TIME / 4))  # Assuming 4 phases
        traci.trafficlight.setPhase(tls_id, phase_index)
        print(f"Traffic light {tls_id} synchronized to phase {phase_index}.")

def adjust_traffic_lights(tls_ids, edge_ids, threshold=10):
    for tls_id in tls_ids:
        # Aggregate vehicle counts from all edges
        total_vehicle_count = sum(traci.edge.getLastStepVehicleNumber(edge_id) for edge_id in edge_ids)
        
        # Adjust phase duration based on aggregated vehicle count
        if total_vehicle_count > threshold:
            traci.trafficlight.setPhaseDuration(tls_id, GREEN_DURATION + 10)  # Extend green phase
        else:
            traci.trafficlight.setPhaseDuration(tls_id, GREEN_DURATION)

def main():
    # Start SUMO simulation
    sumoCmd = ["sumo-gui", "-c", "trial.sumocfg"]  # or "sumo" for non-GUI mode
    traci.start(sumoCmd)

    # Start timer
    start_time = time.time()

    # Define edge-to-traffic-light mappings
    edge_mapping = {
        "J33": [':J33_0', ':J34_0', ':J38_0', ':J39_0'],
        "J34": [':J34_0', ':J35_0', ':J36_0', ':J33_0', ':J37_0'],
        "J35": [':J35_0', ':J41_0', ':J40_0', ':J34_0'],
        "J36": [':J36_0', ':J40_0', ':J39_0', ':J34_0'],
        "J37": [':J37_0', ':J38_0']
    }
    
    # Get all traffic light IDs in the network
    tls_ids = traci.trafficlight.getIDList()  
    
    # Run the simulation
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:  # Stop when no more vehicles are expected
        traci.simulationStep()
        
        # Synchronize traffic lights
        synchronize_traffic_lights(tls_ids)
        
        # Adjust traffic light durations based on vehicle counts
        for tls_id, edge_ids in edge_mapping.items():
            adjust_traffic_lights([tls_id], edge_ids)
        
        step += 1
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Simulation completed in {total_time:.2f} seconds.")
    
    # End timer and calculate total time

    # Close the simulation
    traci.close()

    # Display the total simulation time

if __name__ == '__main__':
    main()
