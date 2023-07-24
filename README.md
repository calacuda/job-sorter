# Job Sorter

Job Sorter will sort jobs based on their description using naive bayesian classification.

## Compatibility

- Upwork
- LinkedIn (planned)
- Indeed (planned)
- GlassDoor (planned)

## Usage

1. [train a model](#training-a-model)
2. run the model with a link to the data. i.e: `gig-parse --model /PATH/TO/MODEL upwork 'https://www.upwork.com/ab/feed/jobs/rss?q=...`

## Training a Model

generate a CSV file with two columns; `text` and `alert`. the `text` column store the job desctiption in the format: `listing title: listing description`. the `alert` column should contain either `True` or `False` representing if the user should be informed of the listing. I made my CSV using Pandas, but yours can be made using what ever tool you comforatble with.

## TODOs

- [ ] separate the notification and prediction functions to a "utils.py" file
- [ ] write a csv maker
- [ ] add a LinkedIn parser
- [ ] add a Indeed parser
- [ ] add a Glassdoor parser
