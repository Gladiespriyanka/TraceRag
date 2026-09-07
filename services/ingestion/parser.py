from io import BytesIO
from pypdf import PdfReader
def parse_pdf(data:bytes)->str: return "\n\n".join((p.extract_text() or "") for p in PdfReader(BytesIO(data)).pages).strip()
def parse_bytes(data,content_type,filename): return parse_pdf(data) if content_type=="application/pdf" or filename.lower().endswith(".pdf") else data.decode("utf-8",errors="ignore")
