# Job Vacancy Search System

A Python-based tool to search and scrape job vacancies from **NCS (National Career Service)** and **TimesJobs**.

## 📌 Features
- **Multi-Portal Scraping**: Fetches jobs from NCS and Careerjet.
- **Dynamic Search**: Search by Designation, Location, and Experience.
- **Data Normalization**: Unified JSON output format.
- **Dual Interface**:
  - **CLI**: Command-line interface for quick execution.
  - **Streamlit UI**: a web-based dashboard for easy interaction.
- **Export**: Save results as JSON and Excel.

## 🛠 Tech Stack
- **Python 3.x**
- **Selenium**: Web scraping (NCS & Careerjet).
- **BeautifulSoup**: HTML Parsing (Internal).
- **Streamlit**: Web UI.
- **Pandas**: Data handling and Excel export.

## 🚀 Installation

1. **Clone the repository** (if applicable)
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Setup Drivers**:
   - Ensure Google Chrome is installed.
   - `selenium` should handle driver management, or install `chromedriver` separately if needed.

## 🏃 Usage

### 1. Command Line Interface (CLI)
Run the script with arguments:
```bash
python main.py --designation "Python Developer" --location "Bangalore" --experience "1-3 Years"
```
**Output**: 
- `output/jobs.json`
- `output/jobs.xlsx`

### 2. Streamlit UI
Run the web app:
```bash
streamlit run app.py
```
Open the provided URL (usually `http://localhost:8501`) in your browser.

## 📂 Project Structure
```
job_scraper/
├── scraper/
│   ├── ncs_scraper.py      # Selenium scraper for NCS
│   ├── careerjet_scraper.py # Selenium scraper for Careerjet
├── utils/
│   ├── formatter.py        # Data normalization and saving
├── output/                 # Generated files
├── main.py                 # CLI Entry point
├── app.py                  # Streamlit App
├── requirements.txt        # Dependencies
└── README.md               # Documentation
```

## ⚠️ Challenges & Notes
- **Dynamic Content**: NCS uses complex dynamic loading which requires Selenium.
- **Anti-Scraping**: Portals may block frequent requests. The scrapers use basic wait times but may need proxies for heavy use.
- **Selectors**: HTML structure of portals changes frequently. If scraping fails, selectors in `scraper/*.py` may need updating.

## 📜 Output Sample (JSON)
```json
[
    {
        "Job Title": "Python Developer",
        "Company Name": "Tech Corp",
        "Location": "Bangalore",
        "Experience Required": "1-3 Years",
        "Salary Details": "Not Disclosed",
        "Job Portal Name": "TimesJobs",
        "Job URL": "https://..."
    }
]
```
