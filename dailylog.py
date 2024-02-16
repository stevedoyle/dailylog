# Script for summarizing log entries from daily notes.
#
# Log entires are list items in the '## Log' section of daily note files.
# Daily note files are markdown files with the name format: YYYY-MM-DD.md

from version import __version__
from datetime import date
import os
import click
import dateutil
import logging
import pendulum
import re

def extractLogData(contents):
    data = []
    collecting = False
    for line in contents:
        if line.startswith('## Log'):
            collecting = True
            continue
        if not collecting:
            continue
        if re.search('\s*-', line):
            data.append(line)
            continue
        if line.startswith('#'):
            collecting = False
            break

    return data

def getFilesInRange(fpath, begin, end):
    begindate = dateutil.parser.parse(begin).date()
    enddate = dateutil.parser.parse(end).date()

    files = []
    with os.scandir(fpath) as it:
        for entry in it:
            if entry.name.endswith(".md") and entry.is_file():
                try:
                    filedate = dateutil.parser.parse(
                        os.path.basename(entry).split('.')[0]).date()
                    if (begindate <= filedate) and (filedate <= enddate):
                        files.append(entry.path)
                except dateutil.parser.ParserError as err:
                    continue
    return files

def getLogData(files):
    logdata = {}
    for entry in files:
        with open(entry, encoding='UTF-8') as f:
            name = os.path.splitext(
                os.path.basename(entry))[0]
            ld = extractLogData(f.readlines())
            logdata[name] = ld
    return logdata

def gatherDailyLogData(path, begin, end):
    try:
        files = getFilesInRange(path, begin, end)
        ld = getLogData(files)
        return ld
    except ValueError as err:
        print(f'Error parsing date: {err}')
        return {}

def storeDailyLogData(outfile, data):
    with open(outfile, 'w') as f:
        for date, entries in sorted(list(data.items()), key=lambda x:x[0].lower(), reverse=True):
            if len(entries) == 0:
                continue
            f.write('## ' + date + '\n\n')
            for entry in entries:
                f.write(entry)

##########################################################################

def get_dates_today():
    today = pendulum.today().to_date_string()
    return today, today

def get_dates_yesterday():
    yesterday = pendulum.yesterday().to_date_string()
    return yesterday, yesterday

def get_dates_thisweek():
    today = pendulum.today()
    start = today.start_of('week').to_date_string()
    end = today.end_of('week').to_date_string()
    return start, end

def get_dates_lastweek():
    lastweek = pendulum.today().subtract(weeks=1)
    start = lastweek.start_of('week').to_date_string()
    end = lastweek.end_of('week').to_date_string()
    return start, end

def get_dates_thismonth():
    today = pendulum.today()
    start = today.start_of('month').to_date_string()
    end = today.end_of('month').to_date_string()
    return start, end

def get_dates_lastmonth():
    lastmonth = pendulum.today().subtract(months=1)
    start = lastmonth.start_of('month').to_date_string()
    end = lastmonth.end_of('month').to_date_string()
    return start, end

def get_dates_thisquarter():
    today = pendulum.today()
    start = today.first_of('quarter').to_date_string()
    end = today.last_of('quarter').to_date_string()
    return start, end

def get_dates_lastquarter():
    lastmonth = pendulum.today().subtract(months=3)
    start = lastmonth.first_of('quarter').to_date_string()
    end = lastmonth.last_of('quarter').to_date_string()
    return start, end

def get_dates_thisyear():
    today = pendulum.today()
    start = today.start_of('year').to_date_string()
    end = today.end_of('year').to_date_string()
    return start, end

def get_dates_lastyear():
    lastyear = pendulum.today().subtract(years=1)
    start = lastyear.start_of('year').to_date_string()
    end = lastyear.end_of('year').to_date_string()
    return start, end

def get_dates(start, end,
              today, yesterday,
              thisweek, thismonth, thisquarter, thisyear,
              lastweek, lastmonth, lastquarter, lastyear):
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")
    if today:
        start, end = get_dates_today()
    elif yesterday:
        start, end = get_dates_yesterday()
    elif thisweek:
        start, end = get_dates_thisweek()
    elif thismonth:
        start, end = get_dates_thismonth()
    elif thisquarter:
        start, end = get_dates_thisquarter()
    elif thisyear:
        start, end = get_dates_thisyear()
    elif lastweek:
        start, end = get_dates_lastweek()
    elif lastmonth:
        start, end = get_dates_lastmonth()
    elif lastquarter:
        start, end = get_dates_lastquarter()
    elif lastyear:
        start, end = get_dates_lastyear()
    return start, end

##########################################################################

@click.command()

@click.version_option(version=__version__)
@click.option('--log', default='warning',
              help='Logging level (info, debug)')
@click.option('--path', default='.',
              help='Path where the daily note files are stored.',
              type=click.Path(exists=True, file_okay=False))
@click.option('--out', default='daily-log-data.md',
              help='File where the collated data will be stored')
@click.option('--from', 'from_',
              default=pendulum.today(),
              help='Start of time period (default is today).',
              type=click.DateTime())
@click.option('--to', default=pendulum.today(),
              help='End of time period (default is today).',
              type=click.DateTime())
@click.option('--today', default=False, is_flag=True,
              help="Today's summary. Overrides --from and --to values.")
@click.option('--yesterday', default=False, is_flag=True,
              help="Yesterday's summary. Overrides --from and --to values.")
@click.option('--thisweek', default=False, is_flag=True,
              help="This week's summary. Overrides --from and --to values.")
@click.option('--thismonth', default=False, is_flag=True,
              help="This month's summary. Overrides --from and --to values.")
@click.option('--thisquarter', default=False, is_flag=True,
              help="This quarter's summary. Overrides --from and --to values.")
@click.option('--thisyear', default=False, is_flag=True,
              help="This year's summary. Overrides --from and --to values.")
@click.option('--lastweek', default=False, is_flag=True,
              help="Last week's summary. Overrides --from and --to values.")
@click.option('--lastmonth', default=False, is_flag=True,
              help="Last month's summary. Overrides --from and --to values.")
@click.option('--lastquarter', default=False, is_flag=True,
              help="Last quarter's summary. Overrides --from and --to values.")
@click.option('--lastyear', default=False, is_flag=True,
              help="Last year's summary. Overrides --from and --to values.")
def dailylog(log, path, out,
           from_, to,
           today, yesterday,
           thisweek, thismonth, thisquarter, thisyear,
           lastweek, lastmonth, lastquarter, lastyear):
    """Summarize daily note log data

    Multiple options are provided for specifying the time period. Only the
    daily log data within the specified time period will be analysed. If no
    time period is specified, today's daily note will be used.

    Daily note log information is extracted from 'Daily Note' files which
    follow the convention that there is a separate file for each day and the
    file name follows the pattern: 'YYYY-MM-DD.md', e.g. 2024-02-16.md.
    """
    # Logging setup
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log}")
    logging.basicConfig(format='%(message)s', level=numeric_level)

    start, end = get_dates(from_, to,
                           today, yesterday,
                           thisweek, thismonth, thisquarter, thisyear,
                           lastweek, lastmonth, lastquarter, lastyear)
    logging.info(f'{start} -> {end}')

    data = gatherDailyLogData(path, start, end)
    storeDailyLogData(out, data)


##########################################################################

if __name__ == "__main__":
    dailylog()
