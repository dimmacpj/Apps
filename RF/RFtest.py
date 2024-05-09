import os
import sys

class RFtest:
    def first_keyword(self):
        fp = open('C:\\Users\\neal.peng\\Documents\\Programming\\RF\\robot_fk', 'a')
        fp.write('this is the first keyword\r\n')
        fp.close()
    
    def plus(self, arg_a, arg_b):
        return int(arg_a) + int(arg_b)

    def multi(self, arg_a, arg_b, arg_c):
        return int(arg_a)*int(arg_b)*int(arg_c)