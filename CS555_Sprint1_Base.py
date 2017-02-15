# -*- coding: utf-8 -*-
"""Created on Sun Feb 12 01:22:22 2017@author: Kunal"""

"""
Format for Individual = [ID, Full Name, Sex, Birth Date, Death Date, Family ID list where Spouse, Family ID list where Child]
Format for Family = [ID, Husband ID, Wife ID, Marriage Date, Divorce Date, List of Children IDs]
"""

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

"""This function parses the GEDCOM File and returns 2 lists: one for individuals and another for families"""
def parse(file_name):
    f = open(file_name,'r')
    f_len = file_len(open(file_name))
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
                        indi[3] = date
                    if(date_id == 'DEAT'):
                        indi[4] = date
                    if(date_id == 'MARR'):
                        fam[3] = date
                    if(date_id == 'DIV'):
                        fam[4] = date
    return list_indi, list_fam

def main(file_name):
    list_indi, list_fam = parse(file_name)
    list_indi.sort()
    list_fam.sort()
    print_list(list_indi)
    print_list(list_fam)

main('testGEDCOMFile.ged')