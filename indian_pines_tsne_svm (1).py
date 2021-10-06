# -*- coding: utf-8 -*-
"""indian_pines_tsne_svm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MLSGL3BF_VqlhdPFGzminDw4cfYeMNYe
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.svm import SVC
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

!pip install hvplot
import hvplot
import hvplot.pandas

pd.options.plotting.backend = 'hvplot'

df = pd.read_csv('https://raw.githubusercontent.com/syamkakarla98/Hyperspectral_Image_Analysis_Simplified/master/Data/Dataset.csv')
df.head(3)

X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

X.shape, y.shape

#def init(n_components=2, perplexity=30.0, early_exaggeration=12.0, learning_rate=200.0, 
#         n_iter=1000, n_iter_without_progress=300, min_grad_norm=1e-07, metric='euclidean', 
#         init='random', verbose=0, random_state=None, method='barnes_hut', angle=0.5, n_jobs=None)

#tsne = TSNE(n_components=3, init='pca', random_state=0)
tsne_em = TSNE(n_components=2, perplexity=10, n_iter=1200, verbose=1).fit_transform(df)
#points = tsne.fit_transform(X)

principalDf = pd.DataFrame(data = tsne_em, columns = ['TSNE-1','TSNE-2'])
finalDf = pd.concat([principalDf, df[['class']]], axis = 1)
finalDf.to_csv('indian_pines_depois_tsne.csv')

finalDf.head()

X_train, X_test, y_train, y_test, indices_train, indices_test  = train_test_split(tsne_em, y,  range(X.shape[0]), 
                                                                                  test_size = 0.35, random_state = 0, stratify=y)

X_train.shape, X_test.shape

#svm = SVC(kernel='rbf', degree = 10, gamma='scale', cache_size=1024*7)
svm = SVC(C = 9000, kernel = 'poly', cache_size = 32*1024)
svm.fit(X_train, y_train)

y_pred = svm.predict(X_test)

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print(f'Accuracy: {accuracy_score(y_test, y_pred)*100}%')

!pip install -q scikit-plot
import scikitplot as skplt

skplt.metrics.plot_confusion_matrix(
    y_test, 
    y_pred,
    figsize=(12,12));

import plotly.graph_objects as go

fig = go.Figure(data=go.Heatmap(
                   z= confusion_matrix(y_test, y_pred),
                   x=[f'class-{i}' for i in np.unique(df.loc[:, 'class'].values)],
                   y=[f'class-{i}' for i in np.unique(df.loc[:, 'class'].values)],
                   hoverongaps = False))
fig.show()

# print(confusion_matrix(y_test,y_pred))
print('Classification report:\n',classification_report(y_test,y_pred))

plt.figure(figsize=(8, 6))
plt.imshow(df.iloc[:, -1].values.reshape((145, 145)), cmap='jet')
plt.colorbar()
plt.axis('off')
plt.title('Ground Truth')
plt.savefig('ground_truth.png')
plt.show()

!pip install tqdm
from tqdm import tqdm
pre = y_pred

clmap = [0]*X.shape[0]

for i in tqdm(range(len(indices_train))):
    clmap[indices_train[i]] = y[indices_train[i]]

for i in tqdm(range(len(indices_test))):
    clmap[indices_test[i]] = pre[i]

plt.figure(figsize=(8, 6))
plt.imshow(np.array(clmap).reshape((145, 145)), cmap='jet')
plt.colorbar()
plt.axis('off')
plt.title('Classification Map (TSNE + SVM)')
plt.savefig('Classification_map.png')
plt.show()