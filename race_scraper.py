# Race Results Scraper
# This script scrapes race timing data from a sports timing website using bib numbers
# It handles data backup, resumption of interrupted scraping, and CSV output

import requests
from bs4 import BeautifulSoup
import csv
import time
import os
from datetime import datetime

# Base URL for the timing website - accepts bib number as a query parameter
# Example: https://sowers.ibansport.hk/?query=1001
url_pattern = "https://sowers.ibansport.hk/?query={}"

def get_scraped_bibs(filename):
    """
    Load a set of previously scraped bib numbers from an existing CSV file.
    This allows the script to resume from where it left off if interrupted.
    
    Args:
        filename (str): Path to the CSV file containing previously scraped results
        
    Returns:
        set: A set of bib numbers that have already been scraped
    """
    scraped_bibs = set()
    if os.path.exists(filename):
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                try:
                    next(reader)  # Skip the header row
                except StopIteration:
                    return scraped_bibs  # Return empty set for empty file
                
                # Add each bib number to the set
                for row in reader:
                    if row and row[0]:  # Check for valid bib number in first column
                        scraped_bibs.add(row[0])
        except Exception as e:
            print(f"Error reading backup file: {str(e)}")
            return set()  # Return empty set on error
    return scraped_bibs

def append_to_csv(filename, row, write_header=False):
    """
    Append a single result row to the CSV file. Creates new file with header if needed.
    
    Args:
        filename (str): Path to the CSV file
        row (list): Data row to append
        write_header (bool): Whether to write the header row (for new files)
    """
    try:
        file_exists = os.path.exists(filename)
        mode = 'a' if file_exists else 'w'
        with open(filename, mode=mode, newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if write_header and not file_exists:
                # Define CSV headers for race timing data
                writer.writerow(["Bib Number", "Runner Name", "Category Ranking", 
                               "CP1 Time", "CP2 Time", "CP3 Time", "CP4 Time", 
                               "CP5 Time", "FP Time", "Timestamp"])
            writer.writerow(row)
    except Exception as e:
        print(f"Error writing to CSV: {str(e)}")

# Main execution block
if __name__ == "__main__":
    # Output filename for results
    filename = "race_results.csv"
    backup_name = None

    # Create backup of existing results file if it exists
    # This prevents data loss if the script needs to be restarted
    if os.path.exists(filename):
        backup_name = f"race_results_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            os.rename(filename, backup_name)
            print(f"Created backup of existing file: {backup_name}")
        except Exception as e:
            print(f"Error creating backup: {str(e)}")
            backup_name = None

    # Load previously scraped bib numbers to avoid duplicate scraping
    scraped_bibs = get_scraped_bibs(backup_name) if backup_name else set()

    # Create new results file with headers
    append_to_csv(filename, [], write_header=True)

    # Main scraping loop - processes each bib number in range
    for bib_number in range(1001, 9999):  # Adjust range based on race parameters
        # Skip previously scraped bib numbers
        if str(bib_number) in scraped_bibs:
            print(f"Bib {bib_number} already scraped, skipping...")
            continue
            
        print(f"Scraping data for Bib {bib_number}...")
        url = url_pattern.format(bib_number)
        
        try:
            # Request the timing data page for this bib number
            response = requests.get(url)
            time.sleep(0)  # Optional delay between requests (adjust as needed)
            
            if response.status_code == 200:
                # Parse the HTML response
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find all paragraphs containing timing data
                paragraphs = soup.find_all('p')
                
                # Initialize dictionary to store runner's data
                data = {
                    "bib": None,
                    "name": None,
                    "category": None,
                    "cp1": None,  # Checkpoint 1 time
                    "cp2": None,  # Checkpoint 2 time
                    "cp3": None,  # Checkpoint 3 time
                    "cp4": None,  # Checkpoint 4 time
                    "cp5": None,  # Checkpoint 5 time
                    "fp": None    # Finish time
                }
                
                # Parse each paragraph for timing data
                for p in paragraphs:
                    text_tag = p.find('text')
                    if text_tag:
                        label = text_tag.text.strip()
                        value = p.text.replace(label, '').strip()
                        
                        # Map data to appropriate dictionary keys
                        if "Bib Number" in label:
                            data["bib"] = value
                        elif "Runner Name" in label:
                            data["name"] = value
                        elif "Category Ranking" in label:
                            data["category"] = value
                        elif "CP1" in label:
                            data["cp1"] = value
                        elif "CP2" in label:
                            data["cp2"] = value
                        elif "CP3" in label:
                            data["cp3"] = value
                        elif "CP4" in label:
                            data["cp4"] = value
                        elif "CP5" in label:
                            data["cp5"] = value
                        elif "FP" in label:
                            data["fp"] = value

                # Only save if we found valid runner data
                if data["bib"] or data["name"]:
                    row = [
                        data["bib"],
                        data["name"],
                        data["category"],
                        data["cp1"],
                        data["cp2"],
                        data["cp3"],
                        data["cp4"],
                        data["cp5"],
                        data["fp"],
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Add timestamp for tracking
                    ]
                    append_to_csv(filename, row)
                    print(f"Saved data for Bib {bib_number}")
                    
                    # Debug output showing which fields contained data
                    found_data = [k for k, v in data.items() if v]
                    print(f"Found data for fields: {', '.join(found_data)}")
                else:
                    print(f"No valid data found for Bib {bib_number}, skipping.")
            
            else:
                print(f"Failed to retrieve page for Bib {bib_number}")
                
        except requests.RequestException as e:
            print(f"Error requesting Bib {bib_number}: {str(e)}")
            time.sleep(5)  # Longer delay on network errors
            continue
        except Exception as e:
            print(f"Unexpected error processing Bib {bib_number}: {str(e)}")
            continue

    print("Scraping complete. Results saved to race_results.csv")
