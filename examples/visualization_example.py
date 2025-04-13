"""
Example script demonstrating the visualization capabilities of the Robotic Arm Analyzer package.
"""

from robotic_arm_analyzer.visualization import RoboticArmVisualizer

def main():
    # Initialize the visualizer
    visualizer = RoboticArmVisualizer()

    # Example 1: Plot torque vs length for different angles
    print("Plotting torque vs length for different angles...")
    mass = 1.0  # kg
    min_length = 0.1  # meters
    max_length = 1.0  # meters
    
    # Plot for different angles
    for angle in [0, 30, 45, 60, 90]:
        visualizer.plot_torque_vs_length(mass, min_length, max_length, angle)

    # Example 2: Plot power profiles
    print("\nPlotting power profiles...")
    max_power = 100  # Watts
    acceleration_time = 1.0  # seconds
    total_time = 5.0  # seconds
    
    visualizer.plot_power_profiles(max_power, acceleration_time, total_time)

    # Example 3: Combined analysis
    print("\nPlotting combined analysis...")
    visualizer.plot_combined_analysis(
        mass=mass,
        min_length=min_length,
        max_length=max_length,
        angle=45,
        max_power=max_power,
        acceleration_time=acceleration_time,
        total_time=total_time
    )

if __name__ == "__main__":
    main() 