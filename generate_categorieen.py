"""
Generate categorieen.txt with all category paths in parent--child--grandchild-- format
"""
import json

# Read grandchildren data
with open('categories/grandchildren.json', encoding='utf-8') as f:
    data = json.load(f)

# Generate category paths
lines = []
for item in data:
    line = f"{item['grandparentName']}--{item['parentName']}--{item['name']}--"
    lines.append(line)

# Sort alphabetically
lines.sort()

# Write to file
with open('categories/categorieen.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"Generated categorieen.txt with {len(lines)} category paths")
