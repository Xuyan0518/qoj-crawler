from playwright.sync_api import sync_playwright

STORAGE_STATE_FILE = "qoj_session.json"

def login_and_save_session():
    """Manually log in once and save the session to reuse later."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://qoj.ac/login")

        print("Please log in manually in the browser window...")
        input("Press Enter after you have logged in successfully...")

        context.storage_state(path=STORAGE_STATE_FILE)
        print(f"✅ Session saved to {STORAGE_STATE_FILE}")
        browser.close()

if __name__ == "__main__":
    login_and_save_session()