from src.ika_classifier.api.model.KMeansModel import *
from src.ika_classifier.api.model.Metrics import *
from src.ika_classifier.api.helper.GmailHelper import GmailDataFactory
from src.ika_classifier.api.database.mongo import mdb
import pandas as pd
import flask
import nltk
import os

PATH = os.environ.get("PATH_FILE", default=False)
ENV = os.environ.get("FLASK_ENV", default=False)
HOME_URI = os.environ.get("HOME_URI", default=False)
GOOGLE_GMAIL_URI = os.environ.get("GOOGLE_GMAIL_URI", default=False)

nltk.download("punkt")
nltk.download("stopwords")
"""
Usage: build labels in mails from clustering Model
GET host:port/labelling/gmail/{name_file}

example : 
"""

app = flask.Blueprint("labelling", __name__)


@app.route("/api/v1/labelling/", methods=["GET", "POST"])
def build_label_mail():
    """method to build label from clustering Model
    this function take word, convert its to vector, calculate distance between vector from elbow method and using Kmeans.
    Args:
        name_file:

    Returns:

    """
    mycol = mdb["streamer"]
    train = pd.DataFrame(list(mycol.find()))
    
    clean_train_reviews = pre_processing_dataset(train)

    vocab_frame = build_vocab_frame(clean_train_reviews)

    tfidf_matrix, tfidf_vectorizer = build_tfidf_matrix_vector(clean_train_reviews)

    # calculating the within clusters sum-of-squares for 19 cluster amounts
    # calculating the optimal number of clusters
    n_clusters = optimal_number_of_clusters(calculate_wcss(tfidf_matrix))

    clusters, k_means_model = build_cluster_from_model(n_clusters, tfidf_matrix)

    labels = build_label_mails(
        vocab_frame,
        k_means_model,
        tfidf_vectorizer,
        clusters,
        clean_train_reviews,
        n_clusters,
    )

    if ENV == "production":
        len_labels = len(labels[0])
        return flask.redirect(
            flask.url_for(
                "google_auth.home_page",
                code=302,
                len_labels=len_labels,
                mails=clean_train_reviews,
            )
        )
    else:
        for mail in clean_train_reviews:
            # print(mail)
            # print(mail['idMail'])
            for lbl in mail["label"][:1]:
                GmailDataFactory("prod").create_label(
                    "me",
                    name_label=lbl,
                    label_list_visibility="labelShow",
                    message_list_visibility="show",
                )
            labels_ids = GmailDataFactory("prod").get_label_ids("me", mail["label"])

            GmailDataFactory("prod").modify_message(
                user_id="me",
                mail_id=mail["idMail"],
                mail_labels=create_msg_labels(labels_ids[:1]),
            )

        return flask.redirect(flask.url_for("google_auth.home_page", code=302))

@app.route("/api/v1/labelling/deleteAll/")
def delete_all_label():
    """Delete all labels.
    Args:
    """
    labels = GmailDataFactory("prod").list_label("me")
    for label in labels:
        if label["type"] == "user":
            GmailDataFactory("prod").delete_label_from_id("me", label["id"])

    return flask.redirect(HOME_URI, code=302)


@app.route("/labelling/create/", methods=["POST"])
def create_label_mails(requests):
    clean_train_reviews = requests.form["mails"]
    len_labels = requests.form["len_labels"]

    for mail in clean_train_reviews:
        for lbl in mail["label"][:len_labels]:
            GmailDataFactory("prod").create_label(
                "me",
                name_label=lbl,
                label_list_visibility="labelShow",
                message_list_visibility="show",
            )
        labels_ids = GmailDataFactory("prod").get_label_ids("me", mail["label"])

        GmailDataFactory("prod").modify_message(
            user_id="me",
            mail_id=mail["idMail"],
            mail_labels=create_msg_labels(labels_ids[:1]),
        )

    return flask.redirect(GOOGLE_GMAIL_URI, code=302)


def create_msg_labels(labels_id):
    """Create object to update labels.
    Args:
        labels_id:
    Returns:
      A label update object.
    """
    return {"removeLabelIds": [], "addLabelIds": labels_id}
