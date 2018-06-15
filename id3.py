import ast
import csv
import sys
import math
import os
from math import log
from kFold.kFoldCrossValidation import *
from random import seed
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
		'indice_nome': indice_nome	
	}
	return data

#Cria um mapa Dado um cabeçalho tem se um indice e vice e verca
def get_nome_cabecalho_mapa_indice(headers):
	nome_indice = {}
	indice_nome = {}
	for i in range(0, len(headers)):
		nome_indice[headers[i]] = i
		indice_nome[i] = headers[i]
	return indice_nome, nome_indice	

#projecao das colunas
def projeta_colunas(data, colunas_projeta):
	#lista com cabeçalhos e linhas ldata linha, rdata Headers
	h_data = list(data['header'])
	l_data = list(data['linhas'])
	todas_col = list(range(0, len(h_data)))

	projeta_colunas_idx = [data['nome_indice'][nome] for nome in colunas_projeta]
	remove_colunas = [col_idx for col_idx in todas_col if col_idx not in projeta_colunas_idx]

	for deleta_col in sorted(remove_colunas, reverse=True):
		del h_data[deleta_col]
		for l in l_data:
			del r[deleta_col]

	indice_nome, nome_indice = get_nome_cabecalho_mapa_indice(h_data)
	
	return {'header': h_data, 'linhas': l_data,
			'nome_indice': nome_indice,
			'indice_nome': indice_nome}

#retorna mapa valor sem repticoes dentro do database	
def get_valor_unico(data):
	indice_nome = data['indice_nome']
	indices = indice_nome.keys()
	mapa_de_valor = {}	
	for indice in iter(indices):
		mapa_de_valor[indice_nome[indice]] = set()
#constroi mapa de valor de acordo com indice
	for data_linha in data['linhas']:
		for indice in indice_nome.keys():
			atributo_nome = indice_nome[indice]
			valor = data_linha[indice]
			if valor not in mapa_de_valor.keys():
				mapa_de_valor[atributo_nome].add(valor)
	return mapa_de_valor					
#retornar os rotulos das clases
def get_classes(data, atributo_alvo):
	linhas = data['linhas']
	id_coluna = data['nome_indice'][atributo_alvo]
	classes = {}
	for l in linhas:
		valor = l[id_coluna]
		if valor in classes:
			classes[valor] = classes[valor]+1
		else:
			classes[valor] = 1
	return classes

#entropia deft (com mais atributos) para calcular especificamente da particao 
def entropyII(n, classes):
	ent = 0
	for classe in classes.keys():
		p = classes[classe]/ n	
		ent += - p * math.log(p, 2)
		return ent	


#particiona o conjuto de dados por grupo de atributos
def particao_conjunto(data, grupo_atributo):
	particao = {}
	linhas = data['linhas']
	indice_atributo = data['nome_indice'][grupo_atributo]
	for l in linhas:
		valor_linha = l[indice_atributo]
		if valor_linha not in particao.keys():
			particao[valor_linha] =  {
				'nome_indice': data['nome_indice'],
				'indice_nome': data['indice_nome'],	
				'linhas': list()
			}
		particao[valor_linha]['linhas'].append(l)
	return particao


def  entropia_conjunto(data, atributo, atributo_alvo):
	linhas = data['linhas']
	n = len(linhas)
	particoes = particao_conjunto(data, atributo)

	ent_conj = 0

	for chave_particao in particoes.keys():
		particionado = particoes[chave_particao]
		tamanho_part = len(particionado['linhas'])
		classes_part = get_classes(particionado, atributo_alvo)
		entropia_part = entropyII(tamanho_part, classes_part)
		ent_conj += tamanho_part/ n*entropia_part
	return ent_conj, particoes


#retorna classe mais comun 
def classe_mais_pala(classes):
	pala = max(classes, key=lambda k:classes[k])
	return pala

def id3(data, unicos, restantes, alvo):
	classes = get_classes(data, alvo) #carrega um dicionario baseado na classe alvo
	no={} #sendo uma arvore o no que esta sendo avaliado

	if len(classes.keys())==1:
		no['classe']=next(iter(classes.keys()))
		return no
	if len(restantes) == 0:
		no['classe']=classe_mais_pala(classes)
		return no
	n = len(data['linhas'])
	ent = entropyII(n, classes)

	max_ganho = None
	max_atributo = None
	max_paticoes = None
	#resto é o atributo que dentro dos atributos restantes
	for resto in restantes:
		ent_conj, particoes = entropia_conjunto(data, resto,alvo)
		ganho = ent - ent_conj
		if max_ganho is None or ganho > max_ganho:
			max_ganho=ganho
			max_atributo = resto
			max_paticoes = particoes

	if max_ganho is None:
		no['classe']=classe_mais_pala(classes)
		return no

	no['atributo']=max_atributo
	#armazenara a subarvore ou seja o no percorrido 
	no['nodes']= {}
	#atributos restantes na subarvore abaixo
	restantes_subarvores = set(restantes)
	restantes_subarvores.discard(max_atributo)
	#atributos unicos no conjunto passado
	valores_unicos = unicos[max_atributo]

	for valor in valores_unicos:
		if valor not in max_paticoes.keys():
			no['nodes'][valor] = {'classe':classe_mais_pala(classes)}
			continue
		particoes = max_paticoes[valor]
		no['nodes'][valor] = id3(particoes, unicos, restantes_subarvores, alvo)
	return no

#calcular entropia a partir de uma base de dados DATA(incompleto, falta fazer a comunicação a partir do metodo CarregaDados)
def entropy(data):
  from math import log
  log2 = lambda x:log(x)/log(2) # Para que manja Logaritmos se aproveitamos da troca de base.
  results = uniquecounts(data) #Usamos a função uniquicounts para contar as classes do conjunto.
  ent = 0.0
  for r in results.keys():
      p = float(results[r])/len(data)
      ent = ent-(p*log2(p))#Calculamos a entropia aqui.
  return ent

# carrega as classes e os dados
def CarregaDados (arquivoNome):
	dados = []
	with open(arquivoNome) as arquivo:
	    linha = arquivo.read().split()
	classes = linhas.pop(0).split(';')
	dados = [i.split(';') for i in linhas]
	return classes, dados

#carrega configuracao da arvore arquivo que facilita adaptar o script para qualquer conjuto de dados
def configuracao(arquivoConfig):
	#ast o módulo ast ajuda  a processar árvores da gramática de sintaxe abstrata (Abstract Sintax Trees)
	with open(arquivoConfig, 'r') as arquivo:
		data = arquivo.read()
	return ast.literal_eval(data)
#verifica se consisti apenas nas seguintes estruturas literais de Python: strings, números, tuplas, listas, dicts, booleanos e None.


#Funçao que atrzves do no raiz imprime as regras da arvore
def imprime_lindamente_arvore(raiz):
	pilha = []
	regras = set()
	def percorre(no, pilha, regras):
		if 'classe' in no:
			pilha.append(' ENTAO:'+no['classe'])
			regras.add(''.join(pilha))
			pilha.pop()
		elif 'atributo' in no:
			nodata = 'SE ' if not pilha else '->'
			pilha.append(nodata+no['atributo']+'=')
			for sub_chave in no['nodes']:
				pilha.append(sub_chave)
				percorre(no['nodes'][sub_chave], pilha, regras)
				pilha.pop()
			pilha.pop()

	percorre(raiz, pilha, regras)
	print(os.linesep.join(regras))


def count_erro(raiz, teste, atributo_alvo):
	erro = 0
	exemplos = teste['linhas']
	indices = teste['nome_indice']
	def percorre(no, erro, exemplo, indices, atributo_alvo):
		if 'classe' in no:
			if no['classe'] is not exemplo[indices[atributo_alvo]]:
				erro+=1
		elif 'atributo' in no:
				sub_chave = exemplo[indices[no['atributo']]]
				percorre(no['nodes'][sub_chave], erro, exemplo, indices, atributo_alvo)
	for exemplo in exemplos:
		percorre(raiz, erro, exemplo, indices, atributo_alvo)
	return erro


def main():
	argv = sys.argv
	print("Command line args {}: ".format(argv))
	config=configuracao(argv[1])
	data = carrega_csv(config['data_file'])

	#Kfolds Cross Validation
	seed(42)
	k = config['kFolds']
	n_exemplos = config['n_exemplos']
	folds = cross_validation_part(data['linhas'], k, n_exemplos)
	treinamento=[]
	tamanho_folds = len(folds)
	erroFolds=[]*tamanho_folds
	#apos ter splitado os dados testa o fold e avalia o erro
	for fold in folds:
		data['linhas'] = fold
		teste = data.copy()
		folds.remove(fold)

		for i in range(len(folds)):
			treinamento +=folds[i] #CHUPA BRUNO!!!!!!!!
		data['linhas'] = treinamento
		#aplica o id3 no conjunto de treinamento 
		data = projeta_colunas(data, config['projecao_colunas'])
		atributo_alvo = config['atributo_alvo']
		restantes = set(data['header'])
		restantes.remove(atributo_alvo)
		unicos = get_valor_unico(data)
		raiz = id3(data, unicos, restantes, atributo_alvo)
		erro = count_erro(raiz, teste, atributo_alvo)
		erroFolds.append(erro/len(teste['linhas']))
	#calcula a media de erro do folds e padrao
	media_erro = sum(erroFolds)/k
	erro_padrao = math.sqrt((media_erro*(1-media_erro))/n_exemplos)
	# intervalo para 95% de confianca para estimativa do erro verdadeiro
	min_range = media_erro-(1.96*erro_padrao)
	max_range = media_erro+(1.96*erro_padrao)	
	imprime_lindamente_arvore(raiz)
	print("---------------------------------******************DESCRICAO DE ERROS*************------------------------------------")
	print("Media erro:"+media_erro+)
	print("Intervalode de:"+min_range+"<ERRO VERDADEIRO<"+max_range)
if __name__ == "__main__": main()