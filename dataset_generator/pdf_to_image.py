import subprocess


def pdf2image(pathPDF, pathImage):
    try:
        params = ['magick', 'convert',
                  # '-verbose',
                  '-density', '200x200',
                  # '-trim',
                  pathPDF,
                  '-quality', '100',
                  # '-flatten',
                  # '-sharpen', '0x1.0',
                  pathImage]
        subprocess.check_call(params)
    except:
        print('pls install ImageMagick')

import os

def get_all_file_in_folder(path):
    l=[]
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".pdf"):
                l.append(os.path.join(root, file).replace('\\', '/'))
    return l

if __name__ == "__main__":
    pdf_files = get_all_file_in_folder('zoho\\')
    for pdf in pdf_files:
        # print(pdf, pdf[:-4]+'.jpg')
        pdf2image(pdf, pdf[:-4]+'.jpg')
