"""Describe which hyperlink observations have usable subreddit embeddings."""

import numpy as np
import pandas as pd


def embedding_coverage(links, embeddings):
    """Return community coverage, link coverage and community activity tables.

    Match names after stripping whitespace and lowercasing, without modifying
    inputs. A usable embedding has a nonblank name, 300 finite coordinates and
    at least one nonzero coordinate. Reject ambiguous normalized names.
    """
    names = embeddings["subreddit"].astype("string").str.strip().str.lower()
    valid_names = names.notna() & names.ne("")
    if names[valid_names].duplicated().any():
        raise ValueError("Embedding names must be unique after normalization.")
    columns = [f"embedding_{i}" for i in range(1, 301)]
    vectors = embeddings[columns].to_numpy(dtype=float)
    usable = valid_names & np.isfinite(vectors).all(axis=1) & (vectors != 0).any(axis=1)
    usable_names = set(names[usable])

    source = links["SOURCE_SUBREDDIT"].astype("string").str.strip().str.lower()
    target = links["TARGET_SUBREDDIT"].astype("string").str.strip().str.lower()
    source_covered = source.isin(usable_names)
    target_covered = target.isin(usable_names)
    groups = np.select(
        [source_covered & target_covered, source_covered, target_covered],
        ["both", "source_only", "target_only"], default="neither",
    )
    group_order = ["both", "source_only", "target_only", "neither"]
    observations = pd.DataFrame({
        "coverage": groups,
        "negative": links["LINK_SENTIMENT"].eq(-1).to_numpy(),
    })
    link_summary = observations.groupby("coverage").agg(
        links=("negative", "size"), negative_links=("negative", "sum"),
    ).reindex(group_order, fill_value=0)
    link_summary["link_share"] = link_summary["links"] / len(links) if len(links) else np.nan
    link_summary["negative_rate"] = link_summary["negative_links"] / link_summary["links"].replace(0, np.nan)

    # Count each community's link appearances, incoming plus outgoing.
    activity = pd.concat([source, target], ignore_index=True)
    activity = activity[activity.notna() & activity.ne("")].value_counts()
    covered = activity.index.isin(usable_names)
    community_rows = []
    for label, mask in [("usable_embedding", covered), ("no_usable_embedding", ~covered)]:
        counts = activity[mask]
        community_rows.append({
            "coverage": label, "communities": len(counts),
            "community_share": len(counts) / len(activity) if len(activity) else np.nan,
            "median_link_appearances": counts.median(),
            "mean_link_appearances": counts.mean(),
        })
    community_summary = pd.DataFrame(community_rows).set_index("coverage")
    community_activity = activity.rename_axis("subreddit").rename("link_appearances").to_frame()
    community_activity["has_usable_embedding"] = covered
    return community_summary, link_summary, community_activity
