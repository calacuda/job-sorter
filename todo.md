# TODO

- [x] separate the notification and prediction functions to a "utils.py" file
- [x] add an RSS feed server that serves recent job listings
- [x] catagorize gigs by date
- [ ] catagorize gigs by date **& source** (in fomrat "GIG_DIR/{source}/{year}/{month}/{day}/gig")
- [ ] add discord messaging notifs
  - [ ] add toml config file with:
    - discord settings (message target (channel and server or user). wether to message server, user, or both.)
    - locations for the models for Upwork, LinkedIn, Indeed, & Glassdoor
  - [ ] add command line arg to NOT notify via discord
  - [ ] add command line arg to NOT notify via desktop notifs
- [ ] write a CSV maker
- [ ] add cmd-line arg to pull jobs from all sources at one time
- [ ] add a LinkedIn parser
- [ ] add a Indeed parser
- [ ] add a Glassdoor parser
