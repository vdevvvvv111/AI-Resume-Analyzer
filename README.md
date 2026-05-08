# Resume Analyzer

A FastAPI web application that analyzes PDF/DOCX resumes and provides a score + feedback.

### **Features**
- Upload PDF or DOCX resumes
- Extracts text and checks for email, phone, education
- Scores resume out of 100 based on completeness
- Provides specific improvement feedback

### **Tech Stack**
- Python 3.11
- FastAPI
- PyPDF2, python-docx

### **How to Run**
1. `python -m venv venv`
2. `venv\Scripts\activate` 
3. `pip install -r requirements.txt`
4. `uvicorn main:app --reload`
5. Open http://127.0.0.1:8000

### **Author**
Vishnu Dev V