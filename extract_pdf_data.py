#!/usr/bin/env python3
import pdfplumber
import pandas as pd
import re
import argparse


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
        # Skip lines until we find the marker
        start_idx = 0
        for i, line in enumerate(lines):
            if "global gender gap index indicators" in line.lower():
                start_idx = i + 1
                break
        # Now process only lines after the marker
        for i, line in enumerate(lines[start_idx:], start=start_idx):
            if pattern not in line.lower():
                continue

            found_pattern = True
            print(f"\nDEBUG: Found pattern '{pattern}' in line {i}: '{line}'")
            parts = line.split()
            print(f"DEBUG: Line parts: {parts}")
            print(f"DEBUG: Number of parts: {len(parts)}")

            if pattern == "educational attainment":
                # Only parse if line starts with 'Educational Attainment' and has at least 6 parts
                if line.lower().startswith("educational attainment") and len(parts) >= 6:
                    try:
                        rank_str = parts[2]  
                        result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                        result["score"] = float(parts[3]) 
                        break
                    except (ValueError, IndexError) as e:
                        print(f"Parsing error: {e}")
                        print(f"Line: {line}")
                        print(f"Parts: {parts}")

            # Handle literacy format (fewer parts)
            elif pattern == "literacy" and len(parts) >= 4:
                try:
                    rank_str = parts[2]  # "87th"
                    result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                    result["score"] = float(parts[3])  # "0.977"
                    # For literacy, diff, left, right are not available (shown as "-")
                except (ValueError, IndexError) as e:
                    print(f"Parsing error: {e}")
                    print(f"Line: {line}")
                    print(f"Parts: {parts}")

            # Handle labour-force participation rate format
            elif pattern == "labour-force participation rate" and len(parts) >= 9:
                print(f"DEBUG: Processing labour-force participation rate with {len(parts)} parts")
                try:
                    # Based on the output we saw: ['Labour-force', 'participation', 'rate%', '104th', '0.679', '-19.90', '42.17', '62.07', '0-100']
                    rank_str = parts[3]  # "104th"
                    result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                    result["score"] = float(parts[4])  # "0.679"
                    result["diff"] = float(parts[5])    # "-19.90"
                    result["left"] = float(parts[6])    # "42.17"
                    result["right"] = float(parts[7])   # "62.07"
                    print(f"DEBUG: Successfully parsed - rank: {result['rank']}, score: {result['score']}, diff: {result['diff']}, left: {result['left']}, right: {result['right']}")
                except (ValueError, IndexError) as e:
                    print(f"Parsing error: {e}")
                    print(f"Line: {line}")
                    print(f"Parts: {parts}")
                    # Try to parse the last part that might be causing issues
                    if len(parts) > 8:
                        print(f"DEBUG: Last part '{parts[8]}' might be causing the issue")

            # Handle professional and technical workers format
            elif pattern == "professional and technical workers" and len(parts) >= 10:
                print(f"DEBUG: Processing professional and technical workers with {len(parts)} parts")
                try:
                    # Based on the output we saw: ['Professional', 'and', 'technical', 'workers%', '1st', '1.000', '2.04', '48.98', '51.02', '0-100']
                    rank_str = parts[4]  # "1st"
                    result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                    result["score"] = float(parts[5])  # "1.000"
                    result["diff"] = float(parts[6])    # "2.04"
                    result["left"] = float(parts[7])    # "48.98"
                    result["right"] = float(parts[8])   # "51.02"
                    print(f"DEBUG: Successfully parsed - rank: {result['rank']}, score: {result['score']}, diff: {result['diff']}, left: {result['left']}, right: {result['right']}")
                except (ValueError, IndexError) as e:
                    print(f"Parsing error: {e}")
                    print(f"Line: {line}")
                    print(f"Parts: {parts}")
                    # Try to parse the last part that might be causing issues
                    if len(parts) > 9:
                        print(f"DEBUG: Last part '{parts[9]}' might be causing the issue")

            # Handle legislators format
            elif pattern == "legislators" and len(parts) >= 11:
                print(f"DEBUG: Processing legislators with {len(parts)} parts")
                try:
                    # Based on the output we saw: ['Legislators,', 'senior', 'officials', 'and', 'managers%', '106th', '0.349', '-48.24', '25.88', '74.12', '0-100']
                    rank_str = parts[5]  # "106th"
                    result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                    result["score"] = float(parts[6])  # "0.349"
                    result["diff"] = float(parts[7])    # "-48.24"
                    result["left"] = float(parts[8])    # "25.88"
                    result["right"] = float(parts[9])   # "74.12"
                    print(f"DEBUG: Successfully parsed - rank: {result['rank']}, score: {result['score']}, diff: {result['diff']}, left: {result['left']}, right: {result['right']}")
                except (ValueError, IndexError) as e:
                    print(f"Parsing error: {e}")
                    print(f"Line: {line}")
                    print(f"Parts: {parts}")
                    # Try to parse the last part that might be causing issues
                    if len(parts) > 10:
                        print(f"DEBUG: Last part '{parts[10]}' might be causing the issue")

            # Handle wage equality format
            elif pattern == "wage equality" and len(parts) >= 11:
                print(f"DEBUG: Processing wage equality with {len(parts)} parts")
                try:
                    # Based on the output we saw: ['Wage', 'equality', 'for', 'similar', 'work1-7', '(best)', '109th', '0.579', '-', '-', '-']
                    rank_str = parts[6]  # "109th"
                    result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                    result["score"] = float(parts[7])  # "0.579"
                    # For wage equality, diff, left, right are not available (shown as "-")
                    if parts[8] != "-":
                        result["diff"] = float(parts[8])
                    if parts[9] != "-":
                        result["left"] = float(parts[9])
                    if parts[10] != "-":
                        result["right"] = float(parts[10])
                    print(f"DEBUG: Successfully parsed - rank: {result['rank']}, score: {result['score']}, diff: {result['diff']}, left: {result['left']}, right: {result['right']}")
                except (ValueError, IndexError) as e:
                    print(f"Parsing error: {e}")
                    print(f"Line: {line}")
                    print(f"Parts: {parts}")
                    # Try to parse the last part that might be causing issues
                    if len(parts) > 10:
                        print(f"DEBUG: Last part '{parts[10]}' might be causing the issue")

            # Handle earned income format
            elif pattern == "earned income" and len(parts) >= 11:
                print(f"DEBUG: Processing earned income with {len(parts)} parts")
                try:
                    # Based on the output we saw: ['Estimated', 'earned', "incomeint'l", '$', '1,000', '91st', '0.598', '-8.45', '12.58', '21.03', '0-150']
                    rank_str = parts[5]  # "91st"
                    result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                    result["score"] = float(parts[6])  # "0.598"
                    result["diff"] = float(parts[7])    # "-8.45"
                    result["left"] = float(parts[8])    # "12.58"
                    result["right"] = float(parts[9])   # "21.03"
                    print(f"DEBUG: Successfully parsed - rank: {result['rank']}, score: {result['score']}, diff: {result['diff']}, left: {result['left']}, right: {result['right']}")
                except (ValueError, IndexError) as e:
                    print(f"Parsing error: {e}")
                    print(f"Line: {line}")
                    print(f"Parts: {parts}")
                    # Try to parse the last part that might be causing issues
                    if len(parts) > 10:
                        print(f"DEBUG: Last part '{parts[10]}' might be causing the issue")

            # Handle economic participation summary format
            elif pattern == "economic participation" and len(parts) >= 6 and line.lower().startswith("economic participation and opportunity"):
                print(f"DEBUG: Processing economic participation summary with {len(parts)} parts")
                try:
                    rank_str = parts[4]  # "107th"
                    result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                    result["score"] = float(parts[5])  # "0.620"
                    # For summary, diff, left, right may be unavailable (shown as "-")
                    if len(parts) > 6 and parts[6] != "-":
                        result["diff"] = float(parts[6])
                    if len(parts) > 7 and parts[7] != "-":
                        result["left"] = float(parts[7])
                    if len(parts) > 8 and parts[8] != "-":
                        result["right"] = float(parts[8])
                    print(f"DEBUG: Successfully parsed - rank: {result['rank']}, score: {result['score']}, diff: {result['diff']}, left: {result['left']}, right: {result['right']}")
                    break
                except (ValueError, IndexError) as e:
                    print(f"Parsing error: {e}")
                    print(f"Line: {line}")
                    print(f"Parts: {parts}")
                    if len(parts) > 8:
                        print(f"DEBUG: Last part '{parts[8]}' might be causing the issue")
                # Do not break here, continue to next line if parsing fails

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
            print("Lines containing 'economic':")
            for i, line in enumerate(lines):
                if "economic" in line.lower():
                    print(f"Line {i}: {line}")
            print("Lines containing 'participation':")
            for i, line in enumerate(lines):
                if "participation" in line.lower():
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
    parser = argparse.ArgumentParser(description="Extract PDF data for a given pattern.")
    parser.add_argument('--run-all', action='store_true', help='Process all pages (default: False)')
    parser.add_argument('--pattern', type=str, default='professional and technical workers', help='Pattern to search for in the PDF')
    args = parser.parse_args()

    pattern = args.pattern
    run_all = args.run_all
    if run_all:
        df = read_pdfs(pattern)
        df.to_csv(f"wef_{pattern.replace(' ', '_')}.csv", index=False)
    else:
        # Process pages
        results = []
        for page_number in [117]:
            print(f"\nProcessing page {page_number}...")
            data = extract_pdf_data(page_number, pattern)
            results.append(data)
        df = pd.DataFrame(results)
        print("\nDataFrame of extracted results:")
        print(df)
