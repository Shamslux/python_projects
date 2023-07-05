# -*- coding: utf-8 -*-

""" Here we have a function to convert PDF to DOC. 
I was tired seeking online converter websites. =P """

from pdf2docx import Converter

def convert_pdf_to_word(pdf_file, output_file):
    cv = Converter(pdf_file)
    cv.convert(output_file, start=0, end=None)
    cv.close()

pdf_file = {YOUR PDF FILE}
output_file = {THE DOC CONVERTED OUTPUT FILE PATH}

convert_pdf_to_word(pdf_file, output_file)
