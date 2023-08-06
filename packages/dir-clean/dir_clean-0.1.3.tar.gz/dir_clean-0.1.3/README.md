# dir_clean

This package can help you to clean up the directory.

Files or directories older than the specified number of days will be deleted.

## Usage

```bash
usage: __main__.py [-h] [-d KEEP_DAYS] [-c CONF_FILE] [--dry-run]

optional arguments:
  -h, --help            show this help message and exit
  -d KEEP_DAYS, --keep-days KEEP_DAYS
                        days to keep (default: 7)
  -c CONF_FILE, --conf-file CONF_FILE
                        configuration filename (default: dir_clean.conf)
  --dry-run


```

## Configuration file format

Each line consists of these items, separated by commas:

- path: path to search.

- regex: Regular expression to match directories or files to clean. (optional)

- days: how many days to keep. (optional)



Example:

```
/services/www/log,.+,3
```

## Date comparison

By default, the modification date of the file or directory will be read as a comparison with the current date, but you can also specify the date of a file or directory through the regular expression.

```
/services/www/log,.+?-(?P<m>\d{2})-(?P<d>\d{2})-(?P<y>\d{4})\.log,7
```








