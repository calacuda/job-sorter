from os.path import expanduser, join, isfile, exists
from os import listdir
from pathlib import Path
from plyer import notification
import json
import argparse
from .train import entry_point as train
from .upwork import entry_point as upwork 
from .server import entry_point as server_start
from .utils import get_configs


def get_args():
    """returns arguments made using argsparse"""
    parser = argparse.ArgumentParser(
                    prog='gig-parse',
                    description='automatically sort gigs from various sources')
    # parser.add_argument("--model", dest="model", required=True, help="the model to use, or when training, this is the fiel path to save the model to.")

    subparsers = parser.add_subparsers(required=True)
    
    upw_parser = subparsers.add_parser('upwork')
    # upw_parser.add_argument("url", help="the url to request RSS feed data from.")
    # upw_parser.add_argument("-m", "--model", dest="model", required=True, help="the model to use to classify jobs.")
    upw_parser.set_defaults(func=upwork)

    train_parser = subparsers.add_parser('train')
    train_parser.add_argument("csv", help="the csv to train based on. should have a column called 'text', containing the text description of the gig, and one called 'alert', deffines wether the user should be alerted (1 for alert, 0 for not alert)")
    train_parser.add_argument("-o", "--output", dest="model", required=True, help="the file path to save the model to. (note that the file extension \".pkl\" will be added automatically if not present)")
    train_parser.set_defaults(func=train)

    server = subparsers.add_parser('server')
    server.set_defaults(func=server_start)

    return parser.parse_args()



def run_cli():
    """runs the cli"""
    # print(f"found {len(good_gigs)} gigs to look into.")
    args = get_args()
    # print(args)
    # print("=" * 80)
    configs = get_configs()

    args.func(args, configs)
    


if __name__ == "__main__":
    run_cli()
