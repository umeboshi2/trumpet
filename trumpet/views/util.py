from dateutil.parser import parse as dateparse


def get_start_end_from_request(request, timestamps=False,
                               verbose=False):
    start = dateparse(request.GET['start'])
    end = dateparse(request.GET['end'])
    if verbose:
        print("START, END", start, end)
    if timestamps:
        raise RuntimeError("Timestamps not supported.")
    return start, end
