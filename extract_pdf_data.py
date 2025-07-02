#!/usr/bin/env python3
import pdfplumber
import pandas as pd
import re

def extract_pdf_data(page_number, pdf_path):
    """Extract data from PDF using pdfplumber, print debug info, and return a dictionary of results."""
    result = {
        "country_name": None,
        "page_number": page_number,
        "tert_ed_score": None,
        "tert_ed_rank": None,
        "tert_ed_diff": None,
        "tert_ed_left": None,
        "tert_ed_right": None,
    }
    with pdfplumber.open(pdf_path) as pdf:
        # Get the first page
        page = pdf.pages[0]
        
        # Extract text
        text = page.extract_text()
        lines = text.split('\n')

        # Try to extract country name, score, rank, and year from line 13
        country_name = None
        if len(lines) > 13:
            line13 = lines[13]

        # To get the country name, extract everything before the first digit
        country_match = re.match(r"^([^\d]+)", line13)
        if country_match:
            country_name = country_match.group(1).strip()
            country_name = re.sub(r"\s*\(.*\)$", "", country_name).strip()
            result["country_name"] = country_name
        else:
            print("Debug - failed to find country name in line 13")
        
        # Extract tertiary education data
        for i, line in enumerate(lines):
            if 'tertiary education' in line.lower():
                parts = line.split()
                if len(parts) >= 9:
                    try:
                        rank_str = parts[4]
                        result["tert_ed_rank"] = int(''.join(filter(str.isdigit, rank_str)))
                        result["tert_ed_score"] = float(parts[5])
                        result["tert_ed_diff"] = float(parts[6])
                        result["tert_ed_left"] = float(parts[7])
                        result["tert_ed_right"] = float(parts[8])
                    except (ValueError, IndexError) as e:
                        print(f"Error parsing tertiary education line: {e}")
                        print(f"Line: {line}")
                        print(f"Parts: {parts}")
                break
    
    return result

if __name__ == "__main__":
    # Process pages
    results = []
    for i in [117]:
        filename = f"page_{i:03d}.pdf"
        print(f"\nProcessing {filename}...")
        data = extract_pdf_data(i, filename)
        results.append(data)
    df = pd.DataFrame(results)
    print("\nDataFrame of extracted results:")
    print(df)
