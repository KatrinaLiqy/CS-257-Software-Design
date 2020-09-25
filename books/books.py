#books.py
#Authors: Claire Schregardus and Katrina Li
import csv
import sys


#readBookFile
#Store the information on the title, published year and author(s)
#of each book.
#parameter: bookFile(.csv file) refers to the books.csv test File
#return: booklist(list) is a 2d list with the first colomn a book
#title, the second column the published year, and the third column
#one of the authors. So it takes two lines to store info about
#Good Omens
def readBookFile(bookFile):
  booklist=[]
  with open(bookFile, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for bookInfo in reader:
      singleBook = [0,0,0]
      #print(row)
      singleBook[0] = bookInfo[0]
      singleBook[1] = bookInfo[1]


      if ") and" not in bookInfo[2]:
        singleBook[2] = bookInfo[2]
        booklist.append(singleBook)

      else:
        authors = bookInfo[2].split(' and ')
        for i in range(len(authors)):
          singleBook[2] = authors[i]
          booklist.append(singleBook)
          singleBook = [0,0,0]
          singleBook[0] = bookInfo[0]
          singleBook[1] = bookInfo[1]

  return booklist




# getAuthorByKeyword
# triggered by correct input of get-author-by-keyword arguments
# parameters: keyString(string)
#            The function looks for authors with names that include keyString
#            booklist(list) is the whole dataset produced after readBookFile()
# return: No returns, but prints the authors and their books it found.
def getAuthorByKeyword(keyString, booklist):
  selectedAuthors = {} # a 2d list
  keyString = keyString.lower()

  for book in booklist:
    if (keyString in book[2].lower()):
      # if the author has the keyword
      #dict[key] = value
      
      if book[2] not in selectedAuthors.keys():
        selectedAuthors[book[2]] = []
        selectedAuthors[book[2]].append(book[0])
      #if book[2] in selectedAuthors.keys():
      else:
        selectedAuthors[book[2]].append(book[0])
  if len(selectedAuthors) == 0:
    print("There are no authors with names containing '" +keyString +\
      "' in this dataset.")
  else:  
    print("Here are the authors whose names contain '" + keyString + \
    "' and the books they wrote:")      
    for k, v in selectedAuthors.items():
      print(k, v)      
        # if the author is already in selectedAuthors



# getBookByKeyword
# triggered by correct input of get-book-by-keyword arguments
# parameters: keyString(string)
#            The function looks for books with titles that include keyString
#            booklist(list) is the whole dataset produced after readBookFile()
# return: No returns, but prints the results on books it found.
def getBookByKeyword(keyString, booklist):
  selectedBookTitles = []
  keyString = keyString.lower()

  for book in booklist:
    if (keyString in book[0].lower()):
      if book[0] not in selectedBookTitles:
        selectedBookTitles.append(book[0])
  if len(selectedBookTitles) == 0:
    print("There are no books with titles containing '" + keyString + "' in this dataset.")
  else:
    print("Here are the books with titles containing '" + keyString + "':")
    for title in selectedBookTitles:
      print(title)


  
# getBookByYear
# triggered by correct input of get-book-by-year arguments
# parameters: startYear(int), endYear(int)
#            The function looks for books published within the 
#            year range (inclusive)
#            startYear and endYear can be the same
#            booklist(list) is the whole dataset produced after readBookFile()
# return: No returns, but prints the results on books it found.
def getBookByYear(startYear, endYear, booklist):
  selectedBooksByYear = []

  if startYear > endYear:
    print("Did you mean " + str(endYear) + " to " + str(startYear) + "?")
    temp = startYear
    startYear = endYear
    endYear = temp
    
  for book in booklist:
    if int(book[1]) <= endYear and int(book[1]) >= startYear:
      #which means it is selected
      if book[0] not in selectedBooksByYear:
        
        selectedBooksByYear.append([book[0],book[1]])
     
  if len(selectedBooksByYear) == 0:
    if startYear == endYear:
      print("There are no books published in " + str(startYear) + " in this dataset.")
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

 
#help
#display the usage/help statement to user
#parameter: n/a
#return: n/a
def help():
  print("Here is the usage manual:")
  f = open("usage.txt","r")
  #for 
  #fl =f.readlines()
  lines = f.readlines()
  for line in lines:
    print(line)
  f.close()


def main():
  booklist = readBookFile('books.csv')
  #very basic mistakes
  if len(sys.argv) < 2:
    print("You need arguments!")
    help()
  elif sys.argv[1] != "-books":
    print("Please type '-books' as the first command.")
    help()
  elif len(sys.argv) < 3:
    print("You need more arguments than -books !")
    help()
  elif not((sys.argv[2] == "get-title-by-keyword") or (sys.argv[2] == "get-author-by-keyword") or (sys.argv[2] == "get-book-by-year")): 
    print("Please check the three features of this tool.")
    help()
  elif len(sys.argv) < 4:
    print("You need more arguments!")
    help()
  #very basic mistakes end here

  elif sys.argv[2] == "get-title-by-keyword":
    if len(sys.argv) > 4:
      print("Too many arguments!")
      help()
    else:
      getBookByKeyword(sys.argv[3], booklist)
  
  elif sys.argv[2] == "get-author-by-keyword":
    if len(sys.argv) > 4:
      print("Too many arguments!")
      help()
    else:  
      getAuthorByKeyword(sys.argv[3], booklist)

  elif sys.argv[2] == "get-book-by-year" and sys.argv[3].isnumeric() is False:
    print("Please enter an integer.")
    help()
    
  elif sys.argv[2] == "get-book-by-year":
    if len(sys.argv) > 5:
      print("Too many arguments!")
      help()
    
    elif len(sys.argv) == 5:
      # two arguments that should be interpreted as ints
      if sys.argv[4].isnumeric() is False:
        print("Please enter an integer after " + sys.argv[3])
        help()
      else:
        #user wants books published in a range of years
        getBookByYear(int(sys.argv[3]),int(sys.argv[4]), booklist)
    
    else:
      #user wants books published in one year
      getBookByYear(int(sys.argv[3]), int(sys.argv[3]), booklist)
  
  # testing edge cases
  # print("-----test for authors-----")
  # getAuthorByKeyword('xx',booklist)
  # getAuthorByKeyword('!',booklist)

  # print("-----test for titles-----")  
  # getBookByKeyword('rainbow', booklist)

  # print("-----test for years-----")
  # getBookByYear(1670, 1650, booklist)
  # #getBookByYear('one', 'two', booklist)

main()
