# QOJ Submission Crawler

A Python-based web crawler for automatically checking submission results on [QOJ (Qingyu Online Judge)](https://qoj.ac). This tool uses Playwright to automate browser interactions and check multiple submission URLs in batch. This project is to ease the burden of manually checking data from the QOJ website by automating the fetching of desired data from the website and comparing the fetched data with local data. 

## Features

- 🔐 **Session Management**: Login once and reuse the session for multiple runs
- 📊 **Batch Processing**: Check multiple submission results in a single run
- 📝 **Result Export**: Save submission results with problem titles, verdicts, and custom labels to a text file
- 🎯 **Progress Tracking**: Visual progress bar using `tqdm` during submission checking

## Project Structure

```
crawler/
├── crawler.py          # Main script for checking submissions
├── login.py            # Script for initial login and session saving
├── variables.py        # Configuration file with submission URLs and labels
├── pyproject.toml      # Project dependencies and configuration
├── qoj_session.json    # Saved browser session (generated after login)
└── submission_results.txt  # Output file with submission results
```

## Prerequisites

- Python 3.9 or higher
- `uv` package manager (or use `pip` if preferred)

## Installation

1. Clone or navigate to the project directory:
   ```bash
   cd crawler
   ```

2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```

   Or using `pip`:
   ```bash
   pip install playwright tqdm requests
   ```

3. Install Playwright browsers:
   ```bash
   playwright install chromium
   ```

## Usage

### Step 1: Configure Submission URLs and Labels

Edit `variables.py` to add your submission URLs and corresponding labels:

```python
urls_text = """
https://qoj.ac/submission/950472
https://qoj.ac/submission/611316
...
"""

labels_text = """ 
AC
AC
...
"""
```

- `urls_text`: One submission URL per line
- `labels_text`: One label per line (e.g., AC, TLE, WA) corresponding to each URL

### Step 2: Login and Save Session

Run the login script to authenticate with QOJ and save your session:

```bash
python login.py
```

This will:
1. Open a browser window
2. Navigate to the QOJ login page
3. Wait for you to manually log in
4. Save the session to `qoj_session.json` for future use

**Note**: You only need to run this once, or whenever your session expires.

### Step 3: Check Submissions

Run the main crawler script:

```bash
python crawler.py
```

The script will:
1. Load submission URLs and labels from `variables.py`
2. Use the saved session to authenticate
3. Visit each submission URL and extract:
   - Problem title
   - Submission result (e.g., "AC ✓", "TL", "WA")
4. Save results to `submission_results.txt` in the format:
   ```
   [Problem Title] - [Result] - [Label]
   ```
**Note**: `Problem Title` and `Result` are fetched from the website, and `Label` is the stored locally. This project is to check `result == label`. 

## Output Format

Results are saved to `submission_results.txt` with one line per submission:

```
#7040. Connected Subgraphs - AC ✓ - AC
#7040. Connected Subgraphs - TL - TLE
#7040. Connected Subgraphs - WA - WA
```

Each line contains:
- **Problem Title**: Extracted from the submission page
- **Result**: The actual verdict from QOJ
- **Label**: Your custom label from `variables.py`

## Dependencies

- **playwright** (>=1.55.0): Browser automation framework
- **tqdm** (>=4.66.0): Progress bar for batch operations
- **requests** (>=2.32.5): HTTP library (included but not actively used in current implementation)

## How It Works

1. **Session Persistence**: The crawler uses Playwright's `storage_state` feature to save and reuse browser sessions, avoiding the need to log in for every run.

2. **Headless Browsing**: The main crawler runs in headless mode (no visible browser) for efficiency, while the login script runs with a visible browser for manual authentication.

3. **Error Handling**: The script gracefully handles missing elements on submission pages, defaulting to "UNKNOWN" if problem titles or results cannot be extracted.

## Troubleshooting

- **Session Expired**: If you get authentication errors, run `login.py` again to refresh your session.
- **Missing Results**: If some submissions show "UNKNOWN", the page structure may have changed or the submission may not be accessible.
- **Browser Not Found**: Make sure you've run `playwright install chromium` after installing dependencies.
