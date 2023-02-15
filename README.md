# MoRe

Creating a dataset from monthly-reports by the german central bank, using the german and english version.

## Usage

### Download

The monthly reports will be saves to the folder ./data. The folder will be created if it does not exist. You can specify the first page number to start from, the default is 0. The script will stop if it reaches the last page. Future scraping will can be done by specifying the last page number of the last run.

```console
python sourcing.py
```

### Preprocessing

1. Separate image based pdfs from text based pdfs -> move image based to ./data/image_based

#### Report Types

The reports contain different main sections that are of interest for this project. I'm currently looking for the most reoccuring ones. The selected german sections are:

1. Konjunkturlage*
    1. Grundtendenzen \ Gesamtwirtschaftliche Lage
    2. Industrie
    3. Baugewerbe
    4. Arbeitsmarkt
    5. Preise
2. Öffentliche Finanzen* (TODO: varies greatly in structure and content)
3. Wertpapiermärkte*
    1. Rentenmarkt
    2. Aktienmarkt
    3. Investmentfonds

