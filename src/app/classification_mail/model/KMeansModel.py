from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import re
import nltk
import collections
from sklearn.metrics import silhouette_samples, silhouette_score
import pandas as pd

FILE = open("./c_usecase_gmail/resultat_clustering.txt", "w")

TOKENIZED_WORDS = ['import', 'px', 'width', 'class', 'pad', 'none', 'td', 'height', 'tabl', 'font', 'px', 'font',
                   'pad', 'margin', 'serif', 'helvetica', 'text', 'color', 'san', 'arial', 'read', 'your', 'thi',
                   'with', 'data', 'learn', 'from', 'email', 'that', 'have', 'bonjour', 'plu', 'compt', 'cordial',
                   'pari', 'mail', 'bien', 'tout', 'screen', 'content', 'don', 'imag', 'med', 'util', 'page',
                   'aur', 'aurion', 'auron', 'avi', 'avon', 'ayon', 'dan', 'e', 'euss', 'eussion', 'eûm',
                   'fuss', 'fussion', 'fûm', 'mêm', 'notr', 'ser', 'serion', 'seron', 'soi', 'somm', 'soyon',
                   'votr', 'éti', 'étion', 'ête', 'dat', 'hav', 'helvetic', 'non', 'decor', 'lin', 'underlin', 'bord',
                   'left', 'top', 'auto', 'display', 'padding', 'bottom', 'this', 'learning', 'about', 'mor', 'will',
                   'siz', 'decor', 'max', 'right', 'a', 'externalclass', 'img', 'block', 'align', 'body,', 'remerc',
                   'bon', 'merc', 'envoy', 'souhait', 'messag', 'fair', 'unsubscrib', 'mak', 'sent', 'help',
                   'vis', 'part', 'amp', 'com', 'cod', 'plus', 'messag', 'cet', 'servic', 'tous',
                   'inform', 'merc', 'pass', 'adress', 'souh', 'body', 'background', 'hov', 'span', 'styl', 'solid',
                   'family', 'cliqu', 'lien', 'fr', 'consult', 'pouv', 'lign', 'jour', 'utilis', 'demand', 'veuill',
                   'appliqu', 'don', 'chang', 'social', 'imag', 'min', 'only', 'equip', 'only', 'medi',
                   'plac', 'question', 'recevoir', 'relat', 'repondr', 'repons', 'reserv', 'googl', 'view', 'tim',
                   'aide', 'autre', 'bientot', 'cedex', 'cent', 'detail', 'direct', 'droit', 'espace', 'ete',
                   'etre', 'foot', 'hide', 'inlin', 'link', 'mobil', 'outlook', 'site', 'sous', 'suivie',
                   'trouve', 'weight', 'aid', 'autr', 'espac', 'hid', 'pag', 'repon', 'sit', 'style', 'time', 'use',
                   'veuillez', 'visit', 'merci', 'more', 'outlin', 'place', 'pouvez', 'rel', 'securit', 'size',
                   'size line', 'important', 'mcntextcontent',
                   'suiv', 'trouv', 'what', 'you', 'non', ',', 'bodi', 'capit', 'etr', 'famili', 'helvet',
                   'onli', 'sou', 'suivi', 'tou', 'utili', 'vi', 'applic', 'bonn', 'border', 'border border',
                   'center', 'cett', 'cliquez', 'code', 'commun', 'concern', 'consultez', 'date',
                   'float', 'footer', 'hover', 'line', 'make', 'media', 'souhaitez', 'francisco']


def body_to_words(raw_body):
    """
    Args:
        raw_body:

    Returns:

    """
    letters_only = re.sub("[^a-zA-Z]", " ", raw_body)
    text = re.sub('<[^<]+?>', '', letters_only)
    text_clean = ' '.join([w for w in text.split() if ((len(w) > 3) and (len(w) < 23))])
    words = text_clean.lower().split()
    stop_words = set(stopwords.words('french') + stopwords.words('english') + TOKENIZED_WORDS)
    meaningful_words = [w for w in words if w not in stop_words]
    # clean_words = [w for w in meaningful_words if w not in TOKENIZED_WORDS]
    return " ".join(meaningful_words)


def word_tokenizer(text):
    """
    Args:
        text:

    Returns:

    """
    tokens = word_tokenize(text, language='french')
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(t) for t in tokens if t not in (stopwords.words('french') + stopwords.words('english'))]
    return tokens


def tokenize_and_stem(text):
    """
    Args:
        text:

    Returns:

    """
    tokens = [word for sent in
              nltk.sent_tokenize(text, language='french') for word in nltk.word_tokenize(sent, language='french')]
    filtered_tokens = []
    stemmer = SnowballStemmer(language='french')
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    """
    first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    Args:
        text:

    Returns:

    """

    tokens = [word.lower() for sent in nltk.sent_tokenize(text, language='french') for word in
              nltk.word_tokenize(sent, language='french')]
    filtered_tokens = []

    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


def pre_processing_dataset(dataset_train):
    """Prepare dataset to list[dict] to do clustering in body
    Args:
        dataset_train:

    Returns:

    """
    num_reviews = dataset_train["body"].size

    clean_train_reviews = []
    for i in range(0, num_reviews):
        if (i + 1) % 1000 == 0:
            print("body %d of %d\n" % (i + 1, num_reviews))
        clean_train_reviews.append({'body': body_to_words(str(dataset_train["body"][i])),
                                    'idMail': dataset_train["idMail"][i]})

    print("Creating the bag of words...\n")
    return clean_train_reviews


def predict_clustering_group(k_means_model, tfidf_matrix):
    """
    Args:
        k_means_model:
        tfidf_matrix:

    Returns:

    """
    cluster_labels = k_means_model.fit_predict(tfidf_matrix)
    print('cluster_labels', cluster_labels)
    silhouette_avg = silhouette_score(tfidf_matrix, cluster_labels)
    print('silhouette_avg', silhouette_avg)
    sample_silhouette_values = silhouette_samples(tfidf_matrix, cluster_labels)
    print('sample_silhouette_values', sample_silhouette_values)
    centers = k_means_model.cluster_centers_
    print('centers', centers)
    n_clusters = centers.shape[0]
    print('n_clusters', n_clusters)
    return cluster_labels, silhouette_avg, sample_silhouette_values


def build_label_mails(vocab_frame, k_means_model, tfidf_vectorizer, clusters, clean_train_reviews, n_clusters):
    """
    Args:
        vocab_frame:
        k_means_model:
        tfidf_vectorizer:
        clusters:
        clean_train_reviews:
        n_clusters:

    Returns:

    """
    order_centroids = k_means_model.cluster_centers_.argsort()[:, ::-1]
    terms = tfidf_vectorizer.get_feature_names()

    label = []
    for cluster in range(n_clusters):
        cluster_label = []
        for ind in order_centroids[cluster, :n_clusters]:
            label_name = vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore')
            cluster_label.insert(cluster, label_name.decode('utf-8'))
        label.append(cluster_label)

    for cluster in range(n_clusters):
        FILE.write("cluster " + str(cluster) + ":" + "\n")
        FILE.write("centroid" + str(cluster) + "\n")

        for i, sentence in enumerate(clusters[cluster]):
            clean_train_reviews[sentence]['cluster_group'] = str(cluster)
            clean_train_reviews[sentence]['label'] = label[cluster]
            FILE.write("mail :" + str(i) + ": " + str(clean_train_reviews[sentence]) + "\n")

    centers = k_means_model.cluster_centers_

    return label


def build_cluster_from_model(n_clusters, tfidf_matrix):
    """
    Args:
        n_clusters:
        tfidf_matrix:

    Returns:
        dict(clusters):
        k_means_model:
    """
    k_means_model = KMeans(n_clusters=n_clusters,
                           init='k-means++',
                           max_iter=300,
                           n_init=1)

    k_means_model.fit(tfidf_matrix)

    clusters = collections.defaultdict(list)
    for i, label in enumerate(k_means_model.labels_):
        clusters[label].append(i)

    return dict(clusters), k_means_model


def build_tfidf_matrix_vector(dataset):
    """
    Args:
        dataset:

    Returns:
        tfidf_matrix:
        tfidf_vectorizer:
    """
    train_body = []
    for i in range(0, len(dataset)):
        train_body.append(dataset[i]['body'])

    tfidf_vectorizer = TfidfVectorizer(tokenizer=tokenize_and_stem,
                                       analyzer='word',
                                       stop_words=stopwords.words('french') +
                                                  TOKENIZED_WORDS +
                                                  stopwords.words('english'),
                                       max_df=0.8,
                                       min_df=0.1,
                                       lowercase=False,
                                       use_idf=True,
                                       max_features=200000,
                                       ngram_range=(1, 3))

    tfidf_matrix = tfidf_vectorizer.fit_transform(train_body)
    print(tfidf_matrix.shape)
    return tfidf_matrix, tfidf_vectorizer


def build_vocab_frame(clean_train_reviews):
    """ Build frame of vocabulary
    Args:
        clean_train_reviews(list): list of mails
    Returns:
        vocab_frame:
    """
    body = [mail['body'] for mail in clean_train_reviews]

    total_vocab_stemmed = []
    total_vocab_tokenized = []

    for i in body:
        allwords_stemmed = tokenize_and_stem(i)  # for each item in 'synopses', tokenize/stem
        total_vocab_stemmed.extend(allwords_stemmed)  # extend the 'totalvocab_stemmed' list

        allwords_tokenized = tokenize_only(i)
        total_vocab_tokenized.extend(allwords_tokenized)

    vocab_frame = pd.DataFrame({'words': total_vocab_tokenized}, index=total_vocab_stemmed)
    return vocab_frame
