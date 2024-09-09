import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet } from "react-native";
import { AnimatedCircularProgress } from "react-native-circular-progress";

const App = () => {
  const [speed, setSpeed] = useState(0);

  useEffect(() => {
    // Set an interval to generate random speed between 10 and 50 km/h
    const interval = setInterval(() => {
      const randomSpeed = Math.floor(Math.random() * 41) + 10;
      // Speed between 10 and 50
      setSpeed(randomSpeed);
    }, 2000); // Update every 2 seconds

    // Clean up the interval when the component unmounts
    return () => clearInterval(interval);
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title2}>Speed Synch App</Text>

      <Text style={styles.title1}>Your Current speed is </Text>

      <AnimatedCircularProgress
        size={150}
        width={15}
        fill={(speed / 100) * 100} // Percentage based on max speed 50 km/h
        tintColor="#ff0000"
        backgroundColor="#d3d3d3"
        rotation={0}
      >
        {() => <Text style={styles.speedText1}>{speed + 7} km/h</Text>}
      </AnimatedCircularProgress>
      <Text style={styles.title}>Maintain a constant speed of </Text>

      <AnimatedCircularProgress
        size={200}
        width={15}
        fill={(speed / 100) * 100} // Percentage based on max speed 50 km/h
        tintColor="blue"
        backgroundColor="#d3d3d3"
        rotation={0}
      >
        {() => <Text style={styles.speedText}>{speed + 10} km/h</Text>}
      </AnimatedCircularProgress>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#f5fcff",
  },
  title: {
    fontSize: 20,
    marginBottom: 20,
    fontWeight: "bold",
    justifyContent: "center",
    alignItems: "center",
    textAlign: "center",
  },
  title2: {
    textDecorationLine: "underline",
    fontSize: 24,
    marginBottom: 20,
    fontWeight: "bold",
    justifyContent: "center",
    alignItems: "center",
    textAlign: "center",
  },
  title1: {
    fontSize: 15,
    marginBottom: 20,
    fontWeight: "bold",
    justifyContent: "center",
    alignItems: "center",
    textAlign: "center",
  },
  speedText: {
    fontSize: 22,
    color: "#333",
    position: "absolute",
  },
  speedText1: {
    fontSize: 10,
    fontWeight: "bold",
    color: "#333",
    position: "absolute",
  },
});

export default App;
