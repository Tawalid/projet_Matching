from django.shortcuts import render,redirect
from .forms import EmployeeForm
from .models import Employee
from django.http import HttpResponse,HttpResponseRedirect
import matplotlib.pyplot as plt
import io
import urllib, base64
def home(request):
    return render(request,'home.html')
def basic(request):
    if request.method == "GET":
        form = EmployeeForm(request.POST)
        return render(request,'basic.html',{'form':form})
    else:
        form= EmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/trait')
def graphes(request):
    #################
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    #importation des informations scrapper
    offre=pd.read_json("C:\webdriver\pages\Rekrute3.json")
    profil= pd.read_json("C:\webdriver\pages\emplois1.json")
    # Visiualisation offres : Experience requise/niveau d'etudes
    offre_num1=offre["Experience requise"].value_counts()#le nombre d'occurence de chaque indice       
    chart=sns.barplot(x=offre_num1.index, y=offre_num1)#cree un graphe avec le nombre d'occurence et les indices
    chart.set_xticklabels(chart.get_xticklabels(), rotation=90)#rotation au niveau d'affichage des indices     
    buf = io.BytesIO()
    chart.figure.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    ######
    ###
    ###
    profil_num1=profil['Experience requise'].value_counts()
    chart=sns.barplot(x=profil_num1.index, y=profil_num1)
    chart.set_xticklabels(chart.get_xticklabels(), rotation=90)
    buf2 = io.BytesIO()#Ouvrir un fichier en mode binaire
    chart.figure.savefig(buf2,format='png')#configuration du graphe
    buf2.seek(0)#Afficher tout le fichier quand on met argument 0
    string = base64.b64encode(buf2.read())#encode en base64
    uri2 =  urllib.parse.quote(string)#Remplacer les caractere speciales de string
    #####
    offre_num2=offre["Etudes"].value_counts()
    chart=sns.barplot(x=offre_num2.index, y=offre_num2)
    chart.set_xticklabels(chart.get_xticklabels(), rotation=90)
    buf3 = io.BytesIO()
    chart.figure.savefig(buf3,format='png')
    buf3.seek(0)
    string = base64.b64encode(buf3.read())
    uri3 =  urllib.parse.quote(string)
    #########
    profil_num2=profil['Etudes'].value_counts()
    chart=sns.barplot(x=profil_num2.index, y=profil_num2)
    chart.set_xticklabels(chart.get_xticklabels(), rotation=90)
    buf4 = io.BytesIO()
    chart.figure.savefig(buf4,format='png')
    buf4.seek(0)
    string = base64.b64encode(buf4.read())
    uri4 =  urllib.parse.quote(string)
    #envoyer un objet HttpResponse avec le données résultantes
    return render(request,'graphes.html',{
        'data': uri,
        'data2': uri2,
        'data3': uri3,
        'data4': uri4
    })

def trait(request):
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.pdfpage import PDFPage
    from io import BytesIO
    import argparse
    import nltk
    from nltk.corpus import stopwords
    import pandas as pd
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    #fonction pour conversion d'un pdf donnée a un text
    def pdf2xt(path):
        rsrcmgr = PDFResourceManager()
        retstr = BytesIO()
        device = TextConverter(rsrcmgr, retstr)
        with open(path, "rb") as fp:  # open in 'rb' mode to read PDF bytes
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.get_pages(fp, check_extractable=True):
                interpreter.process_page(page)
            device.close()
            text = retstr.getvalue()
            retstr.close()
        return text
    #importation du pdf entrer lors du formulaire
    pdf_text = pdf2xt('C:/Users/Taouil Walid/Documents/Projet big data/projdanj/media'+"/"+str(Employee.objects.last()).split("*")[0]).decode("utf-8") 
    F=pdf_text+" "+str(Employee.objects.last()).split("*")[1]
    ##importer les offres scrapper
    df = pd.read_json("C:/webdriver/pages/Rekrute.json")
    X=[]
    for i in range(len(df.Competence)):
        try:
            #Resultat
            A=df.Competence[i]
            text1=[A.lower(),F.lower()]#une liste qui contient l'offre et profil en minuscule
            cv= CountVectorizer()#instantier un counvectorizer qui vas transformer la liste text en matrice des mots d'offre et profil
            count_matrix=cv.fit_transform(text1)#executer la transformation 
            #Resultat qui consiste a calculer la similarité entre les mots du liste "text" avec la fonction cosine_similarity
            #On enregistre ces resultats dans une liste ou il y'a le taux de similarité et les informations de chaque offre
            X.append(str(cosine_similarity(count_matrix)[0,1]*100)+"% pour l'offre de"+df["Nom d'entreprise"][i]+"\n pour poste : "+df["Poste"][i]+" "+df["Link"][i]) 
        except KeyError:
                pass
    ## mettre les valeurs en ordre (ordre humain)
    ###
    import re
    def atof(text):
        try:
            retval = float(text)
        except ValueError:
            retval = text
        return retval

    def natural_keys(text):
        return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]
    ##ces fonctions ont le but de mettre en ordre notre liste des resultats selon le taux de similarité decroissant
    X.sort(reverse =True,key=natural_keys)       
        #envoyer un objet HttpResponse avec le données résultantes
    return render(request,'Matching.html',{
        'data':X[0][:-124],
        'data1':X[1][:-124],
        'data2':X[2][:-124],
        'data3':X[3][:-124],
        'data4':X[4][:-124],
        'data5':X[5][:-124],
        'link':X[0][-124:],
        'link1':X[1][-124:],
        'link2':X[2][-124:],
        'link3':X[3][-124:],
        'link4':X[4][-124:],
        'link5':X[5][-124:]
    })
           
def wordcloud(request):
    import pandas as pd
    from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
    import matplotlib.pyplot as plt 
    from PIL import Image
    from os import path, getcwd
    import numpy as np
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    #Imporation des données
    df=pd.read_json("C:\webdriver\pages\Rekrute3.json")
    text1 = " ".join(df["Nom d'entreprise"])#mettre tout les nom d'entreprises dans un text 
    stop_words=stopwords.words("french")#importer les stopwords du français (et,ou,le ...)
    text1=text1.replace(",", "")#enlever les virgules
    N_text=[]
    #boucle qui sert a enlever les stopwords du text 
    for word in word_tokenize(text1):
        if word not in stop_words:
            N_text.append(word.lower())
    N_text=" ".join(N_text)#le text sans stopwords
    #nettoyage des repitions des informations
    N_text=N_text.replace("maroc alten", "alten maroc").replace("industries meski", "meski holding").replace("services", "").replace("page morocco", "").replace("université mohammed","")
    #importation du logo d'affichage du wordcloud
    d="C:\\Users\\Taouil Walid\\Documents\\Projet big data"
    mask_logo = np.array(Image.open(path.join(d, "Python.png")))
    #instatiation du wordcloud
    wc= WordCloud(background_color="white", max_words=2000, max_font_size=90, random_state=1, mask=mask_logo, stopwords=STOPWORDS)
    #generation du wordcloud
    wc.generate(N_text)
    #reglages des differentes parametres du wordcloud
    image_colors = ImageColorGenerator(mask_logo)
    plt.figure(figsize=[10,10])
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
        #envoyer un objet HttpResponse avec le données résultantes
    return render(request,'wordcloud.html',{
        'data':uri
    })
    