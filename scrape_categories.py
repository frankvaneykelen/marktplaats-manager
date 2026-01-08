"""
Marktplaats Category Scraper
Fetches category data from the Marktplaats API using multi-level endpoints.
"""

import requests
import json
import os
import time
from datetime import datetime
from config import BROWSER_COOKIES


def get_headers():
    """Get HTTP headers for API requests"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'nl-NL,nl;q=0.9,en;q=0.8',
        'Referer': 'https://www.marktplaats.nl/',
        'Origin': 'https://www.marktplaats.nl',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    
    if BROWSER_COOKIES:
        headers['Cookie'] = BROWSER_COOKIES
    
    return headers


def fetch_json(url, description="data"):
    """Fetch JSON data from URL with error handling"""
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"  X Failed to fetch {description}: Status {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"  X Error fetching {description}: {e}")
        return None


def fetch_parent_categories():
    """Fetch parent categories from category-aggregate endpoint"""
    url = "https://www.marktplaats.nl/plaats/api/v1/category-aggregate"
    print(f"Fetching parent categories from {url}")
    
    data = fetch_json(url, "parent categories")
    if not data or not isinstance(data, list):
        print("X Invalid parent category data format")
        return []
    
    parents = []
    for item in data:
        parent = {
            'id': item.get('id'),
            'name': item.get('name'),
            'shortName': item.get('shortName')
        }
        parents.append(parent)
    
    print(f"+ Found {len(parents)} parent categories")
    return parents


def fetch_child_categories(parent_id, parent_name, current=None, total=None):
    """Fetch child categories (buckets) for a parent category"""
    url = f"https://www.marktplaats.nl/plaats/api/v1/category-aggregate/{parent_id}/buckets"
    counter = f"[{current:03d}/{total:03d}] " if current and total else ""
    print(f"  {counter}Fetching children for {parent_name} (ID: {parent_id})...") 
    
    data = fetch_json(url, f"children of {parent_name}")
    
    if data is None:
        print(f"    (API returned None)")
        return []
    
    children = []
    
    # Handle both dict format {"id": "name"} and list format [{"id": x, "name": y}]
    if isinstance(data, dict):
        # Dict format: {"33": "Eten en Koken", "36": "Kunst en Cultuur"}
        for bucket_id, bucket_name in data.items():
            child = {
                'id': int(bucket_id),
                'name': bucket_name,
                'parentId': parent_id,
                'parentName': parent_name
            }
            children.append(child)
    elif isinstance(data, list):
        # List format: [{"id": 33, "name": "Eten en Koken"}]
        for item in data:
            if isinstance(item, dict) and 'id' in item and 'name' in item:
                child = {
                    'id': item['id'],
                    'name': item['name'],
                    'parentId': parent_id,
                    'parentName': parent_name
                }
                children.append(child)
    else:
        print(f"    (Invalid format - expected dict or list, got {type(data)})")
        return []
    
    print(f"    + Found {len(children)} children")
    return children


def fetch_grandchild_categories(parent_id, parent_name, child_id, child_name):
    """Fetch grandchild categories for a child category"""
    url = f"https://www.marktplaats.nl/plaats/api/v1/category-aggregate/{parent_id}/buckets/{child_id}/categories"
    
    data = fetch_json(url, f"grandchildren of {child_name}")
    
    # Categories endpoint returns a list of objects
    if not data or not isinstance(data, list):
        return []
    
    grandchildren = []
    for item in data:
        if isinstance(item, dict):
            grandchild = {
                'id': item.get('id'),
                'name': item.get('name'),
                'shortName': item.get('shortName'),
                'parentId': child_id,
                'parentName': child_name,
                'grandparentId': parent_id,
                'grandparentName': parent_name
            }
            grandchildren.append(grandchild)
    
    return grandchildren


def fetch_all_categories():
    """Fetch all categories using multi-level API endpoints"""
    print("=" * 60)
    print("Fetching categories from Marktplaats API")
    print("=" * 60)
    print()
    
    # Fetch parent categories
    parents = fetch_parent_categories()
    if not parents:
        return None
    
    print()
    
    all_children = []
    all_grandchildren = []
    nested_structure = []
    
    total_parents = len(parents)
    
    # Fetch children and grandchildren for each parent
    for idx, parent in enumerate(parents, 1):
        parent_id = parent['id']
        parent_name = parent['name']
        
        # Fetch children (buckets)
        children = fetch_child_categories(parent_id, parent_name, idx, total_parents)
        
        parent_nested = {
            'id': parent_id,
            'name': parent_name,
            'shortName': parent.get('shortName'),
            'children': []
        }
        
        # Fetch grandchildren for each child
        for child in children:
            child_id = child['id']
            child_name = child['name']
            
            all_children.append(child)
            
            # Fetch grandchildren
            grandchildren = fetch_grandchild_categories(parent_id, parent_name, child_id, child_name)
            all_grandchildren.extend(grandchildren)
            
            # For nested structure, only keep essential fields (no redundant parent references)
            grandchildren_nested = []
            for gc in grandchildren:
                grandchildren_nested.append({
                    'id': gc['id'],
                    'name': gc['name'],
                    'shortName': gc.get('shortName')
                })
            
            child_nested = {
                'id': child_id,
                'name': child_name,
                'parentId': parent_id,
                'parentShortName': parent.get('shortName'),
                'children': grandchildren_nested
            }
            
            parent_nested['children'].append(child_nested)
            
            # Small delay to avoid overwhelming the API
            time.sleep(0.1)
        
        nested_structure.append(parent_nested)
        print()
    
    return {
        'parents': parents,
        'children': all_children,
        'grandchildren': all_grandchildren,
        'nested': nested_structure
    }


def save_files(parsed_data):
    """Save parsed data to various file formats"""
    output_dir = 'categories'
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Save parent categories
    with open(f'{output_dir}/parents.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_data['parents'], f, indent=2, ensure_ascii=False)
    print(f"+ Saved {len(parsed_data['parents'])} parent categories to {output_dir}/parents.json")
    
    # Save child categories
    with open(f'{output_dir}/children.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_data['children'], f, indent=2, ensure_ascii=False)
    print(f"+ Saved {len(parsed_data['children'])} child categories to {output_dir}/children.json")
    
    # Save grandchild categories
    with open(f'{output_dir}/grandchildren.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_data['grandchildren'], f, indent=2, ensure_ascii=False)
    print(f"+ Saved {len(parsed_data['grandchildren'])} grandchild categories to {output_dir}/grandchildren.json")
    
    # Save consolidated nested master file
    master_data = {
        'generated_at': timestamp,
        'total_parents': len(parsed_data['parents']),
        'total_children': len(parsed_data['children']),
        'total_grandchildren': len(parsed_data['grandchildren']),
        'categories': parsed_data['nested']
    }
    with open(f'{output_dir}/categories_master.json', 'w', encoding='utf-8') as f:
        json.dump(master_data, f, indent=2, ensure_ascii=False)
    print(f"+ Saved consolidated master file to {output_dir}/categories_master.json")
    
    # Generate markdown file
    generate_markdown(parsed_data, timestamp, output_dir)


def generate_markdown(parsed_data, timestamp, output_dir):
    """Generate human-readable markdown file"""
    md_content = f"""# Marktplaats Categories

**Generated:** {timestamp}  
**Total Parent Categories:** {len(parsed_data['parents'])}  
**Total Child Categories:** {len(parsed_data['children'])}  
**Total Grandchild Categories:** {len(parsed_data['grandchildren'])}

---

## Category Tree

"""
    
    # Build nested tree structure
    for parent in parsed_data['nested']:
        # Parent category (L1)
        md_content += f"### {parent['name']} (ID: {parent['id']})\n\n"
        
        if parent['children']:
            for child in parent['children']:
                # Child category (L2)
                md_content += f"- **{child['name']}** (ID: {child['id']})\n"
                
                if child['children']:
                    for grandchild in child['children']:
                        # Grandchild category (L3)
                        md_content += f"  - {grandchild['name']} (ID: {grandchild['id']})\n"
                    md_content += "\n"
        else:
            md_content += "*No subcategories*\n"
        
        md_content += "\n"
    
    # Add flat lists section
    md_content += "\n---\n\n## Flat Lists\n\n"
    
    md_content += "### All Parent Categories\n\n"
    for parent in parsed_data['parents']:
        md_content += f"- {parent['name']} (ID: {parent['id']})\n"
    
    md_content += "\n### All Child Categories\n\n"
    for child in parsed_data['children']:
        md_content += f"- {child['name']} -> {child['parentName']} (ID: {child['id']})\n"
    
    md_content += "\n### All Grandchild Categories\n\n"
    for grandchild in parsed_data['grandchildren']:
        md_content += f"- {grandchild['name']} -> {grandchild['parentName']} -> {grandchild['grandparentName']} (ID: {grandchild['id']})\n"
    
    # Save markdown file
    with open(f'{output_dir}/categories.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"+ Saved readable markdown to {output_dir}/categories.md")


def main():
    """Main execution function"""
    print("=" * 60)
    print("Marktplaats Category Scraper")
    print("=" * 60)
    print()
    
    if BROWSER_COOKIES:
        print("- Using browser cookies for authentication")
    else:
        print("WARNING: No browser cookies configured - API may fail")
        print("  Add BROWSER_COOKIES to config.py if you get 401 errors")
    print()
    
    # Fetch all categories using multi-level API
    data = fetch_all_categories()
    if not data:
        print("\nX Failed to fetch category data. Exiting.")
        return
    
    print()
    print("=" * 60)
    print(f"+ Fetched {len(data['parents'])} parents, "
          f"{len(data['children'])} children, "
          f"{len(data['grandchildren'])} grandchildren")
    print("=" * 60)
    print()
    
    # Save to files
    print("Saving files...")
    save_files(data)
    
    print()
    print("=" * 60)
    print("+ Complete! Check the 'categories' folder for output files.")
    print("=" * 60)


if __name__ == "__main__":
    main()

