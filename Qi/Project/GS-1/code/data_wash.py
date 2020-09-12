import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time


class data_wash:
    def __init__(self, data_path = "data\附件1：123家有信贷记录企业的相关数据.xlsx"):
        # 数据路径
        self.data_path = data_path

        # 读取三张基表
        self.company_df = None
        self.in_pro = None
        self.out_pro = None

        # 是否一附件
        if self.data_path.split("：")[0] == "data\附件1":
            print("附件1")
            self.is_data_1 = True
        
        else:
            self.is_data_1 = False

        self.init()
        
    def init(self):
        self.read_data()
        self.cal_season_mean()


    def read_data(self):
        self.company_df = pd.read_excel(self.data_path, sheet_name = "企业信息")
        self.in_pro = pd.read_excel(self.data_path, sheet_name = "进项发票信息")
        self.out_pro = pd.read_excel(self.data_path, sheet_name = "销项发票信息")
    

    def cal_season_mean(self):

        season_1 = ["01","02","03"]
        season_2 = ["04","05","06"]
        season_3 = ["07","08","09"]
        season_4 = ["10","11","12"]

        new_excel = dict()
        for i in range(2):
            print(i)
            # 进项/出项
            if i == 0:
                sheet_pro = self.in_pro
            else:
                sheet_pro = self.out_pro
           
            # 有效票
            company_in_valid = sheet_pro[sheet_pro["发票状态"].str.contains("有效发票")]

            
            # 对进项的数据按公司进行分组，并分别计算季度，总金额等
            for name, group in company_in_valid.groupby(["企业代号"]):
                print(name)
                in_sum_money = group["金额"].sum()
                in_tax_sum_money = group["税额"].sum()

                # 总金额除以季度数
                mean_sum_money = 0
                mean_sum_tax   = 0

                # 数据包含的季度数
                num_season = 0

                # 包含的季度数
                sea_contain = []

                # 新表格的列
                excel_i_col = dict()

                # 计算税收和进项/出项的季度平均
                for index, row in group.iterrows():
                    #print(row["开票日期"])
                    month = datetime.strptime(str(row["开票日期"]), '%Y-%m-%d %H:%M:%S').strftime('%m')
                    year  = datetime.strptime(str(row["开票日期"]), '%Y-%m-%d %H:%M:%S').strftime('%Y')

                    if month in season_1:
                        str_con = str(year) + "_1"
                        if str_con not in sea_contain:
                            sea_contain.append(str_con)
                    
                    if month in season_2:
                        str_con = str(year) + "_2"
                        if str_con not in sea_contain:
                            sea_contain.append(str_con)

                    if month in season_3:
                        str_con = str(year) + "_3"
                        if str_con not in sea_contain:
                            sea_contain.append(str_con)
                    
                    if month in season_4:
                        str_con = str(year) + "_4"
                        if str_con not in sea_contain:
                            sea_contain.append(str_con)
                
                num_season = len(sea_contain)
                if num_season > 0:
                    mean_sum_money = in_sum_money / num_season
                    mean_sum_tax   = in_tax_sum_money / num_season
                
                if i == 0:
                    if self.is_data_1:
                        excel_i_col["信誉评级"] = self.company_df[self.company_df["企业代号"].isin([name])]["信誉评级"].values[0]
                        excel_i_col["是否违约"] = self.company_df.loc[self.company_df["企业代号"] == name]["是否违约"].values[0]

                    # 进项总金额
                    excel_i_col["进项总金额"]      = in_sum_money

                    # 进项总税收
                    excel_i_col["进项总税收"]      = in_tax_sum_money

                    # 进项平均季度
                    excel_i_col["进项季度平均金额"] = mean_sum_money

                    # 进项平均季度税收
                    excel_i_col["进项季度平均税收"] = mean_sum_tax

                    # 进项的季度数
                    excel_i_col["进项季度总数"] = num_season

                    
                    new_excel[name] = excel_i_col
                
                else :
                    new_excel[name]["销项总金额"] = in_sum_money

                    new_excel[name]["销项总税收"] = in_tax_sum_money

                    new_excel[name]["销项季度平均金额"] = mean_sum_money

                    new_excel[name]["销项季度平均税收"] = mean_sum_tax

                    new_excel[name]["销项季度总数"] = num_season

                    new_excel[name]["总利润"] = new_excel[name]["销项总金额"] - new_excel[name]["进项总金额"]
                    
                    new_excel[name]["季度平均利润"] = new_excel[name]["销项季度平均金额"] - new_excel[name]["进项季度平均金额"]
                


        excel_save = pd.DataFrame(new_excel).T

        save_path = self.data_path.strip().split("：")[0]
        save_path += "_数据清洗.xlsx"
        excel_save.to_excel(save_path)
            
                
if __name__ == "__main__":
    ana = data_wash(data_path="data\附件2：302家无信贷记录企业的相关数据.xlsx")
    #excel_i_col = dict()
    
    #company_df = pd.read_excel("data\附件1：123家有信贷记录企业的相关数据.xlsx", sheet_name = "企业信息")
    #excel_i_col = company_df.loc[company_df["企业代号"].isin(["E11"])]["信誉评级"]
    #print(excel_i_col.values[0])
    '''
    a = '2020-05-08 10:55:00'
    b = datetime.strptime(a, '%Y-%m-%d %H:%M:%S').strftime('%m')
    print(b)
    '''