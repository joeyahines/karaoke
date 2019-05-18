from flask import Blueprint, flash, g, redirect, render_template, request, url_for, send_file
from flask import current_app

import glob, os
import youtube_dl

from wtforms import Form, StringField, validators


class ConvertForm(Form):
    youtube_link = StringField('Youtube Link', [validators.Length(min=4, max=100)])


bp = Blueprint("convert", __name__)


@bp.route("/", methods=("GET", "POST"))
def index():
    form = ConvertForm(request.form)
    if request.method == 'POST' and form.validate():
        link = form.youtube_link.data
        filename = download_youtube(link)
        uploads = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename)
        return send_file(uploads, as_attachment=True, attachment_filename=filename)
    else:
        return render_template('home.html', form=form)


def download_youtube(url):
    path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
    ydl_opts = {
        "outtmpl": "{}/%(title)s.%(ext)s".format(path),
        "format": "worst",
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'avi',
        }],
        "restrictfilenames": True,
        "download_archive": os.path.join(path, "download.log")
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)

        title = youtube_dl.utils.sanitize_filename(info_dict["title"], restricted=True)

        if os.path.isfile(os.path.join(path, title + ".avi")):
            return title + ".avi"

        ydl.download([url])

    list_of_files = glob.glob(os.path.join(path, "*.avi"))
    latest_file = max(list_of_files, key=os.path.getctime)

    return os.path.basename(latest_file)