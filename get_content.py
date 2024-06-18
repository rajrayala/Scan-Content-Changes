import os
import csv
import requests
import json
import hashlib
from deepdiff import DeepDiff
from bs4 import BeautifulSoup
from github import Github, InputGitAuthor, InputGitTreeElement
import datetime

def read_urls_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        urls = [row[0] for row in csv_reader]
    return urls

def element_to_dict(element):
    result = {}
    for child in element.children:
        if child.name:
            child_dict = element_to_dict(child)
            if child_dict:  # Only add non-empty elements
                if child.name in result:
                    if not isinstance(result[child.name], list):
                        result[child.name] = [result[child.name]]
                    result[child.name].append(child_dict)
                else:
                    result[child.name] = child_dict
        elif child.string and child.string.strip():
            return child.string.strip()
    return result

def prune_empty(data):
    if isinstance(data, dict):
        return {k: prune_empty(v) for k, v in data.items() if prune_empty(v)}
    if isinstance(data, list):
        return [prune_empty(i) for i in data if prune_empty(i)]
    return data

def fetch_clean_content(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()

    body_content = soup.find('body')
    if body_content:
        content_dict = element_to_dict(body_content)
    else:
        content_dict = element_to_dict(soup)

    pruned_content = prune_empty(content_dict)
    return pruned_content

def save_json(content, filename):
    with open(filename, 'w') as file:
        json.dump(content, file, indent=4)

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return None

def compare_json(new_data, old_data):
    return DeepDiff(old_data, new_data, ignore_order=True).to_dict()

def get_hashed_filename(url):
    return hashlib.sha256(url.encode('utf-8')).hexdigest() + '.json'

def update_repo(file_path, commit_message):
    token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')
    workspace = os.getenv('GITHUB_WORKSPACE')

    g = Github(token)
    repo = g.get_repo(repo_name)

    with open(file_path, 'r') as file:
        content = file.read()

    ref = repo.get_git_ref("heads/main")
    main_sha = ref.object.sha
    commit = repo.get_commit(main_sha)

    element = repo.create_git_blob(content, 'utf-8')
    tree_element = InputGitTreeElement(
        path=os.path.relpath(file_path, workspace),
        mode='100644',
        type='blob',
        sha=element.sha
    )

    base_tree = repo.get_git_tree(commit.commit.tree.sha)
    tree = repo.create_git_tree([tree_element], base_tree=base_tree)

    author = InputGitAuthor(
        name=os.getenv('GITHUB_ACTOR'),
        email=f"{os.getenv('GITHUB_ACTOR')}@users.noreply.github.com"
    )
    new_commit = repo.create_git_commit(commit_message, tree, [commit.commit], author=author)

    ref.edit(new_commit.sha)

def update_change_log(url, changes):
    change_log_file = 'changeLog.json'
    if os.path.exists(change_log_file):
        with open(change_log_file, 'r') as file:
            change_log = json.load(file)
    else:
        change_log = []

    change_entry = {
        "url": url,
        "changes": changes,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    change_log.insert(0, change_entry)
    
    with open(change_log_file, 'w') as file:
        json.dump(change_log, file, indent=4)
    
    update_repo(change_log_file, f'Update change log for {url}')

def main():
    repo_path = os.getenv('GITHUB_WORKSPACE')
    csv_file_path = os.path.join(repo_path, 'urls.csv')

    urls = read_urls_from_csv(csv_file_path)

    for url in urls:
        content = fetch_clean_content(url)
        json_filename = os.path.join(repo_path, get_hashed_filename(url))
        old_content = load_json(json_filename)

        if old_content:
            diff = compare_json(content, old_content)
            if diff:
                update_change_log(url, diff)
                save_json(content, json_filename)
                update_repo(json_filename, f'Update content for {url}')
        else:
            save_json(content, json_filename)
            update_repo(json_filename, f'Add new content for {url}')

if __name__ == "__main__":
    main()
