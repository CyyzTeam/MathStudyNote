import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

# 中文乱码和坐标轴负号的处理
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
 
class image:
    def __init__(self, data_path = "data\附件1_数据清洗.xlsx"):
        self.data_path = data_path

        self.data_df = None
        self.init()
    
    def init(self):
        self.read_data()
        self.sum_profit_pie()

    def read_data(self):
        self.data_df = pd.read_excel(self.data_path)

    def sum_profit_pie(self):
        index = 0
        plt.figure(figsize=(7,7))
        #figure, ax = plt.subplots(1,2)
        for name,group in self.data_df.groupby(["是否违约"]):

            profit = group["总利润"]
            
            max_profit = profit.max()
            min_profit = profit.min()

            num_interval = 5
            interval_profit = (max_profit - min_profit) / num_interval
            print(interval_profit)
            pie_dict = dict()
            total = 0
            for i_profit in profit:
                for i in range(num_interval):
                    if i not in pie_dict:
                        pie_dict[i] = 0
                    if i_profit > min_profit + interval_profit * i and i_profit < min_profit + interval_profit * (i+1):
                            pie_dict[i] += 1
                            total += 1
                        
                            
            
            labels = []
            for i in range(num_interval):
                if pie_dict[i] != 0:
                    pie_dict[i] /= total
                    min_dis = min_profit + interval_profit * i
                    max_dis = max_profit + interval_profit * (i+1)
                    labels.append("[" + str(int(min_dis)) + "," +  str(int(max_dis)) + "]")
                    #labels.append(i)

            sizes = []
            print(pie_dict)
            for i in range(num_interval):
                if pie_dict[i] != 0:
                    sizes.append(pie_dict[i])

            #ax[0][0].axes(aspect='equal')
            #ax[0][1].axes(aspect='equal')

            '''
            ax[index].pie(
                x = sizes,
                labels = labels,
                autopct='%3.1f%%',
                #pctdistance = 0.8,
                labeldistance = 1,
                radius = 1.15, # 设置饼图的半径
            )
            '''
            
            plt.barh(y = labels , width = sizes)
            #ax[index].legend()
            #ax[index].legend(loc = 'lower left')
            index += 1
           
        plt.show()



        


if __name__ == "__main__":
    img = image()

    

        