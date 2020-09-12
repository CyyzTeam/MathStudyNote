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
        self.score_pie()
        #self.season_bar()
        #self.sum_profit_bar()
        #self.sum_tax_bar()

    def read_data(self):
        self.data_df = pd.read_excel(self.data_path)
    
    def score_pie(self):
        figure, ax = plt.subplots(1,2)
        for name,group in self.data_df.groupby(["是否违约"]):

            count = group.loc[:, "信誉评级"].value_counts()
            sum_count = count.sum()
            count = dict(count)

            labels = []
            sizes = []

            for key, value in count.items():
                labels.append(key)
                sizes.append(value/sum_count)
          
            if name == "否":
                ax[0].set_title("未违约信誉评级占比")
                ax[0].pie(
                    x = sizes,
                    labels = labels,
                    # 设置百分比的格式，这里保留一位小数
                    autopct='%.1f%%',
                    # 设置百分比标签与圆心的距离
                    pctdistance=0.8, 
                    # 设置教育水平标签与圆心的距离
                    labeldistance = 1.15, 
                    # 设置饼图的初始角度
                    startangle = 180, 
                )
            else:
                ax[1].set_title("违约信誉评级占比")
                ax[1].pie(
                    x = sizes,
                    labels = labels,
                    # 设置百分比的格式，这里保留一位小数
                    autopct='%.1f%%',
                    # 设置百分比标签与圆心的距离
                    pctdistance=0.8, 
                    # 设置教育水平标签与圆心的距离
                    labeldistance = 1.15, 
                    # 设置饼图的初始角度
                    startangle = 180, 
                )
        plt.show()

            


    def size_label(self, profit, bound = 10000):
        max_profit = profit.max()
        min_profit = profit.min()

        num_interval = 200
        interval_profit = (max_profit - min_profit) / num_interval
        print(interval_profit)
        pie_dict = dict()
        total = 0
        for i_profit in profit:
            for i in range(num_interval):
                if i not in pie_dict:
                    pie_dict[i] = 0

                if i_profit > (min_profit + interval_profit * i) and i_profit < (min_profit + interval_profit * (i+1)):
                        pie_dict[i] += 1
                        total += 1

                    
        labels = []
        for i in range(num_interval):
            if pie_dict[i] != 0:
                pie_dict[i] /= total
                min_dis = min_profit + interval_profit * i
                max_dis = min_profit + interval_profit * (i+1)
                labels.append("[" + str(int(min_dis/bound)) + "," +  str(int(max_dis/bound)) + "]")
                #labels.append(i)

        sizes = []
        print(pie_dict)
        for i in range(num_interval):
            if pie_dict[i] != 0:
                sizes.append(pie_dict[i])
        
        return labels,sizes

    def sum_tax_bar(self):
        index = 0
        figure, ax = plt.subplots(1,2)
        for name,group in self.data_df.groupby(["是否违约"]):

            profit = group["销项总税收"]
            labels,sizes = self.size_label(profit)
            #ax[0][0].axes(aspect='equal')
            #ax[0][1].axes(aspect='equal')
            ax[index].barh(y = labels , width = sizes)
            ax[index].set_xlabel("各个税收区间占比")
            ax[0].set_ylabel("销项总税收区间(单位：万元)")
            if(name == "否"):
                ax[index].set_title("未违约销项总税收各部分占比")
            else:
                ax[index].set_title("违约销项总税收各部分占比")
            #ax[index].legend()
            #ax[index].legend(loc = 'lower left')
            index += 1
        plt.show()
       # plt.savefig("./img/总税收占比图.png", dpi = 300)


    def season_bar(self):
        index = 0
        #plt.figure(figsize=(7,7))
        figure, ax = plt.subplots(1,2)
        for name,group in self.data_df.groupby(["是否违约"]):

            profit = group["季度平均利润"]
            
            labels,sizes = self.size_label(profit)

            #ax[0][0].axes(aspect='equal')
            #ax[0][1].axes(aspect='equal')

            
            ax[index].barh(y = labels , width = sizes)
            ax[index].set_xlabel("各个利润区间占比")
            ax[0].set_ylabel("平均季度利润区间(单位：万元)")
            if(name == "否"):
                ax[index].set_title("未违约平均季度利润各部分占比")
            else:
                ax[index].set_title("违约平均季度利润各部分占比")
            #ax[index].legend()
            #ax[index].legend(loc = 'lower left')
            index += 1
           
        plt.show()
        #plt.savefig("./img/季度利润占比图.png")

    def sum_profit_bar(self):
        index = 0
        #plt.figure(figsize=(7,7))
        #plt.figure(figsize=(200,100))
        figure, ax = plt.subplots(1,2)
        for name,group in self.data_df.groupby(["是否违约"]):

            profit = group["总利润"]
            
            labels,sizes = self.size_label(profit)

            #ax[0][0].axes(aspect='equal')
            #ax[0][1].axes(aspect='equal')

            
            ax[index].barh(y = labels , width = sizes)
            ax[index].set_xlabel("各个利润区间占比")
            ax[0].set_ylabel("利润区间(单位：万元)")
            if(name == "否"):
                ax[index].set_title("未违约总利润各部分占比")
            else:
                ax[index].set_title("违约总利润各部分占比")
            #ax[index].legend()
            #ax[index].legend(loc = 'lower left')
            index += 1
           
        plt.show()
        
        #plt.savefig("./img/总利润占比图.jpg",dpi=500, bbox_inches='tight')


if __name__ == "__main__":
    img = image()

    

        