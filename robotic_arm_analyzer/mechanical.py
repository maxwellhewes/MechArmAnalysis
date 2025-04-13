"""
Mechanical analysis module for robotic arm requirements.
"""

import numpy as np
from typing import Tuple, List

class MechanicalAnalyzer:
    def __init__(self):
        """Initialize the mechanical analyzer."""
        self.gravity = 9.81  # m/s²

    def calculate_torque(self, mass: float, distance: float, angle: float = 0) -> float:
        """
        Calculate the required torque for a joint.
        
        Args:
            mass (float): Mass of the load in kg
            distance (float): Distance from joint to load in meters
            angle (float): Angle of the joint in degrees (0 is horizontal)
            
        Returns:
            float: Required torque in Nm
        """
        # Convert angle to radians
        angle_rad = np.radians(angle)
        # Calculate torque including gravitational force
        torque = mass * self.gravity * distance * np.sin(angle_rad)
        return torque

    def calculate_moment_of_inertia(self, mass: float, length: float) -> float:
        """
        Calculate the moment of inertia for a uniform rod.
        
        Args:
            mass (float): Mass of the link in kg
            length (float): Length of the link in meters
            
        Returns:
            float: Moment of inertia in kg·m²
        """
        return (1/12) * mass * length**2

    def calculate_required_power(self, torque: float, angular_velocity: float) -> float:
        """
        Calculate the required power for a joint.
        
        Args:
            torque (float): Torque in Nm
            angular_velocity (float): Angular velocity in rad/s
            
        Returns:
            float: Required power in Watts
        """
        return torque * angular_velocity

    def analyze_joint_requirements(self, 
                                 masses: List[float], 
                                 distances: List[float], 
                                 angles: List[float]) -> Tuple[List[float], List[float]]:
        """
        Analyze requirements for multiple joints.
        
        Args:
            masses (List[float]): List of masses for each joint
            distances (List[float]): List of distances for each joint
            angles (List[float]): List of angles for each joint
            
        Returns:
            Tuple[List[float], List[float]]: Required torques and moments of inertia for each joint
        """
        torques = []
        inertias = []
        
        for mass, distance, angle in zip(masses, distances, angles):
            torque = self.calculate_torque(mass, distance, angle)
            inertia = self.calculate_moment_of_inertia(mass, distance)
            torques.append(torque)
            inertias.append(inertia)
            
        return torques, inertias 