from __future__ import unicode_literals
import glob, os, shutil
import youtube_dl


import argparse

parser = argparse.ArgumentParser(description='Karokee My Dudes')
parser.add_argument('youtube_url', metavar='url', type=str, nargs='+',
                    help='Youtube Video Url')
parser.add_argument('--output', dest='output_dir', action='store',
                    help='output directory')

if __name__ == "__main__":
    args = parser.parse_args()

    if args.output_dir is not None:
        dest_dir = args.output_dir
    else:
        dest_dir = None

    ydl_opts = {
        "format": "worst",
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'avi',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:

        ydl.download(args.youtube_url)

    if dest_dir is not None:
        files = glob.iglob(os.path.join(".", "*.avi"))

        for file in files:
            if os.path.isfile(file):
                shutil.copy2(file, dest_dir)