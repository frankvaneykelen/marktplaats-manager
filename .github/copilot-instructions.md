# GitHub Copilot Instructions for Marktplaats Manager

## Creating Ads - General Instructions

Tip: Agent with GPT-4.1 works fine, no need for more expensive models.

When the user provides a prompt in the format: **"create a [book/non-book] ad [length] [width] [height] [weight]"**
These steps apply to ALL ads (books, non-books, etc.):

The text of the ad may not contain URLs or domain names, becuase Marktplaats disallows them.

> Gratis advertenties waarin kosteloos websites worden vermeld of wordt verwezen naar een website worden gedeactiveerd.

> In uw advertentie of in de foto bij uw advertentie staat een dergelijke verwijzing. Om deze reden is uw advertentie gedeactiveerd.

### Common Step 1: Calculate Shipping Options

First, run the shipping calculator to determine the appropriate package size:

```bash
.venv/Scripts/python shipping/calculate_shipping.py [length] [width] [height] [weight]
```

This will return the cheapest PostNL and DHL options, which determines the PackageSize field.

### Common Step 2: Create Folder Structure

Create the following folder structure:

```
ads/
└── [Ad Name]/
    ├── index.txt
    └── photos/
```

**ALWAYS create the `photos/` subfolder!**

### Common Step 3: List /ads/ Folder for Cross-Promotion

Before writing the closing text, you MUST:
1. Use `list_dir` tool on `c:\git\marktplaats\ads`
2. Identify similar items (same category, language, or genre)
3. Extract names/brands to include in the cross-promotion line

### Common Step 4: Standard Closing Format

Always include this exact closing (with blank lines between sections):

```
Ophalen of verzenden mogelijk. Bied wat het [item] voor jou waard is!

Zie ook mijn andere advertenties met [category description - e.g., "boeken van onder anderen [authors]" or "vintage items"].

[the result of the shipping calculator, e.g., "PostNL Brievenbuspakje €4.40 / DHL Brievenbuspakket naar ServicePoint €3.85"]
```

**CRITICAL:** You MUST:
1. List the /ads/ folder to see what other items are available
2. Extract relevant names for cross-promotion
3. Include the shipping calculator result as the LAST line
4. Maintain blank lines between each section of the closing

### Common Step 5: Confirm Completion

After creating the files, remind the user:
```
Done! Created the ad for **[Ad Name]** with the photos folder. 
Move your photos to `ads\[Ad Name]\photos\` and you're ready to go!
```

### Package Size Reference

Based on shipping calculator output:
- **Brievenbuspakje**: ≤ 2kg, fits in 38 x 26.5 x 3.2 cm
- **Klein pakket**: ≤ 3kg (PostNL) / ≤ 5kg (DHL)
- **Gemiddeld pakket**: ≤ 10kg
- **Groot pakket**: 10-23kg

---

## Creating Book Ads

When the user provides a prompt in the format: **"create a book ad [length] [width] [height] [weight]"**

Example: `create a book ad 19.6 13 1.3 170`

### Book-Specific Step 1: Analyze Photos

The user will have provided photos of the book. Extract information from the photos:
- **Title and Author** from the cover
- **Publication year** from copyright page or cover
- **ISBN** if visible
- **Publisher** if shown
- **Book condition** from visual inspection
- **Back cover description** for creating the ad text
- **Reviews/quotes** from cover or inside flaps
- **Weight and dimensions** from any notes in the photos

### Book-Specific Step 2: Create Folder Structure

Create folder using book title and author format:

```
ads/
└── [Book Title] - [Author]/
    ├── index.txt
    └── photos/
```

### Book-Specific Step 3: Generate index.txt

The index.txt file must follow this format:

```
[Category1]--[Category2]--[Category3]--[Subject]--[Year]--Gelezen--Bieden----[PackageSize]
---
[Ad Description]
```

#### Book Category Selection:

Only use the list in ../categories/categorieen.txt. **Do not invent or hallucinate new categories!**

For travel guides use `Boeken--Reisboeken en gidsen--Reisgidsen--`

**Subject (for when Category3 is "Beeldend"):**
- Only for specific art/culture books: Beeldhouwkunst, Grafische vormgeving, Schilder- en Tekenkunst, Overige onderwerpen

**Common Book Categories:**
- **Literatuur**: Literary fiction, classics (Allende, Brontë, Burroughs, Claudel, Coupland)
- **Romans**: General novels (Bakis, Claudel)
- **Spanning/Thriller**: Suspense, crime fiction
- **School, Studie en Wetenschap - Wetenschap**: Science books
- **School, Studie en Wetenschap - Informatica Computer**: Tech books
- **Kunst en Cultuur - Beeldend**: Art books
- **Overige - Biografieën**: Biographies

#### Book Ad Description Template:

```
[Book Title] - [Author]
[Optional: Publisher/Series info]

[Awards/Recognition if applicable - e.g., "Winnaar National Book Award 2018"]

[Opening paragraph describing the book's theme/significance]

**Het verhaal:** / **Over het boek:**
[Summary of the plot or main themes]

[Key quotes from the book or reviews - format with ""]

**Recensies:** / **Reviews:** (if available)
[Quotes from critics/publications with attribution]

[Additional context about the author or book's impact]

**Details:** / **Over [Author]:** (if relevant)
[Author bio or publication details]

Conditie: Gebruikt, gelezen maar in goede staat [add specific condition notes if needed]

**Specificaties:**
- Gewicht: [weight] gram
- Afmetingen: [length] x [width] x [height] cm
- Jaar: [year]
[Add ISBN, publisher, edition info if available]

```

### Book-Specific Writing Guidelines

**Tone & Style:**
- Enthusiastic and knowledgeable
- Use Dutch language naturally
- Highlight unique aspects (awards, author significance, cultural impact)
- Include relevant quotes from reviews or book covers
- Format reviews with attribution (e.g., "- De Groene Amsterdammer")

**Structure:**
- Start with book title and author
- Add recognition/awards if applicable (bold these)
- Provide context and significance
- Include plot/theme summary
- Add reviews/quotes if available
- End with condition, specifications, and standard closing

**CRITICAL for Books:**
1. List the /ads/ folder to see what other books are available
2. Extract author names from similar books (same language/genre). Use their full names, not just last names.
3. Include the shipping calculator result as the LAST line
4. Maintain blank lines between each section of the closing

---

## Creating Non-Book Ads

When the user provides a prompt in the format: **"create a non-book ad [item description] [length] [width] [height] [weight]"**

Example: `create a non-book ad vintage leather backpack 35 28 12 850`

### Non-Book Step 1: Analyze Photos

The user will have provided photos of the item. Extract information from the photos:
- **Item type and brand** from logos or tags
- **Color and material** from visual inspection
- **Condition** (new, vintage, used, etc.)
- **Special features** (zippers, pockets, buttons, decorative elements)
- **Size/dimensions** if visible in photos
- **Age/era** for vintage items
- **Damage or wear** from inspection
- **Original tags or labels** if present

### Non-Book Step 2: Create Folder Structure

Create folder using descriptive item name:

```
ads/
└── [Brand] [Item Type] [Distinguishing Feature]/
    ├── index.txt
    └── photos/
```

Examples:
- `Nike Air Max 90 Vintage Sneakers/`
- `Vintage Leather Backpack Brown/`
- `IKEA Billy Bookcase White/`

### Non-Book Step 3: Generate index.txt

The index.txt file must follow this format:

```
[Category1]--[Category2]--[Category3]----[Year]--[Condition]--Bieden----[PackageSize]
---
[Ad Description]
```

#### Non-Book Category Selection:

Only use the list in ../categories/categorieen.txt. **Do not invent or hallucinate new categories!**

For cassette tapes use `Cd's en Dvd's--Overige--Cassettebandjes--`

**Condition Options:**
- Nieuw (new)
- Zo goed als nieuw (like new)
- Gebruikt (used)
- Vintage

#### Non-Book Ad Description Template:

```
[Brand/Item Name] - [Item Type]

[Opening description - what makes this item special/unique]

**Kenmerken:** / **Features:**
- Merk: [brand]
- Kleur: [color]
- Materiaal: [material]
- Afmetingen: [dimensions if relevant]
[Add other relevant features]

**Conditie:** [New/Used/Vintage with specific details]
[Describe condition, any wear, damage, or special notes]

**Specificaties:**
- Gewicht: [weight] gram
- Afmetingen: [length] x [width] x [height] cm
[Add model number, year, size, etc. if applicable]

Ophalen of verzenden mogelijk. Bied wat [het/de] [item] voor jou waard is!

Zie ook mijn andere advertenties met [category description - e.g., "vintage items", "kleding", "elektronica"].

[the result of the shipping calculator, e.g., "PostNL Klein pakket €7.40 / DHL Pakket naar ServicePoint €4.45"]
```

### Non-Book Writing Guidelines

**Tone & Style:**
- Descriptive and honest
- Use Dutch language naturally
- Highlight unique features, brand value, or vintage appeal
- Be transparent about condition
- Focus on practical details (size, fit, compatibility)

**Structure:**
- Start with brand and item type
- Describe what makes it special
- List key features
- Detail condition honestly
- Provide specifications
- End with standard closing

**CRITICAL for Non-Books:**
1. List the /ads/ folder to see what other similar items are available
2. Extract item types/brands to include in cross-promotion
3. Include the shipping calculator result as the LAST line
4. Maintain blank lines between each section of the closing

### Non-Book Examples

**Clothing:**
- Category: `Kleding | Dames--Jassen--Winterjassen`
- Focus on: Brand, size, material, fit, condition
- Example: Vintage Levi's jacket, Nike sneakers

**Electronics:**
- Category: `Computers en Software--Randapparatuur--Toetsenborden en Muizen`
- Focus on: Model, compatibility, functionality, cables included
- Example: Mechanical keyboard, wireless mouse

**Furniture:**
- Category: `Huis en Inrichting--Meubels--Kasten`
- Focus on: Dimensions, material, assembly, pickup/delivery
- Example: IKEA bookcase, vintage dresser

**Vintage/Collectibles:**
- Category: `Antiek en Kunst--Curiosa en Brocante`
- Focus on: Age, rarity, condition, historical context
- Example: Vintage camera, old advertising signs

---

## Package Size Reference

Based on shipping calculator output:
- **Brievenbuspakje**: ≤ 2kg, fits in 38 x 26.5 x 3.2 cm
- **Klein pakket**: ≤ 3kg (PostNL) / ≤ 5kg (DHL)
- **Gemiddeld pakket**: ≤ 10kg
- **Groot pakket**: 10-23kg

### Example Prompts

**Books:**
- `create a book ad 19.6 13 1.3 170` → Brievenbuspakje
- `create a book ad 22 14 2.5 415` → Klein pakket

**Non-Books:**
- `create a non-book ad vintage backpack 35 28 12 850` → Klein pakket
- `create a non-book ad keyboard 45 15 3 620` → Klein pakket
- `create a non-book ad monitor 60 45 20 8500` → Gemiddeld pakket

---

## Notes

- Always create the `photos/` subfolder
- Use information from photos to write accurate descriptions
- Match tone to item type (enthusiastic for books, practical for electronics, etc.)
- Include all relevant specifications (ISBN for books, model numbers for electronics, etc.)
- For vintage items, mention era and unique characteristics
- Be honest about condition and any defects
