import PyPDF2
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os


def extract_text_from_pypdf2(file_path):
    """Extract text from pdf file using pypdf2"""
    with open(file_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)

        text = ""

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        # write into temp file
        """ with open("temp.txt", "w", encoding="utf-8") as f:
            f.write(text) """
        return text


def extract_tables_from_pdfminer(file_path):
    resource_manager = PDFResourceManager()
    string_io = StringIO()
    device = TextConverter(resource_manager, string_io, laparams=LAParams())
    interpreter = PDFPageInterpreter(resource_manager, device)

    with open(file_path, "rb") as f:
        for page in PDFPage.get_pages(f, caching=True, check_extractable=True):
            interpreter.process_page(page)
    text = string_io.getvalue()
    device.close()
    string_io.close()
    return text


def check_image_based_pdf(file_path):
    """Check if pdf is image based"""
    with open(file_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        page = pdf_reader.pages[0]
        text = page.extract_text()
        if text is None or text == "":
            return True
        else:
            return False


if __name__ == "__main__":
    # check all pdfs in data folder if they are image based
    for file_name in os.listdir("data"):
        if file_name.endswith(".pdf"):
            file_path = os.path.join("data", file_name)
            if check_image_based_pdf(file_path):
                os.makedirs("data/image_based", exist_ok=True)
                os.rename(file_path, os.path.join("data/image_based", file_name))
                print(f"Moved {file_name} to image_based")

    file_name = "1949-01-monthly-report-data.pdf"
    file_path = os.path.join("data", file_name)

    # check if pdf is image based and move file to data/image_based if it is, create a folder named image_based if it doesn't exist
    if check_image_based_pdf(file_path):
        os.makedirs("data/image_based", exist_ok=True)
        os.rename(file_path, os.path.join("data/image_based", file_name))
        print(f"Moved {file_name} to image_based")
        exit()

    pypdf2_text = extract_text_from_pypdf2(file_path)
    with open("tmp/temp_pydf2.txt", "w", encoding="utf-8") as f:
        f.write(pypdf2_text)

    pdfminer_text = extract_tables_from_pdfminer(file_path)
    with open("tmp/temp_pdfminer.txt", "w", encoding="utf-8") as f:
        f.write(pdfminer_text)
