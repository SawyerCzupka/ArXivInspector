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


# Function to download the PDF
def download_pdf(identifier):
    pdf_url = f"http://arxiv.org/pdf/{identifier}.pdf"
    try:
        response = requests.get(pdf_url, stream=True)
        if response.status_code == 200:
            pdf_path = f"./pdfs/{identifier}.pdf"
            os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

            with open(pdf_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
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


# Function to update the database with the download status
def update_db(conn, identifier, status):
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


# Main function that runs the downloading tasks
def main():
    # Establish a connection to the local SQL database
    conn = sqlite3.connect("arxiv_papers.db")
    c = conn.cursor()

    try:
        # Create a new column in the database to track download status if it doesn't exist
        c.execute("ALTER TABLE articles ADD COLUMN downloaded INTEGER DEFAULT 0")
        conn.commit()
    except sqlite3.OperationalError as e:
        logging.warning(
            f'Column "downloaded" already exists in "articles". Message: {e}'
        )
    except Exception as e:
        logging.exception(f"An unexpected error occurred during DB setup. Error: {e}")

    # Retrieve all identifiers from the database
    c.execute("SELECT identifier FROM articles WHERE downloaded = 0")
    identifiers = c.fetchall()
    logging.info(f"Found {len(identifiers)} records to download.")

    # Initialize ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Start the download operations and mark each future with its identifier
        future_to_id = {
            executor.submit(download_pdf, identifier[0]): identifier[0]
            for identifier in identifiers
        }

        # As each download completes, update the database
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


# This is the standard boilerplate that calls the main() function.
if __name__ == "__main__":
    main()
