from playwright.sync_api import sync_playwright
from tqdm import tqdm
from variables import urls_text, labels_text

SUBMISSION_URLS = [url.strip() for url in urls_text.strip().split("\n")]
LABELS = [label.strip() for label in labels_text.strip().split("\n")]
Total_number_of_cases = len(SUBMISSION_URLS)
current_case = 0

# File to store login session
STORAGE_STATE_FILE = "qoj_session.json"
OUTPUT_FILE = "submission_results.txt"

def check_submission_results(urls):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=STORAGE_STATE_FILE)
        page = context.new_page()

        for url in tqdm(urls, desc="Checking submissions", unit="submission"):
            page.goto(url, wait_until="networkidle")

            # Initialize default values
            submission_result = "UNKNOWN"
            problem_title = "UNKNOWN"

            try:
                submission_result = page.locator("a.uoj-score").first.inner_text().strip()
            except:
                pass  # Silently continue if not found

            try:
                problem_title = page.locator("a[href^='/contest/']").first.inner_text().strip()
            except:
                pass  # Silently continue if not found

            results.append({
                "problem": problem_title,
                "result": submission_result
            })

        browser.close()
    return results

def save_results_to_file(results, labels, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for i, item in enumerate(results):
            label_result = labels[i] if i < len(labels) else "N/A"
            line = f"{item['problem']} - {item['result']} - {label_result}\n"
            f.write(line)
    print(f"✅ Results saved to {filename}")

if __name__ == "__main__":
    results_array = check_submission_results(SUBMISSION_URLS)
    save_results_to_file(results_array, LABELS, OUTPUT_FILE)
