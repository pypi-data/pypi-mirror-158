# RARBG-CLI `rarbgcli`

RARBG command line interface for scraping the [rarbg.to](rarbg.to) torrent search engine.

Outputs list of results containing magnet links from a [rarbg.to](rarbg.to) search.

## Usage

    positional arguments:
    search                search term

    optional arguments:
    -h, --help            show this help message and exit
    --category {movies,xxx,music,tvshows,software,games,nonxxx,}, -c {movies,xxx,music,tvshows,software,games,nonxxx,}
    --limit LIMIT, -l LIMIT
                            limit number of torrent magnet links (default: inf)
    --domain DOMAIN, -d DOMAIN
                            domain to search, you could put an alternative mirror domain here (default: rarbgunblocked.org)
    --magnet, -m          output magnet links (default: False)
    --no_cache, -nc       don't use cached results from previous searches (default: False)
    --order {data,filename,leechers,seeders,size,}, -r {data,filename,leechers,seeders,size,}
                            order results (before query) by this key. empty string means no sort (default: )
    --sort {title,date,size,seeders,leechers,}, -s {title,date,size,seeders,leechers,}
                            sort results (after scraping) by this key. empty string means no sort (default: )

Example

```sh
python rarbgcli.py "the stranger things 3" --category movies --limit 10 --magnets
```

### Piping `|`
The program is pipe-friendly, so you could use this tool in conjunction with the [jq](https://stedolan.github.io/jq/) command to filter the JSON output, and then pipe it to your favorite torrent client.

The --magnet option is a convenience option instead of filtering it every time with `jq`, the bellow 2 lines are equivalent:

```sh
rarbgcli "the stranger things 3" -category movies --limit 10 | jq .[].magnet | bittorrent
rarbgcli "the stranger things 3" -category movies --limit 10 --magnet | bittorrent
```

## CAPTCHA

To get around the captcha, the user will be prompted to solve it and enter the cookie in the terminal.

I tried many ways to automate this process (using selenium and tesseract), but it just ends up being overkill, hard to maintain across platforms, and I still didn't get it to work.

This might be automated one day, because it is possible.
