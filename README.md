# DBISAM to JSON

This is a small tool written in python because I needed to extract database values from .dat files programmatically and couldn't find any tools on the internet to do so.
Currently it can read the following fields:

- Varchar
- Int
- Float
- Date

## Usage

```
python read.py <.dat file>

```

Will print the file's records in JSON format
