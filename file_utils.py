import os
import json
import csv
import re
import datetime

def read_urls_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        urls = [row[0] for row in csv_reader]
    return urls

def save_json(content, filename):
    with open(filename, 'w') as file:
        json.dump(content, file, indent=4)

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file {filename}")
                return None
    return None

def sanitize_filename(url):
    return re.sub(r'[\\/*?:"<>|]', "_", url) + '.json'

def update_change_log(url, changes):
    change_log_file = 'change_log.json'
    if os.path.exists(change_log_file):
        with open(change_log_file, 'r') as file:
            try:
                change_log = json.load(file)
            except json.JSONDecodeError:
                change_log = []
    else:
        change_log = []

    change_entry = {
        "url": url,
        "changes": changes,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    change_log.append(change_entry)
    
    with open(change_log_file, 'w') as file:
        json.dump(change_log, file, indent=4)
    
    return change_log_file
