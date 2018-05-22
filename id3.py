import ast
import csv
import sys
import math
import os
#metodo que extrai dados do csv
def carrega_csv(nome_arquivo):
	caminho = os.path.normpath(os.getcwd() + nome_arquivo)
	arquivo = csv.reader(open(caminho))
	linhas = []
	#percorre arquivo 
	for l in arquivo:
		linhas.append(l)

	headers = linhas[0]
	indice_nome, nome_indice =  get_nome_cabecalho_mapa_indice(headers)

	data = {
		'header': headers,
		'linhas': linhas[1:],
		'nome_indice': nome_indice,
		'indice_nome': indice_nome;
	}
	return data


def get_nome_cabecalho_mapa_indice(headers):
	indice_nome = {}
	nome_indice = {}
	for i in range(0, len(headers)):
		nome_indice[headers[i]] = i
		indice_nome[i] = headers[i]
	return indice_nome, nome_indice	