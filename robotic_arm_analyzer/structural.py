"""
Structural analysis module for circular tubing in robotic arms.
"""

import numpy as np
from typing import Tuple, List

class TubingAnalyzer:
    def __init__(self, youngs_modulus: float = 200e9, poissons_ratio: float = 0.3):
        """
        Initialize the tubing analyzer.
        
        Args:
            youngs_modulus (float): Young's modulus in Pa (default: 200 GPa for steel)
            poissons_ratio (float): Poisson's ratio (default: 0.3 for steel)
        """
        self.E = youngs_modulus
        self.v = poissons_ratio

    def calculate_section_properties(self, 
                                  outer_diameter: float, 
                                  wall_thickness: float) -> Tuple[float, float, float]:
        """
        Calculate section properties for circular tubing.
        
        Args:
            outer_diameter (float): Outer diameter in meters
            wall_thickness (float): Wall thickness in meters
            
        Returns:
            Tuple[float, float, float]: Area, moment of inertia, and section modulus
        """
        inner_diameter = outer_diameter - 2 * wall_thickness
        area = np.pi * (outer_diameter**2 - inner_diameter**2) / 4
        moment_of_inertia = np.pi * (outer_diameter**4 - inner_diameter**4) / 64
        section_modulus = moment_of_inertia / (outer_diameter / 2)
        
        return area, moment_of_inertia, section_modulus

    def calculate_bending_stress(self, 
                               moment: float, 
                               outer_diameter: float, 
                               wall_thickness: float) -> float:
        """
        Calculate maximum bending stress.
        
        Args:
            moment (float): Bending moment in Nm
            outer_diameter (float): Outer diameter in meters
            wall_thickness (float): Wall thickness in meters
            
        Returns:
            float: Maximum bending stress in Pa
        """
        _, _, section_modulus = self.calculate_section_properties(outer_diameter, wall_thickness)
        return moment / section_modulus

    def calculate_axial_stress(self, 
                             axial_force: float, 
                             outer_diameter: float, 
                             wall_thickness: float) -> float:
        """
        Calculate axial stress.
        
        Args:
            axial_force (float): Axial force in N
            outer_diameter (float): Outer diameter in meters
            wall_thickness (float): Wall thickness in meters
            
        Returns:
            float: Axial stress in Pa
        """
        area, _, _ = self.calculate_section_properties(outer_diameter, wall_thickness)
        return axial_force / area

    def calculate_torsional_stress(self, 
                                 torque: float, 
                                 outer_diameter: float, 
                                 wall_thickness: float) -> float:
        """
        Calculate maximum torsional stress.
        
        Args:
            torque (float): Torque in Nm
            outer_diameter (float): Outer diameter in meters
            wall_thickness (float): Wall thickness in meters
            
        Returns:
            float: Maximum torsional stress in Pa
        """
        inner_diameter = outer_diameter - 2 * wall_thickness
        polar_moment = np.pi * (outer_diameter**4 - inner_diameter**4) / 32
        return torque * (outer_diameter / 2) / polar_moment

    def calculate_combined_stress(self,
                                axial_force: float,
                                bending_moment: float,
                                torque: float,
                                outer_diameter: float,
                                wall_thickness: float) -> Tuple[float, float]:
        """
        Calculate combined stress using von Mises criterion.
        
        Args:
            axial_force (float): Axial force in N
            bending_moment (float): Bending moment in Nm
            torque (float): Torque in Nm
            outer_diameter (float): Outer diameter in meters
            wall_thickness (float): Wall thickness in meters
            
        Returns:
            Tuple[float, float]: von Mises stress and maximum principal stress in Pa
        """
        # Calculate individual stress components
        sigma_axial = self.calculate_axial_stress(axial_force, outer_diameter, wall_thickness)
        sigma_bending = self.calculate_bending_stress(bending_moment, outer_diameter, wall_thickness)
        tau_torsion = self.calculate_torsional_stress(torque, outer_diameter, wall_thickness)
        
        # Calculate von Mises stress
        sigma_vm = np.sqrt((sigma_axial + sigma_bending)**2 + 3 * tau_torsion**2)
        
        # Calculate maximum principal stress
        sigma_max = (sigma_axial + sigma_bending) / 2 + np.sqrt(((sigma_axial + sigma_bending) / 2)**2 + tau_torsion**2)
        
        return sigma_vm, sigma_max

    def calculate_strain(self, stress: float) -> float:
        """
        Calculate strain from stress.
        
        Args:
            stress (float): Stress in Pa
            
        Returns:
            float: Strain (unitless)
        """
        return stress / self.E

    def analyze_tubing(self,
                      outer_diameter: float,
                      wall_thickness: float,
                      axial_force: float = 0,
                      bending_moment: float = 0,
                      torque: float = 0) -> dict:
        """
        Perform complete analysis of tubing under given loads.
        
        Args:
            outer_diameter (float): Outer diameter in meters
            wall_thickness (float): Wall thickness in meters
            axial_force (float): Axial force in N
            bending_moment (float): Bending moment in Nm
            torque (float): Torque in Nm
            
        Returns:
            dict: Dictionary containing all analysis results
        """
        # Calculate section properties
        area, moment_of_inertia, section_modulus = self.calculate_section_properties(
            outer_diameter, wall_thickness)
        
        # Calculate individual stresses
        sigma_axial = self.calculate_axial_stress(axial_force, outer_diameter, wall_thickness)
        sigma_bending = self.calculate_bending_stress(bending_moment, outer_diameter, wall_thickness)
        tau_torsion = self.calculate_torsional_stress(torque, outer_diameter, wall_thickness)
        
        # Calculate combined stresses
        sigma_vm, sigma_max = self.calculate_combined_stress(
            axial_force, bending_moment, torque, outer_diameter, wall_thickness)
        
        # Calculate strains
        epsilon_axial = self.calculate_strain(sigma_axial)
        epsilon_bending = self.calculate_strain(sigma_bending)
        gamma_torsion = tau_torsion / (self.E / (2 * (1 + self.v)))
        
        return {
            'section_properties': {
                'area': area,
                'moment_of_inertia': moment_of_inertia,
                'section_modulus': section_modulus
            },
            'stresses': {
                'axial': sigma_axial,
                'bending': sigma_bending,
                'torsional': tau_torsion,
                'von_mises': sigma_vm,
                'max_principal': sigma_max
            },
            'strains': {
                'axial': epsilon_axial,
                'bending': epsilon_bending,
                'torsional': gamma_torsion
            }
        } 