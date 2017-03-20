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
    bad_date_list = []
    for i in list_indi:
        if(i[3] > curr_date):
            bad_date_list.append(i[3])
            print("US01: The Birth Date " + i[3] + " of Individual " + i[0] + " occurs before the current date.")
        if(i[4] != 0):
            if(i[4] > curr_date):
                bad_date_list.append(i[4])
                print("US01: The Death Date " + i[4] + " of Individual " + i[0] + " occurs before the current date.")
    for i in list_fam:
        if(i[3] > curr_date):
            bad_date_list.append(i[3])
            print("US01: The Marriage Date " + i[3] + " of Family " + i[0] + " occurs before the current date.")
        if(i[4] != 0):
            if(i[4] > curr_date):
                bad_date_list.append(i[4])
                print("US01: The Divorce Date " + i[4] + " of Family " + i[0] + " occurs before the current date.")
    if(len(bad_date_list) == 0):
        print("US01: All the Dates are before the current date.")
        print()
    else:
        print("US01: The following Date(s) occur after the current date: ", end = '')
        print(bad_date_list)
        print()

def getBirthDateByID(list_indi, id):
    for i in list_indi:
        if(i[0] == id):
            return i[3]

def BirthBeforeMarr(list_indi, list_fam):
    bad_list = []
    for i in list_indi:
        birth_date = i[3]
        if(i[5] != []):
            for j in i[5]:
                if(birth_date > getMarrDateByID(list_fam, j)):
                    bad_list.append(i[0])
                    print("US02: The Individual " + i[0] + " has Birth Date occuring after his/her Marriage Date.")
                    break
    if(len(bad_list) == 0):
        print("US02: All the Individuals have their Birth Dates occuring before their respective Marriage Dates.")
        print()
    else:
        print("US02: The following Individual(s) have their Birth Dates occuring after their respective Marriage Dates: ", end = '')
        print(bad_list)
        print()

def noBigamy(list_indi, list_fam):
    bad_list = []
    for i in list_indi:
        temp_fam = []
        temp = []
        if(len(i[5]) > 1):
            self_id = i[0]
            for j in i[5]:
                temp.append(getMarrDateByID(list_fam, j))
                temp.append(j)
                temp.append(getSpouseByID(list_fam, j, self_id))
                temp.append(getDivDateByID(list_fam, j))
                temp.append(getDeathDateByID(list_indi, getSpouseByID(list_fam, j, self_id)))
                temp_fam.append(temp)
                temp = []
            temp_fam.sort()
            for k in range(1, len(temp_fam)):
                if(temp_fam[k-1][3] == None and temp_fam[k-1][4] == None):
                    bad_list.append(self_id)
                    print("US11: The Individual " + self_id + " is married to Individual " + temp_fam[k][2] + " in Family " + temp_fam[k][1] + " while still married to Individual " + temp_fam[k-1][2] + " in Family " + temp_fam[k-1][1] + ".")
                else:
                    if(temp_fam[k-1][3] != None):
                        if(temp_fam[k][0] < temp_fam[k-1][3]):
                            bad_list.append(self_id)
                            print("US11: The Individual " + self_id + " is married to Individual " + temp_fam[k][2] + " in Family " + temp_fam[k][1] + " before divorcing spouse " + temp_fam[k-1][2] + " in Family " + temp_fam[k-1][1] + ".")
                    if(temp_fam[k-1][4] != None):
                        if(temp_fam[k][0] < temp_fam[k-1][4]):
                            bad_list.append(self_id)
                            print("US11: The Individual " + self_id + " is married to Individual " + temp_fam[k][2] + " in Family " + temp_fam[k][1] + " before the death of spouse " + temp_fam[k-1][2] + " in Family " + temp_fam[k-1][1] + ".")
    if(len(bad_list) == 0):
        print("US11: No Individual is involved in any kind of Bigamy.")
        print()
    else:
        print("US11: The following Individual(s) are involved in Bigamy: ", end = '')
        print(bad_list)
        print()

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
    bad_list = []
    for i in list_fam:
        if(getMarrAgeByID(list_indi, i[1], i[3])<14):
            bad_list.append(i[1])
            print("US10: The Individual " + i[1] + " married before turning 14 years of age in family " + i[0] + ".")
        if(getMarrAgeByID(list_indi, i[2], i[3])<14):
            bad_list.append(i[2])
            print("US10: The Individual " + i[2] + " married before turning 14 years of age in family " + i[0] + ".")
    if(len(bad_list) == 0):
        print("US10: No Individual married before turning 14 years of age.")
        print()
    else:
        print("US10: The following Individual(s) married before turning 14 years of age: ", end = '')
        print(bad_list)
        print()

def getMarrAgeByID(list_indi, id, marr_date):
    temp = marr_date.split('-')
    marr_year = int(temp[0])
    marr_month = int(temp[1])
    marr_date = int(temp[2])
    for i in list_indi:
        if(i[0] == id):
            birth_date = i[3]
    temp = birth_date.split('-')
    birth_year = int(temp[0])
    birth_month = int(temp[1])
    birth_date = int(temp[2])
    return marr_year - birth_year - ((marr_month, marr_date) < (birth_month, birth_date))

def getAgeByID(list_indi, id):
    dead_flag = 0
    for i in list_indi:
        if(i[0] == id):
            birth_date = i[3]
            temp = birth_date.split('-')
            birth_year = int(temp[0])
            birth_month = int(temp[1])
            birth_date = int(temp[2])
            if(i[4] != 0):
                death_date = i[4]
                dead_flag = 1
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
    bad_list = []
    for i in list_fam:
        if(getSexByID(list_indi, i[1]) != 'M'):
            bad_list.append(i[1])
            print("US21: The Individual " + i[1] + " in family " + i[0] + " has incorrect Gender role.")
        if(getSexByID(list_indi, i[2]) != 'F'):
            bad_list.append(i[2])
            print("US21: The Individual " + i[2] + " in family " + i[0] + " has incorrect Gender role.")
    if(len(bad_list) == 0):
        print("US21: The Individuals in all the Families have correct gender roles.")
        print()
    else:
        print("US21: The following Individual(s) have incorrect gender role: ", end = '')
        print(bad_list)
        print()

def getSexByID(list_indi, id):
    for i in list_indi:
        if(i[0] == id):
            return i[2]

def UniqueID(list_indi, list_fam):
    indi_id_list = []
    fam_id_list = []
    dup_iid_list = []
    dup_fid_list = []
    flag = 0
    for i in list_indi:
        indi_id_list.append(i[0])
    for i in list_fam:
        fam_id_list.append(i[0])
    if(len(indi_id_list) == len(set(indi_id_list)) and len(fam_id_list) == len(set(fam_id_list))):
        print("\nUS22: All the IDs are unique.")
        print()
    else:
        for i in indi_id_list:
            flag = 0
            for j in indi_id_list:
                if (i == j):
                    flag += 1
                    if(flag > 1):
                        dup_iid_list.append(i)
        for i in fam_id_list:
            flag = 0
            for j in fam_id_list:
                if (i == j):
                    flag += 1
                    if(flag > 1):
                        dup_fid_list.append(i)
        if(len(dup_iid_list) != 0):
            print("\nUS22: The following Individual ID(s) have been duplicated: ", end = '')
            print(set(dup_iid_list))
            print()
        if(len(dup_fid_list) != 0):
            print("US22: The following Family ID(s) have been duplicated: ", end = '')
            print(set(dup_fid_list))
            print()

def BirthBeforeDeath(list_indi):
    bad_list= []
    for i in list_indi:
        if(i[4] != 0):
            if(i[3] > i[4]):
                bad_list.append(i[0])
                print("US03: The Individual " + i[0] + " has his/her Birth date occuring after the Death date.")
    if(len(bad_list) == 0):
        print("US03: All the Individuals have their Birth dates occuring before their Death dates.")
        print()
    else:
        print("US03: The following Individual(s) have their Birth dates occuring after their Death dates: ", end = '')
        print(bad_list)
        print()

def MarrBeforeDiv(list_fam):
    bad_list = []
    for i in list_fam:
        if(i[4] != 0):
            if(i[3] > i[4]):
                bad_list.append(i[0])
                print("US04: The Family " + i[0] + " has Marriage date occuring after the Divorce date.")
    if(len(bad_list) == 0):
        print("US04: All the Families have their Marriage dates occuring before their Divorce dates.")
        print()
    else:
        print("US04: The following Family(s) have their Marriage dates occuring after their Divorce dates: ", end = '')
        print(bad_list)
        print()

def list_deceased(list_indi):
    """ US29 - List the deceased individuals """
    deceased = []
    for individual in list_indi:
        if individual[4] is not 0:
            deceased.append(individual[0])
    print("US29: List of Deceased individuals is : ", deceased)
    print()

def list_living_married(list_indi, list_fam):
    """ US30 - List the living married people """
    living_married = []
    for i in list_fam:
        if(getDeathDateByID(list_indi, i[1]) == None):
            if(i[1] not in living_married):
                living_married.append(i[1])
        if(getDeathDateByID(list_indi, i[2]) == None):
            if(i[2] not in living_married):
                living_married.append(i[2])
    print ("US30: List of Living Married Individuals", living_married)
    print()

def birthBeforeDeathOfParents(list_indi, list_fam):
    bad_data_list = []
    for i in list_fam:
        if(i[5] != []):
            for j in i[5]:
                child_birth_date = getBirthDateByID(list_indi, j)
                if(getDeathDateByID(list_indi, i[2]) != None):
                    mother_death_date = getDeathDateByID(list_indi, i[2])
                    if(child_birth_date > mother_death_date):
                        bad_data_list.append(j)
                        print("US09: The child " + j + " was born after the death of his/her mother " + i[2] + ".")
                if(getDeathDateByID(list_indi, i[1]) != None):
                    father_month_diff = diff_months(child_birth_date, getDeathDateByID(list_indi, i[1]))
                    if(father_month_diff > 9):
                        bad_data_list.append(j)
                        print("US09: The child " + j + " was born 9 months after the death of his/her father " + i[1] + ".")
    if(len(bad_data_list) == 0):
        print("US09: All children were born before the deaths of their parents without any data flaws.")
        print()
    else:
        print("US09: The following children have their birth date flawed as per the death date of their parents: ", end = '')
        print(bad_data_list)
        print()

def diff_months(date1, date2):
    temp1 = date1.split('-')
    temp2 = date2.split('-')
    ndate1 = datetime.date(int(temp1[0]), int(temp1[1]), int(temp1[2]))
    ndate2 = datetime.date(int(temp2[0]), int(temp2[1]), int(temp2[2]))
    return int((ndate1 - ndate2).days / 30.4)

def parentsNotTooOld(list_indi, list_fam):
    bad_data_list = []
    for i in list_fam:
        if(i[5] != []):
            mother_age = getAgeByID(list_indi, i[2])
            father_age = getAgeByID(list_indi, i[1])
            for j in i[5]:
                child_age = getAgeByID(list_indi, j)
                if(mother_age - child_age >= 60):
                    bad_data_list.append(i[2])
                    print("US12: The mother " + i[2] + " is 60 years or more older than her child " + j + ".")
                if(father_age - child_age >= 80):
                    bad_data_list.append(i[1])
                    print("US12: The father " + i[1] + " is 80 years or more older than her child " + j + ".")
    if(len(bad_data_list) == 0):
        print("US12: None of the parents are too old.")
        print()
    else:
        print("US12: The following parents are too old compared to their children: ", end = '')
        print(bad_data_list)
        print()

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
    UniqueID(list_indi, list_fam)
    DatesBeforeCurrDate(list_indi, list_fam)
    BirthBeforeMarr(list_indi, list_fam)
    NoMarriageBefore14(list_indi, list_fam)
    CorrectGenderRoles(list_indi, list_fam)
    noBigamy(list_indi, list_fam)
    BirthBeforeDeath(list_indi)
    MarrBeforeDiv(list_fam)
    list_deceased(list_indi)
    list_living_married(list_indi, list_fam)
    birthBeforeDeathOfParents(list_indi, list_fam)
    parentsNotTooOld(list_indi, list_fam)

main('testGEDCOMFile_IncorrectData.ged')