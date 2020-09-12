import pandas as pd
import numpy as np

moneys = [100000 , 300000 ,  500000, 700000]
align_money = [300000, 500000, 700000, 1000000]

profit_po = [i for i in np.arange(0.04, 0.16, 0.01)]
print(profit_po)
lend_data_1 = False
'''
平均客户流失率：y = 2.188+0.659*ln(x)

x为贷款年利率、y为客户流失率
A模型：y=2.239+0.669*ln(x)，R方为：0.982
B模型：y=2.158+0.651*ln(x)，R方为：0.988
C模型：y=2.168+0.659*ln(x)，R方为：0.992

y_i = [n_i * x * (1 - 信风) - n_i * 信风] *(1 - model)
'''
# 最多能借多少钱
max_money = 100000000
max_money_name = "1亿"

def cal_max_profit(risk,cred = "A"):
    i_mon = 0
    r_i  = 0
    r_po  = 0
    for index in range(len(moneys)):
        n_i = moneys[index]
        #print(index)
        for i_po in profit_po:
            y_i = 0
            if cred == "A":
                y_i = (n_i * i_po * (1 - risk) - n_i * risk) * (1 - (2.239+0.669*np.log(i_po)))
            elif cred == "B":
                y_i = (n_i * i_po * (1 - risk) - n_i * risk) * (1 - (2.158+0.651*np.log(i_po)))
            elif cred == "C":
                y_i = (n_i * i_po * (1 - risk) - n_i * risk) * (1 - (2.168+0.659*np.log(i_po)))
            elif cred == "Q":
                y_i = (n_i * i_po * (1 - risk) - n_i * risk) * (1 - (2.188+0.659*np.log(i_po)))
            
            if y_i > i_mon:
                i_mon = y_i
                r_i = index
                r_po = i_po

                
    #print(r_i)
    return i_mon, r_i, r_po
    

if lend_data_1:

    data_df = pd.read_excel("output/Q1_predict.xlsx")
    data_risk   = data_df["pred_possibility"]
    data_name   = data_df["name"]
    data_credit = data_df["credit"]
    max_lend_money = 0
    
    bank_profit = []
    every_company_lendmoney = []
    every_company_money_rate = []
    for index in range(len(data_name)):

        max_profit, n_index, possibility = cal_max_profit(data_risk[index], data_credit[index])
        max_lend_money += align_money[n_index]
        risk = data_risk[index]

        if risk <= 0.2:
            possibility *= (1 - risk)
        
        if possibility == 0:
            possibility = 0.04
        
        if risk > 0.65:
            every_company_lendmoney.append(0)
            every_company_money_rate.append(0)
        else:
            every_company_lendmoney.append(align_money[n_index])
            every_company_money_rate.append(possibility)
    
    if max_lend_money > max_money:
        sum_risk = data_risk.sum()
        for index in range(len(data_name)):
            if every_company_lendmoney[index] > 0:
                every_company_lendmoney[index] -= ((data_risk[index] / sum_risk) * (max_lend_money - max_money))
            
            if every_company_lendmoney[index] < 0:
                every_company_lendmoney[index] = 0
                every_company_money_rate[index] = 0

    else:
        print(max_lend_money)
    
    pd_len_money = dict()
    pd_len_money["name"] = data_name
    pd_len_money["最多可以借的钱"] = every_company_lendmoney
    pd_len_money["利率"] = every_company_money_rate

    pd_len_money = pd.DataFrame(pd_len_money)

    pd_len_money.to_excel("output/Q1-"+max_money_name+"各个公司可借的钱.xlsx")

else:

    data_df = pd.read_excel("output/Q2_predict.xlsx")
    data_risk   = data_df["pred_possibility"]
    data_name   = data_df["name"]

    max_lend_money = 0
    
    bank_profit = []
    every_company_lendmoney = []
    every_company_money_rate = []
    for index in range(len(data_name)):

        max_profit, n_index, possibility = cal_max_profit(data_risk[index], "Q")
        max_lend_money += align_money[n_index]
        risk = data_risk[index]
        if risk <= 0.2:
            possibility *= (1 - risk)
        
        if possibility == 0:
            possibility = 0.04
        
        if risk > 0.65:
            every_company_lendmoney.append(0)
            every_company_money_rate.append(0)
        else:
            every_company_lendmoney.append(align_money[n_index])
            every_company_money_rate.append(possibility)
    
    if max_lend_money > max_money:
        sum_risk = data_risk.sum()
        for index in range(len(data_name)):
            if every_company_lendmoney[index] > 0:
                every_company_lendmoney[index] -= ((data_risk[index] / sum_risk) * (max_lend_money - max_money))
            
            if every_company_lendmoney[index] < 0:
                every_company_lendmoney[index] = 0
                every_company_money_rate[index] = 0

    else:
        print(max_lend_money)
    
    pd_len_money = dict()
    pd_len_money["name"] = data_name
    pd_len_money["最多可以借的钱"] = every_company_lendmoney
    pd_len_money["利率"] = every_company_money_rate

    pd_len_money = pd.DataFrame(pd_len_money)

    pd_len_money.to_excel("output/Q2-"+max_money_name+"各个公司可借的钱.xlsx")




