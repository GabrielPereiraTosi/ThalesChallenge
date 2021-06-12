import os
from datetime import datetime


def write_log(arquivo, diretorioA, diretorioB):
    log_file = open('log.txt', 'a')
    data_hora_atual = datetime.now()
    data_hora_atual_s = data_hora_atual.strftime('%d/%m/%Y %H:%M')
    conteudo_log = "File name: {}; Origin folder: {}; Destination folder: {}; Moved time: {}\n".format(arquivo,
                                                                                                       diretorioA,
                                                                                                       diretorioB,
                                                                                                       data_hora_atual_s)
    log_file.write(conteudo_log)
    log_file.close()

def organizar(diretorioA, diretorioB, regx):
    arquivos = os.listdir(diretorioA)

    for arquivo in arquivos:
        if arquivo.find(regx) >= 0:
            write_log(arquivo, diretorioA, diretorioB)
            os.rename(os.path.join(diretorioA, arquivo), os.path.join(diretorioB, arquivo))

if __name__ == '__main__':
    config_file = open('configFile.txt', 'r')
    configuracoes = config_file.readlines()
    organizar(os.path.join(configuracoes[0].rstrip('\n')), os.path.join(configuracoes[1].rstrip('\n')),
              configuracoes[2])
    config_file.close()
