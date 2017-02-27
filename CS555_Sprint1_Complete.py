# -*- coding: utf-8 -*-
"""Created on Sun Feb 12 01:22:22 2017@author: Kunal"""

"""
Format for Individual = [ID, Full Name, Sex, Birth Date, Death Date, Family ID list where Spouse, Family ID list where Child]
Format for Family = [ID, Husband ID, Wife ID, Marriage Date, Divorce Date, List of Children IDs]
"""

import datetime

"""This function creates a new list for an individual"""
def indi_list():
    op_list = [0 for i in range(7)]
    op_list[5] = []
    return op_list

"""This function creates a new list for a family"""
def fam_list():
    op_list = [0 for i in range(6)]
    op_list[5] = []
    return op_list

"""This function takes input '/Last_Name/' and returns 'Last_Name' as output (removes the slashes in .ged file)"""
def getLastName(str):
    temp=''
    for i in str:
        if(i != '/'):
            temp += i
    return temp

"""This function prints the contents of the input list"""
def print_list(ip_list):
    print("\n")
    for i in ip_list:
        print(i)

"""This function returns the Current Date"""
def getCurrDate():
    curr_date = str(datetime.date.today())
    return curr_date

"""This function converts the Date Format from '2000 JAN 5' to '2000-01-05' while parsing"""
def convertDateFormat(date):
    temp = date.split()
    if(temp[1] == 'JAN'): temp[1] = '01';
    if(temp[1] == 'FEB'): temp[1] = '02';
    if(temp[1] == 'MAR'): temp[1] = '03';
    if(temp[1] == 'APR'): temp[1] = '04';
    if(temp[1] == 'MAY'): temp[1] = '05';
    if(temp[1] == 'JUN'): temp[1] = '06';
    if(temp[1] == 'JUL'): temp[1] = '07';
    if(temp[1] == 'AUG'): temp[1] = '08';
    if(temp[1] == 'SEP'): temp[1] = '09';
    if(temp[1] == 'OCT'): temp[1] = '10';
    if(temp[1] == 'NOV'): temp[1] = '11';
    if(temp[1] == 'DEC'): temp[1] = '12';
    if(temp[2] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']):
        temp[2] = '0' + temp[2]
    return (temp[0] + '-' + temp[1] + '-' + temp[2])

"""This function returns True if all the Dates are before the Current Date, otherwise returns False"""
def DatesBeforeCurrDate(list_indi, list_fam):
    curr_date = getCurrDate()
    for i in list_indi:
        if(i[3] > curr_date):
            return False
        if(i[4] != 0):
            if(i[4] > curr_date):
                return False
    for i in list_fam:
        if(i[3] > curr_date):
            return False
        if(i[4] != 0):
            if(i[4] > curr_date):
                return False
    return True

def getBirthDateByID(list_indi, id):
    for i in list_indi:
        if(i[0] == id):
            return i[3]

def BirthBeforeMarr(list_indi, list_fam):
    for i in list_fam:
        marr_date = i[3]
        if(getBirthDateByID(list_indi, i[1]) > marr_date):
            return False
        if(getBirthDateByID(list_indi, i[2]) > marr_date):
            return False
    return True

def noBigamy(list_indi, list_fam):
    for i in list_indi:
        temp_fam = []
        temp = []
        if(len(i[5]) > 1):
            no_of_fam = len(i[5])
            self_id = i[0]
            for j in i[5]:
                temp.append(getMarrDateByID(list_fam, j))
                temp.append(j)
                temp.append(getSpouseByID(list_fam, j, self_id))
                temp_fam.append(temp)
                temp = []
        temp_fam.sort()
        for k in range(1,len(temp_fam)):
            if(temp_fam[k][0] <= temp_fam[k-1][0]):
                return False
            if(getDivDateByID(list_fam, temp_fam[k-1][1]) != None):
                if(temp_fam[k][0] < getDivDateByID(list_fam, temp_fam[k-1][1])):
                    return False
            if(getDeathDateByID(list_indi, temp_fam[k-1][2]) != None):
                if(temp_fam[k][0] < getDeathDateByID(list_indi, temp_fam[k-1][2])):
                    return False
    return True

def getMarrDateByID(list_fam, id):
    for i in list_fam:
        if(i[0] == id):
            return i[3]

def getSpouseByID(list_fam, fam_id, sp_id):
    for i in list_fam:
        if(i[0] == fam_id):
            if(i[1] == sp_id):
                return i[2]
            if(i[2] == sp_id):
                return i[1]

def getDivDateByID(list_fam, id):
    for i in list_fam:
        if(i[0] == id):
            if(i[4] != 0):
                return i[4]

def getDeathDateByID(list_indi, id):
    for i in list_indi:
        if(i[0] == id):
            if(i[4] != 0):
                return i[4]

def NoMarriageBefore14(list_indi, list_fam):
    for i in list_fam:
        if(getAgeByID(list_indi, i[1])<14 or getAgeByID(list_indi, i[2])<14):
            return False
    return True

def getAgeByID(list_indi, id):
    dead_flag = 0
    for i in list_indi:
        if(i[0] == id):
            birth_date = i[3]
            if(i[4] != 0):
                death_date = i[4]
                dead_flag = 1
    temp = birth_date.split('-')
    birth_year = int(temp[0])
    birth_month = int(temp[1])
    birth_date = int(temp[2])
    if(dead_flag == 1):
        temp = death_date.split('-')
        death_year = int(temp[0])
        death_month = int(temp[1])
        death_date = int(temp[2])
        return death_year - birth_year - ((death_month, death_date) < (birth_month, birth_date))
    curr_date = getCurrDate().split('-')
    curr_year = int(curr_date[0])
    curr_month = int(curr_date[1])
    curr_date = int(curr_date[2])
    return curr_year - birth_year - ((curr_month, curr_date) < (birth_month, birth_date))

def CorrectGenderRoles(list_indi, list_fam):
    for i in list_fam:
        if(getSexByID(list_indi, i[1]) != 'M'):
            return False
        if(getSexByID(list_indi, i[2]) != 'F'):
            return False
    return True

def getSexByID(list_indi, id):
    for i in list_indi:
        if(i[0] == id):
            return i[2]

def UniqueID(list_indi, list_fam):
    indi_id_list = []
    fam_id_list = []
    for i in list_indi:
        indi_id_list.append(i[0])
    for i in list_fam:
        fam_id_list.append(i[0])
    if(len(indi_id_list) != len(set(indi_id_list))):
        return False
    if(len(fam_id_list) != len(set(fam_id_list))):
        return False
    return True

"""This function parses the GEDCOM File and returns 2 lists: one for individuals and another for families"""
def parse(file_name):
    f = open(file_name,'r')
    indi_on = 0
    fam_on = 0
    list_indi = []
    list_fam = []
    indi = indi_list()
    fam = fam_list()
    for line in f:
        str = line.split()
        if(str != []):
            if(str[0] == '0'):
                if(indi_on == 1):
                    list_indi.append(indi)
                    indi = indi_list()
                    indi_on = 0
                if(fam_on == 1):
                    list_fam.append(fam)
                    fam = fam_list()
                    fam_on = 0
                if(str[1] in ['NOTE', 'HEAD', 'TRLR']):
                    pass
                else:
                    if(str[2] == 'INDI'):
                        indi_on = 1
                        indi[0] = (str[1])
                    if(str[2] == 'FAM'):
                        fam_on = 1
                        fam[0] = (str[1])
            if(str[0] == '1'):
                if(str[1] == 'NAME'):
                    indi[1] = str[2] + " " + getLastName(str[3])
                if(str[1] == 'SEX'):
                    indi[2] = str[2]
                if(str[1] in ['BIRT', 'DEAT', 'MARR', 'DIV']):
                    date_id = str[1]
                if(str[1] == 'FAMS'):
                    indi[5].append(str[2])
                if(str[1] == 'FAMC'):
                    indi[6] = str[2]
                if(str[1] == 'HUSB'):
                    fam[1] = str[2]
                if(str[1] == 'WIFE'):
                    fam[2] = str[2]
                if(str[1] == 'CHIL'):
                    fam[5].append(str[2])
            if(str[0] == '2'):
                if(str[1] == 'DATE'):
                    date = str[4] + " " + str[3] + " " + str[2]
                    if(date_id == 'BIRT'):
                        indi[3] = convertDateFormat(date)
                    if(date_id == 'DEAT'):
                        indi[4] = convertDateFormat(date)
                    if(date_id == 'MARR'):
                        fam[3] = convertDateFormat(date)
                    if(date_id == 'DIV'):
                        fam[4] = convertDateFormat(date)
    return list_indi, list_fam

def main(file_name):
    list_indi, list_fam = parse(file_name)
    list_indi.sort()
    list_fam.sort()
    print_list(list_indi)
    print_list(list_fam)
    if(UniqueID(list_indi, list_fam)):
        print("\nAll the IDs for the Individuals and the Families are Unique.")
    else:
        print("\nOne or more IDs for the Individuals or the Families are not Unique.")
    if(DatesBeforeCurrDate(list_indi, list_fam)):
        print("\nAll the Dates are before the Current Date.")
    else:
        print("\nOne or more Dates are not before the Current Date.")
    if(BirthBeforeMarr(list_indi, list_fam)):
        print("\nAll the Birth Dates are before the respective Marriage Dates")
    else:
        print("\nOne or more Birth Dates are not before their respective Marriage Date.")
    if(NoMarriageBefore14(list_indi, list_fam)):
        print("\nNobody married before turning at least 14 years of age.")
    else:
        print("\nOne or more persons married before turning 14 years of age.")
    if(CorrectGenderRoles(list_indi, list_fam)):
        print("\nThe gender roles in all the families are correct.")
    else:
        print("\nOne or more families have incorrect gender roles.")
    if(noBigamy(list_indi, list_fam)):
        print("\nThere is no Bigamy among the Families.")
    else:
        print("\nOne or more families have Bigamy.")

main('testGEDCOMFile.ged')