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

        # Get the overall score
        if pattern.lower() == "gender gap index":
            print(f"DEBUG: Looking for gender gap index pattern")
            # Skip until we find "index and subindex"
            index_start = 0
            for i, line in enumerate(lines):
                if "index and subindex" in line.lower():
                    index_start = i + 1
                    print(f"DEBUG: Found 'index and subindex' at line {i}")
                    break
            
            # Look for "gender gap index" line after the index section starts
            for i, line in enumerate(lines[index_start:], start=index_start):
                if "gender gap index" in line.lower():
                    print(f"DEBUG: Found 'gender gap index' line at line {i}: '{line}'")
                    # The next line should contain the 2024 and 2023 data
                    if i + 1 < len(lines):
                        data_line = lines[i + 1]
                        print(f"DEBUG: Data line: '{data_line}'")
                        parts = data_line.split()
                        print(f"DEBUG: Data line parts: {parts}")
                        
                        # Look for 2024 data (usually the first set of numbers)
                        try:
                            # The format appears to be: [2024_score] [2024_rank] [2023_score] [2023_rank]
                            if len(parts) >= 2:
                                # First two parts should be 2024 score and rank
                                score_str = parts[0]  # e.g., "0.710"
                                rank_str = parts[1]   # e.g., "78th"
                                result["score"] = float(score_str)
                                result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                                print(f"DEBUG: Successfully parsed 2024 data - rank: {result['rank']}, score: {result['score']}")
                            else:
                                print(f"DEBUG: Not enough parts in data line: {parts}")
                        except (ValueError, IndexError) as e:
                            print(f"DEBUG: Error parsing gender gap index data: {e}")
                            print(f"Data line: {data_line}")
                            print(f"Parts: {parts}")
                    break

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
            if pattern.lower() not in line.lower():
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

            # Handle sex ratio format
            elif pattern == "sex ratio" and len(parts) >= 9:
                print(f"DEBUG: Processing sex ratio with {len(parts)} parts")
                try:
                    # Based on the output we saw: ['Sex', 'ratio', 'at', 'birth**%', '129th', '0.936', '-', '-', '-']
                    rank_str = parts[4]  # "129th"
                    result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                    result["score"] = float(parts[5])  # "0.936"
                    # For sex ratio, diff, left, right are not available (shown as "-")
                    if len(parts) > 6 and parts[6] != "-":
                        result["diff"] = float(parts[6])
                    if len(parts) > 7 and parts[7] != "-":
                        result["left"] = float(parts[7])
                    if len(parts) > 8 and parts[8] != "-":
                        result["right"] = float(parts[8])
                    print(f"DEBUG: Successfully parsed - rank: {result['rank']}, score: {result['score']}, diff: {result['diff']}, left: {result['left']}, right: {result['right']}")
                except (ValueError, IndexError) as e:
                    print(f"Parsing error: {e}")
                    print(f"Line: {line}")
                    print(f"Parts: {parts}")
                    if len(parts) > 8:
                        print(f"DEBUG: Last part '{parts[8]}' might be causing the issue")

            # Handle life expectancy format
            elif pattern == "life expectancy" and len(parts) >= 8:
                print(f"DEBUG: Processing life expectancy with {len(parts)} parts")
                try:
                    # Based on the output we saw: ['Healthy', 'life', 'expectancy**years', '58th', '1.046', '-', '-', '-']
                    rank_str = parts[3]  # "58th"
                    result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                    result["score"] = float(parts[4])  # "1.046"
                    # For life expectancy, diff, left, right are not available (shown as "-")
                    if len(parts) > 5 and parts[5] != "-":
                        result["diff"] = float(parts[5])
                    if len(parts) > 6 and parts[6] != "-":
                        result["left"] = float(parts[6])
                    if len(parts) > 7 and parts[7] != "-":
                        result["right"] = float(parts[7])
                    print(f"DEBUG: Successfully parsed - rank: {result['rank']}, score: {result['score']}, diff: {result['diff']}, left: {result['left']}, right: {result['right']}")
                    break
                except (ValueError, IndexError) as e:
                    print(f"DEBUG: Error parsing life expectancy data: {e}")
                    continue

            # Handle Health and Survival summary format
            elif pattern == "Health and Survival" and len(parts) >= 4 and line.lower().startswith("health and survival"):
                print(f"DEBUG: Processing Health and Survival summary with {len(parts)} parts")
                try:
                    rank_str = parts[3]  # "73rd" (not parts[2])
                    result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                    result["score"] = float(parts[4])  # "0.970" (not parts[3])
                    # For summary, diff, left, right may be unavailable (shown as "-")
                    if len(parts) > 5 and parts[5] != "-":
                        result["diff"] = float(parts[5])
                    if len(parts) > 6 and parts[6] != "-":
                        result["left"] = float(parts[6])
                    if len(parts) > 7 and parts[7] != "-":
                        result["right"] = float(parts[7])
                    print(f"DEBUG: Successfully parsed - rank: {result['rank']}, score: {result['score']}, diff: {result['diff']}, left: {result['left']}, right: {result['right']}")
                    break
                except (ValueError, IndexError) as e:
                    print(f"DEBUG: Error parsing Health and Survival data: {e}")
                    continue

            # Handle political empowerment format (summary line)
            elif pattern == "political empowerment" and len(parts) >= 4:
                print(f"DEBUG: Processing political empowerment with {len(parts)} parts")
                try:
                    # Based on the output we saw: ['Political', 'Empowerment', '61st', '0.257', '-', '-', '-']
                    rank_str = parts[2]  # "61st"
                    result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                    result["score"] = float(parts[3])  # "0.257"
                    # Handle missing values represented by "-"
                    result["diff"] = None if parts[4] == "-" else float(parts[4])
                    result["left"] = None if parts[5] == "-" else float(parts[5])
                    result["right"] = None if parts[6] == "-" else float(parts[6])
                    print(f"DEBUG: Successfully parsed - rank: {result['rank']}, score: {result['score']}, diff: {result['diff']}, left: {result['left']}, right: {result['right']}")
                    break
                except (ValueError, IndexError) as e:
                    print(f"DEBUG: Error parsing political empowerment data: {e}")
                    continue

            # Handle head of state format
            elif pattern == "head of state" and len(parts) >= 13:
                print(f"DEBUG: Processing head of state with {len(parts)} parts")
                try:
                    # Based on the output we saw: ['Years', 'with', 'female/male', 'head', 'of', 'state', '(last', '50)', '12th', '0.346', '-24.29', '12.85', '37.15', '0-50']
                    rank_str = parts[8]  # "12th"
                    result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                    result["score"] = float(parts[9])  # "0.346"
                    result["diff"] = float(parts[10])    # "-24.29"
                    result["left"] = float(parts[11])    # "12.85"
                    result["right"] = float(parts[12])   # "37.15"
                    print(f"DEBUG: Successfully parsed - rank: {result['rank']}, score: {result['score']}, diff: {result['diff']}, left: {result['left']}, right: {result['right']}")
                    break
                except (ValueError, IndexError) as e:
                    print(f"DEBUG: Error parsing head of state data: {e}")
                    continue

            # Handle ministerial positions format
            elif pattern == "ministerial positions" and len(parts) >= 9:
                print(f"DEBUG: Processing ministerial positions with {len(parts)} parts")
                try:
                    # Based on the output we saw: ['Women', 'in', 'ministerial', 'positions%', '116th', '0.125', '-77.78', '11.11', '88.89', '0-100']
                    rank_str = parts[4]  # "116th"
                    result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                    result["score"] = float(parts[5])  # "0.125"
                    result["diff"] = float(parts[6])    # "-77.78"
                    result["left"] = float(parts[7])    # "11.11"
                    result["right"] = float(parts[8])   # "88.89"
                    print(f"DEBUG: Successfully parsed - rank: {result['rank']}, score: {result['score']}, diff: {result['diff']}, left: {result['left']}, right: {result['right']}")
                    break
                except (ValueError, IndexError) as e:
                    print(f"DEBUG: Error parsing ministerial positions data: {e}")
                    continue

            # Handle women in parliament format
            elif pattern == "women in parliament" and len(parts) >= 8:
                print(f"DEBUG: Processing women in parliament with {len(parts)} parts")
                try:
                    # Based on the output we saw: ['Women', 'in', 'parliament%', '105th', '0.236', '-61.80', '19.10', '80.90', '0-100']
                    rank_str = parts[3]  # "105th"
                    result["rank"] = int("".join(filter(str.isdigit, rank_str)))
                    result["score"] = float(parts[4])  # "0.236"
                    result["diff"] = float(parts[5])    # "-61.80"
                    result["left"] = float(parts[6])    # "19.10"
                    result["right"] = float(parts[7])   # "80.90"
                    print(f"DEBUG: Successfully parsed - rank: {result['rank']}, score: {result['score']}, diff: {result['diff']}, left: {result['left']}, right: {result['right']}")
                    break
                except (ValueError, IndexError) as e:
                    print(f"DEBUG: Error parsing women in parliament data: {e}")
                    continue

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
            print("Lines containing 'health':")
            for i, line in enumerate(lines):
                if "health" in line.lower():
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
