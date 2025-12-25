# Graduan Company Scraper

A Python script that scrapes company information and emails from [Graduan.com](https://graduan.com), a Malaysian graduate job portal.

## Features

- Extracts company names and email addresses from all listed companies
- Automatically paginates through all company listings
- Real-time CSV export (data saved as it's collected)
- Rate-limited requests (0.3s delay) to avoid server overload
- Progress tracking with visual indicators

## Requirements

- Python 3.6+
- `requests` library

```bash
pip install requests
```

## Usage

```bash
python scrape_graduan.py
```

### Sample Output

```
======================================================================
Scraping Graduan Companies
======================================================================
Total companies: 500, Total pages: 25

[Page 1/25] https://graduan.com/company
----------------------------------------------------------------------
  ✓ [1] hr@company.com | Company Name
  ✗ No email: another-company
```

## Output

Results are saved to `graduan_companies.csv`:

| Column | Description |
|--------|-------------|
| email | Company email address |
| company_name | Company name |
| position | Reserved for future use |

## ⚠️ Disclaimer

This tool is for **educational and personal use only**.

- Respect the website's terms of service and robots.txt
- Use responsibly and ethically
- The author is not responsible for any misuse

## 🚫 License Restrictions

By using this software, you agree to the following:

1. **No Commercial Use** - This project is strictly prohibited for commercial, business, or for-profit purposes
2. **Legal Compliance** - You must comply with all applicable local, state, and national laws and regulations in your jurisdiction
3. **Data Protection** - You are responsible for handling any collected data in accordance with privacy laws (e.g., PDPA in Malaysia, GDPR in EU)
4. **User Responsibility** - The user assumes all liability for the use of this tool
5. **No Warranty** - This software is provided "as is" without any warranty

**Violation of these terms may result in legal consequences.**
