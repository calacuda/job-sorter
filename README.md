# Job Sorter

Job Sorter will sort jobs based on their description using naive bayesian classification.

## Compatibility

- Upwork
- LinkedIn (planned)
- Indeed (planned)
- GlassDoor (planned)

## Usage

1. [train a model](#Training a Model)
2. run the model with a link to the data. i.e: `gig-parse --model /PATH/TO/MODEL upwork 'https://www.upwork.com/ab/feed/jobs/rss?q=...`

## Training a Model

generate a CSV file with two columns; `text` and `alert`. the `text` column store the job desctiption in the format: `listing title: listing description`. the `alert` column should contain either `True` or `False` representing if the user should be informed of the listing. I made my CSV using Pandas, but yours can be made using what ever tool you comforatble with.
