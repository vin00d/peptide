# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/02_learn.ipynb (unless otherwise specified).

__all__ = ['Learner']

# Cell

from .imports import *
from .utils import *
from .data import ProteinDataset


# Cell

# from sklearn.utils import parallel_backend


class Learner:
    """Class for training and prediction."""

    def __init__(
        self,
        X_train: np.ndarray,  # X_train numpy ndarray
        y_train: np.ndarray,  # y_train numpy ndarray
        X_test: np.ndarray,  # X_test numpy ndarray
        y_test: np.ndarray,  # y_test numpy ndarray
        ohe: bool = False,  # to use one hot encoding or not
        scaler: bool = False,  # to use standard scaling or not
        pca: bool = True,  # to use principal component analysis or not
        pca_n_components: int = 50,  # PCA number of components
        param_grids: list = None,  # param_grid for grid search, if None - gets default grid from utils
    ):
        """Initialize learner for training and prediction."""
        self.classifiers = ["LogisticRegression", "LinearSVC", "XGBClassifier"]
        self.X_train, self.y_train = X_train, y_train
        self.X_test, self.y_test = X_test, y_test
        self.ohe, self.scaler, self.pca = ohe, scaler, pca
        self.pca_n_components = pca_n_components
        self.pipeline = self.create_pipeline()
        self.param_grids = (
            get_default_param_grid() if param_grids is None else param_grids
        )

        self.grid_list, self.train_results = [], []
        pred_cols = [
            "best_params",
            "accuracy",
            "recall",
            "precision",
            "f1",
        ]
        pred_index = [*self.classifiers, "LabelSpreading"]
        self.predict_results = pd.DataFrame(index=pred_index, columns=pred_cols)

    def create_pipeline(self) -> Pipeline:
        """Create and return pipeline"""

        steps = []
        if self.ohe:
            steps.append(("ohe", OneHotEncoder(handle_unknown="ignore", sparse=False)))
        if self.scaler:
            steps.append(("scaler", StandardScaler()))
        if self.pca:
            steps.append(("pca", PCA(n_components=self.pca_n_components)))
        steps.append(("classifier", "passthrough"))

        pipe = Pipeline(steps)

        return pipe

    def train(
        self,
        scoring: str = "accuracy",  # must be one of https://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter
        cv: int = 5,  # defaults to 5-fold CV
        n_jobs: int = -1,  #  defaults to -1 to use all cores
    ) -> tuple[list, list]:
        """Run GridSearchCV for all models on X_train and y_train of dataset.
        Returns:
            train_results: list of grid search results
            grid_list: list of trained grid objects
        """

        result_list = []
        grid_list = []

        for classifier, param_grid in zip(self.classifiers, self.param_grids):
            print(f"Starting grid search for {classifier}")
            grid = GridSearchCV(
                estimator=self.pipeline,
                param_grid=param_grid,
                n_jobs=n_jobs,
                cv=cv,
                scoring=scoring,
                verbose=1,
            )

            # with parallel_backend("multiprocessing"):
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                grid.fit(self.X_train, self.y_train)

            result_list.append(pd.DataFrame.from_dict(grid.cv_results_))
            grid_list.append(grid)

        self.train_results = result_list
        self.grid_list = grid_list

        return self.train_results, self.grid_list

    def get_top_5_train_results(self) -> list:
        "Return top 5 results for each grid"
        results = []
        for result in self.train_results:
            results.append(result.sort_values("rank_test_score")[:5])
        return results

    def predict(self) -> pd.DataFrame:
        """Get predictions on the dataset's X_test from best estimators of GridSearchCV."""
        # results = []
        for classifier, grid in zip(self.classifiers, self.grid_list):
            preds = grid.predict(self.X_test)
            result = [
                # classifier,
                grid.best_params_,
                accuracy_score(self.y_test, preds),
                recall_score(self.y_test, preds),
                precision_score(self.y_test, preds),
                f1_score(self.y_test, preds),
            ]
            self.predict_results.loc[classifier, :] = result

        return self.predict_results

    ## Unsupervised Learning ##

    def pick_k(
        self,
        max_clusters: int = 10,  # max number of clusters to try out
        pca_n_components: int = 50,  # number of components to reduce to in PCA
    ) -> np.ndarray:  # PCA reduced X
        """Plot elbow and silohutte curves & print silohutte scores to help determine the ideal 'k' for Kmeans."""

        # concat X
        X = np.concatenate((self.X_train, self.X_test), axis=0)
        assert (self.X_train.shape[0] + self.X_test.shape[0]) == X.shape[0]

        if self.ohe:  # One Hot Encode X
            ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)
            X = ohe.fit_transform(X)

        if self.scaler:  # Scale
            scalr = StandardScaler()
            X = scalr.fit_transform(X)

        if self.pca:  # Dim Reduce X
            pca = PCA(n_components=pca_n_components)
            X = pca.fit_transform(X)

        # visualize elbow plot
        visualize_elbow(X, np.arange(2, max_clusters))
        # visualize silhouette scores and plot
        plot_silhouette_scores(max_clusters=max_clusters, X=X)

        return X

    def analyze_clusters(
        self,
        X_pca: np.ndarray,  # dim reduced X numpy ndarray
        k: int,  # the chosen value of k for KMeans
        random_state: int = 10,  # random state for KMeans
    ) -> None:
        """Perform KMeans clustering, print cluster counts and plot clusters from the result."""

        km = KMeans(n_clusters=k, random_state=random_state).fit(X_pca)
        print(f"Cluster counts: {Counter(km.labels_)}")
        visualize_clusters(km.labels_, X_pca)

    ## Semi Supervised Learning ##

    def run_label_spreading(
        self, pca_n_components: int = 50  # number of components to reduce to in PCA
    ) -> None:
        """Run Label Spreading, print report, append results to predict_results."""

        # concat X
        X = np.concatenate((self.X_train, self.X_test), axis=0)
        assert (self.X_train.shape[0] + self.X_test.shape[0]) == X.shape[0]

        # concat y
        y = np.concatenate((self.y_train, np.full(self.y_test.shape, -1)), axis=0)
        assert (self.y_train.shape[0] + self.y_test.shape[0]) == y.shape[0]

        if self.ohe:  # One Hot Encode X
            ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)
            X = ohe.fit_transform(X)

        if self.scaler:  # Scale
            scalr = StandardScaler()
            X = scalr.fit_transform(X)

        if self.pca:  # Dim Reduce X
            pca = PCA(n_components=pca_n_components)
            X = pca.fit_transform(X)

        # Run LableSpreading
        lbl_spread = LabelSpreading(kernel="knn", alpha=0.01)
        lbl_spread.fit(X, y)
        semi_sup_preds = lbl_spread.transduction_[self.X_train.shape[0] :]
        assert semi_sup_preds.shape[0] == self.X_test.shape[0]

        # print result
        print(classification_report(self.y_test, semi_sup_preds))

        result = [
            lbl_spread.get_params(),
            accuracy_score(self.y_test, semi_sup_preds),
            recall_score(self.y_test, semi_sup_preds),
            precision_score(self.y_test, semi_sup_preds),
            f1_score(self.y_test, semi_sup_preds),
        ]
        self.predict_results.loc["LabelSpreading", :] = result
