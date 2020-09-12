import numpy as np
from dataset import Dataset
import xgboost as xgb
from xgboost import plot_importance
import matplotlib.pyplot  as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score  # 准确率
from sklearn.model_selection import KFold

# 中文乱码和坐标轴负号的处理
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def img_importance(model):
    all_plot_label = ['信誉评级',"总成本","季度平均成本",
                 "总收入", "季度平均收入","总利润",
                 "季度平均利润", "总增值税", "季度平均增值税"]
    

    importance = model.get_fscore()

    tuples = [(k, importance[k]) for k in importance]
    tuples = sorted(tuples, key=lambda x: x[1])

    labels, values = zip(*tuples)
    ylocs = np.arange(len(values))

    new_labels = []
    for  lab in labels:
        i_label = int(lab[1])
        new_labels.append(all_plot_label[i_label])

    _, ax = plt.subplots(1, 1)
    ax.barh(new_labels, values, align='center', height=0.2)
    ax.set_title('Feature importance', fontsize=15)
    ax.set_xlabel('F score', fontsize = 15)
    ax.set_ylabel("Features", fontsize = 15)

    xlim = (0, max(values) * 1.1)
    ylim = (-1, len(values))
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    ylocs = np.arange(len(values))
    for x, y in zip(values, ylocs):
        ax.text(x + 1, y, x, va='center')

    plt.show()


def xgb_model(trn_x, trn_y, val_x, val_y, verbose, class_pred = 0.65,show = False):
    params={'booster':'gbtree',
        'objective': 'binary:logistic',
        'eval_metric': ['logloss'],
        'max_depth':12,
        'lambda':10,
        'subsample':0.75,
        'colsample_bytree':0.75,
        'min_child_weight':2,
        'eta': 0.1,
        'seed':0,
        'nthread':8,
        'silent':1}

    # 生成数据集格式
    dtrain = xgb.DMatrix(trn_x,trn_y)
    num_rounds = 500
    record = dict()

    # xgboost模型训练
    model = xgb.train(params,
                      dtrain,
                      num_rounds,
                      [(xgb.DMatrix(trn_x, trn_y), 'train'), (xgb.DMatrix(val_x, val_y), 'valid')], 
                      verbose_eval=verbose, 
                      early_stopping_rounds=500, 
                      callbacks = [xgb.callback.record_evaluation(record)]
                      )
    
    # 对测试集进行预测
    dtest = xgb.DMatrix(val_x)
    y_pred = model.predict(dtest, ntree_limit=model.best_ntree_limit)
    
    print(y_pred)
    acc_pred = []
    for pred in y_pred:
        if pred > class_pred:
            acc_pred.append(1)
        else:
            acc_pred.append(0)

    # 计算准确率
    accuracy = accuracy_score(val_y,acc_pred)
    print('accuarcy:%.2f%%'%(accuracy*100))
    if show:
        img_importance(model)

    return accuracy, model

class_pred = 0.65
is_train_1 = True
save = False
total_acc = 0
max_acc = 0
random_seed = 2019
k = 5

data_set = Dataset(is_train_1 = is_train_1)
all_data,all_labels = data_set.get_data

fold = list(KFold(k, shuffle = True, random_state = random_seed).split(all_data))
np.random.seed(random_seed)

for i, (trn, val) in enumerate(fold) :
    print(i+1, "fold")
    
    trn_x = all_data[trn, :]
    trn_y = all_labels[trn]

    val_x = all_data[val, :]
    val_y = all_labels[val]
    
    acc, model = xgb_model(trn_x, trn_y, val_x, val_y, verbose = False, class_pred = class_pred,show = True)
    total_acc += acc
    
    if save and acc > max_acc:
        max_acc = acc
        if is_train_1:
            model.save_model('model/q1_xgb' + str(i) + '.model')
        else:
            model.save_model('model/q2_xgb' + str(i) + '.model')
print('total_acc:%.2f%%'%(total_acc/5*100))