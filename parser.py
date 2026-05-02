import pdfplumber
from playwright.sync_api import sync_playwright
import time
import random


# ---------------------------
# 1. PDF → TEXT
# ---------------------------
def parse_cv_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        return text.strip()
    except Exception as e:
        print(f"❌ PDF error: {e}")
        return None


# ---------------------------
# 2. HUMAN-LIKE DELAY
# ---------------------------
def human_delay(min_s=2, max_s=5):
    time.sleep(random.uniform(min_s, max_s))


# ---------------------------
# 3. STEALTH JOB SCRAPER
# ---------------------------
def parse_job_link_stealth(url):
    try:
        with sync_playwright() as p:

            # Persistent browser (VERY IMPORTANT)
            browser = p.chromium.launch_persistent_context(
                user_data_dir="browser_data",  # saves cookies
                headless=False,                # MUST be False
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
            )

            page = browser.new_page()

            print("🌐 Opening page...")
            page.goto(url, timeout=60000)

            # Wait like a human
            human_delay(5, 8)

            # Move mouse randomly (anti-bot)
            page.mouse.move(100, 200)
            human_delay(1, 2)
            page.mouse.move(400, 500)

            # Scroll slowly
            page.mouse.wheel(0, 1000)
            human_delay(2, 4)

            # Try to accept cookies (if exists)
            try:
                page.click("button:has-text('Accept')", timeout=3000)
            except:
                pass

            print("🔍 Extracting job description...")

            # Indeed-specific selector
            try:
                job_text = page.locator("#jobDescriptionText").inner_text(timeout=5000)
            except:
                print("⚠️ Fallback to full page text")
                job_text = page.inner_text("body")

            print("✅ Extraction done")

            # Keep browser open for debugging (optional)
            # input("Press ENTER to close browser...")

            browser.close()

            return job_text

    except Exception as e:
        print(f"❌ Scraping failed: {e}")
        return None


# ---------------------------
# 4. CLEAN TEXT
# ---------------------------
def clean_text(text):
    if not text:
        return None
    return " ".join(text.split())


# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    cv_path = "your_cv.pdf"
    job_url = "https://de.indeed.com/viewjob?jk=945c214a5d7cecba"

    print("📄 Parsing CV...")
    cv_text = parse_cv_pdf(cv_path)

    print("🌐 Scraping job...")
    job_text = parse_job_link_stealth(job_url)

    cv_text = clean_text(cv_text)
    job_text = clean_text(job_text)

    print("\n----- CV PREVIEW -----\n")
    print(cv_text[:500] if cv_text else "❌ CV failed")

    print("\n----- JOB PREVIEW -----\n")
    print(job_text[:500] if job_text else "❌ Job scraping failed")