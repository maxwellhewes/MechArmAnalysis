"""
Example script demonstrating the use of the Robotic Arm Analyzer package.
"""

from robotic_arm_analyzer.mechanical import MechanicalAnalyzer
from robotic_arm_analyzer.electrical import ElectricalAnalyzer

def main():
    # Initialize analyzers
    mech_analyzer = MechanicalAnalyzer()
    elec_analyzer = ElectricalAnalyzer()

    # Example parameters for a 3-joint robotic arm
    masses = [1.0, 0.8, 0.5]  # kg
    distances = [0.3, 0.2, 0.15]  # meters
    angles = [45, 30, 0]  # degrees
    operating_time = 2.0  # hours

    # Mechanical analysis
    torques, inertias = mech_analyzer.analyze_joint_requirements(masses, distances, angles)
    
    # Calculate power requirements for each joint
    angular_velocities = [1.0, 1.0, 1.0]  # rad/s
    joint_powers = []
    for torque, angular_velocity in zip(torques, angular_velocities):
        power = mech_analyzer.calculate_required_power(torque, angular_velocity)
        joint_powers.append(power)

    # Electrical analysis
    total_power, energy_wh, capacity_ah = elec_analyzer.analyze_power_system(joint_powers, operating_time)

    # Print results
    print("\nMechanical Analysis Results:")
    for i, (torque, inertia) in enumerate(zip(torques, inertias), 1):
        print(f"Joint {i}:")
        print(f"  Required Torque: {torque:.2f} Nm")
        print(f"  Moment of Inertia: {inertia:.4f} kg·m²")
        print(f"  Required Power: {joint_powers[i-1]:.2f} W")

    print("\nElectrical Analysis Results:")
    print(f"Total Power Consumption: {total_power:.2f} W")
    print(f"Required Battery Capacity: {energy_wh:.2f} Wh ({capacity_ah:.2f} Ah)")

if __name__ == "__main__":
    main() 