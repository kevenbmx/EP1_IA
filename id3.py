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


# carrega as classes e os dados
def CarregaDados(arquivoNome):
	dados = []
	with open(arquivoNome) as arquivo:
	    lines = arquivo.read().split()
	classes = lines.pop(0).split(';')
	dados = [i.split(';') for i in lines]
	return classes, dados

# mapeia todos os atributos possiveis (somente strings por enquanto)
def DefineAtributos(classes,dados):
	resp = []
	cont = 0
	for c in classes:
		ex = []
		for l in dados:
			if type(l) != int:
				ex.append(l[cont])
			else:
				ex.append('num')
		cont+=1
		ex = list(set(ex))
		resp.append(ex)
	return resp

# começa a contagem de atributos (incompleto)
def ContaAtributos(classes, dados, atributos):
	resp = []
	for a in atributos:
		r = {}
		for b in a:
			r[b] = 0
		resp.append(r)
	return resp
