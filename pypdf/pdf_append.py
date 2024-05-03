import PyPDF2
lista_pdf = ["data/file_1.pdf","data/file_2.pdf"]
nombre_salida = "receta_append.pdf"
pdf_final = PyPDF2.PdfMerger()
for nombre_archivo in lista_pdf:
    pdf_final.append(nombre_archivo)

pdf_final.write(nombre_salida)
pdf_final.close()