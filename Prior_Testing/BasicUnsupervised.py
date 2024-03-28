import numpy as np
import matplotlib.pyplot as plt


class KMeans:
    def __init__(self, n_clusters, max_iter=100):
        self.n_clusters = n_clusters
        self.max_iter = max_iter

    def fit(self, X):
        # Initialize centroids randomly
        self.centroids = X[np.random.choice(X.shape[0], self.n_clusters, replace=False)]

        for _ in range(self.max_iter):
            # Assign each data point to the nearest centroid
            labels = np.argmin(((X[:, np.newaxis] - self.centroids) ** 2).sum(axis=2), axis=1)

            # Update centroids
            new_centroids = np.array([X[labels == k].mean(axis=0) for k in range(self.n_clusters)])

            # Check for convergence
            if np.allclose(self.centroids, new_centroids):
                break

            self.centroids = new_centroids

        self.labels_ = labels
        return self


# Example usage
if __name__ == "__main__":
    # Generate sample data
    np.random.seed(0)
    X = np.concatenate([np.random.randn(100, 2) + [3, 3],
                        np.random.randn(100, 2) + [-3, 3],
                        np.random.randn(100, 2) + [0, -3]])

    # Instantiate and fit KMeans model
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(X)

    # Visualize clusters and centroids
    plt.figure(figsize=(8, 6))
    plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_, cmap='viridis', alpha=0.5)
    plt.scatter(kmeans.centroids[:, 0], kmeans.centroids[:, 1], c='red', marker='x', s=100)
    plt.title('K-Means Clustering')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.show()
