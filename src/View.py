import schedule
import threading
import time
import os

import PySimpleGUI as sg

from src.Organizando import organizar, vizualizar_dados, write_config, guarda_log_e_config


class View:

    def __init__(self):
        #Criação da tela
        sg.theme('Reddit')
        layout = [
            [sg.Text('RegX', size=(18, 1)),
             sg.Input(key='regx', size=(25, 1))],
            [sg.Text('Diretório Origem', size=(18, 1)),
             sg.Input(key='origin', size=(50, 1))],
            [sg.Text('Diretório Destinatário', size=(18, 1)),
             sg.Input(key='destination', size=(50, 1))],
            [sg.Text('Período'), sg.Combo(values=list(range(1, 121)), key='periodo', default_value=60, size=(4, 1))],
            [sg.Output(size=(175, 30), key='output')],
            [sg.Button('Run')]
        ]
        self.janela = sg.Window('Organizador de Arquivos', layout)

    def iniciar(self):
        while True:
            #Pegando todos os eventos e valores recebidos na tela até que a mesma seja fechada
            evento, valores = self.janela.read()

            if evento == sg.WIN_CLOSED:
                if os.path.isfile('config.txt'):
                    guarda_log_e_config()
                break
            if evento == 'Run':
                #Caso o programa já esteja com um processo rodando não será possivel criar outro
                if os.path.isfile('config.txt'):
                    sg.popup('Já esta sendo executado um processo de organização, '
                             'caso deseje mudar a configuração finalize o processo atual.')
                #Validando campos para que nao estejam vazios ou com diretórios incorretos
                elif (not os.path.isdir(valores['origin'])) or valores['origin'] == '':
                    sg.popup('Diretório Origem', 'É necessário que se utilize um diretório válido para a organização.')
                elif (not os.path.isdir(valores['destination'])) or valores['destination'] == '':
                    sg.popup('Diretório Destinatário', 'É necessário que se utilize um diretório válido para a organização.')
                elif valores['regx'] == '':
                    sg.popup('RegX', 'É necessário que se utilize um Regx válido.')
                #Inicia o processo de organização
                else:
                    print('Iniciando o processo de organização...')
                    write_config(valores['origin'], valores['destination'], valores['regx'], valores['periodo'])
                    with open('config.txt', 'r') as config:
                        configuracoes = config.readlines()
                        diretorio_a = configuracoes[0].rstrip('\n')
                        diretorio_b = configuracoes[1].rstrip('\n')
                        regx = configuracoes[2].rstrip('\n')
                        periodo = int(configuracoes[3].rstrip('\n'))
                        threading.Thread(target=self.job_threading, args=(diretorio_a, diretorio_b, regx,
                                                                          periodo), daemon=True).start()

    def job_threading(self, diretorio_a, diretorio_b, regX, periodo):
        #Configura um agendamento de tarefa em que cada periodo em segundos a tarefa seja executada
        schedule.every(periodo).seconds.do(self.job, diretorio_a, diretorio_b, regX)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def job(self, diretorio_a, diretorio_b, regx):
        #Chama o metodo principal para a organização de arquivos
        self.janela.find_element('output').Update('')
        organizar(diretorio_a, diretorio_b, regx)
        print(vizualizar_dados())


v = View()
v.iniciar()
