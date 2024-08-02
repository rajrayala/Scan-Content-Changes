# Scan Content Changes

This project is designed to scan web pages for changes in their content and log these changes in a JSON file. It compares the current content of web pages with previously stored versions, logs any detected changes, and optionally commits these changes to a GitHub repository.

## Features

- Fetches and cleans HTML content from a list of URLs.
- Converts HTML content to a structured JSON format.
- Compares current and previous JSON data to detect changes.
- Logs detected changes in a JSON file.
- Commits the updated content and change log to a GitHub repository.

## Prerequisites

- Python 3.7+
- GitHub account with a repository to store the logs and content.
- GitHub Personal Access Token with repo access.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/rajrayala/Scan-Content-Changes.git
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Setup environment variables:**

    - `GITHUB_WORKSPACE`: Path to your local GitHub workspace (default is the current directory).
    - `GITHUB_TOKEN`: Your GitHub Personal Access Token.
    - `GITHUB_REPOSITORY`: The name of your GitHub repository (e.g., `your-username/Scan-Content-Changes`).
    - `GITHUB_REF`: The branch name to commit changes to (default is `main`).

2. **Prepare the URLs CSV file:**

    Create a file named `urls.csv` in the project directory with a list of URLs to scan. Each URL should be on a new line.

    Example `urls.csv`:
    ```csv
    https://google.com/drive
    https://google.in
    ```

3. **Run the script:**

    ```sh
    python main.py
    ```

## Project Structure

- `main.py`: Main script to execute the content scanning and logging process.
- `fetcher.py`: Module to fetch and clean HTML content from URLs.
- `file_utils.py`: Utility functions for reading URLs, saving/loading JSON files, and updating the change log.
- `github_utils.py`: Functions to handle GitHub repository updates.
- `compare_json.py`: Serialize and compare JSON data.
- `requirements.txt`: List of required Python packages.
- `urls.csv`: CSV file containing the list of URLs to scan.
- `results/`: Directory where JSON files for each URL are stored.
- `change_log.json`: File where detected changes are logged.

## Example Workflow

1. **Fetch Content:** The script fetches HTML content from the URLs listed in `urls.csv`.
2. **Clean and Convert:** The HTML content is cleaned (scripts and styles removed) and converted to a structured JSON format.
3. **Compare:** The current JSON content is compared with the previously stored version.
4. **Log Changes:** Any detected changes are logged in `change_log.json`.
5. **Commit to GitHub:** The updated JSON content and change log are committed to the specified GitHub repository.

## Customization

- **HTML Cleaning:** Modify the `fetch_clean_content` function in `fetcher.py` to customize the cleaning process.
- **Comparison Settings:** Adjust the settings of `DeepDiff` in the `compare_json` function in `compare_json.py` to change how differences are detected.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## Troubleshooting

- **JSON Decode Errors:** Ensure the `change_log.json` and other JSON files are properly formatted and not corrupted.
- **GitHub Commit Issues:** Verify your GitHub token has the necessary permissions and the environment variables are correctly set.
- **Dependencies:** Ensure all required packages are installed by running `pip install -r requirements.txt`.

## Contact

For any questions or issues, please open an issue on the GitHub repository or contact the project maintainer.
