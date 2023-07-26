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

Generate a CSV file with two columns; `text` and `alert`. The `text` column store the job desctiption in the format: `listing title: listing description`. The `alert` column should contain either `True` or `False` representing if the user should be informed of the listing. I made my CSV using Pandas, but yours can be made using what ever tool you comforatble with.

## TODOs

For a more detailed TODO list see: [todo.md](todo.md).

- [x] **1.** add an RSS feed server that serves recent job listings
- [x] **2.** catagorize gigs by date
- [ ] **3.** add discord messaging
- [ ] **4.** write a csv maker
- [ ] **5.** add a LinkedIn parser
- [ ] **6.** add a Indeed parser
- [ ] **7.** add a Glassdoor parser
