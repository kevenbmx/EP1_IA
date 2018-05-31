import ast
import csv
import sys
import math
import os
from math import log

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

#projecao das colunas
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

#retorna mapa valor sem repticoes dentro do database	
def get_valor_unico(data):
	indice_nome = data['nome_indice']
	indices = indice_nome.keys()
	mapa_de_valor = {}	
	for indice in iter(indices):
		mapa_de_valor[indice_nome] = set()
	#constroi mapa de valor de acordo com indice
	for l_data in data['linhas']:
		for indice in indice_nome.keys()
			atributo_nome = indice_nome[indice]
			valor = l_data[indice]
			if valor not in mapa_de_valor.keys()
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
		p = clases[classe]/ n	
		ent += - p * math.log(p, 2)
		return ent	


#particiona o conjuto de dados por grupo de atributos
def particao(data, grupo_atributo):
	paticao = {}
	linhas = data['linhas']
	indice_atributo = data['nome_indice'][grupo_atributo]
	for l in linhas:
		valor_linha = l[indice_atributo]
		if valor_linha not in paticao.keys()
			particao[valor_linha] =  {
				'nome_indice':data['nome_indice']
				'indice_nome':data['indice_nome']
				'linhas':list()
			}
		particao[valor_linha]['linhas'].append(l)
	return particao


def  entropia_conjunto(data, atributo, atributo_alvo):
	linhas = data['linhas']
	n = len(linhas)
	particoes = particao(data, atributo)

	ent_conj = 0

	for chave_particao in particoes.keys():
		particionado = particoes[chave_particao]
		tamanho_part = len(particionado['linhas'])
		classes_part = get_classes(particionado, atributo_alvo)
		entropia_part = entropyII(tamanho_part, classes_part)
		ent_conj += tamanho_part/(n*entropia_part)
	return ent_conj, particoes


#retorna classe mais comun 
def classe_mais_pala(classes)
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
	no['nodes']= {} #armazenara a subarvore ou seja o no percorrido 
	#atributos restantes na subarvore abaixo
	restantes_subarvores = set(restantes)
	restantes_subarvores.discard(max_atributo)

	valores_unicos = unicos[max_atributo] #atributos unicos no conjunto passado

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
	    lines = arquivo.read().split()
	classes = lines.pop(0).split(';')
	dados = [i.split(';') for i in lines]
	return classes, dados

#carrega configuracao da arvore arquivo que facilita adaptar o script para qualquer conjuto de dados
def configuracao(arquivoConfig):
	#ast o módulo ast ajuda  a processar árvores da gramática de sintaxe abstrata (Abstract Sintax Trees)
	with open(arquivoConfig, 'r') as arquivo:
		data = arquivo.read().repalce('\n', '')#retira linhas
	return ast.literal_eval(data)
#verifica se consisti apenas nas seguintes estruturas literais de Python: strings, números, tuplas, listas, dicts, booleanos e None.


# mapeia todos os atributos possiveis (somente strings por enquanto)
def DefineAtributos (classes,dados):
	resp = []
	cont = 0
	for c in classes:
		ex = []
		for d in dados:
			try:
				numero = int(d[cont])
				ex.append('num')
			except Exception:
				ex.append(d[cont])		    	
		cont+=1
		ex = list(set(ex))
		ex.sort()
		resp.append(ex)
	return resp


'''
começa a contagem de atributos 
atributosDescricao indices: 
	0 = contagem, 
	1 = contagem da classe1, 
	2 = contagem da classe2,
	3 = entropia
'''
def AtributosDescricao (classes, dados, atributos):
	resp = []
	for a in atributos:
		r = {}
		for b in a:
			r[b] = [0, 0, 0, 0]
		resp.append(r)
	for d in dados:
		j = dados.index(d)
		for a in d:
			i = d.index(a)
			try:
				numero = int(a)
				# 							IMPLEMENTAR
			except Exception:
				aux = resp[i]
				aux2 = aux[a]
				aux2[0]+=1
				#print (d[len(d)-1])
				atri = atributos[len(atributos)-1]
				if d[len(d)-1] == atri[0]:
					aux2[1]+=1
				else:
					aux2[2]+=1
	return resp

# carrega em atributosDescricao a entropia de todos os atributos
def Entropia(atributosDescricao,atributos):
	resp = atributosDescricao
	for ad in resp:
		a = atributos[resp.index(ad)]
		for b in a:
			atual = ad[b]
			try:
				entropiaP =  - ((atual[1]/atual[0]) * (log(atual[1]/atual[0])/log(2)))
			except Exception:
				entropiaP = 0
			try:
				entropiaN =  - ((atual[2]/atual[0]) * (log(atual[2]/atual[0])/log(2)))
			except Exception:
				entropiaN = 0
			atual[3] = entropiaP + entropiaN
	return resp

# calcula o ganho de todas as classes
def Ganho(atributosDescricao,atributos,classes):
	resp = {}
	aux = atributosDescricao[len(atributosDescricao)-1]
	aux1 = atributos[len(atributos)-1]
	a1 = aux[aux1[0]]
	a2 = aux[aux1[1]]
	total = a1[0]+a2[0]
	entropiaTotal = - ((a1[0]/total) * (log(a1[0]/total)/log(2))) - ((a2[0]/total) * (log(a2[0]/total)/log(2)))
	for ad in atributosDescricao:
		ganho = entropiaTotal
		for a in ad:
			b = ad[a]
			ganho -= (b[0]/total)*b[3]
		i = atributosDescricao.index(ad)
		resp[classes[i]] = ganho
	return resp




def main():
	argv = sys.argv
    print("Command line args {}: ".format(argv))
 if __name__ == "__main__": main()