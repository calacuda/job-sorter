from feedparser import parse, parsers
from markdownify import markdownify
from os.path import expanduser, join, isfile, exists
from os import listdir
from pathlib import Path
from plyer import notification
import json
import pickle
from hashlib import sha256


N_GIGS = 100
HIST_LEN = N_GIGS * 3
DATA_DIR = expanduser("~/.local/share/upwork-rss/")
# stores hashes of the gigs that have been proccessed.
# this ensures that the user only get promted abhout the gig once.
HIST_FILE = join(DATA_DIR, "job-history.lst")
SPAM_FILE = join(DATA_DIR, "spam.json")
GIG_DIR = join(DATA_DIR, "gigs/")


class UpworkGig:
    def __init__(self, link: str, title: str, desc: str):
        self.link = link
        self.title = title
        self.desc = desc
        self.hash = sha256(self.str().encode("utf-8")).hexdigest()
        # self.set_hash()

    def __str__(self):
        loc_desc = markdownify(self.desc)
        return f"# [{self.title}]({self.link})\n{loc_desc}"

        # def set_hash(self):
        #     """sets self.hash to get a unique identifier"""
        #     self.hash = hash(str(self))

    def str(self):
        return f"{self.title}: {self.desc}"

    def is_new(self) -> bool:
        """returns true if this gig has not been proccessed yet"""
        if isfile(HIST_FILE): 
            with open(HIST_FILE, "r") as history:
                return self.hash not in history.read()
        else:
            return False

def make_gig(gig) -> UpworkGig:
    """self explanitory and prob unnessesary."""
    return UpworkGig(gig.link, gig.title, gig.content[0].value)


def get_new_gigs(url: str) -> [UpworkGig]:
    """takes an RSS url. returns an list of tuples. the first element of these tuples is a link to the job posting. """
    return [
        gig for gig in 
            [make_gig(e) for e in parse(url).entries] 
        if gig.is_new()
    ]


def record_gigs(good_gigs: [UpworkGig], bad_gigs: [UpworkGig]):
    """puts new hashes in the HIST_FILE"""
    hashes = [gig.hash for gig in good_gigs + bad_gigs]
    print(f"{len(good_gigs)}/{len(bad_gigs)}")

    with open(HIST_FILE, "r") as history:
        hashes = history.readlines()[-HIST_LEN + len(hashes):] + hashes    
    
    with open(HIST_FILE, "w") as history:
        [history.write(hash.strip() + "\n") for hash in hashes]
        history.write("\n")
        # for hash in history.readlines()[-HIST_LEN + len(hashes):] + hashes:
        #     print(type(hash), f"{hash}")

    with open(SPAM_FILE, "r") as spam:
        spam_messages = json.loads(spam.read()) + [str(gig) for gig in bad_gigs]
    
    with open(SPAM_FILE, "w") as spam:
        spam.write(json.dumps(spam_messages))


def filter_gigs(gigs: [UpworkGig], model: str) -> [UpworkGig]:
    """returns a list of good gigs that the user should look into"""
    # TODO: filter using Naive Bayesian spam filtering
    model, v = pickle.load(open(model, "rb"))
    counts = v.transform([str(gig) for gig in gigs])
    predictions = model.predict(counts)
    # print(len(predictions), "predictions", predictions[0:10])
    # predictions = predictions
    # print(len([gigs[i] for i, p in predictions if not p]))

    return ([gigs[i] for i, p in enumerate(predictions) if p], [gigs[i] for i, p in enumerate(predictions) if not p]) 


def notify_user(good_gigs: [UpworkGig]):
    """sends a notification to the user with information about the good gigs"""
    # make a new diretory in gigs_dir.
    md_dirs = listdir(GIG_DIR)
    md_dirs = md_dirs if md_dirs else ["0"]
    next_dir = max(int(d) for d in md_dirs) + 1
    p = join(GIG_DIR, str(next_dir))
    path = Path(p)
    path.mkdir(parents=True, exist_ok=False)
    
    # write to markdown files in a dir.
    for gig in good_gigs:
        with open(join(p, gig.title.replace("/", "\\") + ".md"), "w") as f:
            f.write(str(gig))
            f.write("\n")

    # send system notif with directory name.
    notification.notify(title = 'New upwork gigs', message = f"Path: {p}", app_icon = '', timeout = 15)

    # TODO: send discord message with path and each gig (as markdown)

    pass


def ensure_files():
    """ensures all directories and files exist. if not, it makes them with default values."""
    if not exists(GIG_DIR):
        path = Path(GIG_DIR)
        path.mkdir(parents=True, exist_ok=True)
    
    for path, contents in [(SPAM_FILE, "[]"), (HIST_FILE, "")]: 
        if not isfile(path):
            with open(path, "w") as f:
                print(path, contents)
                f.write(contents)


def entry_point(args):
    """runs the cli"""
    ensure_files()
    # args = get_args()
    url = args.url
    model = args.model
    gigs = get_new_gigs(url)
    print(f"sorting {len(gigs)} new gigs")
    
    if not gigs:
        return

    good_gigs, bad_gigs = filter_gigs(gigs, model)
    print(f"{len(good_gigs)} good_gigs | {len(bad_gigs)} bad_gigs")
    record_gigs(good_gigs, bad_gigs)
    print(f"found {len(good_gigs)} gigs to look into.")
    
    if good_gigs:
        notify_user(good_gigs)


if __name__ == "__main__":
    entry_point()
