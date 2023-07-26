from feedparser import parse, parsers
import json
import pickle
from .utils import *


N_GIGS = 100
HIST_LEN = N_GIGS * 3
# DATA_DIR = join(DATA_DIR, "/upwork/")
# stores hashes of the gigs that have been proccessed.
# this ensures that the user only get promted abhout the gig once.


def make_gig(gig) -> Gig:
    """self explanitory and prob unnessesary."""
    return Gig(gig.link, gig.title, gig.content[0].value)


def get_new_gigs(url: str) -> [Gig]:
    """takes an RSS url. returns an list of tuples. the first element of these tuples is a link to the job posting. """
    return [
        gig for gig in 
            [make_gig(e) for e in parse(url).entries] 
        if gig.is_new()
    ]


def record_gigs(good_gigs: [Gig], bad_gigs: [Gig]):
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


def entry_point(args):
    """runs the cli"""
    ensure_files([DATA_DIR])
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
