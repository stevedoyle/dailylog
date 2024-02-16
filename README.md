# dailylog

A utility for gathering log entries from daily notes and collating them into a single file.

The utility assumes the following conventions:

- Log entires in daily notes are list items in a ``## Log`` section.
- Daily note file names have the format: `YYYY-MM-DD.md`, e.g. `2024-02-16.md`

## Examples

Daily note log data:

```markdown
## Log

- Example log entry
- Another example log entry
```

Gathering the daily log entries into a file called `daily-log-info.md`:

```bash
dailylog --path=./examples --thisyear --out=daily-log-info.md
```

## Installation

Installation uses setuptools to install the utility from a cloned repo.

```bash
git clone https://github.com/stevedoyle/dailylog.git
cd dailylog
pip install --editable .
```

## Usage

```text
Usage: dailylog.py [OPTIONS]

  Summarize daily note log data

  Multiple options are provided for specifying the time period. Only the daily
  log data within the specified time period will be analysed. If no time
  period is specified, today's daily note will be used.

  Daily note log information is extracted from 'Daily Note' files which follow
  the convention that there is a separate file for each day and the file name
  follows the pattern: 'YYYY-MM-DD.md', e.g. 2024-02-16.md.

Options:
  --version                       Show the version and exit.
  --log TEXT                      Logging level (info, debug)
  --path DIRECTORY                Path where the daily note files are stored.
  --out TEXT                      File where the collated data will be stored
  --from [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                                  Start of time period (default is today).
  --to [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                                  End of time period (default is today).
  --today                         Today's summary. Overrides --from and --to
                                  values.
  --yesterday                     Yesterday's summary. Overrides --from and
                                  --to values.
  --thisweek                      This week's summary. Overrides --from and
                                  --to values.
  --thismonth                     This month's summary. Overrides --from and
                                  --to values.
  --thisquarter                   This quarter's summary. Overrides --from and
                                  --to values.
  --thisyear                      This year's summary. Overrides --from and
                                  --to values.
  --lastweek                      Last week's summary. Overrides --from and
                                  --to values.
  --lastmonth                     Last month's summary. Overrides --from and
                                  --to values.
  --lastquarter                   Last quarter's summary. Overrides --from and
                                  --to values.
  --lastyear                      Last year's summary. Overrides --from and
                                  --to values.
  --help                          Show this message and exit.
```
