import lxml.html
import os, sys
import requests
from csv import DictReader


if not os.path.exists('Books'):
    os.mkdir('Books')
elif not os.path.isdir('Books'):
    print('Error: a file named "Books" cannot be in the execution directory.')
    sys.exit(0)


class Book:
    def __init__(self, idx, title, edition, subject, url):
        self.idx = idx
        self.title = title
        self.edition = edition
        self.name = '%s, %s' % (self.title, self.edition)
        self.subject = self.process(subject)
        self.url = url
        self.epub = None

    def __repr__(self):
        return '%i: %s, %s [%s]' % (self.idx, self.title, self.edition, self.subject)

    def process(self, subject):
        subject = subject.split(';')[0]

        try:
            os.mkdir(os.path.join('Books', subject))
        except FileExistsError:
            pass
        finally:
            self.path = os.path.join('Books', subject, self.name + '.pdf')
            self.epat = os.path.join('Books', subject, self.name + '.epub')

        return subject

    def scrape(self):
        if os.path.exists(self.path) and os.path.exists(self.epat):
            print('Info: %s already saved.' % self.path)
            print('Info: %s already saved.' % self.epat)
            self.save = lambda: 0

            return 0

        response = requests.get(self.url)
        html = lxml.html.fromstring(response.content)
        epub = None

        try:
            xpath = html.xpath('//*[@id="main-content"]/article[1]/div/div/div[2]/div/div/a')

            if not bool(xpath):
                xpath = html.xpath('//*[@id="main-content"]/article[1]/div/div/div[2]/div[1]/a')
                epub  = html.xpath('//*[@id="main-content"]/article[1]/div/div/div[2]/div[2]/a')
                epub = epub[0]

            xpath = xpath[0]
        except IndexError:
            print('Error: %i %s server access point missing' % (self.idx, self.name))

            self.save = lambda: 0
            return False

        else:
            stub = xpath.get('href')
            pdf = 'https://link.springer.com/%s' % stub

            # self.pdf  = requests.get(pdf).content
            self.pdf = pdf

            if epub:
                stub = epub.get('href')
                epub = 'https://link.springer.com/%s' % stub
                # self.epub = requests.get(epub).content
                self.epub = epub

            print('PDF: %s' % self.pdf)
            print('EPUB: %s' % self.epub)


    def writeToFile(self):
        # PDF
        if self.pdf:
            with open('download-pdf.txt', 'a') as writer:
                writer.write(str(self.pdf) +'\n')
                writer.close()

        # EPUB
        if self.epub:
            with open('download-csv.txt', 'a') as writer:
                writer.write(str(self.epub) + '\n')
                writer.close()


    def save(self):
        if self.pdf and not os.path.exists(self.path):
            with open(self.path, 'wb') as fhand:
                fhand.write(self.pdf)
            print('Saved: %s' % self.path)
        elif not self.pdf:
            print('Info: Springer does not furnish this as pdf.')
        else:
            print('Info: %s already saved.' % self.path)

        if self.epub and not os.path.exists(self.epat):
            with open(self.epat, 'wb') as fhand:
                fhand.write(self.epub)
            print('Saved: %s' % self.epat)
        elif not self.epub:
            print('Info: Springer does not furnish this as epub.')
        else:
            print('Info: %s already saved.' % self.epat)


source = 'source.csv'

with open(source, mode='r') as file:
    reader = DictReader(file)

    for idx, row in enumerate(reader):
        book = Book(**{
            'idx': idx,
            'title': row['Book Title'],
            'edition': row['Edition'],
            'subject': row['Subject Classification'],
            'url': row['OpenURL'],
        })

        print('\n', book)
        book.scrape()
        book.writeToFile()
        # book.save()
        print('\n')
