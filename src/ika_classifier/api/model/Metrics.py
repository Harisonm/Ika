from sklearn.cluster import KMeans
from math import sqrt


def optimal_number_of_clusters(wcss):
    """Calculates the greatest distance between the points that mark the
    sum of intra-cluster squares for 19 calculated squares
    with `calculate_wcss()`

    Args
        wcss(list): list containing the intra-cluster sum of squares values
    Returns
    """

    x1, y1 = 2, wcss[0]
    x2, y2 = 20, wcss[len(wcss) - 1]

    distances = []
    for i in range(len(wcss)):
        x0 = i + 2
        y0 = wcss[i]

        numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        denominator = sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        distances.append(numerator / denominator)
    return distances.index(max(distances)) + 2


def calculate_wcss(data):
    """Calculates the sum of intra-cluster squares for 19
    number of clusters, starting with a minimum of 2 clusters

    Args:
        data(DateFrame) : data set to do the `.fit()` of KMeans

    Returns:
        wcss(list) : list containing the values of intra-cluster sum of squares
    """

    wcss = []
    for n in range(2, 21):
        kmeans = KMeans(n_clusters=n)
        kmeans.fit(X=data)
        wcss.append(kmeans.inertia_)

    return wcss
