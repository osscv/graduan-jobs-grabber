import requests
import re
import html
import json
import csv
import time
import os

# User agent to use for all requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
}

OUTPUT_FILE = "graduan_companies.csv"

def extract_page_data(url):
    """Extract Inertia.js page data from a URL."""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    match = re.search(r'data-page="([^"]+)"', response.text)
    if match:
        decoded = html.unescape(match.group(1))
        return json.loads(decoded)
    return None

def init_csv():
    """Initialize CSV file with headers (always start fresh)."""
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        f.write('email,company_name,position\n')
    print(f"Created {OUTPUT_FILE}")

def append_to_csv(email, company_name, position=''):
    """Append a single row to CSV in real-time."""
    with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([email, company_name, position])

def get_company_details(slug):
    """Fetch company details from individual company page."""
    url = f"https://graduan.com/company/{slug}"
    try:
        data = extract_page_data(url)
        if not data:
            return None, None

        company = data['props'].get('company', {})
        name = company.get('name')
        info = company.get('info', {})
        email = info.get('email') if info else None

        return name, email
    except Exception as e:
        print(f"    Error: {e}")
        return None, None

def main():
    base_url = "https://graduan.com/company"

    # Initialize CSV
    init_csv()

    total_found = 0

    print("=" * 70)
    print("Scraping Graduan Companies")
    print("=" * 70)

    # First page to get total pages
    print(f"\nFetching page 1: {base_url}")
    data = extract_page_data(base_url)
    if not data:
        print("Failed to extract data from main page")
        return

    companies_data = data['props']['companies']
    total_pages = companies_data['last_page']
    total_companies = companies_data['total']

    print(f"Total companies: {total_companies}, Total pages: {total_pages}\n")

    # Process all pages
    for page in range(1, total_pages + 1):
        page_url = base_url if page == 1 else f"{base_url}?page={page}"
        print(f"\n[Page {page}/{total_pages}] {page_url}")
        print("-" * 70)

        try:
            if page > 1:
                data = extract_page_data(page_url)

            if not data:
                print("  Failed to get page data")
                continue

            companies = data['props']['companies']['data']

            for company in companies:
                slug_info = company.get('slug', {})
                if not isinstance(slug_info, dict) or not slug_info.get('slug'):
                    continue

                slug = slug_info['slug']
                company_url = f"https://graduan.com/company/{slug}"

                name, email = get_company_details(slug)

                if email:
                    append_to_csv(email, name or slug.replace('-', ' ').title(), '')
                    total_found += 1
                    print(f"  ✓ [{total_found}] {email} | {name}")
                    print(f"    URL: {company_url}")
                else:
                    print(f"  ✗ No email: {slug}")

                time.sleep(0.3)

        except Exception as e:
            print(f"  Error on page {page}: {e}")

        time.sleep(0.3)

    print("\n" + "=" * 70)
    print(f"DONE! Total companies with emails: {total_found}")
    print(f"Results saved to: {OUTPUT_FILE}")
    print("=" * 70)

if __name__ == "__main__":
    main()
