"""Prepare hyperlink records with explicit, reported transformations."""

import pandas as pd


def prepare_links(body_links, title_links, start="2014-01-01", end="2017-05-01"):
    """Combine files, normalize names and keep timestamps in [start, end).

    Return a new link table and a sequential preparation report. Preserve
    direction, source-post identifiers and labels. Do not deduplicate records
    or filter on embedding availability.
    """
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    if pd.isna(start) or pd.isna(end) or start >= end:
        raise ValueError("start must be earlier than end.")

    links = pd.concat([
        body_links.assign(link_origin="body"),
        title_links.assign(link_origin="title"),
    ], ignore_index=True)
    report = []

    def record(step, frame, affected_rows):
        communities = pd.concat([frame["SOURCE_SUBREDDIT"], frame["TARGET_SUBREDDIT"]])
        report.append({
            "step": step, "rows": len(frame),
            "affected_rows": int(affected_rows),
            "communities": communities.nunique(),
        })

    record("combine_body_and_title", links, 0)
    changed = pd.Series(False, index=links.index)
    for column in ["SOURCE_SUBREDDIT", "TARGET_SUBREDDIT"]:
        original = links[column].astype("string")
        normalized = original.str.strip().str.lower()
        if (normalized.isna() | normalized.eq("")).any():
            raise ValueError(f"{column} contains missing or blank names.")
        changed |= original.ne(normalized)
        links[column] = normalized
    record("normalize_community_names", links, changed.sum())

    timestamps = pd.to_datetime(links["TIMESTAMP"], errors="raise")
    if timestamps.isna().any():
        raise ValueError("TIMESTAMP contains missing values.")
    links["TIMESTAMP"] = timestamps
    keep = timestamps.ge(start) & timestamps.lt(end)
    removed = (~keep).sum()
    links = links.loc[keep].reset_index(drop=True)
    record("filter_analysis_dates", links, removed)
    return links, pd.DataFrame(report).set_index("step")
