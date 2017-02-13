# -*- coding: utf-8 -*-
"""Created on Sun Feb 12 01:22:22 2017@author: Kunal"""

def file_len(f):
    for i,l in enumerate(f):
        pass
    return i+1

file_name = 'KunalDhaimade_Project-01.ged'
f = open(file_name,'r')
f_len = file_len(open(file_name))
print("\n")
cur_line =  0
for line in f:
    cur_line += 1
    str = line.split()
    if(str != []):
        if(cur_line!=f_len):
            print(line, end='')
        else:
            print(line)
        if(str[0] == '0'):
            print("Level Number: "+str[0])
            if(str[1] in ['NOTE', 'HEAD', 'TRLR']):
                print("Tag: "+str[1]+"\n")
            else:
                if(str[2] in ['INDI', 'FAM']):
                    print("Tag: "+str[2]+"\n")
                else:
                    print("Invalid Tag\n")
        if(str[0] == '1'):
            print("Level Number: "+str[0])
            if(str[1] in ['NAME', 'SEX', 'BIRT', 'DEAT', 'MARR', 'DIV', 'FAMS', 'FAMC', 'HUSB', 'WIFE', 'CHIL']):
                print("Tag: "+str[1]+"\n")
            else:
                print("Invalid Tag\n")
        if(str[0] == '2'):
            print("Level Number: "+str[0])
            if(str[1] == 'DATE'):
                print("Tag: "+str[1]+"\n")
            else:
                print("Invalid Tag\n")
