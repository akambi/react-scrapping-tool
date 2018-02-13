# -*- coding: utf-8 -*-
"""
Created on Tue Feb 06 15:33:48 2018

@author: zjaadi
"""
from bs4 import BeautifulSoup
import pandas as pd
from fuzzywuzzy import fuzz
import re

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
    analyzedDataFrame=getDataAnalyzed(protocolDataFrame)
    return analyzedDataFrame

#-----------------------------------------------------------------------------------------------------------

def getDataAnalyzed(dataframe):
    
    return ConvertDataFrameToObject(dataframe)


#-----------------------------------------------------------------------------------------------------------

def ConvertDataFrameToObject(dataframe):
    
    analyzed_array_section_a=getDataAnalyzedSectionA(dataframe)
    analyzed_array_section_b=getDataAnalyzedSectionB(dataframe)
    analyzed_array_section_c=getDataAnalyzedSectionC(dataframe)
    analyzed_array_section_e=getDataAnalyzedSectionE(dataframe,analyzed_array_section_a+analyzed_array_section_b+analyzed_array_section_c)    

        
    return analyzed_array_section_a+analyzed_array_section_b+analyzed_array_section_c+analyzed_array_section_e
    
    
        


#-----------------------------------------------------------------------------------------------------------
def getDataAnalyzedSectionA(dataframe):
    #array of dict
    arrayStorage=[]
    
    #Find EUDRACT NUMBER
    for id,CurrentRow in dataframe.iterrows():
        #find the value of EudraCTNumber using fuzzy score
        score = fuzz.ratio("EUDRACT NUMBER",CurrentRow['RawText'].upper())
        if (score > 90) :
            value=dataframe.at[id+1,'RawText']
            tempdict = {'id':'A.2','value': value.replace(" ", ""),'score': score,'raw_text': value, 'eudractlabel':'EudraCT Number', 'section':'A'}
            arrayStorage.append(tempdict) 

    #Find STUDY TITLE
    for id,CurrentRow in dataframe.iterrows():
    #find the value of StudyTitle using fuzzy score    
        score = fuzz.ratio("STUDY TITLE",CurrentRow['RawText'].upper())    
        if (score > 90) :
            value=dataframe.at[id+1,'RawText']
            tempdict = {'id':'A.3','value': value,'score': score,'raw_text': value, 'eudractlabel':'Full title of the trial', 'section':'A'}
            arrayStorage.append(tempdict) 
     
    #Find NA
    tempdict = {'id':'A.3.1','value': '' ,'score': 0,'raw_text': '', 'eudractlabel':'Title of the trial for lay people, in easily understood, i.e. non-technical language', 'section':'A'}
    arrayStorage.append(tempdict)         
   
    #Find NA
    tempdict = {'id':'A.3.2','value': '' ,'score': 0,'raw_text': '', 'eudractlabel':'Name of the abbreviated title of the trial where available', 'section':'A'}
    arrayStorage.append(tempdict) 
      
    
    #Find PROTOCOL CODE
    for id,CurrentRow in dataframe.iterrows():
    #find the value of PROTOCOL CODE using fuzzy score    
        score = fuzz.ratio("PROTOCOL CODE",CurrentRow['RawText'].upper())    
        if (score > 90) :
            value=dataframe.at[id+1,'RawText']
            tempdict = {'id':'A.4.1','value': value,'score': score,'raw_text': value, 'eudractlabel':"Sponsor's protocol code number", 'section':'A'}
            arrayStorage.append(tempdict) 
    
    #Find VERSION OF THE DOCUMENT
    for id,CurrentRow in dataframe.iterrows():
    #find the value of VERSION OF THE DOCUMENT using fuzzy score    
        score = fuzz.ratio("VERSION OF THE DOCUMENT",CurrentRow['RawText'].upper())    
        if (score > 90) :
            value=dataframe.at[id+1,'RawText']
            tempdict = {'id':'A.4.2','value': value,'score': score,'raw_text': value, 'eudractlabel':"Sposnsor's protocol version", 'section':'A'}
            arrayStorage.append(tempdict)
            
            
    #Find DATE OF THE DOCUMENT
    for id,CurrentRow in dataframe.iterrows():
    #find the value of VERSION OF THE DOCUMENT using fuzzy score    
        score = fuzz.ratio("DATE OF THE DOCUMENT",CurrentRow['RawText'].upper())    
        if (score > 90) :
            value=dataframe.at[id+1,'RawText']
            tempdict = {'id':'A.4.3','value': value,'score': score,'raw_text': value, 'eudractlabel':"Sponsor's protocol date", 'section':'A'}
            arrayStorage.append(tempdict)     
 
    #not to find in the prototcol, they're will be sent with no values                
    #Find ISRCTN number
    tempdict = {'id':'A.5.1','value': '','score': 0,'raw_text': '', 'eudractlabel':'ISRCTN number', 'section':'A'}
    arrayStorage.append(tempdict)
    #Find US NCT number
    tempdict = {'id':'A.5.2','value': '','score': 0,'raw_text': '', 'eudractlabel':'US NCT Nnumber', 'section':'A'}
    arrayStorage.append(tempdict)
    
    #Find VERSION OF THE DOCUMENT
    for id,CurrentRow in dataframe.iterrows():
    #find the value of VERSION OF THE DOCUMENT using fuzzy score    
        score = fuzz.ratio("UNIVERSAL TRIAL NUMBER",CurrentRow['RawText'].upper())    
        if (score > 90) :
            value=dataframe.at[id+1,'RawText']
            tempdict = {'id':'A.5.3','value': value,'score': score,'raw_text': value, 'eudractlabel':'WHO Universal Trail Number (UTN)', 'section':'A'}
            arrayStorage.append(tempdict) 
    #not to find in the prototcol, they're will be sent with no values        
    #Find "is this a resubmission ?"
    tempdict = {'id':'A.6.1','value': '','score': 0,'raw_text': '', 'eudractlabel':'is this a resubmission ?', 'section':'A'}
    arrayStorage.append(tempdict)
    #Find "if yes indicate the resubmission letter"
    tempdict = {'id':'A.6.2','value': '','score': 0,'raw_text': '', 'eudractlabel':'if yes indicate the resubmission letter', 'section':'A'}
    arrayStorage.append(tempdict)
    #Find "is the trial part of agreed pip ?"
    tempdict = {'id':'A7','value': '','score': 0,'raw_text': '', 'eudractlabel':'is the trial part of agreed Paediatric Investigation Plan ?', 'section':'A'}
    arrayStorage.append(tempdict)        
    #Find PIP EMANO
    tempdict = {'id':'A8','value': '','score': 0,'raw_text': '', 'eudractlabel':'Ema Decision number of Paediatric Investigation Plan', 'section':'A'}
    arrayStorage.append(tempdict)          
    
        
    return arrayStorage

#-----------------------------------------------------------------------------------------------------------

    
def getDataAnalyzedSectionB(dataframe):
    #array of dict
    arrayStorage=[]
    
    #Find "B.1 SPONSOR" part
    #Find "SPONSOR ~ Name of oganisation"
    for id,CurrentRow in dataframe.iterrows():
    #find the value of SPONSOR using fuzzy score    
        score = fuzz.ratio("SPONSOR",CurrentRow['RawText'].upper())    
        if (score > 90) :
            value=dataframe.at[id+1,'RawText']
            tempdict = {'id':'b.1.1','value': value,'score': score,'raw_text': value, 'eudractlabel':'Name of Organisation','section':'B'}
            arrayStorage.append(tempdict) 
    #not to find in the prototcol, they will be given default values           
    #Find "Given name"
    tempdict = {'id':'b.1.2.1','value': 'Valérie','score': 100,'raw_text': '', 'eudractlabel':'Given Name','section':'B'}
    arrayStorage.append(tempdict)
    #Find "Middle Name"
    tempdict = {'id':'b.1.2.2','value': '','score': 100,'raw_text': '', 'eudractlabel':'Middle Name','section':'B'}
    arrayStorage.append(tempdict)
    #Find "Family name"
    tempdict = {'id':'b.1.2.3','value': 'Fautier','score': 100,'raw_text': '', 'eudractlabel':'Family Name','section':'B'}
    arrayStorage.append(tempdict)        
    #Find "Street address"
    tempdict = {'id':'b.1.3.1','value': '50 rue Carnot','score': 100,'raw_text': '', 'eudractlabel':'Street Address','section':'B'}
    arrayStorage.append(tempdict) 
    #Find "Town/City"
    tempdict = {'id':'b.1.3.2','value': 'Suresnes','score': 100,'raw_text': '', 'eudractlabel':'Town/City','section':'B'}
    arrayStorage.append(tempdict) 
    #Find "Post code"
    tempdict = {'id':'b.1.3.3','value': '92284','score': 100,'raw_text': '', 'eudractlabel':'Postal Code','section':'B'}
    arrayStorage.append(tempdict)  
    #Find "Country"
    tempdict = {'id':'b.1.3.4','value': 'France','score': 100,'raw_text': '', 'eudractlabel':'Country','section':'B'}
    arrayStorage.append(tempdict) 
    
    #Find "Telephone number"
    #Find "Country Dialing Prefix" +33
    tempdict = {'id':'b.1.4.1','value': '+33','score': 100,'raw_text': '', 'eudractlabel':'Country Dialing Prefix','section':'B'}
    arrayStorage.append(tempdict)        
    #Find "Local Area Code"
    tempdict = {'id':'b.1.4.2','value': '','score': 100,'raw_text': '', 'eudractlabel':'Local Area Code','section':'B'}
    arrayStorage.append(tempdict)    
    #Find "Phone number"
    tempdict = {'id':'b.1.4.3','value': '155727063','score': 100,'raw_text': '', 'eudractlabel':'Phone Number','section':'B'}
    arrayStorage.append(tempdict)    
    #Find "Extension"
    tempdict = {'id':'b.1.4.4','value': '','score': 100,'raw_text': '', 'eudractlabel':'Extension','section':'B'}
    arrayStorage.append(tempdict)    
    
    #Find "Fax number"
    #Find "Country Dialing Prefix" +33
    tempdict = {'id':'b.1.5.1','value': '+33','score': 100,'raw_text': '', 'eudractlabel':'Country Dialing Prefix','section':'B'}
    arrayStorage.append(tempdict)    
    #Find "Local Area Code"
    tempdict = {'id':'b.1.5.2','value': '','score': 100,'raw_text': '', 'eudractlabel':'Local Area Code','section':'B'}
    arrayStorage.append(tempdict)    
    #Find "Phone number"
    tempdict = {'id':'b.1.5.3','value': '155725412','score': 100,'raw_text': '', 'eudractlabel':'Phone number','section':'B'}
    arrayStorage.append(tempdict)    
    #Find "Extension"
    tempdict = {'id':'b.1.5.4','value': '','score': 100,'raw_text': '', 'eudractlabel':'Extension','section':'B'}
    arrayStorage.append(tempdict)      
    
    #Find "email"
    tempdict = {'id':'b.1.6','value': 'valerie.fautrier@servier.com','score': 100,'raw_text': '', 'eudractlabel':'E-mail','section':'B'}
    arrayStorage.append(tempdict) 
    
    #-----------------------
   
    #Find "B.3 Status of the sponsor" part
    #not to find in the prototcol, they will be given default values           
    #Find "Commerial"
    tempdict = {'id':'b.3.1','value': 'yes','score': 100,'raw_text': '', 'eudractlabel':'B.3.1 and B.3.1 Status of the sponsor','section':'B'}
    arrayStorage.append(tempdict)
    #Find "Non commercial,"
    tempdict = {'id':'b.3.2','value': 'no','score': 100,'raw_text': '', 'eudractlabel':'B.3.1 and B.3.1 Status of the sponsor', 'section':'B'}
    arrayStorage.append(tempdict)
    
    #-----------------------

    #Find "B.4 Status of the sponsor" part
    #not to find in the prototcol, they will be given default values           
    #Find "Name of organisation"
    tempdict = {'id':'b.4.1','value': 'ADIR','score': 100,'raw_text': '', 'eudractlabel':'Name of organisation', 'section':'B'}
    arrayStorage.append(tempdict)
    #Find "Country"
    tempdict = {'id':'b.4.2','value': 'France','score': 100,'raw_text': '', 'eudractlabel':'Country', 'section':'B'}
    arrayStorage.append(tempdict)
    
    #-----------------------

    #Find "B.5 Contact point designated by the sponsor for further information" part
    #not to find in the prototcol, they will be given default values           
    #Find "Name of organisation"
    tempdict = {'id':'b.5.1','value': value,'score': 100,'raw_text':'', 'eudractlabel':'Name of organisation', 'section':'B'}
    arrayStorage.append(tempdict) 
    #Find "Functional name of contact point"
    tempdict = {'id':'b.5.2','value': 'Clinical Studies Departement','score': 100,'raw_text': '', 'eudractlabel':'Functional name of contact point', 'section':'B'}
    arrayStorage.append(tempdict)      
    #Find "Street address"
    tempdict = {'id':'b.5.3.1','value': '50 rue Carnot','score': 100,'raw_text': '', 'eudractlabel':'Street Address','section':'B'}
    arrayStorage.append(tempdict) 
    #Find "Town/City"
    tempdict = {'id':'b.5.3.2','value': 'Suresnes','score': 100,'raw_text': '', 'eudractlabel':'Town/City','section':'B'}
    arrayStorage.append(tempdict) 
    #Find "Country"
    tempdict = {'id':'b.5.3.3','value': '92284','score': 100,'raw_text': '', 'eudractlabel':'Postal Code','section':'B'}
    arrayStorage.append(tempdict)  
     #Find "Country"
    tempdict = {'id':'b.5.3.4','value': 'France','score': 100,'raw_text': '', 'eudractlabel':'Country','section':'B'}
    arrayStorage.append(tempdict)
    
    #Find "Telephone number"
    #Find "Country Dialing Prefix" +33
    tempdict = {'id':'b.5.4.1','value': '+33','score': 100,'raw_text': '', 'eudractlabel':'Country Dialing Prefix','section':'B'}
    arrayStorage.append(tempdict)    
    #Find "Local Area Code"
    tempdict = {'id':'b.5.4.2','value': '','score': 100,'raw_text': '', 'eudractlabel':'Local Area Code','section':'B'}
    arrayStorage.append(tempdict)    
    #Find "Phone number"
    tempdict = {'id':'b.5.4.3','value': '1.55.72.70.63','score': 100,'raw_text': '', 'eudractlabel':'Phone number','section':'B'}
    arrayStorage.append(tempdict)    
    #Find "Extension"
    tempdict = {'id':'b.5.4.4','value': '','score': 100,'raw_text': '', 'eudractlabel':'Extension','section':'B'}
    arrayStorage.append(tempdict)    
    
    #Find "Fax number"
    #Find "Country Dialing Prefix" +33
    tempdict = {'id':'b.5.5.1','value': '+33','score': 100,'raw_text': '', 'eudractlabel':'Country Dialing Prefix','section':'B'}
    arrayStorage.append(tempdict)      
    #Find "Local Area Code"
    tempdict = {'id':'b.5.5.2','value': '','score': 100,'raw_text': '', 'eudractlabel':'Local Area Code','section':'B'}
    arrayStorage.append(tempdict)      
    #Find "Phone number"
    tempdict = {'id':'b.5.5.3','value': '155725412','score': 100,'raw_text': '', 'eudractlabel':'Phone number','section':'B'}
    arrayStorage.append(tempdict)      

    #Find "Extension"
    tempdict = {'id':'b.5.5.4','value': '','score': 100,'raw_text': '', 'eudractlabel':'Extension','section':'B'}
    arrayStorage.append(tempdict)      
    
    #Find "email" "Functional email address rather than a personal one"
    tempdict = {'id':'b.5.6','value': 'clinicaltrial@servier.com','score': 100,'raw_text': '', 'eudractlabel':'E-mail','section':'B'}
    arrayStorage.append(tempdict) 
            
    return arrayStorage

    #-----------------------


def getDataAnalyzedSectionC(dataframe):
    #array of dict
    arrayStorage=[]
    #find "C1 request for the competent authority" part
    #not to find in the prototcol, they will be given default values           
    #Find "Given name"
    tempdict = {'id':'c.1.5.1','value': 'yes','score': 100,'raw_text': '', 'eudractlabel':'Do you want a copy of the CTA form data saved on EudraCT as an XML file ? ','section':'C'}
    arrayStorage.append(tempdict)
    #Find "Middle Name"
    tempdict = {'id':'c.1.5.1.1','value': 'clilicaltrials@servier.com','score': 100,'raw_text': '', 'eudractlabel':'If Yes provide the e-mail address(es) to which it should be sent (up to five addresses)','section':'C'}
    arrayStorage.append(tempdict)
    #Find "Family name"
    tempdict = {'id':'c.1.5.1.2','value': 'yes','score': 100,'raw_text': '', 'eudractlabel':'Do you want to recieve this via password protected link(s)','section':'C'}
    arrayStorage.append(tempdict)
    
    return arrayStorage 

    #-----------------------

def getDataAnalyzedSectionE(dataframe,abc_sections_array):
    #array of dict
    arrayStorage=[]    
    
    #Find "INDICATION"
    for id,CurrentRow in dataframe.iterrows():
    #find the value of INDICATION using fuzzy score    
        score = fuzz.ratio("INDICATION",CurrentRow['RawText'].upper())    
        if (score > 90) :
            value=dataframe.at[id+1,'RawText']
            tempdict = {'id':'e.1.1','value': value,'score': score,'raw_text': value, 'eudractlabel':'Specify the medical condition(s) to be investigated (free text)','section':'E'}
            arrayStorage.append(tempdict) 
    
    #Find ""
    tempdict = {'id':'e.1.1.1','value': value,'score': 100,'raw_text': '', 'eudractlabel':'Medical condition in easily understood language','section':'E'}
    arrayStorage.append(tempdict)
    #Find ""
    tempdict = {'id':'e.1.1.2','value':'','score': 100,'raw_text': '', 'eudractlabel':'Identify the therapeutic area','section':'E'}
    arrayStorage.append(tempdict)
   
    #E1.2 medDRA information 
    #deductible field from INDICATION
    tempdict = {'id':'e.1.2.1','value':'','score': 100,'raw_text': '', 'eudractlabel':'Term','section':'E'}
    arrayStorage.append(tempdict)
    
    #deductible field INDICATION
    tempdict = {'id':'e.1.2.2','value':'','score': 100,'raw_text': '', 'eudractlabel':'Level','section':'E'}
    arrayStorage.append(tempdict)
    
    #deductible field INDICATION
    tempdict = {'id':'e.1.2.3','value':'','score': 100,'raw_text': '', 'eudractlabel':'Classification code','section':'E'}
    arrayStorage.append(tempdict)
    
    #E2 Objective of the trial 
    #Find "PRIMARY OBJECTIVE"
    for id,CurrentRow in dataframe.iterrows():
    #find the value of PRIMARY OBJECTIVE using fuzzy score    
        #score = fuzz.ratio("PRIMARY OBJECTIVE",CurrentRow['RawText'].upper()) 
        #if score > 70 : print [score,CurrentRow['RawText'].upper()]
        #print 'before'
        pattern=re.compile("^(.|\n)*[0-9](\.[0-9])*(\.)?(.|\n)*PRIMARY OBJECTIVE(.|\n)*$",re.IGNORECASE)
        obj=pattern.match(CurrentRow['RawText'].upper())
        if (obj and dataframe.at[id,'documentpart']=='Header'):
            print 'after'
            print [CurrentRow['RawText'].upper()]
            stop_flag=dataframe.at[id,'Container']
            idCopy=id+1
            value=''
            while(dataframe.at[idCopy,'Container']!=stop_flag):
                 value=value+dataframe.at[idCopy,'RawText']
                 idCopy += 1
            tempdict = {'id':'e.2.1','value': value,'score': score,'raw_text': value, 'eudractlabel':'Main objective of the trial','section':'E'}
            arrayStorage.append(tempdict)
    
    #Find "SECONDARY OBJECTIVE"
    for id,CurrentRow in dataframe.iterrows():
    #find the value of SECONDARY OBJECTIVE using fuzzy score    
        #score = fuzz.ratio("SECONDARY OBJECTIVE",CurrentRow['RawText'].upper()) 
        #if score > 60 : print [score,CurrentRow['RawText'].upper(),dataframe.at[id+1,'RawText']]
        pattern=re.compile("^(.|\n)*[0-9](\.[0-9])*(\.)?(.|\n)*SECONDARY OBJECTIVE(.|\n)*$")
        obj=pattern.match(CurrentRow['RawText'].upper())
        if (obj and dataframe.at[id,'documentpart']=='Header'):
            print 'after'
            print [CurrentRow['RawText'].upper()]
            stop_flag=dataframe.at[id,'Container']
            idCopy=id+1
            value=''
            while(dataframe.at[idCopy,'Container']!=stop_flag):
                 value=value+dataframe.at[idCopy,'RawText']
                 idCopy += 1
            tempdict = {'id':'e.2.2','value': value,'score': score,'raw_text': value, 'eudractlabel':'Secondary objectives of the trial','section':'E'}
            arrayStorage.append(tempdict)
            
    #deductible field 
    tempdict = {'id':'e.2.3','value':'','score': 100,'raw_text': '', 'eudractlabel':'Is there a sub-study?','section':'E'}
    arrayStorage.append(tempdict)
    
    #deductible field 
    tempdict = {'id':'e.2.3.1','value':'','score': 100,'raw_text': '', 'eudractlabel':'If Yes give the full title, date and version of each sub-study and their related objectives','section':'E'}
    arrayStorage.append(tempdict)
    
    #Find "INCLUSION CRITERIA"
    for id,CurrentRow in dataframe.iterrows():
    #find the value of INCLUSION CRITERIA using regex 
        pattern=re.compile("^(.|\n)*[0-9](\.[0-9])*(\.)?(\s|\\xa0|\n)*INCLUSION CRITERIA(.|\n)*$")
        obj=pattern.match(CurrentRow['RawText'].upper())
        if (obj and dataframe.at[id,'documentpart']=='Header'):
            print 'after'
            print [CurrentRow['RawText'].upper()]
            stop_flag=dataframe.at[id,'Container']
            idCopy=id+1
            value=''
            while(dataframe.at[idCopy,'Container']!=stop_flag):
                 value=value+dataframe.at[idCopy,'RawText']
                 idCopy += 1
            tempdict = {'id':'e.3','value': value,'score': score,'raw_text': value, 'eudractlabel':'Principal inclusion criteria','section':'E'}
            arrayStorage.append(tempdict)
     
    #Find "NON-INCLUSION CRITERIA"
    for id,CurrentRow in dataframe.iterrows():
    #find the value of NON-INCLUSION CRITERIA using regex  
        pattern=re.compile("^(.|\n)*[0-9](\.[0-9])*(\.)?(\s|\\xa0|\n)*NON-INCLUSION CRITERIA(.)*$")
        obj=pattern.match(CurrentRow['RawText'].upper())
        #if it matches the pattern and it's a header 
        if (obj and dataframe.at[id,'documentpart']=='Header'):
            print 'after'
            print [CurrentRow['RawText'].upper()]
            stop_flag=dataframe.at[id,'Container']
            idCopy=id+1
            value=''
            #get all paragraph of the header with embedded headers
            while(dataframe.at[idCopy,'Container']!=stop_flag):
                 value=value+dataframe.at[idCopy,'RawText']
                 idCopy += 1
            tempdict = {'id':'e.4','value': value,'score': score,'raw_text': value, 'eudractlabel':'Principal exclusion criteria','section':'E'}
            arrayStorage.append(tempdict)       
    #E.5 END POINTS(s)
    #Find "PRIMARY ENDPOINTS"
    for id,CurrentRow in dataframe.iterrows():
    #find the value of PRIMARY ENDPOINTS CRITERIA using regex    
        pattern=re.compile("^(.|\n)*[0-9](\.[0-9])*(\.)?(\s|\\xa0|\n)*END(.)*POINT(.)*$",re.IGNORECASE)
        obj=pattern.match(CurrentRow['RawText'].upper())
        #if it matches the pattern and it's a header 
        if (obj and dataframe.at[id,'documentpart']=='Header'):
            print 'after'
            print [CurrentRow['RawText'].upper()]
            stop_flag=dataframe.at[id,'Container']
            idCopy=id+1
            value=''
            #get all paragraph of the header with embedded headers
            while(dataframe.at[idCopy,'Container']!=stop_flag):
                 value=value+dataframe.at[idCopy,'RawText']
                 idCopy += 1
            tempdict = {'id':'e.5.1','value': value,'score': score,'raw_text': value, 'eudractlabel':'Primary end point(s)','section':'E'}
            arrayStorage.append(tempdict)
    
    #deductible field 
    tempdict = {'id':'e.5.1.1','value':'','score': 100,'raw_text': '', 'eudractlabel':'Timepoint(s) of evaluation of this end point','section':'E'}
    arrayStorage.append(tempdict)        
    
    #Find "SECONDARY ENDPOINTS"
    for id,CurrentRow in dataframe.iterrows():
    #find the value of PRIMARY ENDPOINTS CRITERIA using regex    
        pattern=re.compile("^(.|\n)*[0-9](\.[0-9])*(\.)?(\s|\\xa0|\n)*SECONDARY ENDPOINT(.)*$",re.IGNORECASE)
        obj=pattern.match(CurrentRow['RawText'].upper())
        #if it matches the pattern and it's a header 
        if (obj and dataframe.at[id,'documentpart']=='Header'):
            print 'after'
            print [CurrentRow['RawText'].upper()]
            stop_flag=dataframe.at[id,'Container']
            idCopy=id+1
            value=''
            #get all paragraph of the header with embedded headers
            while(dataframe.at[idCopy,'Container']!=stop_flag):
                 value=value+dataframe.at[idCopy,'RawText']
                 idCopy += 1
            tempdict = {'id':'e.5.2','value': value,'score': score,'raw_text': value, 'eudractlabel':'Secondary end point(s))','section':'E'}
            arrayStorage.append(tempdict)     
     
    #deductible field 
    tempdict = {'id':'e.5.2.1','value':'','score': 100,'raw_text': '', 'eudractlabel':'Timepoint(s) of evaluation of this end point','section':'E'}
    arrayStorage.append(tempdict)  
    
    #E.6 SCOPE OF THE TRIAL   
    #deductible field 
    exist=search_keywords(['diagnosis'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.6.1','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Diagnosis','section':'E'}
    arrayStorage.append(tempdict)
    
    #deductible field 
    exist=search_keywords(['propylaxis','prophylactic','prevention','vaccine','vaccination'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.6.2','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Prophylaxis','section':'E'}
    arrayStorage.append(tempdict)  
    
    #deductible field 
    exist=search_keywords(['therapy'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.6.3','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Therapy','section':'E'}
    arrayStorage.append(tempdict)  
    
    #deductible field 
    exist=search_keywords(['safety'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.6.4','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Safety','section':'E'}
    arrayStorage.append(tempdict)  
    
    #deductible field 
    exist=search_keywords(['efficacy'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.6.5','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Efficacy','section':'E'}
    arrayStorage.append(tempdict)  
    
     #deductible field 
    exist=search_keywords(['pharmacokinetic','pharmacokinetics'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.6.6','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Pharmacokinetic','section':'E'}
    arrayStorage.append(tempdict)
    
    #deductible field 
    exist=search_keywords(['pharacodynamic','pharacodynamics'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.6.7','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Pharacodynamic','section':'E'}
    arrayStorage.append(tempdict)  
    
    #deductible field 
    exist=search_keywords(['bioequivalence', 'bioequivalences'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.6.8','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Bioequivalence','section':'E'}
    arrayStorage.append(tempdict)  
    
    #deductible field 
    exist=search_keywords(['dose response','dose ranging', 'controlled dose', 'dose finding'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.6.9','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Dose Response','section':'E'}
    arrayStorage.append(tempdict)  
    
    #deductible field 
    exist=search_keywords(['pharmacogenetic','pharmacogenetics'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.6.10','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Pharmacogenetic','section':'E'}
    arrayStorage.append(tempdict) 
    
    #deductible field 
    exist=search_keywords(['pharmacogenomic','pharmacogenomics'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.6.11','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Pharmacogenomic','section':'E'}
    arrayStorage.append(tempdict)  
    
    #deductible field 
    exist=search_keywords(['pharmacoeconomic','pharmacoeconomics'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.6.12','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Pharmacoeconomic','section':'E'}
    arrayStorage.append(tempdict)  
    
    #deductible field 
    exist='No'
    tempdict = {'id':'e.6.13','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Others','section':'E'}
    arrayStorage.append(tempdict) 
     
    
    #E.7 TRIAL TYPE AND PHASE 
    #deductible field 
    exist=search_keywords(['pharmacokinetics','phase i','phase 1','phase 1b','single dose'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.7.1','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Human pharmacology (Phase I)','section':'E'}
    arrayStorage.append(tempdict)
    
    #deductible field if yes in e.7.1 specify
    exist=search_keywords(['first in man','first in human'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.7.1.1','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'First Administration to Human','section':'E'}
    arrayStorage.append(tempdict)
    
    #deductible field if yes in e.7.1 specify
    exist=search_keywords(['bioequivalence'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.7.1.2','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Bioequivalence Study','section':'E'}
    arrayStorage.append(tempdict)
    
    
    #deductible field 
    exist=search_keywords(['therapeutic exploratory','phase ii','phase 2'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.7.2','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Therapeutic exploratory (Phase II)','section':'E'}
    arrayStorage.append(tempdict)  
    
    #deductible field 
    exist=search_keywords(['therapeutic confirmatory','phase iii','phase 3'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.7.3','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Therapeutic confirmatory (Phase III)','section':'E'}
    arrayStorage.append(tempdict) 
    
    #deductible field 
    exist=search_keywords(['therapeutic use','phase vi','phase 4'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.7.4','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Therapeutic use (Phase IV)','section':'E'}
    arrayStorage.append(tempdict)
    
    #E.8 DESIGN OF THE TRIAL 
    #deductible field 
    exist=search_keywords(['controlled'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.8.1','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Controlled','section':'E'}
    arrayStorage.append(tempdict)
    
    #deductible field 
    exist=search_keywords(['randomised'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.8.1.1','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Randomised','section':'E'}
    arrayStorage.append(tempdict)  
    
    #deductible field 
    exist=search_keywords(['open'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.8.1.2','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Open','section':'E'}
    arrayStorage.append(tempdict) 
    
    #deductible field 
    exist=search_keywords(['single blind'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.8.1.3','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Single blind','section':'E'}
    arrayStorage.append(tempdict) 
    
    #deductible field 
    exist=search_keywords(['double blind'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.8.1.4','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Double blind','section':'E'}
    arrayStorage.append(tempdict) 
    
    #deductible field 
    exist=search_keywords(['parallel group'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.8.1.5','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Parallel group','section':'E'}
    arrayStorage.append(tempdict) 
    
    #deductible field 
    exist=search_keywords(['cross over'],pd.DataFrame(abc_sections_array).append(pd.DataFrame(arrayStorage)))
    tempdict = {'id':'e.8.1.6','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Cross Over','section':'E'}
    arrayStorage.append(tempdict) 
    
    #deductible field 
    exist='No'
    tempdict = {'id':'e.8.1.7','value': exist,'score': 100,'raw_text': '', 'eudractlabel':'Other','section':'E'}
    arrayStorage.append(tempdict) 
    
    
    
    return arrayStorage

 #-----------------------------------------------------------------------------------------------------------
    
def search_keywords(keywords_list,dataframe):
    
    full_title=dataframe[dataframe['id']=='A.3'].iloc[0]['value']
    main_objective=dataframe[dataframe['id']=='e.2.1'].iloc[0]['value']
    primary_endpoint=dataframe[dataframe['id']=='e.5.1'].iloc[0]['value']
    inclusion_criteria=dataframe[dataframe['id']=='e.3'].iloc[0]['value']
    exclusion_criteria=dataframe[dataframe['id']=='e.4'].iloc[0]['value']
    
    text=full_title+" "+main_objective+" "+primary_endpoint+" "+inclusion_criteria+" "+exclusion_criteria
    text=text.upper()
    
    for keyword in keywords_list:
        if keyword.upper() in text:
            return 'Yes'
    return 'No'   

        
         
  

#test code
#HTMLPath = "C:\Users\zjaadi\Desktop\CL3-95005-004 EAP_Protocol Final version_31-05-2016.htm"
#HTMLPath = "C:\Users\zjaadi\Desktop\CL2-95005-002_TASCO1_Amended Protocol_INT_ Final Version CLEAN_25-01-2017.htm"
#ps_dataframe=pd.DataFrame(getProtocolScrap(open(HTMLPath)))
#dataframe=getProtocolData(open(HTMLPath))

