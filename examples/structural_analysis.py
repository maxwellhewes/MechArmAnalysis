"""
Example script demonstrating structural analysis of circular tubing.
"""

from robotic_arm_analyzer.structural import TubingAnalyzer
import numpy as np

def format_stress(stress: float) -> str:
    """Format stress value with appropriate unit prefix."""
    if abs(stress) >= 1e9:
        return f"{stress/1e9:.2f} GPa"
    elif abs(stress) >= 1e6:
        return f"{stress/1e6:.2f} MPa"
    else:
        return f"{stress:.2f} Pa"

def format_strain(strain: float) -> str:
    """Format strain value in microstrain."""
    return f"{strain*1e6:.2f} με"

def main():
    # Initialize the analyzer with default steel properties
    analyzer = TubingAnalyzer()
    
    # Example 1: Basic analysis of a robotic arm link
    print("\nExample 1: Basic Robotic Arm Link Analysis")
    print("----------------------------------------")
    
    # Input parameters
    outer_diameter = 0.025  # 25mm
    wall_thickness = 0.002  # 2mm
    axial_force = 1000      # 1kN
    bending_moment = 50     # 50Nm
    torque = 20            # 20Nm
    
    # Perform analysis
    results = analyzer.analyze_tubing(
        outer_diameter=outer_diameter,
        wall_thickness=wall_thickness,
        axial_force=axial_force,
        bending_moment=bending_moment,
        torque=torque
    )
    
    # Print results
    print("\nSection Properties:")
    print(f"Area: {results['section_properties']['area']*1e6:.2f} mm²")
    print(f"Moment of Inertia: {results['section_properties']['moment_of_inertia']*1e12:.2f} mm⁴")
    print(f"Section Modulus: {results['section_properties']['section_modulus']*1e9:.2f} mm³")
    
    print("\nStresses:")
    print(f"Axial Stress: {format_stress(results['stresses']['axial'])}")
    print(f"Bending Stress: {format_stress(results['stresses']['bending'])}")
    print(f"Torsional Stress: {format_stress(results['stresses']['torsional'])}")
    print(f"Von Mises Stress: {format_stress(results['stresses']['von_mises'])}")
    print(f"Maximum Principal Stress: {format_stress(results['stresses']['max_principal'])}")
    
    print("\nStrains:")
    print(f"Axial Strain: {format_strain(results['strains']['axial'])}")
    print(f"Bending Strain: {format_strain(results['strains']['bending'])}")
    print(f"Torsional Strain: {format_strain(results['strains']['torsional'])}")
    
    # Example 2: Stress vs Wall Thickness Analysis
    print("\n\nExample 2: Stress vs Wall Thickness Analysis")
    print("--------------------------------------------")
    
    # Vary wall thickness and analyze
    wall_thicknesses = np.linspace(0.001, 0.005, 5)  # 1mm to 5mm
    print("\nWall Thickness (mm) | Von Mises Stress (MPa)")
    print("----------------------------------------")
    
    for thickness in wall_thicknesses:
        results = analyzer.analyze_tubing(
            outer_diameter=outer_diameter,
            wall_thickness=thickness,
            axial_force=axial_force,
            bending_moment=bending_moment,
            torque=torque
        )
        print(f"{thickness*1000:8.1f} mm      | {results['stresses']['von_mises']/1e6:8.2f} MPa")

if __name__ == "__main__":
    main() 