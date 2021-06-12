import os


def organizar(diretorioA, diretorioB, regx):
    arquivos = os.listdir(diretorioA)

    for arquivo in arquivos:
        if arquivo.find(regx) >= 0:
            os.rename(os.path.join(diretorioA, arquivo), os.path.join(diretorioB, arquivo))

if __name__ == '__main__':
    config_file = open('configFile.txt', 'r')
    configuracoes = config_file.readlines()
    organizar(os.path.join(configuracoes[0].rstrip('\n')), os.path.join(configuracoes[1].rstrip('\n')),
              configuracoes[2].rstrip('\n'))
    config_file.close()
