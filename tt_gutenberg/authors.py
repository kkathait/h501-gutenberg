import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from .data import load_authors, load_metadata, load_languages


def get_author_languages():
    authors = load_authors()
    metadata = load_metadata()
    languages = load_languages()

    books = metadata[
        ["gutenberg_id", "gutenberg_author_id"]
    ].dropna()

    author_languages = books.merge(
        languages[["gutenberg_id", "language"]],
        on="gutenberg_id",
        how="inner"
    )

    counts = (
        author_languages
        .groupby("gutenberg_author_id")["language"]
        .nunique()
        .reset_index(name="translation_count")
    )

    return authors.merge(
        counts,
        on="gutenberg_author_id",
        how="left"
    )


def list_authors(by_languages=False, alias=False):
    authors = get_author_languages()

    if by_languages:
        authors = authors.sort_values(
            "translation_count",
            ascending=False
        )

    if alias:
        aliases = authors["alias"].dropna()
        aliases = aliases[aliases.str.strip() != ""]
        return aliases.tolist()

    return authors["author"].dropna().tolist()


def plot_translations(over="birth_century"):
    authors = get_author_languages()

    authors = authors.dropna(
        subset=["author", "birthdate", "translation_count"]
    ).copy()

    authors["birth_century"] = (
        authors["birthdate"].astype(int) // 100
    ) * 100

    plot = sns.barplot(
        data=authors,
        x=over,
        y="translation_count",
        errorbar=("ci", 95)
    )

    plot.set_xlabel("Birth Century")
    plot.set_ylabel("Average Number of Languages")

    plt.show()

    return plot