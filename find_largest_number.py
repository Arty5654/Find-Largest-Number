# Find the largest number in a PDF, both raw and adjusted for unit labels
# Usage: python find_largest_number.py path/to/document.pdf

import argparse
import re

from pypdf import PdfReader

# Matches numbers like 1,234
NUMBER_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")

# Unit labels and their multipliers
SCALE_PATTERNS = [
    (re.compile(r"in\s+trillions", re.IGNORECASE), 1_000_000_000_000),
    (re.compile(r"in\s+billions", re.IGNORECASE), 1_000_000_000),
    (re.compile(r"in\s+millions", re.IGNORECASE), 1_000_000),
    (re.compile(r"in\s+thousands", re.IGNORECASE), 1_000),
]


def get_scale(line):
    # If this line declares a unit, like Millions, return the multiplier
    for pattern, multiplier in SCALE_PATTERNS:
        if pattern.search(line):
            return multiplier
    return None

def should_scale(num, line):
    # Check if the number is a dollar value by checking if there is a decmial point
    if f"${num}" in line:
        return False
    return "." in num



def find_numbers(pdf_path):
    # Read every page of the PDF and return a list of (raw, adjusted, page, line)
    results = []
    reader = PdfReader(pdf_path)

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        # Reset each page
        current_scale = 1

        for line in text.splitlines():
            # If the line says a unit, such as "in millions," then update the scale
            scale = get_scale(line)
            if scale is not None:
                current_scale = scale

            # Find every number on current line
            for num in NUMBER_RE.findall(line):
                value = float(num.replace(",", ""))
                # Only scale decial numbers to not confuse non-dollar values
                if current_scale > 1 and should_scale(num, line):
                    adjusted = value * current_scale
                else:
                    adjusted = value
                results.append((value, adjusted, page_num, line.strip()))

    return results


def main():
    parser = argparse.ArgumentParser(description="Find the largest number in a PDF.")
    parser.add_argument("pdf", help="Path to the PDF file.")
    args = parser.parse_args()

    numbers = find_numbers(args.pdf)

    raw_value, _, raw_page, _ = max(numbers, key=lambda x: x[0])
    _, adj_scaled, adj_page, _ = max(numbers, key=lambda x: x[1])

    print(f"Largest raw number: {raw_value:,} (page {raw_page})")
    print(f"Largest adjusted number: {adj_scaled:,} (page {adj_page})")


if __name__ == "__main__":
    main()
