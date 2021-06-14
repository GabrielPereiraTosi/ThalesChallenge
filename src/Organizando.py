import os
from datetime import datetime


def write_config(diretorio_a, diretorio_b, regx, periodo):
    # Armazena as configurações usadas em um .txt
    with open('config.txt', 'a') as arquivo:
        arquivo.write("{}\n{}\n{}\n{}\n".format(diretorio_a, diretorio_b, regx, periodo))


def write_log(arquivo, diretorio_a, diretorio_b):
    # Armazena os dados de cada arquivo movimentado em um .txt
    with open('log.txt', 'a') as log_file:
        data_hora_atual = datetime.now()
        data_hora_atual_s = data_hora_atual.strftime('%d/%m/%Y %H:%M')
        conteudo_log = "Nome arquivo: {}; Diretorio origem: {}; Diretorio destinatario: {}; Movido em: {}\n".format(
            arquivo,
            diretorio_a,
            diretorio_b,
            data_hora_atual_s)
        log_file.write(conteudo_log)


def vizualizar_dados():
    retorno = '----------------------------------LOG----------------------------------\n'
    if os.path.isfile('log.txt'):
        with open('log.txt', 'r') as log:
            log_r = log.readlines()

        for linha_l in log_r:
            retorno += linha_l + '\n'
    else:
        retorno += 'Nenhum arquivo com o regx informado...'
    return retorno


def organizar(diretorio_a, diretorio_b, regx):
    arquivos = os.listdir(diretorio_a)

    for arquivo in arquivos:
        # Move o arquivo encontrado para o diretorio destinatario caso o regx informado seja encontrado
        if arquivo.rfind(regx) >= 0:
            write_log(arquivo, diretorio_a, diretorio_b)
            os.rename(os.path.join(diretorio_a, arquivo), os.path.join(diretorio_b, arquivo))


def guarda_log_e_config():
    # Armazena os arquivos log.txt e config.txt em um pasta target
    target_path = os.path.realpath('target')
    if os.path.isfile('log.txt'):
        log_nome = 'log_{}_{}-{}.txt'.format(datetime.now().date(), datetime.now().hour, datetime.now().minute)
        log_path = os.path.realpath('log.txt')
        os.rename(log_path, os.path.join(target_path, log_nome))
    config_nome = 'config_{}_{}-{}.txt'.format(datetime.now().date(), datetime.now().hour, datetime.now().minute)
    config_path = os.path.realpath('config.txt')
    os.rename(config_path, os.path.join(target_path, config_nome))
