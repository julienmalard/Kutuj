import os
import io
import json


class Diccionario(object):
    def __init__(símismo):
        símismo.direc = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Trads')
        with open(símismo.direc, encoding='utf8') as d:
            símismo.dic = json.load(d)

        símismo.verificar_estados()

        símismo.lenguas = símismo.dic['Lenguas']

        símismo.leng = símismo.lenguas[símismo.dic['Actual']]
        símismo.trads_act = símismo.leng['Trads']
        símismo.izq_a_derech = símismo.leng['IzqaDerech']

    def guardar(símismo):
        with io.open(símismo.direc, 'w', encoding='utf8') as d:
            json.dump(símismo.dic, d, ensure_ascii=False)

    def verificar_estados(símismo):
        dic_lenguas = símismo.dic['Lenguas']
        estándar = dic_lenguas['Español']['Trads']

        for nombre, leng in dic_lenguas.items():
            llenos = []
            for frase in estándar:
                if frase in leng['Trads'].keys() and leng['Trads'][frase] != '':
                    llenos.append(1)
                else:
                    llenos.append(0)
            símismo.lenguas[nombre]['Estado'] = sum(llenos)/len(llenos)
