#!/usr/bin/env python3
"""
Shipping cost calculator for PostNL and DHL
Usage: python calculate_shipping.py <length> <width> <height> <weight> [country]
Example: python calculate_shipping.py 19.6 13 1.3 170
Example: python calculate_shipping.py 19.6 13 1.3 170 BE
"""

import sys
import yaml
from pathlib import Path


def parse_dimensions(dim_str):
    """Parse dimension string like '38 x 26.5 x 3.2 cm' or '14 x 9 cm' or special formats"""
    # Handle special format like "L + B + H = max. 90 cm, langste zijde = max. 60 cm"
    if 'L + B + H' in dim_str:
        # Skip this complex format for now - we can't easily parse it
        return None
    
    parts = dim_str.replace('cm', '').strip().split('x')
    return [float(p.strip()) for p in parts]


def fits_in_box(pkg_dims, max_dims):
    """Check if package fits in the shipping box (any orientation)"""
    # Sort both dimension lists to compare smallest to smallest, etc.
    pkg_sorted = sorted(pkg_dims)
    max_sorted = sorted(max_dims)
    
    # Check if all package dimensions fit within box dimensions
    return all(p <= m for p, m in zip(pkg_sorted, max_sorted))


def parse_weight_limit(weight_str):
    """Parse weight string like '2 kg' or '500 g' to grams"""
    weight_str = weight_str.strip().lower()
    if 'kg' in weight_str:
        return float(weight_str.replace('kg', '').strip()) * 1000
    elif 'g' in weight_str:
        return float(weight_str.replace('g', '').strip())
    return float(weight_str)


def find_cheapest_options(length, width, height, weight, country='Nederland'):
    """Find cheapest PostNL and DHL shipping options"""
    # Load tariffs
    tariffs_file = Path(__file__).parent / 'tariffs.yaml'
    with open(tariffs_file, 'r', encoding='utf-8') as f:
        tariffs = yaml.safe_load(f)
    
    pkg_dims = [length, width, height]
    weight_g = weight
    
    postnl_options = []
    dhl_options = []
    
    # Get country data
    country_key = 'België' if country.upper() in ['BE', 'BELGIË', 'BELGIUM'] else 'Nederland'
    
    # Check PostNL options
    if 'PostNL' in tariffs and country_key in tariffs['PostNL']:
        for service_name, service_data in tariffs['PostNL'][country_key].items():
            if not isinstance(service_data, dict):
                continue
            
            # Check dimensions
            if 'max. dimensions' in service_data:
                max_dims = parse_dimensions(service_data['max. dimensions'])
                if max_dims is None:
                    continue
                if not fits_in_box(pkg_dims, max_dims):
                    continue
            
            # Check weight
            if 'max. weight' in service_data:
                max_weight = parse_weight_limit(service_data['max. weight'])
                if weight_g > max_weight:
                    continue
            
            if 'min. weight' in service_data:
                min_weight = parse_weight_limit(service_data['min. weight'])
                if weight_g < min_weight:
                    continue
            
            # Get price
            if 'price' in service_data:
                price_str = service_data['price'].replace('€', '').strip()
                price = float(price_str)
                postnl_options.append({
                    'name': service_name,
                    'price': price,
                    'price_str': service_data['price']
                })
    
    # Check DHL options
    if 'DHL' in tariffs and country_key in tariffs['DHL']:
        for service_name, service_data in tariffs['DHL'][country_key].items():
            if not isinstance(service_data, dict) or service_name == 'Extra opties':
                continue
            
            # Check dimensions
            if 'max. dimensions' in service_data:
                max_dims = parse_dimensions(service_data['max. dimensions'])
                if max_dims is None:
                    continue
                if not fits_in_box(pkg_dims, max_dims):
                    continue
            
            # Check weight
            if 'max. weight' in service_data:
                max_weight = parse_weight_limit(service_data['max. weight'])
                if weight_g > max_weight:
                    continue
            
            if 'min. weight' in service_data:
                min_weight = parse_weight_limit(service_data['min. weight'])
                if weight_g < min_weight:
                    continue
            
            # Get price
            if 'price' in service_data:
                price_str = service_data['price'].replace('€', '').strip()
                price = float(price_str)
                dhl_options.append({
                    'name': service_name,
                    'price': price,
                    'price_str': service_data['price']
                })
    
    # Find cheapest options (prefer pakket/brievenbuspakket over envelop)
    def service_priority(option):
        """Lower score = higher priority. Prefer brievenbuspakket over envelop."""
        name = option['name'].lower()
        if 'envelop' in name and 'brievenbuspakket' not in name:
            return (2, option['price'])  # Lowest priority
        elif 'brievenbuspakket' in name or 'brievenbuspakje' in name:
            return (0, option['price'])  # Highest priority
        else:
            return (1, option['price'])  # Medium priority
    
    cheapest_postnl = min(postnl_options, key=service_priority) if postnl_options else None
    cheapest_dhl = min(dhl_options, key=service_priority) if dhl_options else None
    
    return cheapest_postnl, cheapest_dhl


def main():
    if len(sys.argv) < 5:
        print("Usage: python calculate_shipping.py <length> <width> <height> <weight> [country]")
        print("Example: python calculate_shipping.py 19.6 13 1.3 170")
        print("Example: python calculate_shipping.py 19.6 13 1.3 170 BE")
        sys.exit(1)
    
    try:
        length = float(sys.argv[1])
        width = float(sys.argv[2])
        height = float(sys.argv[3])
        weight = float(sys.argv[4])
        country = sys.argv[5] if len(sys.argv) > 5 else 'NL'
        
        postnl, dhl = find_cheapest_options(length, width, height, weight, country)
        
        results = []
        if postnl:
            results.append(f"PostNL {postnl['name']} {postnl['price_str']}")
        if dhl:
            results.append(f"DHL {dhl['name']} {dhl['price_str']}")
        
        if results:
            print(' / '.join(results))
        else:
            print("No shipping options found for these dimensions/weight")
    
    except ValueError as e:
        print(f"Error: Invalid input - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
