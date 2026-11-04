# Sparks and Wildfires on Reddit

## Abstract

Subreddits often link to each other and sometimes it is to make fun of or attack another community. These attacks are not harmless since they can affect the communities they target. We wanted to understand what happens after such an attack. Our first idea was that conflicts spread like fire: one attack brings another, other communities join and it gets bigger and bigger. With more than 850,000 links between 2014 and 2017, each marked as negative or not, we can check if this idea is right. We also look at what lights these fires in the first place and what the communities behind them have in common, to better understand the nature of conflicts on Reddit. This could help Reddit know where to act: stop conflicts from spreading or keep an eye on what starts them.

## Research Questions

Central question: do conflicts between Reddit communities spread like fire?

1. Does one attack lead to more? We check if the target hits back and if other communities join in.
2. Does a common enemy make allies? We check if communities that attack the same target get closer or fight each other too.
3. Do conflicts burn out? We follow pairs of communities with many attacks between them and see if the conflict goes on, calms down or stops.
4. What lights the fires? We study the communities that attack the most and what they have in common. We also check if events like the 2016 US election make attacks more frequent.

## Proposed Additional Datasets

None. We use the two datasets given with the project, the [Reddit Hyperlink Network](https://snap.stanford.edu/data/soc-RedditHyperlinks.html) and the [subreddit embeddings](https://snap.stanford.edu/data/web-RedditEmbeddings.html).

The hyperlink data has 858,488 links between subreddits, in a title file and a body file (about 690 MB). For each link we have the source and target communities, a timestamp, a negativity label and 86 features of the source post.

The embeddings describe community participation patterns for 51,278 subreddits. Two subreddits are close when the same users post in both.

For RQ4 we also write a short list of event dates and the subreddits they concern.

## Methods

**RQ1.** After A attacks B, we look at the next days and weeks. We check if B attacks A back, how fast, and if other communities also attack B. We compare with what happens after a normal link from A to B, to check that it is really a reply and not just two communities that always fight.

**RQ2.** We take two communities that start attacking the same target and count the links between them in the months before and after. If a common enemy makes them allies, they should link more and attack each other less. We compare with communities that attack as much but choose their targets at random, so that very hostile communities do not change the result.

**RQ3.** We take pairs with many attacks in a short time and follow them each month for one year. We put them in three groups: the conflict goes on, it calms down but they still link, or it stops because they stop linking. Pairs taken at their worst moment can look calmer later just by chance, so we take this into account.

**RQ4.** We look for communities that attack much more than the others, check if they are the same over the years and see who they attack using the embeddings. We also do RQ1 again without them. For events like the 2016 US election, we compare attacks before and after the event with other dates.

**Dropped.** We also had the idea to check if a community starts to write like its attacker.

## Proposed Timeline

| Period | Tasks |
|---|---|
| Until 6/11 (P2) | Data pipeline, descriptive statistics, first analyses, proposal |
| 7/11 to 15/11 | Milestone 1a: first version of RQ1, RQ2 and RQ3 |
| 16/11 to 29/11 | Milestone 1b: final RQ1, RQ2 and RQ3, robustness checks |
| 30/11 to 6/12 | Milestone 2a: RQ4 |
| 7/12 to 18/12 (P3) | Milestone 2b: data story website, code cleaning, final review |

## Organization within the Team

| Milestone | Task | Who |
|---|---|---|
| 1a (15/11) | First version of RQ1, RQ2 and RQ3 | Hassan, Mara and Szabina |
| 1b (29/11) | RQ1: does one attack lead to more? | Hassan |
| 1b (29/11) | RQ2: does a common enemy make allies? | Mara |
| 1b (29/11) | RQ3: do conflicts burn out? | Szabina |
| 2a (6/12) | RQ4: events outside Reddit | Hassan |
| 2a (6/12) | RQ4: characteristics of the communities that attack the most | Mara and Szabina |
| 2b (18/12) | Data story website | All |

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

## Project Structure

The directory structure of the project looks like this:

```
├── data                        <- Local datasets
│
├── src                         <- Source code
│   ├── data                            <- Loading, feature schema, validation and preprocessing
│   ├── models                          <- Model implementations
│   ├── utils                           <- Reusable analysis utilities, including embedding coverage
│   ├── scripts                         <- Standalone scripts
│
├── tests                       <- Automated tests
│
├── results.ipynb               <- Explanations, data inspection and analysis results
│
├── pip_requirements.txt        <- Python dependencies
└── README.md
```
