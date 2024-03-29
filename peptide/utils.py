# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/99_utils.ipynb (unless otherwise specified).

__all__ = ['get_default_param_grid', 'visualize_2pcs', 'visualize_3pcs', 'train_predict', 'visualize_elbow',
           'plot_silhouette_scores', 'visualize_clusters']

# Cell

from .imports import *


# Cell


def get_default_param_grid() -> list:
    """Create and return a default gird search param grid"""

    lr_grid = [
        {
            "classifier": [LogisticRegression()],
            "classifier__solver": ["lbfgs"],
            "classifier__penalty": ["l2"],
            "classifier__C": np.logspace(-2, 2, 5),  # default=1.0
            "classifier__max_iter": [1000, 5000, 10000],  # default=100
        },
        {
            "classifier": [LogisticRegression()],
            "classifier__solver": ["liblinear"],
            "classifier__penalty": ["l1", "l2"],
            "classifier__C": np.logspace(-2, 2, 5),
            "classifier__max_iter": [1000, 5000, 10000],
        },
    ]
    svm_grid = [
        {
            "classifier": [LinearSVC()],
            "classifier__loss": ["hinge"],  # default=squared_hinge
            "classifier__penalty": ["l2"],  # default=l2
            "classifier__C": np.logspace(-2, 2, 5),  # default=1.0
            "classifier__max_iter": [10000, 20000],  # default=1000
        },
        {
            "classifier": [LinearSVC()],
            "classifier__loss": ["squared_hinge"],
            "classifier__penalty": ["l1", "l2"],
            "classifier__C": np.logspace(-2, 2, 5),
            "classifier__max_iter": [10000, 20000],
        },
    ]
    xgb_grid = [
        {
            "classifier": [XGBClassifier()],
            # "classifier__gamma": (5, 10),
            "classifier__learning_rate": np.linspace(0.03, 0.3, 4),  # default 0.1
            "classifier__max_depth": [3, 4, 5, 6],  # default 6
            "classifier__n_estimators": [100, 300],  # default 100
            # "classifier__subsample": (0.5, 1),
        }
    ]

    return [lr_grid, svm_grid, xgb_grid]


# Cell


def visualize_2pcs(
    pcs: np.ndarray,  # dimensionality reduced 'X' numpy ndarray
    y: np.ndarray,  # 'y' numpy array
) -> None:
    """Visualize 2 principal components."""
    fig, ax = plt.subplots(figsize=(10, 5))
    plot = plt.scatter(pcs[:, 0], pcs[:, 1], c=y, marker=".")
    ax.set_xlabel("PC 1")
    ax.set_ylabel("PC 2")
    ax.legend(handles=plot.legend_elements()[0], labels=["No", "Yes"])


# Cell


def visualize_3pcs(
    pcs: np.ndarray,  # dimensionality reduced 'X' numpy ndarray
    y: np.ndarray  # 'y' numpy array
) -> None:
    """Visualize 3 principal components."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax = fig.add_subplot(projection="3d")
    plot = ax.scatter(pcs[:, 0], pcs[:, 1], pcs[:, 2], c=y)
    ax.set_xlabel("PC 1")
    ax.set_ylabel("PC 2")
    ax.set_zlabel("PC 3")
    ax.legend(handles=plot.legend_elements()[0], labels=["No", "Yes"])


# Cell


def train_predict(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray
) -> pd.DataFrame:
    """Utility helper function to quickly train and predict"""

    lr = LogisticRegression(max_iter=10000)
    lr.fit(X_train, y_train)

    svc = LinearSVC(max_iter=10000)
    svc.fit(X_train, y_train)

    xgb = XGBClassifier()
    xgb.fit(X_train, y_train)

    lr_preds = lr.predict(X_test)
    svc_preds = svc.predict(X_test)
    xgb_preds = xgb.predict(X_test)

    scores = []
    for preds in [lr_preds, svc_preds, xgb_preds]:
        scores.append(
            [
                accuracy_score(y_test, preds),
                recall_score(y_test, preds),
                precision_score(y_test, preds),
                f1_score(y_test, preds),
            ]
        )

    return pd.DataFrame(
        scores, columns=["acc", "recall", "precision", "f1"], index=["lr", "svc", "xgb"]
    )


# Cell


def visualize_elbow(
    X: np.ndarray,  # 'X' numpy ndarray
    ks: list,  # list of 'k' values to try - ideally 2 to 10
    random_state: int = 10  # random state for KMeans
) -> None:
    """Visualize elbow plot for KMeans."""

    fig, ax = plt.subplots()
    inertias = []
    for k in ks:
        kmeans = KMeans(n_clusters=k, random_state=random_state).fit(X)
        inertias.append(kmeans.inertia_)
    plt.plot(ks, inertias)
    plt.xticks(ks)
    plt.xlabel("Number of clusters")
    plt.ylabel("Inertia")
    plt.title("Elbow plot")


# Cell


def plot_silhouette_scores(
    max_clusters: int,  # max value for 'k' for KMeans clustering
    X: np.ndarray,   # the 'X' numpy ndarray
    random_state: int = 10  # random state for KMeans
) -> None:
    """List and plot silhouette scores for KMeans."""

    silhouette_scores, clusters = [], []

    for n_clusters in range(2, max_clusters + 1):
        clusterer = KMeans(n_clusters=n_clusters, random_state=random_state)
        cluster_labels = clusterer.fit_predict(X)
        silhouette_avg = silhouette_score(X, cluster_labels)
        clusters.append(n_clusters)
        silhouette_scores.append(silhouette_avg)
        print(f"n_clusters: {n_clusters} -- avg silhouette score: {silhouette_avg}")

    # plot
    fig, ax = plt.subplots()
    plt.plot(clusters, silhouette_scores)
    plt.xticks(clusters)
    plt.xlabel("Number of clusters")
    plt.ylabel("Silhouette scores")
    plt.title("Silhoutte Scores vs Clusters")


# Cell


def visualize_clusters(
    clust_lbls: np.ndarray,  # cluster labels after KMeans fitting
    X: np.ndarray  # dim reduced X used for KMeans
) -> None:
    """Visualize clusters in a plot of first 2 principal components."""

    X_plot = pd.DataFrame(X[:, :2], columns=["pc1", "pc2"])
    X_plot["cluster_id"] = clust_lbls
    plt.figure(figsize=(12, 5))
    sns.scatterplot(
        data=X_plot,
        x=X_plot["pc1"],
        y=X_plot["pc2"],
        hue="cluster_id",
        palette="deep",
        legend=True,
    )
