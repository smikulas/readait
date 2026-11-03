"""Load Reddit hyperlink records and subreddit embeddings for inspection and analysis."""

from pathlib import Path

import numpy as np
import pandas as pd

from src.data.schema import FEATURE_NAMES


def load_link_sample(path, n_rows=1000):
    """Read the first n_rows of a hyperlink TSV without transforming its values.

    Community names and post identifiers remain strings. The PROPERTIES column
    remains a comma-separated string of numerical features at this stage.
    This ordered preview is not a representative random sample of the archive.
    """
    if not isinstance(n_rows, int) or isinstance(n_rows, bool) or n_rows <= 0:
        raise ValueError("n_rows must be a positive integer.")

    return pd.read_csv(Path(path), sep="\t", nrows=n_rows, dtype=str)


def load_embedding_sample(path, n_rows=1000):
    """Read the first n_rows of the headerless subreddit embedding CSV.

    Each row contains a community name followed by 300 numeric coordinates.
    Coordinate names identify positions, rather than interpretable features.
    """
    if not isinstance(n_rows, int) or isinstance(n_rows, bool) or n_rows <= 0:
        raise ValueError("n_rows must be a positive integer.")

    columns = ["subreddit"] + [f"embedding_{i}" for i in range(1, 301)]
    return pd.read_csv(
        Path(path), header=None, names=columns, nrows=n_rows,
        dtype={"subreddit": str},
    )


def parse_properties(properties):
    """Expand a Series of source-post features into 86 named numeric columns.

    Preserve the input index so features can be joined back to their records.
    Reject missing, malformed and nonfinite values rather than filling them.
    """
    if properties.empty:
        return pd.DataFrame(index=properties.index, columns=FEATURE_NAMES, dtype=float)

    values = properties.str.split(",")
    if not values.str.len().eq(len(FEATURE_NAMES)).all():
        raise ValueError("Each PROPERTIES field must contain exactly 86 values.")

    features = pd.DataFrame(values.tolist(), index=properties.index, columns=FEATURE_NAMES)
    try:
        features = features.astype(float)
    except (ValueError, TypeError) as error:
        raise ValueError("PROPERTIES values must be numeric.") from error
    if not np.isfinite(features.to_numpy()).all():
        raise ValueError("PROPERTIES values must be finite.")
    return features
