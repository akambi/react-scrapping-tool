# -*- coding: utf-8 -*-
"""
Created on Tue Feb 06 15:33:48 2018

@author: zjaadi
"""
from bs4 import BeautifulSoup
import pandas as pd
from fuzzywuzzy import fuzz
#--------------------------------------------------------------------------------------------------

def getProtocolScrap(HTMLString):
    protocolDataFrame=getProtocolData(HTMLString)
    analyzedDataFrame=getDataframeAnalysis(protocolDataFrame)
    dataObject=ConvertDataframeToObject(analyzedDataFrame)
    return dataObject

#---------------------------------------------------------------------------------------------------
def getProtocolData (HTMLString):
    """ Function to load HTML Filtered studyprotocol, parse it and store it in a panda dataframe """

    #Load the HTML string as a beautiful soup object
    print("Load File")
    soup = BeautifulSoup(HTMLString, "html.parser")    
    
    #focus on body
    htmlBody = soup.body
    
    #create the storage array (to store text and features - will receive dictionnaries
    ArrayStorage = []
    
    #Initialize the headers
    CurrentHeaderH1 = "None"
    CurrentHeaderH2 = "None"   
 
    print("Parse File")
    #parse the descendants of the body
    for descendant in htmlBody.descendants:
         #print(descendant.name,type(descendant))
             
         if(str(descendant.name) == "td"):
             tempstring=""
             for string in descendant.strings:
                 tempstring = tempstring +" "+ string
             tempdict = {'documentpart':"table",'ParentContainer':descendant.parent.name,'HeaderH1':CurrentHeaderH1,'HeaderH2':CurrentHeaderH2,'Container':descendant.name,'RawText':tempstring.strip()}
             ArrayStorage.append(tempdict)
             
         elif((str(descendant.name) == "p") & (str(descendant.parent.name) != "td")):
             tempstring=""
             for string in descendant.strings:
                 tempstring = tempstring +" "+ string
             tempdict = {'documentpart':"paragraph",'ParentContainer':descendant.parent.name,'HeaderH1':CurrentHeaderH1,'HeaderH2':CurrentHeaderH2,'Container':descendant.name,'RawText':tempstring.strip()}
             ArrayStorage.append(tempdict)
    
         elif((str(descendant.name) == "h1") | (str(descendant.name) == "h2") | (str(descendant.name) == "h3") | (str(descendant.name) == "h4") | (str(descendant.name) == "h5") | (str(descendant.name) == "h6")):
             tempstring=""
             for string in descendant.strings:
                 tempstring = tempstring +" "+ string
             if (str(descendant.name) == "h1") : 
                 CurrentHeaderH1 = tempstring
                 CurrentHeaderH2 = "None"
             if (str(descendant.name) == "h2") : CurrentHeaderH2 = tempstring            
             tempdict = {'documentpart':"Header",'ParentContainer':descendant.parent.name,'HeaderH1':CurrentHeaderH1,'HeaderH2':CurrentHeaderH2,'Container':descendant.name,'RawText':tempstring.strip()}
             ArrayStorage.append(tempdict)
    
         elif((str(descendant.name) == "li")):
             tempstring=""
             for string in descendant.strings:
                 tempstring = tempstring +" "+ string
             tempdict = {'documentpart':"list",'ParentContainer':descendant.parent.name,'HeaderH1':CurrentHeaderH1,'HeaderH2':CurrentHeaderH2,'Container':descendant.name,'RawText':tempstring.strip()}
             ArrayStorage.append(tempdict)               
    
    print("Convert to dataframe")     
    #Store array into dataframe
    StorageDataframe = pd.DataFrame(ArrayStorage)
    
    
    return StorageDataframe

#-----------------------------------------------------------------------------------------------------------

def getDataframeAnalysis(dataframe):
    
    
    
    return dataframe

#-----------------------------------------------------------------------------------------------------------
def ConvertDataframeToObject(dataframe):
    #array of dict
    arrayStorage=[]
    
    #FindEudraCTNumber
    for id,CurrentRow in dataframe.iterrows():
        #find the value of EudraCTNumber using fuzzy score
        score = fuzz.ratio("EUDRACT NUMBER",CurrentRow['RawText'].upper())
        if (score > 90) :
            value=dataframe.at[id+1,'RawText']
            tempdict = {'id':'eudract_no','value': value,'score': score,'raw_text': value}
            arrayStorage.append(tempdict) 
                   

    #Find StudyTitle
    for id,CurrentRow in dataframe.iterrows():
    #find the value of StudyTitle using fuzzy score        
        if (score > 90) :
            value=dataframe.at[id+1,'RawText']
            tempdict = {'id':'full_title','value': value,'score': score,'raw_text': value}
            arrayStorage.append(tempdict) 

    #indication      
    #Find med_conditions
    tempdict = {'id':'med_conditions','value': '','score': 0,'raw_text': ''}
    arrayStorage.append(tempdict)
    #Find med_conditions_in_lay_langs
    tempdict = {'id':'med_condition_in_lay_langs','value': '','score': 0,'raw_text': ''}
    arrayStorage.append(tempdict)               
        
    return arrayStorage
    
 
