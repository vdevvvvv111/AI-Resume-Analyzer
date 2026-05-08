from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import PyPDF2
import docx
import io

app = FastAPI(title="Resume Analyzer")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Resume Analyzer</title>
            <style>
                body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
                h1 { color: #333; }
                form { border: 2px dashed #ccc; padding: 30px; border-radius: 10px; }
                input[type="submit"] { background: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; }
            </style>
        </head>
        <body>
            <h1>Resume Analyzer</h1>
            <p>Upload your resume in PDF or DOCX format</p>
            <form action="/analyze" enctype="multipart/form-data" method="post">
                <input name="file" type="file" accept=".pdf,.docx" required><br><br>
                <input type="submit" value="Analyze Resume">
            </form>
        </body>
    </html>
    """

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    content = await file.read()
    
    text = ""
    if file.filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        for page in pdf_reader.pages:
            text += page.extract_text()
    elif file.filename.endswith('.docx'):
        doc = docx.Document(io.BytesIO(content))
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        return {"error": "Only PDF and DOCX supported"}
    
    word_count = len(text.split())
    has_email = "@" in text and "." in text
    has_phone = any(char.isdigit() for char in text)
    has_education = any(word in text.lower() for word in ["bachelor", "master", "degree", "university", "college"])
    
    score = 0
    feedback = []
    
    if word_count > 300: 
        score += 25
        feedback.append("Good length")
    else: 
        feedback.append("Resume too short. Add more details")
    
    if has_email: 
        score += 25
    else: 
        feedback.append("Missing email address")
        
    if has_phone: 
        score += 25
    else: 
        feedback.append("Missing phone number")
        
    if has_education: 
        score += 25
    else: 
        feedback.append("Add education section")
    
    return {
        "filename": file.filename,
        "score": f"{score}/100",
        "word_count": word_count,
        "checks": {
            "has_email": has_email,
            "has_phone": has_phone,
            "has_education": has_education
        },
        "feedback": feedback
    }