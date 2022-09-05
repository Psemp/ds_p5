import pandas

from collections import namedtuple
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score


def optimize_kmeans(data: pandas.DataFrame, k_range: list, fig_ovr: dict = None, show: bool = True) -> None | Figure:
    """
    Function :
    - Helper function to plot Silhouette score and Sum Squared Error to aid the selection of optimal K for K means
    using elbow method

    Args :
    - data : pandas.DataFrame containing only the values relevant to k-means execution
    - k-range : list of k candidates which will be tested and plotted
    - fig_ovr : optional dictionary containing DPI and fig_size if user wants to override the default params
    - show : boolean, default = True, if show = False, returns pyplot.gcf() matplotlib.figure.Figure object

    Returns :
    - None (plt.show()) | matplotlib.figure.Figure object
    """

    if fig_ovr is not None:
        try:
            pc_dpi = fig_ovr["DPI"]
        except KeyError:
            pass
        try:
            fig_size = fig_ovr["figize"]
        except KeyError:
            pass
    else:
        pc_dpi = 150
        fig_size = (10, 5)

    sse_dict = {}
    silhouette_dict = {}

    for k in k_range:
        if k <= 1:
            raise ValueError("Invalid K value in k_range : cannot calculate for k <= 1")
        km = KMeans(n_clusters=k)
        y_predicted = km.fit_predict(data)
        sil = silhouette_score(data, y_predicted)
        sse_dict[k] = (km.inertia_)
        silhouette_dict[k] = sil

    fig, (ax1, ax2) = plt.subplots(
        ncols=2,
        nrows=1,
        figsize=fig_size,
        dpi=pc_dpi,
    )

    ax1.plot(sse_dict.keys(), (sse_dict.values()), marker="x", color="navy")
    ax2.plot(silhouette_dict.keys(), silhouette_dict.values(), marker="x", color="navy")

    ###
    # Titles/Lables
    fig.supxlabel("Number of clusters")
    ax1.set_ylabel("Sum of squared Errors")
    ax1.set_xticks(k_range)
    ax2.set_ylabel("Silhouette score")
    ax2.set_xticks(k_range)
    fig.suptitle("Metric as increasing number of clusters")
    #
    ###
    plt.tight_layout()

    if show:
        plt.show()
    elif not show:
        return plt.gcf()


def dbscan_optimizer(eps_list, min_sample_list, data=pandas.DataFrame) -> dict:

    Couple_hp = namedtuple("Couple_hp", ["eps", "min_sample"])
    metrics = {}

    for eps in eps_list:
        for min_sample in min_sample_list:
            dbscan = DBSCAN(eps=eps, min_samples=min_sample)
            y_predicted = dbscan.fit_predict(data)
            try:
                sil = silhouette_score(data, y_predicted)
                metrics[sil] = Couple_hp(eps=eps, min_sample=min_sample)
            except ValueError:
                continue

    return metrics
