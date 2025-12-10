#!/usr/bin/env python3
import os
import sys
from scrapers.linkedin_scraper import linkedinClass
import time

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_linkedin.py <query> [max]")
        sys.exit(1)

    query = sys.argv[1]
    max_jobs = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    li_at = os.getenv('LINKEDIN_LI_AT') or os.getenv('LI_AT') or os.getenv('LINKEDIN_TOKEN') or os.getenv('linkedin_token')
    if not li_at:
        print("No LinkedIn token found in env. Provide LINKEDIN_LI_AT env var or run with query param.")
        sys.exit(2)

    print("Using LinkedIn token from environment (hidden)")

    scraper = linkedinClass(li_at)
    try:
        ok = scraper.login_with_cookie()
        print(f"Login with cookie returned: {ok}")
    except Exception as e:
        print(f"Login attempt failed: {e}")

    jobs = scraper.search_jobs(query, "", max_jobs_per_search=max_jobs)
    print(f"Found {len(jobs)} jobs")
    # optional: dump page source for debugging
    if os.getenv('LINKEDIN_DUMP_PAGE'):
        try:
            dump_path = os.path.join('temp', f'linkedin_debug_{int(time.time())}.html')
            os.makedirs(os.path.dirname(dump_path), exist_ok=True)
            with open(dump_path, 'w', encoding='utf-8') as f:
                f.write(scraper.driver.page_source)
            print(f"Wrote page source to: {dump_path}")
        except Exception as e:
            print(f"Failed to write page source: {e}")
    for j in jobs[:max_jobs]:
        # Print a short summary
        title = j.get('Title') if isinstance(j, dict) else getattr(j, 'Title', str(j))
        company = j.get('Company') if isinstance(j, dict) else getattr(j, 'Company', '')
        url = j.get('Job_Link') if isinstance(j, dict) else getattr(j, 'Job_Link', '')
        print(f"- {title} @ {company} -> {url}")

    try:
        if hasattr(scraper, 'driver') and scraper.driver:
            scraper.driver.quit()
    except Exception:
        pass

if __name__ == '__main__':
    main()
