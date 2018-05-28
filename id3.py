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

#Cria um mapa Dado um cabeçalho tem se um indice e vice e verca
def get_nome_cabecalho_mapa_indice(headers):
	indice_nome = {}
	nome_indice = {}
	for i in range(0, len(headers)):
		nome_indice[headers[i]] = i
		indice_nome[i] = headers[i]
	return indice_nome, nome_indice	

def projeta_colunas(data, colunas_projeta):
	#lista com cabeçalhos e linhas ldata linha, rdata Headers
	h_data = list(data['headers'])
	l_data = list(data['linhas'])
	todas_col = list(range(0, len(h_data)))

	projeta_colunas_idx = [data['nome_indice'][nome] for nome in colunas_projeta]
	remove_colunas = [col_idx for col_idx in todas_col if col_idx not in projeta_colunas_idx]

	for deleta_col in sorted(remove_colunas, reverse=True):
		del h_data[deleta_col]
		for l in l_data:
			del r[deleta_col]

	indice_nome, nome_indice = get_nome_cabecalho_mapa_indice(h_data)
	
	return {'header': h_data, 'linhas' l_data,
			'nome_indice': nome_indice,
			'indice_nome': indice_nome}	
def get_valor_unico(data):
	indice_nome = data['nome_indice']
	indices = indice_nome.keys()
	mapa_de_valor = {}
	for indice in iter(indices):
		mapa_de_valor[indice_nome] = set()

	for l_data in data['linhas']:
		for indice in indice_nome.keys()
			

def main():
	argv = sys.argv
    print("Command line args {}: ".format(argv))

if __name__ == "__main__": main()