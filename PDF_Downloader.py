import pandas as pd
import requests
import os.path


#Definerer 'ID':
ID='BRnum'  #CHOOSE YOUR OWN "ID COLUMN". 


#Definerer 'data', som at pandas læser Excel-dokumentet, og sætter indekset til 'ID':
data= pd.read_excel('Opgaver/Uge 5/GRI_2017_2020.xlsx', index_col=ID)   #CHANGE THE PATH TO THE EXCEL FILE. 


#Tjekker at feltet "Pdf_URL" faktisk indeholder et link:
data=data[data.Pdf_URL.notnull() == True]   #CHANGE THE "Pdf_URL" TO THE COLUMN IN YOUR EXCEL FILE THAT CONTAINS THE URLs.


#Definerer 'dwn_path', som stien til der hvor den skal smide de downloadede filer:
down_path='Opgaver/Uge 5/PDF_files/'    #CHOOSE THE PATH TO YOUR DOWNLOADED FILES.


#Definerer 'dwn_files', som lister alle filerne i den nuværende mappe:
down_files=os.listdir(down_path)


#Definerer 'exist', som tjekker om filerne allerede er downloadet:
exist=[os.path.basename(f) for f in down_files]


#Filtrerer rækker der allerede er blevet downloadet:
data=data[~data.index.isin(exist)]


#Definerer svarene på, om filerne er blevet downloadet:
dwn="Yes"
n_dwn="No"


#Definerer listen (dictionary), "success", som indeholder "BRnum" og "Yes/No" (alt afhængigt af om de er blevet downloadet):
success={}


#Definerer 'i', som antallet af gange "for-loopet" er kørt:
i = 0


#Kører "for-loopet":
for index in data.index:
    if i> 5:    #CHANGE THE "5" INTO HOW MANY URLs YOU HAVE/WANT TO DOWNLOAD. (WARNING: THIS MIGHT RESULT IN NETWORK CONGESTION! SO BE CAUTIOUS.)
        break


    #Benytter HTTP /GET request til at hente PDF-filer:
    try:
        response = requests.get(data.at[index,"Pdf_URL"]) #CHANGE "Pdf_URL" TO THE COLUMN IN YOUR EXCEL FILE THAT CONTAINS THE URLs.

        #Downloader kun hvis der ligger en PDF-fil:
        if response.headers["content-type"] == "application/pdf":
           
            with open(down_path+index+'.pdf', 'wb') as file:
                file.write(response.content)
                print(response.status_code)
            success[index] = dwn
        else:
            success[index] = n_dwn
            continue
    except:


        #Viser HTTP status-koder:
       print(response.status_code)

    i += 1


#Konverterer dictionary til "dataframe":
DF=pd.DataFrame.from_dict(success,orient="index")


#Skriver en ny Excel-fil med oversigten over downloadede PDF-filer:
with pd.ExcelWriter('Opgaver/Uge 5/PDF_files/Oversigt/PDF Downloads.xlsx',mode='w') as writer:  #CHOOSE THE PATH AND NAME FOR THE SUMMARY EXCEL FILE, WHICH WILL CONTAIN...
    #... AN OVERVIEW OF THE DOWNLOADED PDF FILES.
    DF.to_excel(writer)


    #Giver en tilbagemelding, samt information om hvor oversigten kan findes:
    print("Ny oversigt oprettet, som \"PDF Downloads\" i \"Opgaver/Uge 5/PDF_files/Oversigt/\".")   #CHANGE THE PATH AND NAME FOR THE SUMMARY EXCEL FILE AGAIN.









    

       








   








