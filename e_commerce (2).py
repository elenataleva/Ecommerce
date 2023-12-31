# -*- coding: utf-8 -*-
"""E-Commerce.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Zp_PPv5_TxkHTg0cNbT_1xuZHQrSL8tW

# 1. Data Analysis & visualization
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
import plotly.express as px

data = pd.read_csv('/content/drive/MyDrive/ecommerce_dataset/data.csv', encoding= 'unicode_escape') #ne mi vcituvase nekoi karakteri od dataset
data.shape

data.min()

data.max()

data.std()

data.hist()

data.plot.scatter(x='Country', y='UnitPrice')
plt.xticks(rotation =90)

plt.plot(data.groupby('Country').sum().Quantity)
plt.xticks(rotation=90)

line_up = sns.distplot(data['Quantity'], bins=3, kde=False, rug= True, label='Quantity')
line_down=sns.distplot(data['UnitPrice'], bins=3, kde=False, rug= True, label='UnitPrice')

"""# 2. Data preprocessing & preparation

### *Finding missing values*
"""

data_missing_values = data.isnull().sum()
perc_missing_values = data.isnull().sum() / len(data) * 100
perc_missing_values

data_missing_concat = pd.concat([data_missing_values, perc_missing_values], axis=1)
data_missing_concat.columns = ['Number of missing values','Percentage of missing values']
data_missing_concat

"""### *Visualization of missing values (MCAR)*"""

import missingno as msno
msno.bar(data)

msno.matrix(data)

msno.dendrogram(data) #connectivity by distance

"""### *Deleting missing values*"""

data1 = data.copy()

data1['CustomerID'].mean()

data1.dropna(subset=['CustomerID'], how='any', inplace=True)
data1 #izbrisa 135080 redici so null CustomerID

data1['CustomerID'].isnull().sum()

"""### *Imputing values for missing data NON TIME SERIES*"""

from sklearn.impute import SimpleImputer

data1 = data.copy()

main_imputer = SimpleImputer(strategy = 'constant', fill_value=0) #dodadi konstanta so 0, isto moze i so mean value da se napravi

data1.iloc[:,:] = main_imputer.fit_transform(data1)

data1.isnull().sum()

"""### *Imputing values for missing data TIME SERIES*"""

data['CustomerID'][50:60]

#FORWARD FILL
data.fillna(method='ffill', inplace=True)

data

data['CustomerID'][50:60]

#BACKFILL
data.fillna(method='bfill', inplace=True)
data['CustomerID'][50:60]

"""### *Encoding data with interpolation method*"""

data['Description'].value_counts()

classes = list(set(data['Description']))

dict = {} #convert int to string
for i in range(0,len(classes)):
  dict[classes[i]] = i
dict

#transforming
data1 = data.copy()
data1['Description'] = [dict[i] for i in data1['Description']]

data1['Description']

"""#3. Machine Learning
### *Train/Test, Data Standardization & KNN classification*
"""

data.isnull().sum() #looking for null values

x = data.copy()
x.drop('UnitPrice', axis=1, inplace=True)

x.drop('Country', axis=1, inplace=True)

x.drop('StockCode', axis=1, inplace=True)

x.drop('Description', axis=1, inplace=True)

x.drop('InvoiceDate', axis=1, inplace=True)

x.drop('InvoiceNo', axis=1, inplace=True)
from sklearn.model_selection import train_test_split

X_train,X_test,Y_train,Y_test = train_test_split(x,data['UnitPrice'],test_size=0.2)

X_train

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

X_train

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=5)

# knn.fit(X_train,Y_train)

# y_pred = knn.predict(X_test)

from sklearn.metrics import classification_report,confusion_matrix #for evaluation

from sklearn.model_selection import train_test_split

"""### *XGBoost*"""

data.drop('Country', axis=1, inplace=True)

X_train, X_test, Y_train, Y_test = train_test_split(data.iloc[:,:-1],data.iloc[:,-1:],test_size=0.2)

Y_train

from xgboost import XGBClassifier

model = XGBClassifier()

model.fit(X_train,Y_train)

y_pred = model.predict(X_test)

from sklearn.metrics import f1_score,confusion_matrix,classification_report

print(classification_report(Y_test,y_pred))

