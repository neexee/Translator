#!/usr/bin/python3
import io
import unittest
from parser import Parser, ParserError
from reader import Reader
from lexer import Lexer
class TestParse(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def testfile(self):
        reader = Reader('test.txt')
        lexer = Lexer(reader)
        parser = Parser(lexer)
        t = parser.expression()
        reader.close()
        self.assertEqual(t, 16.0)
    def testbraces(self):
        str = io.StringIO('(1+2)')
        reader = Reader(str)
        lexer = Lexer(reader)
        parser = Parser(lexer)
        t = parser.expression()
        self.assertEqual(t, 3)
if __name__ =="__main__":
    unittest.main()