# purpose of module to convert html file to pdf file

import os
import pdfkit


def pdf_convert(htmlFilename, outputFilename):
    path = os.path.join(os.getcwd(), 'wkhtmltopdf.exe')
    config = pdfkit.configuration(wkhtmltopdf=bytes(path, 'utf8'))
    options1 = {'page-size': 'A4',
                'margin-top': '7mm',
                'margin-right': '0mm',
                'margin-bottom': '0mm',
                'margin-left': '0mm',
                'encoding': "UTF-8"}
    pdfkit.from_file(htmlFilename, outputFilename, configuration=config, options=options1)