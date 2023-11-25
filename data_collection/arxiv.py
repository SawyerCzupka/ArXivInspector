"""
Python Script to generate the database of arxiv identifiers with titles
"""

import requests
import sqlite3
import logging
from xml.etree import ElementTree
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Constants for arXiv OAI API
BASE_URL = "http://export.arxiv.org/oai2"
METADATA_PREFIX = "arXiv"
DATE_START = "2010-01-01"
CATEGORIES = ["cs.CV", "cs.AI", "cs.LG", "cs.CL", "cs.NE", "stat.ML"]

# Establish a connection to the local SQL database
conn = sqlite3.connect("arxiv_papers.db")
c = conn.cursor()

# Create table
c.execute(
    """CREATE TABLE IF NOT EXISTS articles (
                identifier TEXT PRIMARY KEY,
                title TEXT,
                abstract TEXT,
                authors TEXT,
                published_date TEXT,
                categories_str TEXT)"""
)


def save_to_db(article_data):
    with conn:
        c.execute(
            """INSERT OR IGNORE INTO articles (identifier, title, abstract, authors, published_date, categories_str)
                     VALUES (:identifier, :title, :abstract, :authors, :published_date, :categories_str)""",
            article_data,
        )
        return c.rowcount  # Returns 1 if the row was inserted, otherwise 0


def harvest_metadata(setCat: str = "cs"):
    # Date from which to start harvesting
    resumptionToken = None

    while True:
        params = {
            "verb": "ListRecords",
            "metadataPrefix": METADATA_PREFIX if not resumptionToken else None,
            "from": DATE_START if not resumptionToken else None,
            "set": setCat if not resumptionToken else None,
            "resumptionToken": resumptionToken if resumptionToken else None,
        }

        response = requests.get(BASE_URL, params=params)
        logging.info(f"Requested: {response.url}")

        if response.status_code != 200:
            logging.error(f"Error fetching data: {response.text}")
            break

        # Parse XML response
        root = ElementTree.fromstring(response.content)
        records = root.find(".//{http://www.openarchives.org/OAI/2.0/}ListRecords")
        logging.info(f"Received {len(records)} records.")
        if records is None:
            logging.error("No records found in the response.")
            break

        # Counter for successful saves
        successful_saves = 0

        # Iterate over records
        for record in records:
            header = record.find(".//{http://www.openarchives.org/OAI/2.0/}header")
            if header is not None and "status" not in header.attrib:
                metadata = record.find(".//{http://arxiv.org/OAI/arXiv/}arXiv")
                if metadata is not None:
                    categories = metadata.find(
                        ".//{http://arxiv.org/OAI/arXiv/}categories"
                    ).text.split()
                    # Filter categories
                    if any(cat in CATEGORIES for cat in categories):
                        identifier = metadata.find(
                            ".//{http://arxiv.org/OAI/arXiv/}id"
                        ).text

                        title = metadata.find(
                            ".//{http://arxiv.org/OAI/arXiv/}title"
                        ).text.strip()

                        abstract = metadata.find(
                            ".//{http://arxiv.org/OAI/arXiv/}abstract"
                        ).text.strip()

                        authors = ", ".join(
                            [
                                author.find(
                                    ".//{http://arxiv.org/OAI/arXiv/}keyname"
                                ).text
                                for author in metadata.findall(
                                    ".//{http://arxiv.org/OAI/arXiv/}authors/{http://arxiv.org/OAI/arXiv/}author"
                                )
                            ]
                        )
                        published_date = metadata.find(
                            ".//{http://arxiv.org/OAI/arXiv/}created"
                        ).text

                        # Save record to the database
                        successful_saves += save_to_db(
                            {
                                "identifier": identifier,
                                "title": title,
                                "abstract": abstract,
                                "authors": authors,
                                "published_date": published_date,
                                "categories_str": ",".join(categories),
                            }
                        )

        # Log the count of successful saves after each batch
        logging.info(f"Saved {successful_saves} / {len(records)} records.")

        # Check for resumptionToken
        token_element = root.find(
            ".//{http://www.openarchives.org/OAI/2.0/}resumptionToken"
        )
        if token_element is not None:
            resumptionToken = token_element.text
            logging.info(
                f"Resumption Token: {resumptionToken}. Sleeping for 5 seconds..."
            )
            time.sleep(5)
        else:
            conn.close()
            return


# Run the harvester
if __name__ == "__main__":
    # harvest_metadata("cs")
    harvest_metadata("stat")
