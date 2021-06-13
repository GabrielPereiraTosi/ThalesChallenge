import PySimpleGUI as sg
from src.Organizando import organizar


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
            [sg.Text('Period'), sg.Combo(values=list(range(100)), key='period', default_value=60, size=(3, 1))],
            [sg.Output(size=(50, 10))],
            [sg.Button('Run App')]
        ]
        self.janela = sg.Window('Organizer', layout)

    def iniciar(self):
        while True:
            evento, valores = self.janela.read()
            if evento == sg.WIN_CLOSED:
                break
            if evento == 'Run App':
                organizar(valores['origin'], valores['destination'], valores['regx'])
                print(valores['origin'])


v = View()
v.iniciar()
