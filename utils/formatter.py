import json
import pandas as pd
import os
from datetime import datetime

class JobFormatter:
    REQUIRED_FIELDS = [
        "Job Title",
        "Company Name",
        "Location",
        "Experience Required",
        "Salary Details",
        "Job Portal Name",
        "Job URL"
    ]

    @staticmethod
    def normalize_job(job_data):
        """
        Ensures all required fields are present in the job dictionary.
        """
        normalized = {}
        for field in JobFormatter.REQUIRED_FIELDS:
            normalized[field] = job_data.get(field, "N/A")
        
        # Add any extra fields
        for k, v in job_data.items():
            if k not in normalized:
                normalized[k] = v
                
        return normalized

    @staticmethod
    def save_to_json(jobs, filename="output/jobs.json"):
        """
        Saves the list of jobs to a JSON file.
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=4, ensure_ascii=False)
        print(f"Data saved to {filename}")

    @staticmethod
    def save_to_excel(jobs, filename="output/jobs.xlsx"):
        """
        Saves the list of jobs to an Excel file.
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df = pd.DataFrame(jobs)
        df.to_excel(filename, index=False)
        print(f"Data saved to {filename}")
