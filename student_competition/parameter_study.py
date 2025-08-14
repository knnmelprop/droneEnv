#!/usr/bin/env python3
"""
Parameter Sensitivity Analysis for GTM-140 Aircraft
Studies the effect of design variables on competition performance
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ----------------------------------------------------------------------
#   Base Aircraft Configuration
# ----------------------------------------------------------------------

def get_base_configuration():
    """
    Returns the base GTM-140 aircraft configuration
    """
    return {
        'name': 'GTM-140 Turbojet UAV',
        'competition': 'Droniada Sztafeta',
        'max_takeoff_weight': 25.0,  # kg
        'empty_weight': 8.2,         # kg
        'fuel_capacity': 2.6,        # kg
        'payload_weight': 1.0,       # kg
        'engine_weight': 1.75,       # kg
        'wing_area': 0.79,           # m²
        'wing_span': 2.51,           # m
        'aspect_ratio': 8.0,
        'fuselage_length': 1.8,      # m
        'engine_thrust': 140,        # N
        'engine_fuel_consumption': 0.08,  # kg/min
        'cruise_speed': 12,          # m/s
        'mission_time': 30,          # minutes
        'altitude': 55,              # m
    }


# ----------------------------------------------------------------------
#   Parameter Sensitivity Analysis
# ----------------------------------------------------------------------

def wing_area_sensitivity():
    """
    Analyzes sensitivity to wing area changes
    """
    print("="*80)
    print("WING AREA SENSITIVITY ANALYSIS")
    print("Effect on Performance and Constraints")
    print("="*80)
    
    base_config = get_base_configuration()
    wing_areas = np.linspace(0.5, 1.2, 15)  # m²
    
    results = []
    
    for wing_area in wing_areas:
        config = base_config.copy()
        config['wing_area'] = wing_area
        
        # Recalculate wing span based on aspect ratio
        config['wing_span'] = np.sqrt(wing_area * config['aspect_ratio'])
        
        # Calculate performance metrics
        performance = calculate_performance_metrics(config)
        validation = validate_constraints(config, performance)
        
        results.append({
            'wing_area': wing_area,
            'wing_span': config['wing_span'],
            'stall_speed': performance['stall_speed'],
            'wing_loading': performance['wing_loading'],
            'stall_constraint_met': validation['stall_speed_constraint'],
            'drop_accuracy': performance['estimated_drop_accuracy'],
            'drop_accuracy_met': validation['drop_accuracy_constraint'],
        })
    
    # Print results table
    print(f"\n{'Wing Area':<10} {'Wing Span':<10} {'Stall Speed':<12} {'Wing Loading':<12} {'Stall OK':<8} {'Drop Acc':<10} {'Drop OK':<8}")
    print(f"{'(m²)':<10} {'(m)':<10} {'(m/s)':<12} {'(N/m²)':<12} {'':<8} {'(m)':<10} {'':<8}")
    print("-" * 80)
    
    for result in results:
        print(f"{result['wing_area']:<10.2f} {result['wing_span']:<10.2f} {result['stall_speed']:<12.1f} "
              f"{result['wing_loading']:<12.0f} {'✓' if result['stall_constraint_met'] else '✗':<8} "
              f"{result['drop_accuracy']:<10.1f} {'✓' if result['drop_accuracy_met'] else '✗':<8}")
    
    return results


def engine_thrust_sensitivity():
    """
    Analyzes sensitivity to engine thrust changes
    """
    print("="*80)
    print("ENGINE THRUST SENSITIVITY ANALYSIS")
    print("Effect on Performance and Mission Capability")
    print("="*80)
    
    base_config = get_base_configuration()
    thrust_values = np.linspace(100, 200, 11)  # N
    
    results = []
    
    for thrust in thrust_values:
        config = base_config.copy()
        config['engine_thrust'] = thrust
        
        # Calculate performance metrics
        performance = calculate_performance_metrics(config)
        validation = validate_constraints(config, performance)
        
        results.append({
            'thrust': thrust,
            'thrust_to_weight': performance['thrust_to_weight'],
            'power_loading': performance['power_loading'],
            'fuel_required': performance['fuel_required'],
            'fuel_margin': performance['fuel_margin'],
            'fuel_constraint_met': validation['fuel_constraint'],
            'mission_feasible': validation['mission_feasible'],
        })
    
    # Print results table
    print(f"\n{'Thrust':<8} {'T/W':<8} {'P/L':<8} {'Fuel Req':<10} {'Fuel Margin':<12} {'Fuel OK':<8} {'Feasible':<10}")
    print(f"{'(N)':<8} {'':<8} {'':<8} {'(kg)':<10} {'(kg)':<12} {'':<8} {'':<10}")
    print("-" * 80)
    
    for result in results:
        print(f"{result['thrust']:<8.0f} {result['thrust_to_weight']:<8.2f} {result['power_loading']:<8.2f} "
              f"{result['fuel_required']:<10.1f} {result['fuel_margin']:<12.1f} "
              f"{'✓' if result['fuel_constraint_met'] else '✗':<8} "
              f"{'✓' if result['mission_feasible'] else '✗':<10}")
    
    return results


def fuel_capacity_sensitivity():
    """
    Analyzes sensitivity to fuel capacity changes
    """
    print("="*80)
    print("FUEL CAPACITY SENSITIVITY ANALYSIS")
    print("Effect on Mission Duration and Weight")
    print("="*80)
    
    base_config = get_base_configuration()
    fuel_capacities = np.linspace(1.5, 4.0, 11)  # kg
    
    results = []
    
    for fuel_capacity in fuel_capacities:
        config = base_config.copy()
        config['fuel_capacity'] = fuel_capacity
        
        # Calculate performance metrics
        performance = calculate_performance_metrics(config)
        validation = validate_constraints(config, performance)
        
        # Calculate maximum mission time with this fuel
        max_mission_time = fuel_capacity / config['engine_fuel_consumption']
        
        results.append({
            'fuel_capacity': fuel_capacity,
            'total_weight': performance['total_weight'],
            'weight_margin': performance['weight_margin'],
            'max_mission_time': max_mission_time,
            'fuel_margin': performance['fuel_margin'],
            'weight_constraint_met': validation['weight_constraint'],
            'fuel_constraint_met': validation['fuel_constraint'],
        })
    
    # Print results table
    print(f"\n{'Fuel Cap':<10} {'Total Wt':<10} {'Wt Margin':<10} {'Max Time':<10} {'Fuel Margin':<12} {'Wt OK':<8} {'Fuel OK':<8}")
    print(f"{'(kg)':<10} {'(kg)':<10} {'(kg)':<10} {'(min)':<10} {'(kg)':<12} {'':<8} {'':<8}")
    print("-" * 80)
    
    for result in results:
        print(f"{result['fuel_capacity']:<10.1f} {result['total_weight']:<10.1f} {result['weight_margin']:<10.1f} "
              f"{result['max_mission_time']:<10.1f} {result['fuel_margin']:<12.1f} "
              f"{'✓' if result['weight_constraint_met'] else '✗':<8} "
              f"{'✓' if result['fuel_constraint_met'] else '✗':<8}")
    
    return results


def cruise_speed_sensitivity():
    """
    Analyzes sensitivity to cruise speed changes
    """
    print("="*80)
    print("CRUISE SPEED SENSITIVITY ANALYSIS")
    print("Effect on Drop Accuracy and Mission Time")
    print("="*80)
    
    base_config = get_base_configuration()
    cruise_speeds = np.linspace(8, 18, 11)  # m/s
    
    results = []
    
    for cruise_speed in cruise_speeds:
        config = base_config.copy()
        config['cruise_speed'] = cruise_speed
        
        # Calculate performance metrics
        performance = calculate_performance_metrics(config)
        validation = validate_constraints(config, performance)
        
        # Calculate mission time for fixed distance
        mission_distance = 22400  # m
        mission_time = mission_distance / cruise_speed / 60  # minutes
        
        results.append({
            'cruise_speed': cruise_speed,
            'drop_accuracy': performance['estimated_drop_accuracy'],
            'mission_time': mission_time,
            'fuel_efficiency': performance['fuel_efficiency'],
            'drop_accuracy_met': validation['drop_accuracy_constraint'],
            'time_constraint_met': mission_time <= 30,
        })
    
    # Print results table
    print(f"\n{'Speed':<8} {'Drop Acc':<10} {'Mission Time':<12} {'Fuel Eff':<10} {'Drop OK':<8} {'Time OK':<8}")
    print(f"{'(m/s)':<8} {'(m)':<10} {'(min)':<12} {'(kg/km)':<10} {'':<8} {'':<8}")
    print("-" * 80)
    
    for result in results:
        print(f"{result['cruise_speed']:<8.1f} {result['drop_accuracy']:<10.1f} {result['mission_time']:<12.1f} "
              f"{result['fuel_efficiency']:<10.3f} "
              f"{'✓' if result['drop_accuracy_met'] else '✗':<8} "
              f"{'✓' if result['time_constraint_met'] else '✗':<8}")
    
    return results


# ----------------------------------------------------------------------
#   Performance Calculation Functions
# ----------------------------------------------------------------------

def calculate_performance_metrics(config):
    """
    Calculates performance metrics for given configuration
    """
    # Weight breakdown
    total_weight = config['empty_weight'] + config['fuel_capacity'] + config['payload_weight']
    weight_margin = config['max_takeoff_weight'] - total_weight
    
    # Thrust-to-weight ratio
    thrust_to_weight = config['engine_thrust'] / (total_weight * 9.81)
    
    # Wing loading
    wing_loading = (total_weight * 9.81) / config['wing_area']  # N/m²
    
    # Power loading
    power_loading = (total_weight * 9.81) / config['engine_thrust']  # N/N
    
    # Fuel efficiency
    fuel_efficiency = config['engine_fuel_consumption'] / (config['cruise_speed'] / 1000)  # kg/km
    
    # Range capability
    theoretical_range = config['fuel_capacity'] / fuel_efficiency  # km
    
    # Stall speed estimation
    air_density = 1.225  # kg/m³ at sea level
    max_lift_coefficient = 1.4  # Typical for UAV airfoil
    stall_speed = np.sqrt((2 * total_weight * 9.81) / (air_density * config['wing_area'] * max_lift_coefficient))
    
    # Drop accuracy estimation
    drop_altitude = config['altitude']
    drop_time = np.sqrt(2 * drop_altitude / 9.81)  # seconds
    wind_speed = 8.0  # m/s (maximum expected)
    wind_drift = wind_speed * drop_time
    speed_drift = config['cruise_speed'] * drop_time / 10
    estimated_drop_accuracy = np.sqrt(wind_drift**2 + speed_drift**2)
    
    # Mission feasibility
    fuel_required = config['engine_fuel_consumption'] * config['mission_time']
    fuel_margin = config['fuel_capacity'] - fuel_required
    
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


def validate_constraints(config, performance):
    """
    Validates aircraft against competition constraints
    """
    validation = {}
    
    # Weight constraint
    validation['weight_constraint'] = performance['total_weight'] <= config['max_takeoff_weight']
    
    # Mission time constraint
    validation['time_constraint'] = config['mission_time'] <= 30
    
    # Altitude constraint
    validation['altitude_constraint'] = 50 <= config['altitude'] <= 60
    
    # Drop accuracy constraint
    validation['drop_accuracy_constraint'] = performance['estimated_drop_accuracy'] <= 5.0
    
    # Stall speed constraint
    validation['stall_speed_constraint'] = performance['stall_speed'] <= 12.0
    
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


# ----------------------------------------------------------------------
#   Optimization Analysis
# ----------------------------------------------------------------------

def find_optimal_configuration():
    """
    Finds optimal configuration within constraints
    """
    print("="*80)
    print("OPTIMAL CONFIGURATION ANALYSIS")
    print("Finding best parameters for competition performance")
    print("="*80)
    
    # Define parameter ranges
    wing_areas = np.linspace(0.6, 1.1, 6)
    thrust_values = np.linspace(120, 180, 7)
    fuel_capacities = np.linspace(2.0, 3.5, 6)
    cruise_speeds = np.linspace(10, 15, 6)
    
    best_config = None
    best_score = -float('inf')
    feasible_configs = []
    
    print("Searching for optimal configuration...")
    total_combinations = len(wing_areas) * len(thrust_values) * len(fuel_capacities) * len(cruise_speeds)
    current = 0
    
    for wing_area in wing_areas:
        for thrust in thrust_values:
            for fuel_capacity in fuel_capacities:
                for cruise_speed in cruise_speeds:
                    current += 1
                    if current % 100 == 0:
                        print(f"Progress: {current}/{total_combinations} ({current/total_combinations*100:.1f}%)")
                    
                    # Create configuration
                    config = get_base_configuration()
                    config['wing_area'] = wing_area
                    config['wing_span'] = np.sqrt(wing_area * config['aspect_ratio'])
                    config['engine_thrust'] = thrust
                    config['fuel_capacity'] = fuel_capacity
                    config['cruise_speed'] = cruise_speed
                    
                    # Calculate performance
                    performance = calculate_performance_metrics(config)
                    validation = validate_constraints(config, performance)
                    
                    # Calculate score (higher is better)
                    if validation['mission_feasible']:
                        score = calculate_performance_score(config, performance, validation)
                        feasible_configs.append((config, performance, validation, score))
                        
                        if score > best_score:
                            best_score = score
                            best_config = (config, performance, validation, score)
    
    # Print results
    print(f"\nFound {len(feasible_configs)} feasible configurations")
    
    if best_config:
        config, performance, validation, score = best_config
        print(f"\nBEST CONFIGURATION (Score: {score:.2f}):")
        print(f"  Wing Area: {config['wing_area']:.2f} m²")
        print(f"  Wing Span: {config['wing_span']:.2f} m")
        print(f"  Engine Thrust: {config['engine_thrust']:.0f} N")
        print(f"  Fuel Capacity: {config['fuel_capacity']:.1f} kg")
        print(f"  Cruise Speed: {config['cruise_speed']:.1f} m/s")
        print(f"  Total Weight: {performance['total_weight']:.1f} kg")
        print(f"  Stall Speed: {performance['stall_speed']:.1f} m/s")
        print(f"  Drop Accuracy: {performance['estimated_drop_accuracy']:.1f} m")
        print(f"  Thrust-to-Weight: {performance['thrust_to_weight']:.2f}")
    
    return best_config, feasible_configs


def calculate_performance_score(config, performance, validation):
    """
    Calculates a performance score for optimization
    """
    score = 0.0
    
    # Base score for feasibility
    if validation['mission_feasible']:
        score += 100
    
    # Weight margin (more margin is better)
    weight_margin_ratio = performance['weight_margin'] / config['max_takeoff_weight']
    score += weight_margin_ratio * 50
    
    # Stall speed margin (lower stall speed is better)
    stall_margin = 12.0 - performance['stall_speed']
    if stall_margin > 0:
        score += stall_margin * 10
    
    # Drop accuracy (better accuracy is better)
    drop_accuracy_penalty = max(0, performance['estimated_drop_accuracy'] - 5.0)
    score -= drop_accuracy_penalty * 5
    
    # Thrust-to-weight ratio (reasonable range is best)
    t_w_ratio = performance['thrust_to_weight']
    if 0.8 <= t_w_ratio <= 1.5:
        score += 20
    else:
        score -= abs(t_w_ratio - 1.15) * 10
    
    # Fuel efficiency (better efficiency is better)
    fuel_efficiency_bonus = max(0, 0.01 - performance['fuel_efficiency']) * 1000
    score += fuel_efficiency_bonus
    
    return score


# ----------------------------------------------------------------------
#   Main Execution
# ----------------------------------------------------------------------

def main():
    """
    Main function to run parameter sensitivity analysis
    """
    
    print("PARAMETER SENSITIVITY ANALYSIS")
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Run sensitivity analyses
    print("\n1. Wing Area Sensitivity Analysis")
    wing_results = wing_area_sensitivity()
    
    print("\n2. Engine Thrust Sensitivity Analysis")
    thrust_results = engine_thrust_sensitivity()
    
    print("\n3. Fuel Capacity Sensitivity Analysis")
    fuel_results = fuel_capacity_sensitivity()
    
    print("\n4. Cruise Speed Sensitivity Analysis")
    speed_results = cruise_speed_sensitivity()
    
    print("\n5. Optimal Configuration Analysis")
    optimal_config, feasible_configs = find_optimal_configuration()
    
    print("\nANALYSIS COMPLETE!")
    print("="*80)
    
    return {
        'wing_results': wing_results,
        'thrust_results': thrust_results,
        'fuel_results': fuel_results,
        'speed_results': speed_results,
        'optimal_config': optimal_config,
        'feasible_configs': feasible_configs,
    }


if __name__ == '__main__':
    main()
