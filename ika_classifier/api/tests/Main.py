from api.classifier_mail.model.KMeansModel import *
from api.classifier_mail.model.Metrics import *
from helper.GmailHelper import GmailDataFactory
import pandas as pd
import nltk
import sys
import os

PATH = os.environ.get("PATH_SAVE_TRANSFORM", default=False)

nltk.download("punkt")
nltk.download("stopwords")


def build_label_mail(data):
    """
    Args:
        data:

    Returns:

    """
    train = pd.read_csv(PATH + data, encoding="utf-8")

    clean_train_reviews = pre_processing_dataset(train)

    vocab_frame = build_vocab_frame(clean_train_reviews)

    tfidf_matrix, tfidf_vectorizer = build_tfidf_matrix_vector(clean_train_reviews)

    # calculating the within clusters sum-of-squares for 19 cluster amounts
    sum_of_squares = calculate_wcss(tfidf_matrix)

    # calculating the optimal number of clusters
    n_clusters = optimal_number_of_clusters(sum_of_squares)

    clusters, k_means_model = build_cluster_from_model(n_clusters, tfidf_matrix)

    # cluster_labels, silhouette_avg, sample_silhouette_values = predict_clustering_group(k_means_model, tfidf_matrix)

    labels = build_label_mails(
        vocab_frame,
        k_means_model,
        tfidf_vectorizer,
        clusters,
        clean_train_reviews,
        n_clusters,
    )

    for mail in clean_train_reviews:
 
        for lbl in mail["label"][:1]:
            GmailDataFactory("dev").create_label(
                "me",
                name_label=lbl,
                label_list_visibility="labelShow",
                message_list_visibility="show",
            )
        labels_ids = GmailDataFactory("dev").get_label_ids("me", mail["label"])

        GmailDataFactory("dev").modify_message(
            user_id="me",
            mail_id=mail["idMail"],
            mail_labels=create_msg_labels(labels_ids[:1]),
        )


def create_msg_labels(labels_ids):
    """Create object to update labels.

    Returns:
      A label update object.
    """
    return {"removeLabelIds": [], "addLabelIds": labels_ids}


if __name__ == "__main__":
    arg1 = str(sys.argv[1])
    build_label_mail(arg1)
