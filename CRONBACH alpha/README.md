# Cronbach's Alpha Calculator

Automates Cronbach's alpha reliability analysis by pulling survey response data directly from Google Sheets. Built for the pilot testing phase of a quantitative research study on educational tools and academic performance among Grade 11–12 students in Cebu, Philippines.

## Versions

### V1 — Python + Google Sheets API (`Cronbach's Alpha Calculator V1.py`)
Connects to Google Sheets via a service account and computes alpha using `pingouin`. Drops non-item columns by index and returns alpha and a 95% confidence interval.

### V3 — Python + Dashboard Automation (`Cronbach's Alpha Calculator V3.py`)
Upgraded version of V1. Adds dynamic Likert detection, automated dashboard generation, variance breakdown, and cell formatting — all written back to a second sheet in Google Sheets via the API. V2 was an intermediate version that was lost.

### Apps Script Version (`Cronbach's Alpha Calculator (APPSCRIPT VER.).gs`)
Pure Google Apps Script — no Python, no credentials, no setup. Paste into Extensions > Apps Script inside your Google Sheet and run it from the custom menu. Computes alpha entirely via spreadsheet formulas with an auto-generated dashboard.

## Output

```
Cronbach's Alpha: 0.843
95% Confidence Interval: (0.741, 0.946)
```

## Requirements

- Python 3.8+
- A Google Cloud service account with Sheets and Drive API access

Install dependencies:

```bash
pip install gspread oauth2client pandas pingouin
```

## Setup

1. Create a Google Cloud project and enable the **Google Sheets API** and **Google Drive API**
2. Create a **service account** and download the credentials as `cronalpha.json`
3. Place `cronalpha.json` in the project root (it is excluded from version control via `.gitignore`)
4. Share your target Google Sheet with the service account email

## Usage

### V1
Edit the sheet name at the bottom of the script:

```python
alpha, ci = get_cronbach_alpha("Your_Sheet_Name_Here")
```

Then run:

```bash
python "Cronbach's Alpha Calculator V1.py"
```

### V3
Make sure your Google Sheet has a second sheet (Dashboard). Edit the sheet name in the script:

```python
ss = client.open("Your_Sheet_Name_Here")
```

Then run:

```bash
python "Cronbach's Alpha Calculator V3.py"
```

### Apps Script
1. Open your Google Sheet
2. Go to **Extensions > Apps Script**
3. Paste the contents of `Cronbach's Alpha Calculator (APPSCRIPT VER.).gs`
4. Save and reload the sheet
5. Run via **🚀 Research Tools > Run Alpha Automate** in the menu bar

## Notes

- V1 drops columns by index — adjust `df.drop(df.columns[[...]])` to match your sheet's structure
- V3 and the Apps Script version auto-detect Likert columns using a `1–6` range filter, skipping metadata like Grade Level or General Average automatically
- `pingouin` computes the **variance-based (unstandardized)** form of Cronbach's alpha, which is more appropriate than the correlation-based formula when item variances differ
- The 95% CI is bootstrapped by `pingouin` automatically

## Context

Originally written to support the pilot testing phase of a quantitative research study on educational tools and academic performance among Grade 11–12 students in Cebu, Philippines.

---

> `cronalpha.json` is not included in this repository. Never commit service account credentials to version control.

## Author
Peter Abangan — [@peterabangan](https://github.com/peterabangan)
