#!/usr/bin/python3
import argparse
from parser import Parser, ParserError
from token import Token
from reader import Reader
from lexer import Lexer
if __name__ == '__main__':
    aparser = argparse.ArgumentParser(description='Compiler')
    aparser.add_argument('file')
    args = aparser.parse_args()
    try:
       reader = Reader(args.file)
    except IOError as e:
        print(e)
        exit()
    lexer = Lexer(reader)
    c  = lexer.getToken()
    while(c != Token('', 'EOF')):
        print(c)
        c = lexer.getToken()
 #   parser = Parser(lexer)
 #   try:
 #       (t, tree) = parser.expression()
 #   except ParserError as e:
 #       print(e)
 #       exit()
 #   print(t)
 #   print(tree)

