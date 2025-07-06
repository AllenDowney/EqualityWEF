#!/usr/bin/env python3
import pdfplumber
import pandas as pd
import re


def extract_pdf_data(page_number, pattern):
    """Extract data from PDF using pdfplumber, print debug info, and return a dictionary of results."""
    pdf_path = f"pages/page_{page_number:03d}.pdf"
    result = {
        "country": None,
        "page_number": page_number,
        "score": None,
        "rank": None,
        "diff": None,
        "left": None,
        "right": None,
    }
    with pdfplumber.open(pdf_path) as pdf:
        # Get the first page
        page = pdf.pages[0]

        # Extract text
        text = page.extract_text()
        lines = text.split("\n")

        # Try to extract country name, score, rank, and year from line 13
        country_name = None
        if len(lines) > 13:
            line13 = lines[13]

        # To get the country name, extract everything before the first digit
        country_name = re.match(r"^([^\d]+)", line13)
        if country_name:
            country_name = country_name.group(1).strip()
            country_name = re.sub(r"\s*\(.*\)$", "", country_name).strip()
            result["country"] = country_name
            print(f"Extracted country: {country_name}")
        else:
            print("Debug - failed to find country name in line 13")

        # Extract education data
        found_pattern = False
        for i, line in enumerate(lines):
            if pattern in line.lower():
                found_pattern = True
                parts = line.split()

                # Handle literacy format (fewer parts)
                if pattern == "literacy" and len(parts) >= 4:
                    try:
                        rank_str = parts[2]  # "87th"
                        result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                        result["score"] = float(parts[3])  # "0.977"
                        # For literacy, diff, left, right are not available (shown as "-")
                    except (ValueError, IndexError) as e:
                        print(f"Parsing error: {e}")
                        print(f"Line: {line}")
                        print(f"Parts: {parts}")

                # Handle education format (more parts)
                elif len(parts) >= 9:
                    try:
                        rank_str = parts[4]
                        result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                        result["score"] = float(parts[5])
                        result["diff"] = float(parts[6])
                        result["left"] = float(parts[7])
                        result["right"] = float(parts[8])
                    except (ValueError, IndexError) as e:
                        print(f"Parsing error: {e}")
                        print(f"Line: {line}")
                        print(f"Parts: {parts}")
                else:
                    print(
                        f"Not enough parts in line (found {len(parts)}, need >=4 for literacy or >=9 for education)"
                    )
                break

        if not found_pattern:
            print("Pattern not found in any line!")
            print("Lines containing 'literacy':")
            for i, line in enumerate(lines):
                if "literacy" in line.lower():
                    print(f"Line {i}: {line}")

    return result


def read_pdfs(pattern):
    results = []
    for page_number in range(83, 375, 2):
        print(f"Processing page {page_number}...")
        data = extract_pdf_data(page_number, pattern)
        results.append(data)

    df = pd.DataFrame(results)
    return df


if __name__ == "__main__":
    # Process pages
    results = []
    for page_number in [117]:
        print(f"\nProcessing page {page_number}...")
        data = extract_pdf_data(page_number, "primary education")
        results.append(data)
    df = pd.DataFrame(results)
    print("\nDataFrame of extracted results:")
    print(df)
