# -*- coding: utf-8 -*-
"""
Created on Tue Feb 06 15:33:48 2018

@author: zjaadi
"""
from bs4 import BeautifulSoup
import pandas as pd
from fuzzywuzzy import fuzz

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

def getProtocolScrap(HTMLString):
    protocolDataFrame=getProtocolData(HTMLString)
    analyzedDataFrame=getDataframeAnalyzed(protocolDataFrame)
    return analyzedDataFrame

#-----------------------------------------------------------------------------------------------------------

def getDataframeAnalyzed(dataframe):
    
    analyzed_dataframe_section_a=getDataframeAnalyzedSectionA(dataframe)
        
    return analyzed_dataframe_section_a

#-----------------------------------------------------------------------------------------------------------

def ConvertDataFrameToObject(dataframe):
    
    
        
    return dataframe

#-----------------------------------------------------------------------------------------------------------

    
 def getDataframeAnalyzedSectionA(dataframe):
    #array of dict
    arrayStorage=[]
    
    #Find EUDRACT NUMBER
    for id,CurrentRow in dataframe.iterrows():
        #find the value of EudraCTNumber using fuzzy score
        score = fuzz.ratio("EUDRACT NUMBER",CurrentRow['RawText'].upper())
        if (score > 90) :
            value=dataframe.at[id+1,'RawText']
            tempdict = {'id':'eudract_no','value': value.replace(" ", ""),'score': score,'raw_text': value}
            arrayStorage.append(tempdict) 

    #Find STUDY TITLE
    for id,CurrentRow in dataframe.iterrows():
    #find the value of StudyTitle using fuzzy score    
        score = fuzz.ratio("STUDY TITLE",CurrentRow['RawText'].upper())    
        if (score > 90) :
            value=dataframe.at[id+1,'RawText']
            tempdict = {'id':'full_title','value': value,'score': score,'raw_text': value}
            arrayStorage.append(tempdict)      
    
    #Find PROTOCOL CODE
    for id,CurrentRow in dataframe.iterrows():
    #find the value of PROTOCOL CODE using fuzzy score    
        score = fuzz.ratio("PROTOCOL CODE",CurrentRow['RawText'].upper())    
        if (score > 90) :
            value=dataframe.at[id+1,'RawText']
            tempdict = {'id':'sponsor_protocol_no','value': value,'score': score,'raw_text': value}
            arrayStorage.append(tempdict) 
    
    #Find VERSION OF THE DOCUMENT
    for id,CurrentRow in dataframe.iterrows():
    #find the value of VERSION OF THE DOCUMENT using fuzzy score    
        score = fuzz.ratio("VERSION OF THE DOCUMENT",CurrentRow['RawText'].upper())    
        if (score > 90) :
            value=dataframe.at[id+1,'RawText']
            tempdict = {'id':'sponsor_protocol_version','value': value,'score': score,'raw_text': value}
            arrayStorage.append(tempdict)
            
            
    #Find DATE OF THE DOCUMENT
    for id,CurrentRow in dataframe.iterrows():
    #find the value of VERSION OF THE DOCUMENT using fuzzy score    
        score = fuzz.ratio("DATE OF THE DOCUMENT",CurrentRow['RawText'].upper())    
        if (score > 90) :
            value=dataframe.at[id+1,'RawText']
            tempdict = {'id':'sponsor_protocol_version_date','value': value,'score': score,'raw_text': value}
            arrayStorage.append(tempdict)     
    #not to find in the prototcol, they're will be sent with no values                
    #Find ISRCTN number
    tempdict = {'id':'intern_ct_ident_isrctn','value': '','score': 0,'raw_text': ''}
    arrayStorage.append(tempdict)
    #Find US NCT number
    tempdict = {'id':'intern_ct_ident_usnct','value': '','score': 0,'raw_text': ''}
    arrayStorage.append(tempdict)
    
    #Find VERSION OF THE DOCUMENT
    for id,CurrentRow in dataframe.iterrows():
    #find the value of VERSION OF THE DOCUMENT using fuzzy score    
        score = fuzz.ratio("UNIVERSAL TRIAL NUMBER",CurrentRow['RawText'].upper())    
        if (score > 90) :
            value=dataframe.at[id+1,'RawText']
            tempdict = {'id':'intern_ct_ident_utrn','value': value,'score': score,'raw_text': value}
            arrayStorage.append(tempdict) 
    #not to find in the prototcol, they're will be sent with no values        
    #Find "is this a resubmission ?"
    tempdict = {'id':'is_resubmission','value': '','score': 0,'raw_text': ''}
    arrayStorage.append(tempdict)
    #Find "if yes indicate the resubmission letter"
    tempdict = {'id':'resubmission_letter','value': '','score': 0,'raw_text': ''}
    arrayStorage.append(tempdict)
    #Find "is the trial part of agreed pip ?"
    tempdict = {'id':'is_part_pip','value': '','score': 0,'raw_text': ''}
    arrayStorage.append(tempdict)        
    #Find PIP EMANO
    tempdict = {'id':'pip_decision_no','value': '','score': 0,'raw_text': ''}
    arrayStorage.append(tempdict)          
          
        
    return arrayStorage
