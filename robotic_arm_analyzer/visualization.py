"""
Visualization module for robotic arm analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

class RoboticArmVisualizer:
    def __init__(self):
        """Initialize the visualizer."""
        plt.style.use('seaborn-v0_8')

    def plot_torque_vs_length(self, 
                            mass: float, 
                            min_length: float, 
                            max_length: float, 
                            angle: float = 0,
                            num_points: int = 100) -> None:
        """
        Plot required torque vs link length for a given mass and angle.
        
        Args:
            mass (float): Mass of the load in kg
            min_length (float): Minimum link length in meters
            max_length (float): Maximum link length in meters
            angle (float): Joint angle in degrees
            num_points (int): Number of points to plot
        """
        lengths = np.linspace(min_length, max_length, num_points)
        torques = mass * 9.81 * lengths * np.sin(np.radians(angle))
        
        plt.figure(figsize=(10, 6))
        plt.plot(lengths, torques, 'b-', linewidth=2)
        plt.title(f'Required Torque vs Link Length\n(Mass: {mass} kg, Angle: {angle}°)')
        plt.xlabel('Link Length (m)')
        plt.ylabel('Required Torque (Nm)')
        plt.grid(True)
        plt.show()

    def plot_power_profiles(self, 
                          max_power: float, 
                          acceleration_time: float, 
                          total_time: float,
                          num_points: int = 100) -> None:
        """
        Plot different power output profiles (trapezoidal and S-curve).
        
        Args:
            max_power (float): Maximum power output in Watts
            acceleration_time (float): Time to reach maximum power in seconds
            total_time (float): Total time period in seconds
            num_points (int): Number of points to plot
        """
        time = np.linspace(0, total_time, num_points)
        
        # Trapezoidal profile
        trapezoidal = np.zeros_like(time)
        for i, t in enumerate(time):
            if t < acceleration_time:
                trapezoidal[i] = (max_power / acceleration_time) * t
            elif t > total_time - acceleration_time:
                trapezoidal[i] = max_power - (max_power / acceleration_time) * (t - (total_time - acceleration_time))
            else:
                trapezoidal[i] = max_power
        
        # S-curve profile
        s_curve = np.zeros_like(time)
        for i, t in enumerate(time):
            if t < acceleration_time:
                s_curve[i] = max_power * (1 - np.cos(np.pi * t / acceleration_time)) / 2
            elif t > total_time - acceleration_time:
                s_curve[i] = max_power * (1 + np.cos(np.pi * (t - (total_time - acceleration_time)) / acceleration_time)) / 2
            else:
                s_curve[i] = max_power
        
        plt.figure(figsize=(10, 6))
        plt.plot(time, trapezoidal, 'b-', label='Trapezoidal Profile', linewidth=2)
        plt.plot(time, s_curve, 'r--', label='S-curve Profile', linewidth=2)
        plt.title('Power Output Profiles')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (W)')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_combined_analysis(self,
                             mass: float,
                             min_length: float,
                             max_length: float,
                             angle: float = 0,
                             max_power: float = 100,
                             acceleration_time: float = 1.0,
                             total_time: float = 5.0) -> None:
        """
        Create a combined plot showing torque vs length and power profiles.
        
        Args:
            mass (float): Mass of the load in kg
            min_length (float): Minimum link length in meters
            max_length (float): Maximum link length in meters
            angle (float): Joint angle in degrees
            max_power (float): Maximum power output in Watts
            acceleration_time (float): Time to reach maximum power in seconds
            total_time (float): Total time period in seconds
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
        
        # Plot torque vs length
        lengths = np.linspace(min_length, max_length, 100)
        torques = mass * 9.81 * lengths * np.sin(np.radians(angle))
        ax1.plot(lengths, torques, 'b-', linewidth=2)
        ax1.set_title(f'Required Torque vs Link Length\n(Mass: {mass} kg, Angle: {angle}°)')
        ax1.set_xlabel('Link Length (m)')
        ax1.set_ylabel('Required Torque (Nm)')
        ax1.grid(True)
        
        # Plot power profiles
        time = np.linspace(0, total_time, 100)
        trapezoidal = np.zeros_like(time)
        s_curve = np.zeros_like(time)
        
        for i, t in enumerate(time):
            if t < acceleration_time:
                trapezoidal[i] = (max_power / acceleration_time) * t
                s_curve[i] = max_power * (1 - np.cos(np.pi * t / acceleration_time)) / 2
            elif t > total_time - acceleration_time:
                trapezoidal[i] = max_power - (max_power / acceleration_time) * (t - (total_time - acceleration_time))
                s_curve[i] = max_power * (1 + np.cos(np.pi * (t - (total_time - acceleration_time)) / acceleration_time)) / 2
            else:
                trapezoidal[i] = max_power
                s_curve[i] = max_power
        
        ax2.plot(time, trapezoidal, 'b-', label='Trapezoidal Profile', linewidth=2)
        ax2.plot(time, s_curve, 'r--', label='S-curve Profile', linewidth=2)
        ax2.set_title('Power Output Profiles')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Power (W)')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.show() 