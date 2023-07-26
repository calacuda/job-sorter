from os.path import expanduser, join, isfile, exists
from pathlib import Path
from markdownify import markdownify
from datetime import datetime
from hashlib import sha256
from plyer import notification
import pickle


DATA_DIR = expanduser("~/.local/share/gig-parser/")
GIGS_DIR = join(DATA_DIR, "gigs")
HIST_FILE = join(DATA_DIR, "job-history.lst")
SPAM_FILE = join(DATA_DIR, "spam.json")


class Gig:
    def __init__(self, link: str, title: str, desc: str):
        self.link = link
        self.title = title.replace("\n", "")
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


def make_path(date):
    path = GIGS_DIR

    for d in [date.year, date.month, date.day]:
        path = join(path, str(d))
        # print(path)

    return path


def get_dir():
    """gets the next dir to use to store gigs"""
    date = datetime.now()

    path = make_path(date)

    # print(path)

    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)

    return p


def filter_gigs(gigs: [Gig], model: str) -> [Gig]:
    """returns a list of good gigs that the user should look into"""
    # TODO: filter using Naive Bayesian spam filtering
    model, v = pickle.load(open(model, "rb"))
    counts = v.transform([gig.str() for gig in gigs])
    predictions = model.predict(counts)

    return ([gigs[i] for i, p in enumerate(predictions) if p], [gigs[i] for i, p in enumerate(predictions) if not p])


def ensure_files(paths: [str]):
    """ensures all directories and files exist. if not, it makes them with default values."""
    # if not exists(GIG_DIR):
    #     path = Path(GIG_DIR)
    #     path.mkdir(parents=True, exist_ok=True)

    for path in paths:
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
    
    for path, contents in [(SPAM_FILE, "[]"), (HIST_FILE, "")]: 
        if not isfile(path):
            with open(path, "w") as f:
                print(path, contents)
                f.write(contents)


def notify_user(good_gigs: [Gig]):
    """sends a notification to the user with information about the good gigs"""
    # make a new diretory in gigs_dir.
    # md_dirs = listdir(GIG_DIR)
    # md_dirs = md_dirs if md_dirs else ["0"]
    next_dir = get_dir()  # max(int(d) for d in md_dirs) + 1
    # p = join(GIG_DIR, str(next_dir))
    # path = Path(p)
    # path.mkdir(parents=True, exist_ok=False)
    
    # write to markdown files in a dir.

    for gig in good_gigs:
        with open(join(next_dir, gig.title.replace("/", "\\") + ".md"), "w") as f:
            f.write(str(gig))
            f.write("\n")

    # send system notif with directory name.
    notification.notify(title = 'New upwork gigs', message = f"Path: {next_dir}", app_icon = '', timeout = 15)

    # TODO: send discord message with path and each gig (as markdown)
