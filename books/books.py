# Authors: Claire and Katrina
# Revised by: Claire and Katrina
import csv
import argparse


class Book:
    '''Each Book object stores a book title with its published year and one of the authors.
    '''
    def __init__(self, title, author, year):
        '''create a book based on title, author and publish year.
        
        Keyword arguments:
        title -- book title
        author -- author of book
        year -- the published year of a book
        '''
        self.title = title
        self.author = author
        self.year = year

    def printBook(self):
        '''print the info for Book object, used for checking purposes
        '''
        print("title = " + self.title + "; author = " + self.author +
              "; year = " + self.year + "\n")

def readBookFile(bookFile):
    '''Store the information on the title, published year and author(s) of each book.
    
    parameter: 
    bookFile(.csv file) -- refers to the books.csv test File

    return: 
    booklist(list) -- is a list of Book objects with one author for each. 
    So it takes two instances to store info about Good Omens.
    '''   


    booklist = []
    with open(bookFile, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for bookInfo in reader:
            if ") and" not in bookInfo[2]:
                singleBook = Book(bookInfo[0], bookInfo[2], bookInfo[1])
                booklist.append(singleBook)
            else:
                authors = bookInfo[2].split(' and ')
                for i in range(len(authors)):
                    singleBook = Book(bookInfo[0], authors[i], bookInfo[1])
                    booklist.append(singleBook)
    return booklist


def printBooks(booklist):
    '''print the booklist
    parameters:
    booklist(list) -- a list of Book objects with one author for each.
    '''
    for i in range(len(booklist)):
        Book.printBook(booklist[i])


def getAuthorByKeyword(keyString, booklist):
    '''triggered by correct input of -a arguments. 
    The function looks for authors with names that include keyString
    

    parameters: 
    keyString(string) -- the keyword that user inputs
    booklist(list) -- the whole dataset produced after readBookFile()

    return: 
    selectedAuthors(dictionary) -- contains all the authors and all of their books we found
    '''
    selectedAuthors = {}  
    keyString = keyString.lower()

    for book in booklist:
        if (keyString in book.author.lower()):
            if book.author not in selectedAuthors.keys():
                selectedAuthors[book.author] = []
                selectedAuthors[book.author].append(book.title)
            else:
                selectedAuthors[book.author].append(book.title)

    return selectedAuthors


def printAuthorByKeyword(selectedAuthors, keyString):
    '''print the results for getAuthorByKeyword()

    parameters:
    selectedAuthors(dictionary) -- contains all the authors and all of their books we found
    keyString(string) -- the keyword that user inputs
    '''
    if len(selectedAuthors) == 0:
        print("There are no authors with names containing '" +keyString +\
          "' in this dataset.")
    else:
        print("Here are the authors whose names contain '" + keyString + \
        "' and the books they wrote:")
        for k, v in selectedAuthors.items():
            print(k, v)


def getBookByKeyword(keyString, booklist):
    '''triggered by correct input of get-book-by-keyword arguments
    The function looks for books with titles that include keyString
    
    parameters: 
    keyString(string) -- the keyword that user inputs
    booklist(list) -- the whole dataset produced after readBookFile()

    returns:
    selectedBookTitles(list) -- the results on books it found
    '''
    selectedBookTitles = []
    keyString = keyString.lower()

    for book in booklist:
        if (keyString in book.title.lower()):
            if book.title not in selectedBookTitles:
                selectedBookTitles.append(book.title)

    return selectedBookTitles


def printBookByKeyword(selectedBookTitles, keyString):
    '''print the results for getBookByKeyword()

    prameters:
    selectedBookTitles(list) -- the results on books it found
    keyString(string) -- the keyword that user inputs
    '''
    if len(selectedBookTitles) == 0:
        print("There are no books with titles containing '" + keyString +
              "' in this dataset.")
    else:
        print("Here are the books with titles containing '" + keyString + "':")
        for title in selectedBookTitles:
            print(title)


def getBookByYear(startYear, endYear, booklist):
    '''triggered by correct input of get-book-by-year arguments
    The function looks for books published within the year range (inclusive)
    
    parameters:
    startYear(int) -- start year
    endYear(int) -- end year
    booklist(list) -- the whole dataset produced after readBookFile()

    returns:
    selectedBooksByYear(list) -- the results on books it found
    '''
    selectedBooksByYear = []

    if startYear > endYear:
      temp = startYear
      startYear = endYear
      endYear = temp

    for book in booklist:
        if int(book.year) <= endYear and int(book.year) >= startYear:
            if book.title not in selectedBooksByYear:
                selectedBooksByYear.append([book.title, book.year])
    return selectedBooksByYear


def printBookByYear(selectedBooksByYear, startYear, endYear):
    '''print the results for getBookByYear()
    '''
    if startYear > endYear:
        print("Did you mean " + str(endYear) + " to " + str(startYear) + "?")
        print("Here are the books published from " + str(endYear) + \
            " to " + str(startYear) + ":")
    elif len(selectedBooksByYear) == 0:
        if startYear == endYear:
            print("There are no books published in " + str(startYear) +
                  " in this dataset.")
        else:
            print("There are no books published from " + str(startYear) + \
            " to " + str(endYear) + " in this dataset.")
    else:
        if startYear == endYear:
            print("Here are the books published in " + str(startYear) + ":")
        else:
            print("Here are the books published from " + str(startYear) + \
            " to " + str(endYear) + ":")
    for i in range(len(selectedBooksByYear)):
        print(selectedBooksByYear[i][0] + ", published in " + \
        selectedBooksByYear[i][1])


def help():
    '''
    display the usage/help statement to user
    '''
    print("Here is the usage manual:")
    f = open("usage.txt", "r")
    lines = f.readlines()
    for line in lines:
        print(line)
    f.close()


def get_parsed_arguments():
    '''
    parse the command line arguments based on three features

    returns:
    args -- contains all the information about command line arguments
    '''
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '-a', '--authors', nargs='+', help='find authors with a given string')
    parser.add_argument(
        '-t',
        '--titles',
        nargs='+',
        help='find book titles with a given string')
    parser.add_argument(
        '-y',
        '--years',
        nargs='+',
        help='find books within a given range of years')
    args = parser.parse_args()
    return args


def main():
    booklist = readBookFile('books.csv')
    args = get_parsed_arguments()
    if args.authors: 
        if len(args.authors)>1:
            help()
            print("too many arguments!")
            return
        else:
            keyString = args.authors[0]
            selectedAuthors = getAuthorByKeyword(keyString, booklist)
            printAuthorByKeyword(selectedAuthors, keyString)
    if args.titles:
        if len(args.titles)>1:
            help()
            print("too many arguments!")
            return
        else:
            keyString = args.titles[0]
            selectedBookTitles = getBookByKeyword(keyString, booklist)
            printBookByKeyword(selectedBookTitles, keyString)
    if args.years:
        if len(args.years) >2:
            help()
            print("too many arguments!")
            return
        if(args.years[0].isnumeric()):
            startYear = int(args.years[0])
        else:
            help()
            print("please input an integer!")
            return
        if len(args.years) == 1:
            endYear = startYear
        elif(args.years[1].isnumeric()):
            endYear = int(args.years[1])
        else:
            help()
            print("please input an integer!")
            return
        selectedBooksByYear = getBookByYear(startYear, endYear, booklist)
        printBookByYear(selectedBooksByYear, startYear, endYear)
   

main()

