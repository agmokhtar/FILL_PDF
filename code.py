from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject, NumberObject, TextStringObject
import os

def set_need_appearances_writer(writer: PdfFileWriter):
    # See 12.7.2 and 7.7.2 for more information: 
    # http://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/PDF32000_2008.pdf
    try:
        catalog = writer._root_object
        # get the AcroForm tree
        if "/AcroForm" not in catalog:
            writer._root_object.update(
                {NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)
            })

        need_appearances = NameObject("/NeedAppearances")
        writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
        #del writer._root_object["/AcroForm"]['NeedAppearances']
        return writer

    except Exception as e:
        print('set_need_appearances_writer() catch : ', repr(e))
        return writer



def UpdatePDFFile(template, mapping, outputfile):
	tempPDF = open(template, "rb")
	myfile = PdfFileReader(tempPDF)

	writer = PdfFileWriter()
	set_need_appearances_writer(writer)

	n = len(myfile.pages)
	for i in range(n):
		page = myfile.getPage(i)
		writer.updatePageFormFieldValues(page, fields=mapping)
		writer.addPage(page)

	newpdf = open(outputfile,"wb")
	writer.write(newpdf)
	tempPDF.close()
	newpdf.close() 

def main():
	template = 'TEMPLATE.pdf'
	#template = '/Users/arafatg/Box/Arafat_Files/HRG/docs/PEDS_Performance_Appraisal_Form.pdf'
	mapping = {'Name': 'New Name'}
	outputfile = 'out.pdf'
	UpdatePDFFile(template, mapping, outputfile)
	os.system('open {}'.format(outputfile))

if __name__ == '__main__':
	main()