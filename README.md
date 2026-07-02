# Largest Number Finder

Finds the largest number in a PDF two ways:

1. **Raw** – the biggest number exactly as printed.
2. **Adjusted** – the biggest number after applying any scale labels like "in millions" or "in thousands".

## How to Run

Requires Python 3.8+.

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the script
python3 find_largest_number.py path/to/document.pdf
```

## Example Output

```
Largest raw number: 6,000,000.0 (page 93)
Largest adjusted number: 30,704,100,000.0 (page 13)
```

## How it Works

1. Read the PDF one page at a time with `pypdf`.
2. Scan each line for a scale label like `in millions`. When found, that multiplier is applied to the numbers that follow. The scale resets at the start of each new page.
3. For each number found, record its raw value and its adjusted value (raw × scale).
4. Report the largest of each.

## Assumption: Not Every Number on a Scaled Page gets Multiplied

Some pages, page 13 for example, mix dollar amounts with plain counts (headcount, work-years) under the same "Dollars in Millions" heading. Dollar amounts are written with a decimal (`30,704.1`), while counts are whole numbers (`35,110`). The code uses the rule where only numbers with a decimal get scaled when the heading is about dollars.

Without this, a headcount like `35,110` would be read as 35 billion, which isn't what the document means.
