import pandas
import docx
from PyPDF2 import PdfReader

def process_text_file(uploadedFiles):
    """
    Below is a function in Python that identifies each type of file and separates them into strings.

    .. note::
        Implement by Hoang Nguyen

    Parameters
    ----------
    uploadedFiles: List or None
        Filenames import
        
    Return
    ----------
    The entire string of all files.

    Example
    -------
    >>> Upload multiple file (PDF,DOCX,...)
    """
    
    text = ""
    for file in uploadedFiles:
        extension = file.name[len(file.name)-3:]
        if(extension == "pdf"):
            file_reader = PdfReader(file)
            for page in file_reader.pages:
                text += page.extract_text()
        elif(extension == "csv"):
            file_reader = pandas.read_csv(file)
            text += "\n".join(
                file_reader.apply(lambda row: ', '.join(row.values.astype(str)), axis=1))
        elif(extension == "lsx" or extension == "xls"):
            file_reader = pandas.read_excel(file)
            text += "\n".join(
                file_reader.apply(lambda row: ', '.join(row.values.astype(str)), axis=1))
        elif(extension == "ocx" or extension == "docx"):
            file_reader = docx.Document(file)
            list = [paragraph.text for paragraph in file_reader.paragraphs]
            text += ' '.join(list)
    return text
    