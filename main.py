import os
from fetcher import fetch_clean_content
from compare_json import compare_json
from file_utils import read_urls_from_csv, save_json, load_json, sanitize_filename, update_change_log
from github_utils import update_repo

def main():
    repo_path = os.getenv('GITHUB_WORKSPACE', '.')
    csv_file_path = os.path.join(repo_path, 'urls.csv')
    results_dir = os.path.join(repo_path, 'results')

    # Ensure the results directory exists
    os.makedirs(results_dir, exist_ok=True)

    urls = read_urls_from_csv(csv_file_path)

    files_to_commit = []

    for url in urls:
        content = fetch_clean_content(url)
        json_filename = os.path.join(results_dir, sanitize_filename(url))
        old_content = load_json(json_filename)

        if old_content:
            diff = compare_json(content, old_content)
            if diff:
                change_log_file = update_change_log(url, diff)
                save_json(content, json_filename)
                files_to_commit.append(json_filename)
                files_to_commit.append(change_log_file)
        else:
            save_json(content, json_filename)
            files_to_commit.append(json_filename)

    if files_to_commit and os.getenv('GITHUB_TOKEN'):
        update_repo(files_to_commit, 'Update content and change log')
    else:
        print("Changes detected, but not committing because GITHUB_TOKEN is not set or no changes were detected.")

if __name__ == "__main__":
    main()
