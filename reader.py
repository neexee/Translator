from collections import deque
import io
from array import array
class Reader():
    def __init__(self, file, bufferSize = 10):
        self.bufferSize = bufferSize
        if(file=='-'):
            import sys
            self.file = sys.stdin
        elif (isinstance(file, io.StringIO)):
             self.file = file
        else:
            self.file = io.open(file, mode='r')

        self.buffer = array('u')# deque(maxlen=bufferSize)
        self.lastBuffer = []
        self.buffer.extend(self.file.read(self.bufferSize))

    def putBack(self, c):
       self.buffer.insert(0, c) #insertleft

    def peek(self):
        return self.buffer[0]
    def close(self):
        self.file.close()
    def nextChar(self):
        if(len(self.buffer) == 0):
            try:
               str = self.file.read(self.bufferSize)
            #   self.buffer.extend(str)
            except Exception:
                raise EOFError()
            self.buffer.extend(str)
            if(len(self.buffer)  != 0):
                return self.buffer.pop(0) #popleft
            else:
                return None
        else:
            return self.buffer.pop(0)
