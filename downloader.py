import csv
import os, sys
from axel import axel

if not os.path.exists('Books'):
    os.mkdir('Books')
elif not os.path.isdir('Books'):
    print('Error: a file named "Books" cannot be in the execution directory.')
    sys.exit(0)

links = 'downloads.csv'

with open(links) as file:
    reader = csv.reader(file, delimiter=',')

    for idx, row in enumerate(reader):
        print('%i: [%s] Downloading %s' % (idx + 1, row[0], row[1]))
        os.system('wget %s -O "Books/[%s] %s.pdf"' % (row[2], row[0], row[1]))
