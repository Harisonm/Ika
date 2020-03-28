from src.components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
import flask

HOME_URI = '/home'

"""
Usage: delete labels in mails
GET host:port/labelling/gmail/{name_file}

example : 
"""

app = flask.Blueprint('delete_label_util', __name__)


@app.route('/labelling/deleteAll/')
def delete_all_label():
    """Delete all labels.
    Args:
    """
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    labels = GmailDataFactory('prod').list_label('me')
    for label in labels:
        if label['type'] == 'user':
            GmailDataFactory('prod').delete_label_from_id('me',
                                                          label['id'])

    return flask.redirect(HOME_URI, code=302)


if __name__ == '__main__':
    pass
