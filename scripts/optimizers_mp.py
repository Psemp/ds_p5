import concurrent.futures
import pandas

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def get_k_means_score(data: pandas.DataFrame, k: int):
    if k <= 1:
        raise ValueError("Invalid K value in k_range : cannot calculate for k <= 1")
    km = KMeans(n_clusters=k)
    y_predicted = km.fit_predict(data)
    sil = silhouette_score(data, y_predicted)
    inertia = (km.inertia_)
    return k, inertia, sil


def k_means_optimizer(data: pandas.DataFrame, k_range: list, fig_ovr: dict = None, show: bool = True) -> None | Figure:

    k_dict = dict.fromkeys(k_range)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(get_k_means_score, data, k) for k in k_range]

    for p in concurrent.futures.as_completed(results):
        result = (p.result())
        k_p = result[0]
        inertia = result[1]
        silhouette = result[2]
        k_dict[k_p] = (inertia, silhouette)

    # return k_dict
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

    fig, (ax1, ax2) = plt.subplots(
        ncols=2,
        nrows=1,
        figsize=fig_size,
        dpi=pc_dpi,
    )

    sse_dict = {}
    silhouette_dict = {}
    for key in k_dict:
        sse_dict[key] = k_dict[key][0]
        silhouette_dict[key] = k_dict[key][1]

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
