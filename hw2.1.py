# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 12:40:19 2020

@author: Bryce Benjamin
"""

    
#function will slice the strings and place them into variables. Variables will then be printed to corresponding headers

#function will create and output the type B records
def create_B_record(line, fout):
    futures_code =  line[5:8]
    contract_type = line[15:18]
    contract_month = line[18:24]
    contract_month = int(contract_month)
    
    future_exp_date = line[91:99]
    options_exp_date = ''
    options_code = " "
    #only take in records after 202011 and before 202312
    if (contract_month >= 202011 and contract_month <= 202312):
        if(contract_type == "FUT"):
            contract_type = "Fut"
            contract_month = str(contract_month)
            contract_month = contract_month[0:4] + '-' + contract_month[4:]
            future_exp_date = future_exp_date[0:4] + '-' + future_exp_date[4:6] + '-' + future_exp_date[6:]
           
        elif(contract_type == "OOF"):
            contract_type = "Opt"
            contract_month = str(contract_month)
            contract_month = contract_month[0:4] + '-' + contract_month[4:]
            future_exp_date = future_exp_date[0:4] + '-' + future_exp_date[4:6] + '-' + future_exp_date[6:]

            
        if(futures_code == 'CL '):
            futures_code = "CL"
            fout.write("{:10s}{:10s}{:10s}{:10s}{:10s}{:10s}\n".format(futures_code, contract_month, contract_type, future_exp_date, options_code, options_exp_date))
        elif(futures_code == 'LO '):
            options_code = futures_code
            futures_code = "CL"
            options_exp_date = future_exp_date
            future_exp_date = ''
            fout.write("{:10s}{:10s}{:10s}{:10s}{:10s}{:10s}\n".format(futures_code , contract_month, contract_type, future_exp_date, options_code, options_exp_date))
    else:
        return
    
#function will parse and output the 81 records
def create_81_record(line, fout):
    product_code = line[0]
    futures_code =  line[5:8]
    contract_type = line[25:29]
    contract_month = line[29:35]
    strike_price = line[47:54]
    settlement_price = line[108:122]
    contract_month = int(contract_month)
    #only take in records after 2020-11 and before 2023-12
    
    if (contract_month >= 202011 and contract_month  <= 202312):
        if(contract_type == "FUT " or contract_type == "OOFP" or contract_type == "OOFC"):
            contract_month = str(contract_month)
            contract_month = contract_month[0:4] + '-' + contract_month[4:]
            #seperating if it is a option contract or a future contract. If a option contract, will be either a call or put type.
            if(contract_type == "OOFP" or contract_type == "OOFC"):
                
                if(contract_type[3] == "C"):
                    contract_type = "Call"
                    strike_price = float(strike_price)
                    strike_price /= 1000.0 #could be divide by a 100
                    strike_price *= 10.0
                    
                    settlement_price = float(settlement_price)
                    settlement_price /= 100000.0
                    settlement_price *= 1000
                  
                    if(futures_code == "CL "):
                        fout.write("{:10s}{:10s}{:10s}{:<10.2f}{:<10.2f}\n".format(futures_code, contract_month, contract_type, strike_price, settlement_price))
                    elif(futures_code == "LO "):
                        futures_code = "CL"
                        fout.write("{:10s}{:10s}{:10s}{:<10.2f}{:<10.2f}\n".format(futures_code , contract_month, contract_type, strike_price, settlement_price))
               
                elif(contract_type[3] == "P"):
                    contract_type = "Put"
                    strike_price = float(strike_price)
                    strike_price /= 1000.0
                    strike_price *= 10.0
                    
                    settlement_price = float(settlement_price)
                    settlement_price /= 100000.0
                    settlement_price *= 1000
                    if(futures_code == "CL "):
                        fout.write("{:10s}{:10s}{:10s}{:<10.2f}{:<10.2f}\n".format(futures_code, contract_month, contract_type, strike_price, settlement_price))
                    elif(futures_code == "LO "):
                        futures_code = "CL"
                        fout.write("{:10s}{:10s}{:10s}{:<10.2f}{:<10.2f}\n".format(futures_code , contract_month, contract_type, strike_price, settlement_price))
               
            else:
                contract_type = "Fut"
                if (strike_price == "0000000"):
                    strike_price = ""
                    settlement_price = float(settlement_price)
                    settlement_price /= 100000.0
                    settlement_price *= 1000
                    if(futures_code == "CL "):
                        fout.write("{:10s}{:10s}{:10s}{:10s}{:<10.2f}\n".format(futures_code, contract_month, contract_type, strike_price, settlement_price))
                    elif(futures_code == "LO "):
                        futures_code = "CL"
                        fout.write("{:10s}{:10s}{:10s}{:10s}{:<10.2f}\n".format(futures_code , contract_month, contract_type, strike_price, settlement_price))
           
if __name__ == "__main__":
    #will output the header files and then create the tables by calling each function.

    with open('C:/Users/Bryce/Dropbox/Documents/Grad School/School Files/Courses/Data Focused Python/HW/HW2/cme.20200904.c.pa2/cme.20200904.c.pa2', 'rt', encoding = 'utf-8') as fin:
        with open('C:/Users\Bryce/Dropbox/Documents/Grad School/School Files/Courses/Data Focused Python/HW/HW2/CL_expirations_settlements', 'w', encoding = 'utf-8') as fout:
            header_line1 = "{:10s}{:10s}{:10s}{:10s}{:10s}{:<10s}".format("Futures","Contract","Contract","Futures","Options","Options")
            header_line2 = "{:10s}{:10s}{:10s}{:10s}{:10s}{:<10s}".format("Code", "Month", "Type", "Exp Date", "Code", "Exp Date")
            header_line3 = "{:10s}{:10s}{:10s}{:10s}{:10s}{:<10s}".format("--------", "--------", "--------", "--------", "--------", "--------")
            fout.writelines(header_line1)
            fout.write("\n")
            fout.writelines(header_line2)
            fout.write("\n")
            fout.writelines(header_line3)   
            fout.write("\n")
            for line in fin:
                #only take in lines of type B, NYM, and CL or LO
                if (line[0:2] == 'B ' and line[2:5] == 'NYM' and (line[5:15] == 'CL        ' or line[5:15] == 'LO        ') ):
                    create_B_record(line, fout)
                else:
                    continue
            
    
    with open('C:/Users/Bryce/Dropbox/Documents/Grad School/School Files/Courses/Data Focused Python/HW/HW2/cme.20200904.c.pa2/cme.20200904.c.pa2', 'rt', 
              encoding = 'utf-8') as fin:    
        with open('C:/Users\Bryce/Dropbox/Documents/Grad School/School Files/Courses/Data Focused Python/HW/HW2/CL_expirations_settlements', 'a', 
                  encoding = 'utf-8') as fout:
            header_line1 = "{:10s}{:10s}{:10s}{:10s}{:10s}".format("Futures","Contract","Contract","Strike","Settlement")
            header_line2 = "{:10s}{:10s}{:10s}{:10s}{:10s}".format("Code", "Month", "Type", "Price", "Price")
            header_line3 = "{:10s}{:10s}{:10s}{:10s}{:10s}".format("--------", "--------", "--------", "--------", "--------", "--------")
            fout.write(header_line1)
            fout.write("\n")
            fout.write(header_line2)
            fout.write("\n")
            fout.write(header_line3) 
            fout.write("\n")
            for line in fin:
                #only take in lines of type 81, NYM, and CL or LO. Functions also take in the file out files and the line as parameters.
                if (line[0:2] == "81" and line[2:5] == 'NYM' and (line[5:15] == 'CL        ' or line[5:15] == 'LO        ') ):
                    create_81_record(line, fout)
                else:
                   continue
    
