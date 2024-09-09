import traci

def print_traffic_light_ids():
    # Start the SUMO simulation
    traci.start(["sumo-gui", "-c", "trial.sumocfg"])  # Adjust the command as necessary

    # Retrieve and print all traffic light IDs
    tls_ids = traci.trafficlight.getIDList()
    edges_lis=traci.edge.getIDList()
    print("EDGES",edges_lis)
    print("Traffic lights in the simulation:", tls_ids)

    # Close the simulation
    traci.close()

if __name__ == "__main__":
    print_traffic_light_ids()
