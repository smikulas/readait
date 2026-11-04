"""Summarize data-quality issues without modifying the input tables."""

import numpy as np
import pandas as pd


def _missing_or_blank(values):
    """Identify both absent values and whitespace-only strings."""
    return values.isna() | values.astype("string").str.strip().eq("").fillna(False)


def audit_links(links):
    """Count issues in loaded links; duplicate counts exclude the first occurrence.

    Apply to combined body/title records to also detect duplicates across files.
    Source/target names are compared as supplied, before normalization.
    """
    required = ["SOURCE_SUBREDDIT", "TARGET_SUBREDDIT", "POST_ID",
                "TIMESTAMP", "LINK_SENTIMENT"]
    missing = pd.DataFrame({name: _missing_or_blank(links[name]) for name in required})
    key = ["SOURCE_SUBREDDIT", "TARGET_SUBREDDIT", "POST_ID"]
    return pd.Series({
        "rows": len(links),
        "rows_with_missing_required_fields": int(missing.any(axis=1).sum()),
        "missing_required_values": int(missing.sum().sum()),
        "invalid_or_missing_timestamps": int(pd.to_datetime(links["TIMESTAMP"], errors="coerce").isna().sum()),
        "invalid_or_missing_labels": int((~links["LINK_SENTIMENT"].isin([-1, 1])).sum()),
        "duplicate_source_target_post_keys": int(links.duplicated(key).sum()),
        "self_links": int((links["SOURCE_SUBREDDIT"].eq(links["TARGET_SUBREDDIT"]) & ~missing["SOURCE_SUBREDDIT"] & ~missing["TARGET_SUBREDDIT"]).sum()),
    }, name="count")


def audit_embeddings(embeddings):
    """Count missing names, duplicate names, nonfinite and zero vectors.

    Report zero vectors separately from vectors containing NaN or infinity.
    Names are compared as supplied, before normalization.
    """
    names = embeddings["subreddit"]
    columns = [f"embedding_{i}" for i in range(1, 301)]
    vectors = embeddings[columns].to_numpy(dtype=float)
    finite = np.isfinite(vectors).all(axis=1)
    return pd.Series({
        "rows": len(embeddings),
        "coordinates": len(columns),
        "missing_or_blank_names": int(_missing_or_blank(names).sum()),
        "duplicate_names": int(names.duplicated().sum()),
        "nonfinite_vectors": int((~finite).sum()),
        "zero_vectors": int((finite & (vectors == 0).all(axis=1)).sum()),
    }, name="count")
