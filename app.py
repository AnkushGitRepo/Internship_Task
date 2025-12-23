import streamlit as st
import pandas as pd
from scraper.ncs_scraper import NCSScraper
from scraper.careerjet_scraper import CareerjetScraper
from utils.formatter import JobFormatter
import json

st.set_page_config(page_title="Job Search System", layout="wide")

st.title("🔎 Job Vacancy Search System")

# Inputs
with st.sidebar:
    st.header("Search Criteria")
    designation = st.text_input("Designation", "Python Developer")
    location = st.text_input("Location", "Bangalore")
    experience = st.number_input("Experience (Years)", min_value=0, max_value=30, value=1, step=1)
    
    search_btn = st.button("Search Jobs")

if search_btn:
    st.info(f"Searching for {designation} jobs in {location} ({experience} Yrs)...")
    
    # Progress bar
    progress = st.progress(0)
    
    jobs = []
    
    # NCS
    try:
        ncs = NCSScraper()
        ncs_data = ncs.scrape(designation, location, experience)
        if not ncs_data:
             # Fallback to mock for demo if real scraping fails
             ncs_data = ncs.scrape_mock(designation, location, experience) 
             st.warning("NCS scraping returned no results (likely blocked/headless issue). Using mock data.")
        jobs.extend(ncs_data)
    except Exception as e:
        st.error(f"Error scraping NCS: {e}")
    
    progress.progress(50)
    
    # Careerjet (Replacing TimesJobs)
    try:
        cj = CareerjetScraper()
        cj_data = cj.scrape(designation, location, experience)
        if not cj_data:
             st.warning("Careerjet returned no results for this query.")
        jobs.extend(cj_data)
    except Exception as e:
        st.error(f"Error scraping Careerjet: {e}")
        
    progress.progress(100)
    
    if jobs:
        st.success(f"Found {len(jobs)} jobs!")
        
        # DataFrame
        df = pd.DataFrame(jobs)
        st.dataframe(df)
        
        # Download buttons
        json_data = json.dumps(jobs, indent=4, ensure_ascii=False)
        st.download_button("Download JSON", json_data, "jobs.json", "application/json")
        
        # Excel
        # Requires openpyxl
        try:
            excel_file = "jobs_export.xlsx"
            df.to_excel(excel_file, index=False)
            with open(excel_file, "rb") as f:
                 st.download_button("Download Excel", f, "jobs.xlsx")
        except Exception as e:
            st.warning("Could not create Excel file (missing dependency?)")

    else:
        st.warning("No jobs found. Try different keywords.")
