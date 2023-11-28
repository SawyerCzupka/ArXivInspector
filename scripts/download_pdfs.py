"""
This script is designed to download PDFs from the arXiv website based on a list of identifiers
stored in a SQLite database. It updates the database with the download status of each PDF.
The script uses multithreading for efficient downloading and logs the process to a file and console.
"""

import os
import requests
import sqlite3
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("downloader.log"), logging.StreamHandler()],
)


def download_pdf(identifier):
    """
    Downloads a PDF from the arXiv website for a given identifier.

    :param identifier: The arXiv identifier of the paper to be downloaded.
    :return: A tuple containing the identifier and a boolean indicating
             the success or failure of the download.
    """
    pdf_url = f"http://arxiv.org/pdf/{identifier}.pdf"
    try:
        response = requests.get(pdf_url, stream=True)
        if response.status_code == 200:
            pdf_path = f"./pdfs/{identifier}.pdf"
            os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

            with open(pdf_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            logging.info(f"Successfully downloaded {identifier}")
            return identifier, True
        else:
            logging.error(
                f"Failed to download {identifier}. HTTP status code: {response.status_code}"
            )
            return identifier, False
    except Exception as e:
        logging.exception(
            f"An error occurred while downloading {identifier}. Error: {e}"
        )
        return identifier, False


def update_db(conn, identifier, status):
    """
    Updates the SQLite database with the download status of a paper.

    :param conn: The connection object to the SQLite database.
    :param identifier: The arXiv identifier of the paper.
    :param status: The download status (True for success, False for failure).
    """
    try:
        with conn:
            conn.execute(
                "UPDATE articles SET downloaded = ? WHERE identifier = ?",
                (int(status), identifier),
            )
            conn.commit()
        logging.info(f"Updated download status in DB for {identifier}: {status}")
    except Exception as e:
        logging.exception(
            f"An error occurred while updating the database for {identifier}. Error: {e}"
        )


def main():
    """
    Main function to orchestrate the downloading and updating of the database.
    It retrieves paper identifiers from a SQLite database, downloads the corresponding
    PDFs using a ThreadPoolExecutor, and updates the download status in the database.
    """
    # Establish a connection to the local SQL database
    conn = sqlite3.connect("arxiv_papers.db")
    c = conn.cursor()

    try:
        c.execute("ALTER TABLE articles ADD COLUMN downloaded INTEGER DEFAULT 0")
        conn.commit()
    except sqlite3.OperationalError as e:
        logging.warning(
            f'Column "downloaded" already exists in "articles". Message: {e}'
        )
    except Exception as e:
        logging.exception(f"An unexpected error occurred during DB setup. Error: {e}")

    c.execute("SELECT identifier FROM articles WHERE downloaded = 0")
    identifiers = c.fetchall()
    logging.info(f"Found {len(identifiers)} records to download.")

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_id = {executor.submit(download_pdf, identifier[0]): identifier[0] for identifier in identifiers}

        for future in as_completed(future_to_id):
            identifier = future_to_id[future]
            try:
                _, status = future.result()
                update_db(conn, identifier, status)
            except Exception as e:
                logging.exception(
                    f"An error occurred while executing the download task for {identifier}. Error: {e}"
                )

    conn.close()


if __name__ == "__main__":
    main()
