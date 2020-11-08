from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from app.api.model.KMeansModel import *
from app.api.model.Metrics import *
from app.api.database.mongo import mdb
from ikamail.GmailHelper import GmailHelper
from typing import List
import pandas as pd
import nltk
import os

PATH = os.environ.get("PATH_FILE", default=False)
ENV = os.environ.get("ENV", default=False)
HOME_URI = os.environ.get("HOME_URI", default=False)
GOOGLE_GMAIL_URI = os.environ.get("GOOGLE_GMAIL_URI", default=False)

nltk.download("punkt")
nltk.download("stopwords")
"""
Usage: build labels in mails from clustering Model
GET host:port/labelling/gmail/{name_file}

example : 
"""

classifier = APIRouter()

@classifier.get('/labelling/build')
async def build_label_mail():
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
        return RedirectResponse("http://127.0.0.1:8000/")
    else:
        for mail in clean_train_reviews:
            # print(mail)
            # print(mail['idMail'])
            for lbl in mail["label"][:1]:
                GmailHelper("prod").create_label(
                    "me",
                    name_label=lbl,
                    label_list_visibility="labelShow",
                    message_list_visibility="show",
                )
            labels_ids = GmailHelper("prod").get_label_ids("me", mail["label"])

            GmailHelper("prod").modify_message(
                user_id="me",
                mail_id=mail["idMail"],
                mail_labels=create_msg_labels(labels_ids[:1]),
            )

    return RedirectResponse("http://127.0.0.1:8000/")

@classifier.get('/labelling/deleteAll/')
async def delete_all_label():
    """Delete all labels.
    Args:
    """
    labels = GmailHelper("prod").list_label("me")
    for label in labels:
        if label["type"] == "user":
            GmailHelper("prod").delete_label_from_id("me", label["id"])

    return RedirectResponse("http://127.0.0.1:8000/")


@classifier.get("/labelling/create/")
async def create_label_mails(requests):
    clean_train_reviews = requests.form["mails"]
    len_labels = requests.form["len_labels"]

    for mail in clean_train_reviews:
        for lbl in mail["label"][:len_labels]:
            GmailHelper("prod").create_label(
                "me",
                name_label=lbl,
                label_list_visibility="labelShow",
                message_list_visibility="show",
            )
        labels_ids = GmailHelper("prod").get_label_ids("me", mail["label"])

        GmailHelper("prod").modify_message(
            user_id="me",
            mail_id=mail["idMail"],
            mail_labels=create_msg_labels(labels_ids[:1]),
        )
    return RedirectResponse("http://127.0.0.1:8000/")


def create_msg_labels(labels_id):
    """Create object to update labels.
    Args:
        labels_id:
    Returns:
      A label update object.
    """
    return {"removeLabelIds": [], "addLabelIds": labels_id}
