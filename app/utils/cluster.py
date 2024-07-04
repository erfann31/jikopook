from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score


def cluster_extracted_data(extracted_data):
    # لیستی برای ذخیره متون
    texts = []
    for site, links in extracted_data.items():
        texts.extend(links.keys())

    # Step 1: Vectorize the texts
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(texts)

    # Step 2: Determine the optimal number of clusters using the elbow method
    def find_optimal_clusters(data, max_k):
        iters = range(2, max_k + 1)
        sse = []
        silhouette_scores = []
        for k in iters:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
            kmeans.fit(data)
            sse.append(kmeans.inertia_)
            score = silhouette_score(data, kmeans.labels_)
            silhouette_scores.append(score)
        return iters, sse, silhouette_scores

    # Limit the max_k to avoid ValueError
    max_k = min(len(texts) - 1, 10)
    iters, sse, silhouette_scores = find_optimal_clusters(X, max_k)

    # Step 3: Perform KMeans clustering with the optimal number of clusters
    optimal_clusters = iters[silhouette_scores.index(max(silhouette_scores))]
    kmeans = KMeans(n_clusters=optimal_clusters, random_state=42, n_init='auto')
    kmeans.fit(X)
    labels = kmeans.labels_

    # Step 4: Find top terms in each cluster to generate titles
    def generate_cluster_titles(kmeans, vectorizer, num_clusters, top_n=3):
        order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names_out()
        cluster_titles = []
        for i in range(num_clusters):
            top_terms = [terms[ind] for ind in order_centroids[i, :top_n]]
            cluster_title = " ".join(top_terms)
            cluster_titles.append(cluster_title)
        return cluster_titles

    # Generate titles for each cluster
    cluster_titles = generate_cluster_titles(kmeans, vectorizer, optimal_clusters)

    # Step 5: Create a map to display results
    cluster_map = {}
    for i in range(optimal_clusters):
        cluster_map[cluster_titles[i]] = []

    for text, label in zip(texts, labels):
        cluster_map[cluster_titles[label]].append(text)

    return cluster_map
