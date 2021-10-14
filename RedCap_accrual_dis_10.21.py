# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# This script was written on Octiober 2021 by M.Godinez [Data Solutions Analyst at CRTI]
#Issues I was having: was able to get the data to a semi-desire format and then would copy and paste using 
#tool provided by CTRP. This was easy but would had to copy every trial individually and into two sheets
#Also I would spend a lot of time figuring out which trials actually need subject registration since MCC
#does not code for this information the the dashboard provided to me.


#OVERALL ACOMPLISHMENTS: This script takes the data pulled from CTO metrics.
#1. identify the subjects that are actually on study
#2. identify subjects with all data requirements complete
#3. Indenify the trials that actually are complete registrations and therefore subject accrual
#4. Formats every file appropriately and send them to desire path where the user can compress all files and submit
#5. Once submitted you will recieve a confimation from CTRP saying if the submisstion is successful or not

#Load the libraries I usually use

import pandas as pd
import numpy as np
import os


# import CTRP data from dashboard this is only OnCore Accrual
#importing an excel file

file_name=input('File path to pull data:')
ctrp=pd.read_excel(file_name)
#dropping the title column since it would not be nessessary 
# ctrp=ctrp.drop('TITLE', axis=1)

# #load in list of excel that I extracted from STRAP with trials that are fully registered
# # I did use excel manually first - but just plan to do this peridically every month by doing a new download
# full_reg=pd.read_excel('C:/Filepath/file_name.xlsx')

# #make a list of all the trials that are fully registered
# list_reg=list(full_reg['NCI Trial Identifier'])

# #keep only rows from all the OnCore accrual with fully register trials in CTRP
# ctrp_full_reg= ctrp[ctrp['NCI Trial ID'].isin(list_reg)]

# #drop all trials that do not have an on study date - they are not on study
# ctrp_full_reg = ctrp_full_reg.dropna(subset=['FIRST_ONSTUDY_CREATED_DATE'])



# #data that is complete - has all the data elements necessary to be registered to CTRP
# complete= ctrp_full_reg[~ctrp_full_reg.isnull().any(axis=1)]

#================STEP 2 - Data Formatting==========================
#date clean up - for On Study date
list_s =list(ctrp['On Study Date'])

#Loop through all dates
new_dates =list()
for z in list_s:
   if z == 0:
       new_dates.append(z)
   else:
    y=str(z)
    x=y.split(' ')
    w=x[0]
    v=w.split('-')
    yr=v[0]
    mo=v[1]
    da=v[2]
    dia =yr+mo+da
    new_dates.append(dia)
# replace the old dates with new format
ctrp['On Study Date']=new_dates

#Birthdates that do not exist are replaces with this place holder
ctrp['Date of Birth'] = ctrp['Date of Birth'].replace([np.nan,'7/1776','07/1776'], 190007)

#birthdates formatting
list_b =list(ctrp['Date of Birth'])

new_list =list()

for b in list_b:
    if b == 190007:
        new_list.append(b)
    else:
        a=str(b)
        c=a.split('/')
        e=c[0].rstrip()
        f=c[1].rstrip()
        if len(e)==1:
            g='0'+e
            com1=str(f)+str(g)
            new_list.append(com1)
        else:
            com2=str(f)+str(e)
            new_list.append(com2)
        # d=e.split('-')
        # year=d[0]
        # day=d[1]
        # birth= year+day
        #new_list.append(c)
# replace all birthdates       
ctrp['Date of Birth']=new_list

#ZIP code formatting
#add zeros to nan in zip code
ctrp['Zip'] =ctrp['Zip'].replace(np.nan, '00000')
#reduce zip code to only 5 numbers
list_z =ctrp['Zip'] 
new_z =[]
for z in list_z:
   z= str(z)
   y=z.split('-')
   zl=y[0]
   new_z.append(zl)
# replaceing zip   
ctrp['Zip']=new_z


#disease and histology
# list_d =ctrp['Disease Code']

# list_d.unique()

# new_disease =[]
# for d in  list_d:
#     d=str(d)
#     g=d.split('-')
#     new=g[0]
#     if new == 'nan':
#         new='C80.9'
#     new_disease.append(new)
    
# # Clean the histology list
# new_hist=[]
# list_h =complete['Histology']
# for r in  list_h:
#     r=str(r)
#     s=r.split('-')
#     news=s[0]
#     new_hist.append(news)
    
# disease_code=[]
# for pl, sc in zip(new_disease, new_hist): 
#     string=";".join([pl.strip(),sc])
#     print(string)
#     disease_code.append(string)
    
# # Replace with new disease code:
# complete['Disease Site'] =disease_code   

# add empty columns or place holder colunms [These are set]
ctrp['County Code'] = ctrp.apply(lambda _: '', axis=1)
ctrp['Payment Method'] = ctrp.apply(lambda _: '', axis=1)
ctrp['Country'] = ctrp.apply(lambda _: 'US', axis=1)
ctrp['nine']= ctrp.apply(lambda _: ',,,,,,,,', axis=1)
ctrp['end']= ctrp.apply(lambda _: '', axis=1)
ctrp['Index'] = ctrp.apply(lambda _: 'PATIENTS', axis=1)

#more formatting: replacing values to ones that are understandable by CTRP program
#Gender
ctrp['Gender'].replace(['F','M', 'U',np.nan],['Female','Male','Unknown','Unknown'],inplace=True)
#any study site code
ctrp['Study Site'].replace(['Masonic Cancer Center', 'University of Minnesota','Brown','Duke'],[139049,139049,212961,149280],inplace=True)
#race that may be collected differently
ctrp['Race'].replace(['Patient Refusal','More than One race'],['Not Reported', 'Unknown'],inplace=True)
ctrp['Race'].replace(['White (Caucasian)','Native American, Alaskan Native','Other',np.nan,'Asian/Pacific Islander'],['White', 'American Indian or Alaska Native','Unknown','Unknown','Asian'],inplace=True)

#ethnicity that may be collected differently
ctrp['Ethnicity'].replace(['Non-Hispanic','Patient Refusal','More than One race','88'],['Not Hispanic or Latino','Not Reported', 'Unknown','Unknown'],inplace=True)
#some disease sites are not correctly programmed in OnCore so I need to replace them there - this is a place to do that
#ATTENTION -> complete['Disease Site'].replace(['C42.1;9861 ','C42.0;9650 ','C42.0;9861 ','C42.1;9823 '],['C42.1;9861/3' ,'C42.0;9650/3','C42.0;9861/3','C42.1;9823/3'], inplace=True)
ctrp['Disease Code'].replace(['Z1000','620.20'],['V100','620.2'],inplace=True)

ctrp.columns
#make a df containg race
race=ctrp[['NCI ID', 'Sequence No', 'Race']]
#add a place holder columns
race['Index']=race.apply(lambda _: 'PATIENT_RACES', axis=1)
race=race[['Index','NCI ID', 'Sequence No', 'Race']]

race['Race'].unique()

#drop the last column and reoganize df
#complete=complete.drop(columns=[ 'FIRST_ONSTUDY_CREATED_DATE'])
main=ctrp[['Index','NCI ID', 'Sequence No','Zip', 'Country','Date of Birth','Gender','Ethnicity','Payment Method','On Study Date','County Code','Study Site', 'nine','Disease Code','end']]


#=====================STEP 3 Prepare data for Text files=============
#need to seperate the data into trials for the main df and the RACE df
list_of_trials = []
for _, g in main.groupby(main['NCI ID']):
    list_of_trials.append(g)
    
list_of_race= []
for _, g in race.groupby(race['NCI ID']):
    list_of_race.append(g)

#pull and sort the trial names to do file naming and trace/organize the data
trials_name=sorted(list(ctrp['NCI ID'].unique()))
                  





#definition to add quotation to strings because that is requied 
#but omit empty columns (place holders) and columns with comma places holders as well

def foo(s1):
    if s1=='' or ',' in s1:
        return s1
    else:
        return '"%s"' % s1

#turn all the dfs into a list of lists INSTEAD of a list of dfs
masterstring=[]           
for trials in list_of_trials:
    df_trial = trials.astype(str).values.tolist()
    masterstring.append(df_trial)
    
master_race=[]           
for race in list_of_race:
    df_race = race.astype(str).values.tolist()
    master_race.append(df_race)

# download re library which has regex for python
#regex is using symbols to slice/read through text - [hard to understand; I only know basics rn]    
    
import re
#loop through trial numbers
for ind, name in enumerate(trials_name):
    #set up the files names with date (instruction from CTRP) and make sure to write into file
    file=open('{}_20211014.txt'.format(name),"w")
    file.write('"COLLECTIONS"'+','+'"{}"'.format(name)+ ','*9 +'"1"')
    # this means 'enter' move to new line
    file.write('\n')
    for ind2, li in enumerate(masterstring):
        #making sure its the same trial as name with index not by string (error prone but works for now)
        if ind==ind2:
            for li2 in li:
                string_test=str()
                for string in li2:
                    #using definition here to add the quotations
                    string1 = foo(string)
                    string_test = string_test+string1+','
                file.write(string_test)
                file.write('\n')
    for ind3, zi in enumerate(master_race):
        if ind3==ind:
            for zi2 in zi:
                string_race=str()
                for race_string in zi2:
                    race_string1=foo(race_string)
                    string_race = string_race + race_string1 + ','
                #strip that last comm o fthe line before saving
                string_race = string_race.rstrip(',')
                file.write(string_race)
                file.write('\n')
    file.close()
                            
            
           

