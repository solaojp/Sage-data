from io import BytesIO

from pdfminer.converter import HTMLConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from bs4 import BeautifulSoup
from tabula import read_pdf
import fitz

# this is the methos to parse the pdf as an HTML doc
def _extract_html_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    _file_handle = BytesIO()
    converter = HTMLConverter(resource_manager, _file_handle, codec='utf-8')
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()
        _get_html_parser(BeautifulSoup(text,'html.parser'))
    # close open handles
    converter.close()
    _file_handle.close()

def _get_html_parser(soup):
    title = soup.find_all('span', {"style":{"font-family: b'FPICKO+AdvOT863180fb'; font-size:16px"}})
    authors = soup.find_all('span', {"style":{"font-family: b'FPICKO+AdvOT863180fb'; font-size:12px"}})
    print(title)
    for author in authors:
        print(author.text)

# this method is for parsing pictorial data out of pdf
def _get_pictures(pdf_path):
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            print(img)          # this will print image data
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 0:       # this is GRAY or RGB
                pix.writePNG("Pictures/p%s-%s.png" % (i, xref))
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG("Pictures/p%s-%s.png" % (i, xref))
                pix1 = None
            pix = None

#this method is for parsing the tables out of the pdf
def _get_tables(pdf_path):
    df = read_pdf(pdf_path, multiple_tables=True, pages="1-8")
    print(df)

if __name__ == '__main__':

    pdf = 'clinical assessment.pdf'
    _extract_text_from_pdf(pdf)
    _get_pictures(pdf)
    _get_tables(pdf)
