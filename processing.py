import PyPDF2
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os
import tqdm
import multiprocessing


def extract_text_from_pypdf2(file_path):
    """
    Extract text from pdf using PyPDF2 library going page by page adding a new line at the end of each page
    """
    with open(file_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)

        text = ""

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n" + "\n"
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


def parse_quarterly_reports(file_name):
    os.makedirs("data/german_text/quarterly_reports", exist_ok=True)
    month_sequence = ["-02-", "-05-", "-08-", "-11-"]
    for seq in month_sequence:
        if seq in file_name:
            file_path = os.path.join("data/german", file_name)
            text = extract_text_from_pypdf2(file_path)
            with open(
                os.path.join(
                    "data/german_text/quarterly_reports",
                    file_name.replace(".pdf", ".txt"),
                ),
                "w",
                encoding="utf-8",
            ) as f:
                f.write(text)
            # jump out of inner for-loop since we found matching month for file
            break


def parse_quarterly_tax_reports():
    # releveant files are in data/german_text/quarterly_reports
    # store parsed data in data/german_text/quarterly_reports/tax_reports
    # relevent text starts with a line containing only "Steuereinnahmen" -> parse only if such a line is found
    os.makedirs("data/german_text/quarterly_reports/tax_reports", exist_ok=True)
    for file_name in os.listdir("data/german_text/quarterly_reports"):
        if file_name.endswith(".txt"):
            file_path = os.path.join("data/german_text/quarterly_reports", file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                # read file line by line until line containing "Steuereinnahmen" is found
                lines = f.readlines()
                start = False
                start_index = 0
                end = False
                end_index = len(lines)
                for i, line in enumerate(lines):
                    if line.strip() == "Steuereinnahmen" and not start:
                        start = True
                        start_index = i
                    elif line.strip() == "Bundeshaushalt" and start:
                        end = True
                        end_index = i
                if start:
                    if not end:
                        lines_to_write = lines[start_index:]
                    if end:
                        lines_to_write = lines[start_index:end_index]
                    with open(
                        os.path.join(
                            "data/german_text/quarterly_reports/tax_reports",
                            file_name,
                        ),
                        "w",
                        encoding="utf-8",
                    ) as f:
                        f.writelines(lines_to_write)


if __name__ == "__main__":
    # check all pdfs in data folder if they are image based
    """for file_name in os.listdir("data/english"):
    if file_name.endswith(".pdf"):
        file_path = os.path.join("data/english", file_name)
        if check_image_based_pdf(file_path):
            os.makedirs("data/image_based", exist_ok=True)
            os.rename(file_path, os.path.join("data/image_based", file_name))
            print(f"Moved {file_name} to image_based")"""
    """for file_name in os.listdir("data/german"):
    if file_name.endswith(".pdf"):
        file_path = os.path.join("data/german", file_name)
        if check_image_based_pdf(file_path):
            os.makedirs("data/image_based", exist_ok=True)
            os.rename(file_path, os.path.join("data/image_based", file_name))
            print(f"Moved {file_name} to image_based")"""

    file_name = "2022-11-monatsbericht-data.pdf"
    file_path = os.path.join("data\german", file_name)

    # check if pdf is image based and move file to data/image_based if it is, create a folder named image_based if it doesn't exist
    if check_image_based_pdf(file_path):
        os.makedirs("data/image_based", exist_ok=True)
        os.rename(file_path, os.path.join("data/image_based", file_name))
        print(f"Moved {file_name} to image_based")
        exit()

    # use multiprocessing to speed up process and track progress with tqdm
    # files = os.listdir("data/german")
    # num_cores = multiprocessing.cpu_count() // 2
    # file_chunks = [files[i::num_cores] for i in range(num_cores)]
    # pool = multiprocessing.Pool(num_cores)
    # with tqdm.tqdm(total=len(files)) as pbar:
    #     for i, _ in enumerate(pool.imap_unordered(parse_quarterly_reports, files)):
    #         pbar.update()
    # pool.close()
    # pool.join()

    parse_quarterly_tax_reports()
