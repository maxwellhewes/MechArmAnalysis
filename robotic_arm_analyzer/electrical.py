"""
Electrical analysis module for robotic arm requirements.
"""

from typing import List, Tuple

class ElectricalAnalyzer:
    def __init__(self):
        """Initialize the electrical analyzer."""
        self.typical_efficiency = 0.85  # Typical motor efficiency
        self.voltage_nominal = 24.0  # Typical nominal voltage for robotic systems

    def calculate_current(self, power: float, voltage: float = None) -> float:
        """
        Calculate the required current for a motor.
        
        Args:
            power (float): Required power in Watts
            voltage (float, optional): Operating voltage in Volts. Defaults to nominal voltage.
            
        Returns:
            float: Required current in Amperes
        """
        if voltage is None:
            voltage = self.voltage_nominal
        return power / (voltage * self.typical_efficiency)

    def calculate_power_consumption(self, current: float, voltage: float = None) -> float:
        """
        Calculate the power consumption of a motor.
        
        Args:
            current (float): Current draw in Amperes
            voltage (float, optional): Operating voltage in Volts. Defaults to nominal voltage.
            
        Returns:
            float: Power consumption in Watts
        """
        if voltage is None:
            voltage = self.voltage_nominal
        return current * voltage

    def calculate_battery_requirements(self, 
                                    power_consumption: float, 
                                    operating_time: float, 
                                    safety_factor: float = 1.2) -> Tuple[float, float]:
        """
        Calculate battery requirements for the robotic arm.
        
        Args:
            power_consumption (float): Total power consumption in Watts
            operating_time (float): Desired operating time in hours
            safety_factor (float): Safety factor for battery capacity
            
        Returns:
            Tuple[float, float]: Required battery capacity in Watt-hours and Ampere-hours
        """
        # Calculate required energy
        energy_wh = power_consumption * operating_time * safety_factor
        
        # Calculate required capacity in Ah
        capacity_ah = energy_wh / self.voltage_nominal
        
        return energy_wh, capacity_ah

    def analyze_power_system(self, 
                           joint_powers: List[float], 
                           operating_time: float) -> Tuple[float, float, float]:
        """
        Analyze the complete power system requirements.
        
        Args:
            joint_powers (List[float]): List of power requirements for each joint
            operating_time (float): Desired operating time in hours
            
        Returns:
            Tuple[float, float, float]: Total power consumption, required battery capacity in Wh, required battery capacity in Ah
        """
        total_power = sum(joint_powers)
        current = self.calculate_current(total_power)
        energy_wh, capacity_ah = self.calculate_battery_requirements(total_power, operating_time)
        
        return total_power, energy_wh, capacity_ah 