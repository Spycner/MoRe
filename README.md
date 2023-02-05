# MoRe

Creating a dataset from monthly-reports by the german central bank, using the german and english version.

## Usage

### Download

The monthly reports will be saves to the folder ./data. The folder will be created if it does not exist. You can specify the first page number to start from, the default is 0. The script will stop if it reaches the last page. Future scraping will can be done by specifying the last page number of the last run.

```console
python download.py
```
