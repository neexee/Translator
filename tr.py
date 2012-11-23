#!/usr/bin/python3
import argparse
from parser import Parser, ParserError
from generator import Generator
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
    parser = Parser(lexer)
    try:
        t = parser.program()
        #print(t)
        g = Generator(t)
        code = g.generateCode()
        print(code)
    except ParserError as e:
        print(e)
        exit()
