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



def read_show_file():


    print_line()
    print_title('PESSOAS CADASTRADAS')
    print_line()

    sleep(0.5)

    try:
        file_test = open ('listagem_pessoas.txt', 'r')
        file_test.close()

    except:
        print('\033[31mAinda não há um arquivo com nomes salvos. Cadastre uma nova pessoa!\033[m')

    else:
        with open ('listagem_pessoas.txt', 'r') as file_handler:
            for identity in file_handler:
                    print(identity.replace('\n', ''))


def add_person():


    print_line()
    print_title('NOVO CADASTRO')
    print_line()

    nome = str(input('Digite o nome a ser cadastrado: '))
    while True:
        try:
            idade = int(input('Digite a idade da pessoa: '))
        except:
            print('\033[31mErro! Digite um número inteiro para a idade.\033[m')
        else:
            break

    sleep(0.25)


    try:
        file_test = open ('listagem_pessoas.txt', 'r')
        file_test.close()

    except:
        text_w = nome.title() + ' '*(46-len(nome)-len(f'{idade} anos')) + f'{idade} anos'
        with open ('listagem_pessoas.txt', 'w') as file_handler:
            file_handler.write(text_w)

    else:
        text_a = '\n' + nome.title() + ' '*(46-len(nome)-len(f'{idade} anos')) + f'{idade} anos'
        with open ('listagem_pessoas.txt', 'a') as file_handler:
            file_handler.write(text_a)
    finally:
        print(f'Novo registro de {nome.title()} adicionado.')