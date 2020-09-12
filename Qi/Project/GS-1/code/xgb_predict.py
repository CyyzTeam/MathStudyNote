import numpy as np
import xgboost as xgb
from sklearn.metrics import accuracy_score 
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from matplotlib import pyplot as plt
from dataset import Dataset
import pandas as pd

is_pred_1 = True

def ROC(y_true, y_score):
    fpr, tpr, thresholds = roc_curve(y_true, y_score, pos_label=1)
    AUC_ROC = roc_auc_score(y_true, y_score)
    plt.figure()
    plt.plot(fpr,tpr,'-',label='Area Under the Curve (AUC = %0.4f)' % AUC_ROC)
    plt.title('ROC curve')
    plt.xlabel("FPR (False Positive Rate)", fontsize = 15)
    plt.ylabel("TPR (True Positive Rate)", fontsize = 15)
    plt.legend(loc="lower right")
    plt.show()

if is_pred_1:
    model = xgb.Booster(model_file='model/q1_xgb0.model')
    datas = Dataset(is_train_1 = is_pred_1)

    all_data, all_labels = datas.get_data
    name_company,credit = datas.get_name_company

    pred_labels = []

    xgb_data = xgb.DMatrix(all_data)
    all_pred = model.predict(xgb_data)

    for pred in all_pred:
        if pred > 0.65:
            pred_labels.append(1)
        else:
            pred_labels.append(0)

    accuracy = accuracy_score(all_labels,pred_labels)
    ROC(all_labels,all_pred)
    print('accuarcy:%.2f%%'%(accuracy*100))

    save_pred = dict()
    save_pred["name"] = name_company
    save_pred["pred_possibility"] = all_pred
    save_pred["pred_labels"] = pred_labels
    save_pred["credit"] = credit
    save_pred_pd = pd.DataFrame(save_pred)
    #save_pred_pd.to_excel("output/Q1_predict.xlsx")

else:
    model = xgb.Booster(model_file='model/q2_xgb0.model')
    datas = Dataset(data_path = "data/附件2_数据清洗.xlsx",is_data_1 = False,is_train_1 = is_pred_1)

    all_data = datas.get_data
    name_company = datas.get_name_company

    pred_labels = []

    xgb_data = xgb.DMatrix(all_data)
    all_pred = model.predict(xgb_data)

    for pred in all_pred:
        if pred > 0.65:
            pred_labels.append(1)
        else:
            pred_labels.append(0)
    

    save_pred = dict()
    save_pred["name"] = name_company
    save_pred["pred_possibility"] = all_pred
    save_pred["pred_labels"] = pred_labels
    
    save_pred_pd = pd.DataFrame(save_pred)

    save_pred_pd.to_excel("output/Q2_predict.xlsx")