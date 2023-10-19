import xlrd,xlwt
import os,sys
import numpy as np


# 归一化
def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


# 标准化
def standardization(data):
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)
    return (data - mu) / sigma
array_ett = np.zeros((135,611))  #全体数据
workdir = '/home/ming/MNNU_ming/九色乙醇版/'
i=0

for file in os.listdir('/home/ming/MNNU_ming/九色乙醇版/'):
    if 'xls' in os.path.splitext(file)[1] :
        index = int(file.split('-')[0])#数据标号1-27
        abs_path = os.path.join(workdir,file)
        book = xlrd.open_workbook(abs_path)
        names = book.sheet_names()
        sheet = book.sheet_by_index(0)
        column_cm = sheet.col_values(4)[7:]
        array_ett[i] = np.pad(column_cm,(1,9),'constant',constant_values=(index,0))
        i = i+1
        print("...")
tmp_array = array_ett[:,1:-9]
tmp_array = standardization(tmp_array)
array_ett[:,1:-9] = tmp_array
book = xlrd.open_workbook('/media/psf/化院/九色乙醇版/label/label.xlsx')
names = book.sheet_names()
sheet = book.sheet_by_index(0)

for j in range(0,28):
    try:
        column_cm = sheet.row_values(j)
        array_ett[np.where((array_ett==column_cm[0]))[0],-9:] = np.array(column_cm[1:])
    except IndexError:
        print("结束")
        break
np.savetxt("./jiuse.csv",array_ett,delimiter=',')
print("...")
