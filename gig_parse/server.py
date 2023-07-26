from feedgen.feed import FeedGenerator
from flask import make_response, Flask
from os import listdir
from os.path import join, isfile, isdir
from os import walk
from .utils import DATA_DIR, GIGS_DIR, make_path
from datetime import date, timedelta, datetime


app = Flask("job_sorter")
N_ENTRIES = 100


def recurse_dirs(root) -> [str]:
    if isfile(root):
        return

    sub_dirs = [join(root, path) for path in listdir(root) if isdir(join(root, path))]
    dirs = []

    if sub_dirs:
        for d in sub_dirs:
            # print("root: ", d)
            tmp_dirs = recurse_dirs(d)

            if tmp_dirs:
                dirs += tmp_dirs
            else:
                dirs += sub_dirs

    return dirs


def get_recent_gigs() -> [str]:
    # days = recurse_dirs(GIGS_DIR)
    # days.sort()
    # print("days: ", days)
    today = date.today()
    yesterday = today - timedelta(days = 1)

    try:
        gigs = [(today, f) for f in listdir(make_path(today))]
    except FileNotFoundError:
        gigs = []

    try:
        gigs += [(yesterday, f) for f in listdir(make_path(yesterday))]
    except FileNotFoundError:
        pass

    return gigs


@app.route('/rss')
def rss_feed():
    fg = FeedGenerator()
    fg.title('recent job listings')
    fg.description('job listings from Upwork and the like')
    fg.link(href='http://127.0.0.1')
    # TODO: make N_ENTRIES a GET/POST param
    entries = get_recent_gigs()[0: N_ENTRIES]

    for date, path in entries: # get_news() returns a list of articles from somewhere
        path = join(make_path(date), path)
        contents = open(path, "r").readlines()
        fe = fg.add_entry()
        fe.title(path.split("/")[-1][:-3])
        # fe.link(href=contents[0].split("(")[1][:-2])
        fe.description("\n".join(contents))
        # fe.guid(article.id, permalink=False) # Or: fe.guid(article.url, permalink=True)
        # TODO: make author the site the gig came from
        # fe.author(name=article.author.name, email=article.author.email)
        
        # TODO: add date
        # fe.pubDate()

    response = make_response(fg.rss_str())
    response.headers.set('Content-Type', 'application/rss+xml')

    return response


def entry_point():
    app.run()
