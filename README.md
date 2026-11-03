# What Keeps a Reddit Rivalry Alive?

We study how negative references between Reddit communities change over time. We distinguish declining negativity while contact continues from sparse activity or silence, and examine whether audience similarity and reciprocal negativity are associated with these paths.

## Research questions

1. After repeated negative references between two communities, does interaction continue, become sparse, or stop during follow-up?
2. When enough interaction continues, does the proportion of negative references decline, and is this change associated with audience similarity or baseline negativity in both directions?
3. As an optional extension, are shared negative targets associated with different trajectories?

We study observed linking behaviour and associations; these questions do not establish what causes a relationship to change.

## Data

We use the [Reddit Hyperlink Network](https://snap.stanford.edu/data/soc-RedditHyperlinks.html) and [subreddit embeddings](https://snap.stanford.edu/data/web-RedditEmbeddings.html). Hyperlinks provide source and target communities, timestamps, negativity labels and source-post features. Embeddings describe community participation patterns.

A nonnegative link can be neutral or positive. Negative references alone do not establish attacks, and declining negativity does not establish reconciliation.

## Current progress

The notebook loads all three files, inspects their structure, checks data quality and embedding coverage, and prepares links for January 2014–April 2017. The prepared data contains 858,454 links across 67,178 communities. Pair-level trajectories and explanatory comparisons are the next analysis stages.

## Quickstart

From the repository root, create a Python 3.11 environment:

```bash
conda create -n ada-project-26 python=3.11 pip
conda activate ada-project-26
python -m pip install -r pip_requirements.txt
python -m pip install ipykernel
```

Download the following files from the dataset pages into `data/raw/`:

- `soc-redditHyperlinks-body.tsv`
- `soc-redditHyperlinks-title.tsv`
- `web-redditEmbeddings-subreddits.csv`

Open `results.ipynb` in Jupyter or VS Code, select the environment as its kernel, and run all cells from the repository root. Raw data is excluded from Git.

## Project structure

- `results.ipynb`: explanations, data inspection and analysis results.
- `src/data/`: loading, feature schema, validation and preprocessing.
- `src/utils/`: reusable analysis utilities, including embedding coverage.
- `src/models/`: model implementations.
- `src/scripts/`: standalone scripts.
- `data/`: local datasets.
- `tests/`: automated tests.
- `pip_requirements.txt`: Python dependencies.
