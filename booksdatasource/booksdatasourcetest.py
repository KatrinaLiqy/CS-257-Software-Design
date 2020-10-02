'''
booksdatasourcetest.py
Katrina Li and Claire Schregardus
'''

import BooksDataSource
import unittest

class BooksDataSourceTest(unittest.TestCase):
    def setUp(self):
        #print("set up")
        self.my_source = BooksDataSource.BooksDataSource("testBooks.csv", "testAuthors.csv")
        
    def tearDown(self):
        #print("tear down")
        pass
        
    def test_wrong_authorID(self):
        with self.assertRaises(ValueError):
            self.my_source.books(author_id=24)
   
    def test_negative_authorID(self):
        with self.assertRaises(ValueError):
            self.my_source.books(author_id=-1)

    def test_book_search_text(self):
        self.assertEqual(self.my_source.books(search_text="Sul"),[{'title':'Sula', 'publication_year':1973, 'author_id':'2'}])
    
    def test_book_case_sensitivity(self):
        self.assertEqual(self.my_source.books(search_text="sul"),[{'title':'Sula', 'publication_year':1973, 'author_id':'2'}])
    
    def test_wrong_book_search_text(self):
        self.assertEqual(self.my_source.books(search_text="dog"), [])

    def test_start_year(self):
        self.assertEqual(self.my_source.books(start_year=1973),[{'title':'Sula', 'publication_year':1973, 'author_id':'2'},{'title':'All Clear', 'publication_year':2010, 'author_id':'0'}])
        
    def test_end_year(self):
      self.assertEqual(self.my_source.books(end_year=1973),[{'title':'And Then There Were None', 'publication_year':1939, 'author_id':'1'},{'title':'Sula', 'publication_year':1973, 'author_id':'2'}])

    def test_sort_year(self):
      self.assertEqual(self.my_source.books(sort_by='year'),[{'title':'And Then There Were None', 'publication_year':1939, 'author_id':'1'},{'title':'Sula', 'publication_year':1973, 'author_id':'2'},{'title':'All Clear', 'publication_year':2010, 'author_id':'0'}])

    def test_sort_authors(self):
        self.assertEqual(self.my_source.authors(),[{'id':1, 'last_name':'Christie', 'first_name':'Agatha', 'birth_year':1890, \
        'death_year':1976},{'id':2, 'last_name':'Morrison', \
        'first_name':'Toni','birth_year':1931,'death_year':None},{'id':0, \
        'last_name':'Willis','first_name':'Connie', 'birth_year':1945, \
        'death_year':None}])

    def test_author_search_text(self):
      self.assertEqual(self.my_source.authors(search_text="ni"), \
      [{'id':2, 'last_name':'Morrison','first_name':'Toni','birth_year':1931,\
      'death_year':None},{'id':0,'last_name':'Willis','first_name':'Connie', \
      'birth_year':1945, 'death_year':None}])

    def test_author_case_sensitivity(self):
      self.assertEqual(self.my_source.authors(search_text="NI"), \
      [{'id':2, 'last_name':'Morrison','first_name':'Toni','birth_year':1931,\
      'death_year':None},{'id':0,'last_name':'Willis','first_name':'Connie', \
      'birth_year':1945, 'death_year':None}])

    def test_author_wrong_search_text(self):
      self.assertEqual(self.my_source.authors(search_text="cat"), [])
      
    if __name__ == '__main__':
    unittest.main()

