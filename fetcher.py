import requests
from bs4 import BeautifulSoup

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

def element_to_dict(element):
    result = {}
    for child in element.children:
        if child.name:
            child_dict = element_to_dict(child)
            if child_dict:
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
