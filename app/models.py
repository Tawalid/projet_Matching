from django.db import models

# Create your models here.
class Position(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Employee(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    age= models.CharField(max_length=15)
    sexe= models.ForeignKey(Position,on_delete=models.CASCADE)
    portable = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    formation = models.CharField(max_length=100000)
    experiences1 = models.CharField(max_length=100000)
    experiences2 = models.CharField(max_length=100000)
    experiences3 = models.CharField(max_length=100000)
    competences = models.CharField(max_length=100000)
    divers = models.CharField(max_length=1000)
    linkedin = models.CharField(max_length=1000)
    CV=models.FileField(upload_to ='media/pdf') 
    """
    from pdfminer.pdfinterp import PDFResourceManager
    from pdfminer.pdfinterp import PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.pdfpage import PDFPage
    from io import BytesIO 
    import argparse
    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    device = TextConverter(rsrcmgr, retstr)
        #with open(path, "rb") as fp:  # open in 'rb' mode to read PDF bytes
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(CV, check_extractable=True):
        interpreter.process_page(page)
        device.close() 
        text = retstr.getvalue()
        retstr.close()
    pdf_text = text.decode("utf-8") 
    #########"""
    def __str__(self):
        return (str(self.CV)+"*"+" "+str(self.formation)+" "+str(self.competences)+" "+str(self.experiences1)+" "+str(self.experiences2)+" "+str(self.experiences3))