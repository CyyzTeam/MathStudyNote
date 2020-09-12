import pandas as pd
import numpy as np

class Dataset:
    def __init__(self,data_path = "data\附件1_数据清洗.xlsx", is_data_1 = True):
        self.data_path = data_path
        self.data_df   = None
        self.is_data_1 = is_data_1
        self.datas_np = None
        self.labels = None

        self.init()

    def read_data(self):
        self.data_df = pd.read_excel(self.data_path)

    def init(self):
        self.read_data()
        self.data_to_np()

    @property
    def get_data(self):
        if self.is_data_1:
            return self.datas_np, self.labels
        else:
            return self.datas_np 

    def data_to_np(self):
        labels  = []
        datas = []
        name_company = []
        for index,row in self.data_df.iterrows():
            values = []
            #print(index)
            name_company.append(row[0])

            if self.is_data_1:
                if row["是否违约"] == "否":
                    labels.append(0)
                else:
                    labels.append(1)
            if self.is_data_1:
                if row["信誉评级"] == "A":
                    values.append(0.9)
                elif row["信誉评级"] == "B":
                    values.append(0.6)
                elif row["信誉评级"] == "C":
                    values.append(0.3)
                else:
                    values.append(0)

            values.append(row["进项总金额"])
            #values.append(row["进项总税收"])
            values.append(row["进项季度平均金额"])
            #values.append(row["进项季度平均税收"])
            values.append(row["销项总金额"])
            #values.append(row["销项总税收"])
            values.append(row["销项季度平均金额"])
            #values.append(row["销项季度平均税收"])
            values.append(row["总利润"])
            values.append(row["季度平均利润"])
            values.append(row["销项总税收"] - row["进项总税收"])
            values.append(row["销项季度平均税收"] - row["进项季度平均税收"])

            datas.append(values)
        
        datas_np = np.array(datas)
        labels   = np.array(labels)

        self.datas_np = datas_np

        if self.is_data_1:
            self.labels   = labels
        #print(datas_np.shape)
        #print(datas_np)
        #print(labels.shape)



if __name__ == "__main__":
    data = Dataset()

            

            


