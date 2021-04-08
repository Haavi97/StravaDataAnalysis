import csv
import os
import traceback


def get_file_full_path(file_name='activities.csv'):
    return os.getcwd() + os.path.sep + str(file_name)


def reader(file_name='activities.csv'):
    result = []
    try:
        with open(get_file_full_path(file_name), encoding="utf8") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=",")
            field_names = csv_reader.fieldnames
            line_count = 0
            try:
                for row in csv_reader:
                    result.append(row)
                    line_count += 1
            except Exception:
                traceback.print_exc()
                pass
        print('Columns read: {}'.format(line_count))
        return field_names, result
    except FileNotFoundError:
        print(('Please check that you have your file {}' +
               ' in the same folder as this script').format(file_name))


def clean_fields(file_name='activities.csv', output_file='activities.csv'):
    """Eliminating repeated distance field.

    Keeping only the one in meters. Coping all the data to a buffer.
    Very demanding but is the only way to copy safely to the same file.
    """
    infn = get_file_full_path(file_name)
    outfn = get_file_full_path('buffer.csv')
    with open(infn, newline='', encoding="utf8") as csv_file, open(outfn, 'w', newline='', encoding="utf8") as outfile:
        r = csv.reader(csv_file)
        w = csv.writer(outfile)
        header = list(next(r))
        for i in range(len(header)):
            if header[i] == 'Distance':
                header[i] = 'DistanceKm'
                break
        w.writerow(header)
        for row in r:
            w.writerow(row)
    final = get_file_full_path(output_file)
    with open(final, 'w', newline='', encoding="utf8") as csv_file, open(outfn, newline='', encoding="utf8") as outfile:
        r = csv.reader(outfile)
        w = csv.writer(csv_file)
        for row in r:
            w.writerow(row)
    os.remove(outfn)
