# if ENV == "production":
#     len_labels = len(labels[0])
#     return flask.redirect(flask.url_for('google_auth.home_page',
#                                         code=302,
#                                         len_labels=len_labels,
#                                         mails=clean_train_reviews))