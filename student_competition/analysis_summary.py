#!/usr/bin/env python3
"""
Student Competition Analysis Summary
Comprehensive analysis of competition aircraft performance and metrics
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ----------------------------------------------------------------------
#   GTM-140 Aircraft Analysis
# ----------------------------------------------------------------------

def analyze_gtm140_aircraft():
    """
    Analyzes the GTM-140 turbojet aircraft for Droniada Sztafeta competition
    """
    
    print("="*80)
    print("GTM-140 TURBOJET AIRCRAFT ANALYSIS")
    print("Droniada Sztafeta Competition")
    print("="*80)
    
    # Aircraft specifications
    aircraft_specs = {
        'name': 'GTM-140 Turbojet UAV',
        'competition': 'Droniada Sztafeta',
        'max_takeoff_weight': 25.0,  # kg
        'empty_weight': 8.2,         # kg
        'fuel_capacity': 2.6,        # kg
        'payload_weight': 1.0,       # kg (beacon drop system)
        'engine_weight': 1.75,       # kg (GTM-140)
        'wing_area': 0.79,           # m²
        'wing_span': 2.51,           # m
        'aspect_ratio': 8.0,
        'fuselage_length': 1.8,      # m
        'engine_thrust': 140,        # N
        'engine_fuel_consumption': 0.08,  # kg/min at cruise
    }
    
    # Mission specifications
    mission_specs = {
        'altitude': 55,              # m AGL
        'cruise_speed': 12,          # m/s
        'mission_time': 30,          # minutes
        'beacon_drops': 4,
        'circuits': 2,
        'total_distance': 22400,     # m
    }
    
    # Competition constraints
    constraints = {
        'max_weight': 25.0,          # kg
        'max_mission_time': 30,      # minutes
        'altitude_range': (50, 60),  # m
        'drop_accuracy_target': 5.0, # m
        'stall_speed_limit': 12.0,   # m/s
    }
    
    # Calculate performance metrics
    performance = calculate_performance_metrics(aircraft_specs, mission_specs)
    
    # Validate constraints
    constraint_validation = validate_constraints(aircraft_specs, mission_specs, constraints, performance)
    
    # Generate analysis report
    generate_analysis_report(aircraft_specs, mission_specs, constraints, performance, constraint_validation)
    
    return aircraft_specs, mission_specs, performance, constraint_validation


def calculate_performance_metrics(aircraft, mission):
    """
    Calculates key performance metrics for the aircraft
    """
    
    # Weight breakdown
    total_weight = aircraft['empty_weight'] + aircraft['fuel_capacity'] + aircraft['payload_weight']
    weight_margin = aircraft['max_takeoff_weight'] - total_weight
    
    # Thrust-to-weight ratio
    thrust_to_weight = aircraft['engine_thrust'] / (total_weight * 9.81)
    
    # Wing loading
    wing_loading = (total_weight * 9.81) / aircraft['wing_area']  # N/m²
    
    # Power loading
    power_loading = (total_weight * 9.81) / aircraft['engine_thrust']  # N/N
    
    # Fuel efficiency
    fuel_efficiency = aircraft['engine_fuel_consumption'] / (mission['cruise_speed'] / 1000)  # kg/km
    
    # Range capability
    theoretical_range = aircraft['fuel_capacity'] / fuel_efficiency  # km
    
    # Stall speed estimation
    air_density = 1.225  # kg/m³ at sea level
    max_lift_coefficient = 1.4  # Typical for UAV airfoil
    stall_speed = np.sqrt((2 * total_weight * 9.81) / (air_density * aircraft['wing_area'] * max_lift_coefficient))
    
    # Drop accuracy estimation
    drop_altitude = mission['altitude']
    drop_time = np.sqrt(2 * drop_altitude / 9.81)  # seconds
    wind_speed = 8.0  # m/s (maximum expected)
    wind_drift = wind_speed * drop_time
    speed_drift = mission['cruise_speed'] * drop_time / 10
    estimated_drop_accuracy = np.sqrt(wind_drift**2 + speed_drift**2)
    
    # Mission feasibility
    fuel_required = aircraft['engine_fuel_consumption'] * mission['mission_time']
    fuel_margin = aircraft['fuel_capacity'] - fuel_required
    
    return {
        'total_weight': total_weight,
        'weight_margin': weight_margin,
        'thrust_to_weight': thrust_to_weight,
        'wing_loading': wing_loading,
        'power_loading': power_loading,
        'fuel_efficiency': fuel_efficiency,
        'theoretical_range': theoretical_range,
        'stall_speed': stall_speed,
        'estimated_drop_accuracy': estimated_drop_accuracy,
        'fuel_required': fuel_required,
        'fuel_margin': fuel_margin,
        'drop_time': drop_time,
    }


def validate_constraints(aircraft, mission, constraints, performance):
    """
    Validates aircraft against competition constraints
    """
    
    validation = {}
    
    # Weight constraint
    validation['weight_constraint'] = performance['total_weight'] <= constraints['max_weight']
    validation['weight_margin_positive'] = performance['weight_margin'] >= 0
    
    # Mission time constraint
    validation['time_constraint'] = mission['mission_time'] <= constraints['max_mission_time']
    validation['time_margin'] = constraints['max_mission_time'] - mission['mission_time']
    
    # Altitude constraint
    validation['altitude_constraint'] = (
        constraints['altitude_range'][0] <= mission['altitude'] <= constraints['altitude_range'][1]
    )
    
    # Drop accuracy constraint
    validation['drop_accuracy_constraint'] = performance['estimated_drop_accuracy'] <= constraints['drop_accuracy_target']
    
    # Stall speed constraint
    validation['stall_speed_constraint'] = performance['stall_speed'] <= constraints['stall_speed_limit']
    validation['stall_margin'] = constraints['stall_speed_limit'] - performance['stall_speed']
    
    # Fuel constraint
    validation['fuel_constraint'] = performance['fuel_margin'] >= 0
    
    # Overall feasibility
    validation['mission_feasible'] = all([
        validation['weight_constraint'],
        validation['time_constraint'],
        validation['altitude_constraint'],
        validation['fuel_constraint']
    ])
    
    return validation


def generate_analysis_report(aircraft, mission, constraints, performance, validation):
    """
    Generates a comprehensive analysis report
    """
    
    print(f"\nAIRCRAFT SPECIFICATIONS:")
    print(f"  Aircraft: {aircraft['name']}")
    print(f"  Competition: {aircraft['competition']}")
    print(f"  Wing Area: {aircraft['wing_area']:.2f} m²")
    print(f"  Wing Span: {aircraft['wing_span']:.2f} m")
    print(f"  Aspect Ratio: {aircraft['aspect_ratio']:.1f}")
    print(f"  Fuselage Length: {aircraft['fuselage_length']:.1f} m")
    
    print(f"\nWEIGHT BREAKDOWN:")
    print(f"  Empty Weight: {aircraft['empty_weight']:.1f} kg")
    print(f"  Engine Weight: {aircraft['engine_weight']:.1f} kg")
    print(f"  Fuel Capacity: {aircraft['fuel_capacity']:.1f} kg")
    print(f"  Payload Weight: {aircraft['payload_weight']:.1f} kg")
    print(f"  Total Weight: {performance['total_weight']:.1f} kg")
    print(f"  Weight Margin: {performance['weight_margin']:.1f} kg")
    
    print(f"\nENGINE PERFORMANCE:")
    print(f"  Engine: GTM-140 Turbojet")
    print(f"  Thrust: {aircraft['engine_thrust']:.0f} N")
    print(f"  Thrust-to-Weight: {performance['thrust_to_weight']:.2f}")
    print(f"  Wing Loading: {performance['wing_loading']:.0f} N/m²")
    print(f"  Power Loading: {performance['power_loading']:.2f}")
    
    print(f"\nMISSION PROFILE:")
    print(f"  Altitude: {mission['altitude']} m AGL")
    print(f"  Cruise Speed: {mission['cruise_speed']} m/s")
    print(f"  Mission Time: {mission['mission_time']} minutes")
    print(f"  Total Distance: {mission['total_distance']/1000:.1f} km")
    print(f"  Beacon Drops: {mission['beacon_drops']}")
    print(f"  Circuits: {mission['circuits']}")
    
    print(f"\nPERFORMANCE METRICS:")
    print(f"  Fuel Efficiency: {performance['fuel_efficiency']:.3f} kg/km")
    print(f"  Theoretical Range: {performance['theoretical_range']:.1f} km")
    print(f"  Stall Speed: {performance['stall_speed']:.1f} m/s")
    print(f"  Estimated Drop Accuracy: {performance['estimated_drop_accuracy']:.1f} m")
    print(f"  Drop Time: {performance['drop_time']:.1f} s")
    print(f"  Fuel Required: {performance['fuel_required']:.1f} kg")
    print(f"  Fuel Margin: {performance['fuel_margin']:.1f} kg")
    
    print(f"\nCONSTRAINT VALIDATION:")
    status_symbols = {True: "✓ PASS", False: "✗ FAIL"}
    
    print(f"  Weight Limit ({constraints['max_weight']} kg): {status_symbols[validation['weight_constraint']]}")
    print(f"  Time Limit ({constraints['max_mission_time']} min): {status_symbols[validation['time_constraint']]}")
    print(f"  Altitude Range ({constraints['altitude_range'][0]}-{constraints['altitude_range'][1]} m): {status_symbols[validation['altitude_constraint']]}")
    print(f"  Drop Accuracy (<{constraints['drop_accuracy_target']} m): {status_symbols[validation['drop_accuracy_constraint']]}")
    print(f"  Stall Speed (<{constraints['stall_speed_limit']} m/s): {status_symbols[validation['stall_speed_constraint']]}")
    print(f"  Fuel Sufficiency: {status_symbols[validation['fuel_constraint']]}")
    
    print(f"\nOVERALL ASSESSMENT:")
    if validation['mission_feasible']:
        print(f"  ✓ MISSION FEASIBLE - Aircraft meets all critical constraints")
    else:
        print(f"  ✗ MISSION NOT FEASIBLE - Some constraints not met")
    
    print(f"\n" + "="*80)


# ----------------------------------------------------------------------
#   Traditional Turbofan Aircraft Analysis
# ----------------------------------------------------------------------

def analyze_turbo_aircraft():
    """
    Analyzes the traditional turbofan aircraft for educational purposes
    """
    
    print("="*80)
    print("TRADITIONAL TURBOFAN AIRCRAFT ANALYSIS")
    print("Educational Framework")
    print("="*80)
    
    # Aircraft specifications
    aircraft_specs = {
        'name': 'Twin Turbofan Aircraft',
        'type': 'Educational/Reference',
        'max_takeoff_weight': 1500,  # kg
        'empty_weight': 800,         # kg
        'fuel_capacity': 400,        # kg
        'payload_capacity': 300,     # kg
        'wing_area': 15.0,           # m²
        'wing_span': 12.0,           # m
        'aspect_ratio': 9.6,
        'fuselage_length': 8.0,      # m
        'engine_thrust_total': 24000,  # N (2x 12000N)
        'engine_count': 2,
        'cruise_altitude': 10000,    # m
        'cruise_speed': 200,         # m/s
    }
    
    # Mission specifications
    mission_specs = {
        'altitude': 10000,           # m
        'cruise_speed': 200,         # m/s
        'mission_time': 120,         # minutes
        'range': 2400,               # km
        'payload': 200,              # kg
    }
    
    # Calculate performance metrics
    performance = calculate_turbo_performance(aircraft_specs, mission_specs)
    
    # Generate analysis report
    generate_turbo_analysis_report(aircraft_specs, mission_specs, performance)
    
    return aircraft_specs, mission_specs, performance


def calculate_turbo_performance(aircraft, mission):
    """
    Calculates performance metrics for turbofan aircraft
    """
    
    # Weight breakdown
    total_weight = aircraft['empty_weight'] + aircraft['fuel_capacity'] + mission['payload']
    weight_margin = aircraft['max_takeoff_weight'] - total_weight
    
    # Thrust-to-weight ratio
    thrust_to_weight = aircraft['engine_thrust_total'] / (total_weight * 9.81)
    
    # Wing loading
    wing_loading = (total_weight * 9.81) / aircraft['wing_area']  # N/m²
    
    # Power loading
    power_loading = (total_weight * 9.81) / aircraft['engine_thrust_total']  # N/N
    
    # Specific fuel consumption (estimated)
    sfc = 0.00008  # kg/N/s for turbofan
    fuel_flow = sfc * aircraft['engine_thrust_total']  # kg/s
    fuel_efficiency = fuel_flow / (mission['cruise_speed'] / 1000)  # kg/km
    
    # Range capability
    theoretical_range = aircraft['fuel_capacity'] / fuel_efficiency  # km
    
    # Stall speed estimation
    air_density = 0.413  # kg/m³ at 10km altitude
    max_lift_coefficient = 1.8  # Typical for transport aircraft
    stall_speed = np.sqrt((2 * total_weight * 9.81) / (air_density * aircraft['wing_area'] * max_lift_coefficient))
    
    return {
        'total_weight': total_weight,
        'weight_margin': weight_margin,
        'thrust_to_weight': thrust_to_weight,
        'wing_loading': wing_loading,
        'power_loading': power_loading,
        'fuel_efficiency': fuel_efficiency,
        'theoretical_range': theoretical_range,
        'stall_speed': stall_speed,
        'fuel_flow': fuel_flow,
    }


def generate_turbo_analysis_report(aircraft, mission, performance):
    """
    Generates analysis report for turbofan aircraft
    """
    
    print(f"\nAIRCRAFT SPECIFICATIONS:")
    print(f"  Aircraft: {aircraft['name']}")
    print(f"  Type: {aircraft['type']}")
    print(f"  Wing Area: {aircraft['wing_area']:.1f} m²")
    print(f"  Wing Span: {aircraft['wing_span']:.1f} m")
    print(f"  Aspect Ratio: {aircraft['aspect_ratio']:.1f}")
    print(f"  Engine Configuration: {aircraft['engine_count']}x Turbofan")
    print(f"  Total Thrust: {aircraft['engine_thrust_total']/1000:.1f} kN")
    
    print(f"\nWEIGHT BREAKDOWN:")
    print(f"  Empty Weight: {aircraft['empty_weight']:.0f} kg")
    print(f"  Fuel Capacity: {aircraft['fuel_capacity']:.0f} kg")
    print(f"  Payload: {mission['payload']:.0f} kg")
    print(f"  Total Weight: {performance['total_weight']:.0f} kg")
    print(f"  Weight Margin: {performance['weight_margin']:.0f} kg")
    
    print(f"\nPERFORMANCE METRICS:")
    print(f"  Thrust-to-Weight: {performance['thrust_to_weight']:.2f}")
    print(f"  Wing Loading: {performance['wing_loading']:.0f} N/m²")
    print(f"  Fuel Efficiency: {performance['fuel_efficiency']:.3f} kg/km")
    print(f"  Theoretical Range: {performance['theoretical_range']:.0f} km")
    print(f"  Stall Speed: {performance['stall_speed']:.1f} m/s")
    print(f"  Fuel Flow: {performance['fuel_flow']:.2f} kg/s")
    
    print(f"\nMISSION PROFILE:")
    print(f"  Cruise Altitude: {mission['altitude']/1000:.0f} km")
    print(f"  Cruise Speed: {mission['cruise_speed']:.0f} m/s ({mission['cruise_speed']*3.6:.0f} km/h)")
    print(f"  Mission Time: {mission['mission_time']:.0f} minutes")
    print(f"  Range: {mission['range']:.0f} km")
    
    print(f"\n" + "="*80)


# ----------------------------------------------------------------------
#   Comparative Analysis
# ----------------------------------------------------------------------

def comparative_analysis():
    """
    Compares the two aircraft types
    """
    
    print("="*80)
    print("COMPARATIVE AIRCRAFT ANALYSIS")
    print("GTM-140 UAV vs Traditional Turbofan")
    print("="*80)
    
    # Get analysis results
    gtm140_specs, gtm140_mission, gtm140_perf, gtm140_validation = analyze_gtm140_aircraft()
    turbo_specs, turbo_mission, turbo_perf = analyze_turbo_aircraft()
    
    print(f"\nCOMPARISON SUMMARY:")
    print(f"{'Metric':<25} {'GTM-140 UAV':<15} {'Turbofan':<15} {'Ratio':<10}")
    print(f"{'-'*25} {'-'*15} {'-'*15} {'-'*10}")
    
    comparisons = [
        ('Max Takeoff Weight (kg)', gtm140_specs['max_takeoff_weight'], turbo_specs['max_takeoff_weight']),
        ('Wing Area (m²)', gtm140_specs['wing_area'], turbo_specs['wing_area']),
        ('Thrust (N)', gtm140_specs['engine_thrust'], turbo_specs['engine_thrust_total']),
        ('Thrust-to-Weight', gtm140_perf['thrust_to_weight'], turbo_perf['thrust_to_weight']),
        ('Wing Loading (N/m²)', gtm140_perf['wing_loading'], turbo_perf['wing_loading']),
        ('Cruise Speed (m/s)', gtm140_mission['cruise_speed'], turbo_mission['cruise_speed']),
        ('Mission Time (min)', gtm140_mission['mission_time'], turbo_mission['mission_time']),
        ('Stall Speed (m/s)', gtm140_perf['stall_speed'], turbo_perf['stall_speed']),
    ]
    
    for metric, gtm140_val, turbo_val in comparisons:
        ratio = gtm140_val / turbo_val if turbo_val != 0 else float('inf')
        print(f"{metric:<25} {gtm140_val:<15.2f} {turbo_val:<15.2f} {ratio:<10.3f}")
    
    print(f"\nKEY DIFFERENCES:")
    print(f"  • GTM-140 UAV: Small, lightweight, low-altitude, precision mission")
    print(f"  • Turbofan: Large, heavy, high-altitude, long-range transport")
    print(f"  • GTM-140: Competition-optimized for specific mission requirements")
    print(f"  • Turbofan: General-purpose aircraft with broad capability")
    
    print(f"\n" + "="*80)


# ----------------------------------------------------------------------
#   Main Execution
# ----------------------------------------------------------------------

def main():
    """
    Main function to run all analyses
    """
    
    print("STUDENT COMPETITION AIRCRAFT ANALYSIS")
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Run individual analyses
    print("\n1. GTM-140 Turbojet UAV Analysis")
    gtm140_results = analyze_gtm140_aircraft()
    
    print("\n2. Traditional Turbofan Aircraft Analysis")
    turbo_results = analyze_turbo_aircraft()
    
    print("\n3. Comparative Analysis")
    comparative_analysis()
    
    print("\nANALYSIS COMPLETE!")
    print("="*80)
    
    return gtm140_results, turbo_results


if __name__ == '__main__':
    main()
