""" Takes raw csv data from our scraper, outputs different kinds of processed csv files. """
import csv
import datetime
import math
from dateutil.parser import parse

STARTING_PROCESSING_DAYS = -1

def relevant(row_text):
    """ A csv row, which represents a USCIS case, is relevant if it is 1) related to
        i-765 AND 2) either in a state of having been approved or still being processed. """
    whitelist = [
        "received your Form I-765",
        "ordered your new card",
        "mailed your new card",
        "approved your Form I-765"]
    for phrase in whitelist:
        if phrase in row_text:
            return True
    return False


def get_processing_days(row_text):
    """ Returns either number of days case has been processing, or -1 if info is
        not available. """
    if "received your Form I-765" in row_text:
        res = " ".join(row_text.split()[1:4])[:-1]
        received_date = parse(res)
        return (datetime.datetime.now() - received_date).days
    return -1

with open('result.csv', 'r') as r_file:
    with open('filtered.csv', 'w') as w_file:
        reader = csv.reader(r_file, delimiter=' ', quotechar='|')
        writer = csv.writer(w_file, delimiter=' ', quotechar='|')
        for row in reader:
            if not relevant(row[1]):
                continue
            else:
                processing_days = get_processing_days(row[1])
                if STARTING_PROCESSING_DAYS == -1 and processing_days != -1:
                    STARTING_PROCESSING_DAYS = processing_days
                writer.writerow(row + [processing_days])

with open('filtered.csv', 'r') as r_file:
    with open('interpolated.csv', 'w') as w_file:
        reader = csv.reader(r_file, delimiter=' ', quotechar='|')
        writer = csv.writer(w_file, delimiter=' ', quotechar='|')
        previous_processing_days = STARTING_PROCESSING_DAYS
        # temporarily store rows which have not had their processing days
        # calculated
        result_rows_buffer = []
        for row in reader:
            if int(row[2]) == -1:
                result_rows_buffer.append(row)
            else:
                if result_rows_buffer:
                    delta = float(row[2]) - previous_processing_days
                    increment_per_entry = delta / len(result_rows_buffer)
                    for i, result_row in enumerate(result_rows_buffer):
                        processing_days_interpolated = math.floor(
                            i * increment_per_entry + previous_processing_days)
                        print(processing_days_interpolated)
                        writer.writerow(
                            ["done"] + [processing_days_interpolated])
                    result_rows_buffer = []
                previous_processing_days = float(row[2])
                writer.writerow(["processing"] + [row[2]])
