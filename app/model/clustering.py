import warnings
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from hdbscan import flat
from IPython.display import Markdown, display
from kneed import KneeLocator
from loguru import logger
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

from app.config import config

log_dir = config.project_dir / "logs"
logger.add(log_dir / "log.log")

warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.simplefilter(action="ignore", category=UserWarning)

MIN_MATCHES = 250
LAST_TRAIN_MATCH_DATE = datetime(2023, 7, 31)


X_values = [
    "wickets_down",
    "run_rate",
    "req_rate",
    "batter_in_first_10",
    "batter_strike_rate",
    "batter_dismissal_prob",
    "batter_dismissal_vs_style",
    "bowler_economy",
    "bowler_wicket_prob",
    "bowler_wicket_vs_style",
    "bowler_wide_noball_rate",
]


y_values = [
    "outcome",
]

SCALER_CLASSES = {
    "quantile": preprocessing.QuantileTransformer(),
    "standard": preprocessing.StandardScaler(),
    "gaussian": preprocessing.QuantileTransformer(output_distribution="normal"),
    "normalizer": preprocessing.Normalizer(),
}

OUTCOME_DESCS = [
    "label",
    "tot",
    "wide",
    "noball",
    "bye",
    "lebbye",
    "wicket",
    "dot",
    "single",
    "two",
    "three",
    "four",
    "six",
]


def extract_values(d, values: list[str]):
    return d[values]


@dataclass
class Clusterer:
    df: pd.DataFrame = field(default_factory=pd.DataFrame)
    train_dfs: dict[int, dict[int, pd.DataFrame]] = field(default_factory=dict)
    knees: dict[int, list[int]] = field(default_factory=dict)
    clfs: dict[int, list] = field(default_factory=dict)

    def run(self):
        logger.info("starting clustering...")
        self.df = pd.read_csv(config.data_path / "ml_rows.csv", parse_dates=["start_date"])

        df_train = {
            inns: self.df[
                (self.df.start_date <= LAST_TRAIN_MATCH_DATE)
                & (self.df.match_number > MIN_MATCHES)
                & (self.df.innings == inns)
            ]
            for inns in range(2)
        }
        # df_test = {
        #     inns: self.df[(self.df.start_date > LAST_TRAIN_MATCH_DATE) & (self.df.match_number > MIN_MATCHES) & (self.df.innings == inns)]
        #     for inns in range(2)
        # }

        self.train_dfs = {
            inns: {over: df_train[inns].loc[(df_train[inns]["over"] == over)] for over in range(20)}
            for inns in range(2)
        }

        logger.info("training set prepared")

        self.estimate_cluster_sizes()

        logger.info("cluster sizes estimated")

        self.apply_clustering()

    def prepare_training_set(self, inns, over, scaler: str) -> np.ndarray:
        X = extract_values(self.train_dfs[inns][over], X_values)
        scaler_obj = SCALER_CLASSES[scaler]
        fitted_scaler = scaler_obj.fit(X)
        return fitted_scaler.transform(X)

    @staticmethod
    def test_n(n: int, X) -> float:
        kmeans = KMeans(n_clusters=n)
        kmeans.fit(X)
        return kmeans.inertia_

    def find_knee(self, inns, over) -> int:
        X = self.prepare_training_set(inns, over, "normalizer")
        clusters_range = range(11, 31, 1)
        sse = [self.test_n(n, X) for n in clusters_range]
        kneedle = KneeLocator(clusters_range, sse, curve="convex", direction="decreasing")
        if isinstance(kneedle.knee, (int, np.signedinteger)):
            logger.info(f"Knee {inns=} {over=} found at {kneedle.knee}")
            return int(kneedle.knee)
        raise ValueError("No integer-convertible value for knee found")

    def estimate_cluster_sizes(self):
        self.knees = {inns: [self.find_knee(inns, over) for over in range(20)] for inns in range(2)}

    def apply_clustering(self) -> None:
        logger.info("starting with estimated clusters...")
        for scaler in [
            "normalizer",
        ]:  # ["standard", "quantile", "gaussian", "normalizer"]:
            for inns in range(2):
                self.clfs[inns] = []
                for over in range(20):
                    X_scaled = self.prepare_training_set(inns, over, scaler)
                    n_clusters = self.knees[inns][over]
                    clf = flat.HDBSCAN_flat(X_scaled, n_clusters=n_clusters)
                    clf.fit(X_scaled)
                    self.clfs[inns].append(clf)
                    labels = clf.labels_
                    clustered = labels >= 0
                    counts = Counter(labels)
                    total_clusters = np.max(labels) + 1
                    coverage = np.sum(clustered) / X_scaled.shape[0]
                    total_clusters = np.max(labels) + 1
                    logger.info(
                        f"{inns} {over} {n_clusters} {total_clusters} {coverage:.2%} pts:{len(labels)} noisy:{counts[-1]} {[v for k, v in counts.items() if k >= 0]}"
                    )
        logger.info("clustering complete!")

    def plot_clusters(self):
        sns.set_theme(style="darkgrid", font_scale=0.5)
        fig, axs = plt.subplots(4, 5, figsize=(15, 12))

        for inns in range(2):
            for over in range(20):
                data = self.train_dfs[inns][over].sample(10000)

                X = extract_values(data, X_values)
                scaler_obj = SCALER_CLASSES["normalizer"]
                fitted_scaler = scaler_obj.fit(X)
                Xp = fitted_scaler.transform(X)

                tsne = TSNE(n_components=2, metric="euclidean", verbose=0, perplexity=40, n_iter=300)
                results = tsne.fit_transform(Xp)

                n_clusters = self.knees[inns][over]

                clf = self.clfs[inns][over]
                clf.fit(Xp)
                self.clfs[inns].append(clf)
                labels = clf.labels_

                df_res = pd.DataFrame()
                df_res["x"] = results[:, 0]
                df_res["y"] = results[:, 1]
                df_res["c"] = labels

                r = over % 5
                c = over // 5
                ax = axs[c, r]
                sns.scatterplot(
                    x="x",
                    y="y",
                    data=df_res,
                    hue="c",
                    palette=sns.color_palette("hls", 10),
                    legend=False,
                    alpha=0.3,
                    ax=ax,
                    s=10,
                ).set(
                    xticklabels=[],
                    yticklabels=[],
                    xlabel=None,
                    ylabel=None,
                    title=f"over {over} ({n_clusters})",
                )

    def display_cluster_prob_tables(self, minimum_entries: int = 0):
        def title(inns, over) -> str:
            return f"## Innings {inns}, Over {over}"

        def table_hdr() -> str:
            return "\n".join(
                [
                    "| " + " | ".join(OUTCOME_DESCS) + " |",
                    "| " + " | ".join("---:" for _ in OUTCOME_DESCS) + " |",
                ]
            )

        def table_line(k, v) -> str:
            tot = sum(v.values())
            return (
                f"| {k:-2d} | {tot:-6d} | "
                + " | ".join(f"{v[i] / tot:8.2%}" for i in range(np.unique(outcomes).shape[0]))
                + " |"
            )

        for inns in range(2):
            for over in range(20):
                clf = self.clfs[inns][over]
                Xt = extract_values(self.train_dfs[inns][over], X_values)
                yt = extract_values(self.train_dfs[inns][over], y_values)
                scaled_Xt = SCALER_CLASSES["normalizer"].fit(Xt).transform(Xt)
                clf.fit(scaled_Xt)
                labels = clf.labels_
                outcomes = yt["outcome"]
                outcomes.reset_index(drop=True, inplace=True)

                res = {k: defaultdict(int) for k in np.unique(labels)}
                for i, label in enumerate(labels):
                    res[label][outcomes[i]] += 1

                body_lines = "\n".join(table_line(k, v) for k, v in res.items() if sum(v.values()) > minimum_entries)

                display(Markdown(title(inns, over) + "\n" + table_hdr() + "\n" + body_lines))
