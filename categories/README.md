# Marktplaats Categories

This folder contains scraped category data from the Marktplaats API.

## Files Overview

| File | Source API | Description |
|------|-----------|-------------|
| `parents.json` | `/category-aggregate` | 36 top-level parent categories |
| `children.json` | `/category-aggregate/{id}/buckets` | 375 child/bucket categories with parent references |
| `grandchildren.json` | `/category-aggregate/{id}/buckets/{bucket_id}/categories` | 2068 grandchild categories with full hierarchy |
| `categories_master.json` | All 3 APIs combined | Nested structure with metadata + all categories |
| `categories.md` | Generated from JSON | Human-readable markdown with tree view |
| `categorieen.txt` | Generated from grandchildren.json | Flat list of category paths in `parent--child--grandchild--` format for use in `Categorie.txt` files |

## API Structure

The Marktplaats API uses a **3-level hierarchy**:

### Level 1: Parent Categories
```
GET https://www.marktplaats.nl/plaats/api/v1/category-aggregate
```
Returns: List of 36 parent objects
```json
[
  {
    "id": 1,
    "name": "Antiek en Kunst",
    "shortName": "Antiek en Kunst"
  },
  ...
]
```

### Level 2: Child Categories (Buckets)
```
GET https://www.marktplaats.nl/plaats/api/v1/category-aggregate/{parent_id}/buckets
```
Returns: Dict `{"id": "name"}` or List `[{"id": x, "name": y}]`
```json
{
  "1": "Antiek | Eetgerei",
  "2": "Antiek | Gebruiksvoorwerpen",
  ...
}
```

### Level 3: Grandchild Categories
```
GET https://www.marktplaats.nl/plaats/api/v1/category-aggregate/{parent_id}/buckets/{bucket_id}/categories
```
Returns: List of category objects
```json
[
  {
    "id": 2,
    "name": "Bestek",
    "shortName": "Bestek"
  },
  ...
]
```

## Authentication

The API requires **browser cookies** from an active Marktplaats session:

1. Open Marktplaats in your browser and log in
2. Open Developer Tools (F12) → **Application** tab → **Cookies**
3. Copy entire cookie string
4. Add to `config.py`:
   ```python
   BROWSER_COOKIES = "your_cookie_string_here"
   ```

See main [README.md](../README.md#browser-cookies-for-api-access) for detailed instructions.

## Running the Scripts

### 1. Scrape All Categories

```bash
python scrape_categories.py
```

**What it does:**
- Fetches all 36 parent categories
- For each parent, fetches children (with 0.1s delay between requests)
- For each child, fetches grandchildren
- Generates 5 files: `parents.json`, `children.json`, `grandchildren.json`, `categories_master.json`, `categories.md`

**Output:**
```
[001/036] Fetching children for Antiek en Kunst (ID: 1)...
  + Found 11 children
[002/036] Fetching children for Audio, Tv en Foto (ID: 31)...
  + Found 10 children
...
+ Fetched 36 parents, 375 children, 2068 grandchildren
```

**Time:** ~40 seconds (0.1s delay × 375 children)

### 2. Generate Category Paths

```bash
python generate_categorieen.py
```

**What it does:**
- Reads `grandchildren.json`
- Formats each category as `parent--child--grandchild--`
- Sorts alphabetically
- Saves to `categorieen.txt`

**Output:**
```
Generated categorieen.txt with 2068 category paths
```

**Usage:** Copy category paths from `categorieen.txt` to your ad's `Categorie.txt` file:
```
Computers en Software--Computeronderdelen--Computerbehuizingen--Gebruikt--Vraagprijs--400,00--Zwaar--
```

## File Structure Examples

### parents.json
```json
[
  {
    "id": 1,
    "name": "Antiek en Kunst",
    "shortName": "Antiek en Kunst"
  }
]
```

### children.json
```json
[
  {
    "id": 1,
    "name": "Antiek | Eetgerei",
    "parentId": 1,
    "parentName": "Antiek en Kunst"
  }
]
```

### grandchildren.json
```json
[
  {
    "id": 2,
    "name": "Bestek",
    "shortName": "Bestek",
    "parentId": 1,
    "parentName": "Antiek | Eetgerei",
    "grandparentId": 1,
    "grandparentName": "Antiek en Kunst"
  }
]
```

### categories_master.json
```json
{
  "generated_at": "2026-01-09 00:12:22",
  "total_parents": 36,
  "total_children": 375,
  "total_grandchildren": 2068,
  "categories": [
    {
      "id": 1,
      "name": "Antiek en Kunst",
      "children": [
        {
          "id": 1,
          "name": "Antiek | Eetgerei",
          "children": [
            {
              "id": 2,
              "name": "Bestek",
              "shortName": "Bestek"
            }
          ]
        }
      ]
    }
  ]
}
```

### categorieen.txt
```
Antiek en Kunst--Antiek | Eetgerei--Bestek--
Antiek en Kunst--Antiek | Eetgerei--Schalen--
Antiek en Kunst--Antiek | Eetgerei--Servies compleet--
...
```

## Updating Categories

Categories can change over time. To refresh:

```bash
# Re-scrape all categories
python scrape_categories.py

# Regenerate category paths
python generate_categorieen.py
```

**Recommended:** Update monthly or when you notice new categories on Marktplaats.

## Troubleshooting

### Error: 401 Unauthorized
- Your browser cookies expired
- Update `BROWSER_COOKIES` in `config.py`
- See [README.md](../README.md#extracting-cookies-from-browser) for instructions

### Error: Missing files
- Run `python scrape_categories.py` first
- Then run `python generate_categorieen.py`

### Unicode errors in terminal
- Already fixed: Script uses `+` and `X` instead of ✓ and ✗
- Files use UTF-8 encoding

## File Sizes

- `parents.json`: ~2 KB
- `children.json`: ~20 KB
- `grandchildren.json`: ~200 KB
- `categories_master.json`: ~180 KB (optimized nested structure)
- `categories.md`: ~150 KB
- `categorieen.txt`: ~150 KB
