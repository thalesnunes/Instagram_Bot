# -*- coding: utf-8 -*-
from time import sleep

def print_line(lenght=50):


    print('-' *lenght)


def print_title(title, lenght=50):


    size = len(title)
    final = (' ' *((lenght-size)//2)) + title + (' ' *((lenght-size)//2))
    print(final)


def header (title):


    print_line()
    print_title(title)
    print_line()


def menu (option_list):


    for a in range (len(option_list)):
        print (f'{a+1} -- {option_list[a]}')
    print_line()

