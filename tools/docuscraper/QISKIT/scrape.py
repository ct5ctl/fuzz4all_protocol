"""This file scrapes the QISKIT documentation to give the LLM."""

import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

import click
import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape(
    url: str, relevant_class: str = "py", only_link_same_root: bool = True
) -> Tuple[List[str], List[str]]:
    """Scrape the url and return the links and the relevant text chunks.

    The xpath selector is used to select the relevant text chunks.
    e.g. all the elements with class=="py" are relevant.
    """
    # Get the page and parse it
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    # Get the links from the page
    links = soup.find_all("a", href=True)
    # get href attribute
    links_text = [link["href"] for link in links]
    # for link in links_text:
    #     print(f"- {link}")
    # remove relative links with #
    links_text = [link for link in links_text if not link.startswith("#")]
    if only_link_same_root:
        # add the root to the relative links
        # get root by removing the filename from the url
        base_url = os.path.dirname(url)
        print(base_url)
        links_text = [
            link if link.startswith("http") else base_url + "/" + link
            for link in links_text
        ]
    # remove duplicates
    links_text = list(set(links_text))

    # Get the text chunks from the page
    text_chunks = soup.find_all(attrs={"class": relevant_class})

    # Get the text from the text chunks
    text_chunks = [chunk.text for chunk in text_chunks]
    print(f"({len(links_text)} links, {len(text_chunks)} text): {url}.")
    return links_text, text_chunks


@click.command()
@click.option(
    "--url",
    default="https://qiskit.org/documentation/apidoc/terra.html",
    help="The main URL of the documentation to scrape.",
)
@click.option(
    "--output",
    "-o",
    required=True,
    help="The output directory to save the documentation file as md.",
)
@click.option(
    "--max-level",
    default=0,
    help="How many links to follow, 0 = none, 1 = link on the main page, etc.",
)
@click.option(
    "--relevant-class", default="py", help="The class of the elements to scrape."
)
@click.option(
    "--overwrite", is_flag=True, help="If the output file already exists, overwrite it."
)
def scrape_main(
    url: str, output: str, max_level: int, relevant_class: str, overwrite: bool
):
    """Scapes the QISKIT documentation and follow the links."""

    path_csv = os.path.join(output, "qiskit_doc.csv")
    # check that the output csv does not exist
    if os.path.exists(path_csv) and not overwrite:
        print(f"ERROR: The output file {path_csv} already exists.")
        sys.exit(1)

    path_md = os.path.join(output, "qiskit_doc.md")
    # check that the output md does not exist
    if os.path.exists(path_md) and not overwrite:
        print(f"ERROR: The output file {path_md} already exists.")
        sys.exit(1)

    level = 0
    to_visit = [(url, level)]
    visited = set()

    all_records = []

    while to_visit:
        url, level = to_visit.pop()  # depth first algorithm
        # url, level = to_visit.pop(0)  # breadth first algorithm
        if level > max_level:
            continue
        if url in visited:
            continue
        visited.add(url)
        print(f"Visiting {url}")
        links, text = scrape(url, relevant_class=relevant_class)
        # keep only single line text
        text = [line for line in text if "\n" not in line]
        # add as many tab as the level
        text = [f"{'    ' * level}{line}" for line in text]
        all_records.append({"url": url, "links": links, "text": text})
        # Add the links to the to_visit list
        for link in links:
            to_visit.append((link, level + 1))

    # Save the records
    df = pd.DataFrame.from_records(all_records)
    df.to_csv(path_csv, index=False)

    # collect all the elements in the text column
    all_text = df["text"].tolist()
    all_text = [item for sublist in all_text for item in sublist]

    # concatenate
    concatenated_text = "\n".join(all_text)

    # save the concatenated text
    with open(path_md, "w") as f:
        f.write(concatenated_text)
        f.close()


if __name__ == "__main__":
    scrape_main()
