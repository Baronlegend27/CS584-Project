import seaborn as sns
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import KernelDensity
from sklearn.linear_model import LogisticRegression
from sklearn.kernel_approximation import Nystroem
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings

warnings.filterwarnings("ignore", message="X does not have valid feature names, but Nystroem was fitted with feature names")

# Modify data so can use
def preprocess_data(df):
    df['result'] = df['result'].fillna(2).astype(int) # 2 for neither True or False
    df['product_category'] = df['product_category'].astype('category').cat.codes
    return df

# Clustering algo
def fit_gmm(df, row_to_show, j, n_clusters, random_seed = None):
    gmm = GaussianMixture(n_components = n_clusters, random_state = random_seed)
    gmm.fit(df.iloc[:, [row_to_show, j]])
    labels = gmm.predict(df.iloc[:, [row_to_show, j]])
    return labels

# Break down dimensions
def plot_scatter(ax, df, row_to_show, j, labels):
    ax.scatter(df.iloc[:, row_to_show], df.iloc[:, j], c = labels, alpha = 0.5)
    ax.set_xlabel(df.columns[row_to_show])
    ax.set_ylabel(df.columns[j])

# Regression model
def plot_kernel_logistic_regression(ax, df, row_to_show, j, labels):
    nystroem = Nystroem(kernel = 'rbf', n_components = 100)
    X_features = nystroem.fit_transform(df.iloc[:, [row_to_show, j]])

    logistic_regression = LogisticRegression()
    logistic_regression.fit(X_features, labels)

    x_min, x_max = df.iloc[:, row_to_show].min(), df.iloc[:, row_to_show].max()
    y_min, y_max = df.iloc[:, j].min(), df.iloc[:, j].max()
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                         np.linspace(y_min, y_max, 100))
    Z = logistic_regression.predict(nystroem.transform(np.c_[xx.ravel(), yy.ravel()]))
    Z = Z.reshape(xx.shape)

    ax.contourf(xx, yy, Z, alpha = 0.5, cmap = 'viridis')

# Regression Model (Not used)
def plot_kde(ax, df, row_to_show, j, labels):
    for cluster_label in np.unique(labels):
        cluster_indices = np.where(labels == cluster_label)[0]
        cluster_data = df.iloc[cluster_indices, [row_to_show, j]]

        kde = KernelDensity(kernel = 'gaussian', bandwidth = 0.5)
        kde.fit(cluster_data)

        x_values = np.linspace(df.iloc[:, row_to_show].min(), df.iloc[:, row_to_show].max(), 100)
        y_values = np.linspace(df.iloc[:, j].min(), df.iloc[:, j].max(), 100)
        X_grid, Y_grid = np.meshgrid(x_values, y_values)
        xy_grid = np.vstack([X_grid.ravel(), Y_grid.ravel()]).T

        Z = np.exp(kde.score_samples(xy_grid))
        Z = Z.reshape(X_grid.shape)

        ax.contour(X_grid, Y_grid, Z, levels = 5, cmap = 'viridis', alpha = 0.5)

# Use all the previously defined functions
def plot_row(df, row_to_show, n_clusters = None, with_clustering = True, regression = "None"):
    fig, axs = plt.subplots(1, len(df.columns), figsize = (20, 5))
    for j, col2 in enumerate(df.columns):
        if with_clustering:
            labels = fit_gmm(df, row_to_show, j, n_clusters, random_seed = 0)
            df[f'cluster_{j}'] = labels 
        else:
            labels = None

        plot_scatter(axs[j], df, row_to_show, j, labels)

        if regression == "KDE":
            plot_kde(axs[j], df, row_to_show, j, labels)
        if regression == "KLOG":
            plot_kernel_logistic_regression(axs[j], df, row_to_show, j, labels)

    plt.tight_layout()
    plt.savefig('visual.png')

# -------------------------------------------------------------------------------------------------

def to_classify(df):
    to_classify_df = df[df['result'] == 2]
    to_classify_df.to_csv('toClassify.csv', index=False)

def results(df_null, df_filled, compare = False):
    output_ids = df_null['output_id']
    result_df = df_filled[df_filled['output_id'].isin(output_ids)]
    if compare:
        result_df = result_df[['output_id', 'result', 'avg_cluster']]
    result_df.to_csv('toResults.csv', index = False)

def modified_compare(df):
    avg_cluster = df.iloc[:, -6:].mean(axis=1)
    mod_comp_df = df[['output_id', 'result']].copy()
    mod_comp_df['avg_cluster'] = avg_cluster
    mod_comp_df.to_csv('modCompare.csv', index = False) 

# A few more functions for return/result files

file_path = 'output.csv'
df = pd.read_csv(file_path)

df = preprocess_data(df)

to_classify(df)

# Set parameters
row_to_show = 3  # Change this to the row number you want to show (3 is result)
n_clusters = 2  # Change this to the number of clusters if clustering is enabled

# regression options: NONE KDE KLOG
plot_row(df, row_to_show, n_clusters = n_clusters, with_clustering = True, regression = "KLOG")

df.to_csv('outputModified.csv', index = False)

df_null = pd.read_csv('toClassify.csv')
df_filled = pd.read_csv('outputModified.csv')
results(df_null, df_filled, False)

modified_compare(df_filled)
df_filled = pd.read_csv('modCompare.csv')
results(df_null, df_filled, True)

# Print accuracy?
filtered_df = df_filled[df_filled.iloc[:, 1] != 2].copy()

filtered_df['guess'] = (filtered_df.iloc[:, 2] < 0.5).astype(int)
percentage = (filtered_df['guess'] == filtered_df['result']).mean() * 100

df_acc = filtered_df[['output_id', 'result', 'guess']]
df_acc.to_csv('testAcc.csv', index = False)

print("\nAccuracy (Percentage of time when predicted matched actual label): {}%\n".format(percentage))
