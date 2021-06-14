import schedule
import threading
import time
import os

import PySimpleGUI as sg

from src.Organizando import organizar, vizualizar_dados, write_config


class View:

    def __init__(self):
        sg.theme('black')
        layout = [
            [sg.Text('RegX', size=(13, 1)),
             sg.Input(key='regx', size=(20, 1))],
            [sg.Text('Origin Folder', size=(13, 1)),
             sg.Input(key='origin', size=(35, 1))],
            [sg.Text('Destination Folder', size=(13, 1)),
             sg.Input(key='destination', size=(35, 1))],
            [sg.Text('Period'), sg.Combo(values=list(range(100)), key='periodo', default_value=60, size=(3, 1))],
            [sg.Output(size=(130, 35), key='output')],
            [sg.Button('Run App')]
        ]
        self.janela = sg.Window('Organizer', layout)

    def iniciar(self):
        while True:
            evento, valores = self.janela.read()

            if evento == sg.WIN_CLOSED:
                break
            if evento == 'Run App':
                if os.path.isfile('config.txt'):
                    print('Já esta sendo executado um processo de organização, '
                          'caso deseje mudar a configuração finalize o processo atual.')
                else:
                    write_config(valores['origin'], valores['destination'], valores['regx'])
                    threading.Thread(target=self.job_threading, args=(valores['origin'],
                                                                      valores['destination'],
                                                                      valores['regx'],
                                                                      valores['periodo']), daemon=True).start()

    def job_threading(self, diretorioA, diretorioB, regX, periodo):
        schedule.every(periodo).seconds.do(self.job, diretorioA, diretorioB, regX)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def job(self, diretorioA, diretorioB, regX):
        self.janela.find_element('output').Update('')
        organizar(diretorioA, diretorioB, regX)
        print(vizualizar_dados())


v = View()
v.iniciar()
