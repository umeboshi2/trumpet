from datetime import datetime


def _parse_date(date):
    year, month, day = [int(p) for p in date.split('-')]
    return datetime(year, month, day)


def get_start_end_from_request(request, timestamps=False,
                               verbose=False):
    start = request.GET['start']
    end = request.GET['end']
    if verbose:
        print("START, END", start, end)
    if not timestamps:
        start = _parse_date(start)
        end = _parse_date(end)
    return start, end
