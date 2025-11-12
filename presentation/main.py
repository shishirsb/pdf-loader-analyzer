from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates

from interface.api import API
from application.document_analyzer import analyze_document

app = FastAPI()
templates = Jinja2Templates(directory="presentation/templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "response": "response will be shown here"})

@app.post("/")
async def handle_form(request: Request,
    pdf_file: UploadFile = File(...),
    question: str = Form(...)
        ):
    
    try:
        # Validate file upload
        if not pdf_file:
            message = "Please upload a pdf document to analyze!"
            return templates.TemplateResponse("index.html", {"request": request, "response": message})

        # read and process the uploaded PDF file
        pdf_bytes = await pdf_file.read()
        input_data = {'pdf_file': pdf_bytes, 'query': question}

        # Analyze document and get response
        response = analyze_document(input_data)
        return templates.TemplateResponse("index.html", {"request": request, "response": response})
    
    except Exception as e:
        message = f"Error processing document: {str(e)}"
        print(message)
        return templates.TemplateResponse("index.html", {"request": request, "response": message})

