import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os


def scrape_reports():
    """
    set base_page_num and base_url if it changes
    the function will scrape all the reports from the website, starting from the specified page
    """
    base_page_num = 0
    base_url = "https://www.bundesbank.de/action/de/885712/bbksearch?pageNumString="

    while True:
        # GET request the current page
        response = requests.get(f"{base_url}{base_page_num}")

        # Parse the response
        soup = BeautifulSoup(response.content, "html.parser")

        # check if page is empty
        if soup.find("div", class_="no-results"):
            break

        # extract links to the monthly reports, we will get the english ones
        en_report_links = soup.find_all("a", class_="metadata__lang")

        for report_link in tqdm(en_report_links, desc=f"Page {base_page_num}"):
            # GET the individual report
            report_response = requests.get(report_link["href"])

            base_link = "https://www.bundesbank.de"

            # download link in form of '/resource/blob/123456/123456.pdf'
            en_content = BeautifulSoup(report_response.content, "html.parser")
            en_download_link = en_content.find("a", class_="btn btn-primary mr-1 mt-2")[
                "href"
            ]

            en_report_download = requests.get(base_link + en_download_link)
            en_file_name = en_download_link.split("/")[-1]

            # save the report in ./data/
            with open(f"./data/{en_file_name}", "wb") as f:
                f.write(en_report_download.content)

            """
            do the same for the german report, link is a link with hreflang="de"
            example: <link rel="alternate" hreflang="de" 
            href="https://www.bundesbank.de/de/publikationen/berichte/monatsberichte/monatsbericht-august-1949-690230"
            title="German | Deutsch"/>
            """
            de_report_link = en_content.find("link", hreflang="de")["href"]
            de_download_link = BeautifulSoup(
                requests.get(de_report_link).content, "html.parser"
            )
            de_download_link = de_download_link.find(
                "a", class_="btn btn-primary mr-1 mt-2"
            )["href"]

            de_report_download = requests.get(base_link + de_download_link)
            de_file_name = de_download_link.split("/")[-1]

            # save the report in ./data/
            with open(f"./data/{de_file_name}", "wb") as f:
                f.write(de_report_download.content)

        base_page_num += 1


if __name__ == "__main__":
    # scrape the reports
    scrape_reports()
    # check how many reports we have
    print(f"Number of reports: {len(os.listdir('./data'))}")
