  #    _    ______   ___  _________________________  _  __  _________  ________
  #   (_)__/ /_  /  / _ \/ __/ ___/  _/ __/  _/ __ \/ |/ / /_  __/ _ \/ __/ __/
  #  / / _  //_ <  / // / _// /___/ /_\ \_/ // /_/ /    /   / / / , _/ _// _/  
  # /_/\_,_/____/ /____/___/\___/___/___/___/\____/_/|_/   /_/ /_/|_/___/___/  
                                                                             

 #  ____  _ _     _ _       _                     
 # | __ )(_) |__ | (_) ___ | |_ ___  ___ __ _ ___ 
 # |  _ \| | '_ \| | |/ _ \| __/ _ \/ __/ _` / __|
 # | |_) | | |_) | | | (_) | ||  __/ (_| (_| \__ \
 # |____/|_|_.__/|_|_|\___/ \__\___|\___\__,_|___/
                                                
import ast #verifica se o da set consisti apenas nas seguintes estruturas literais de Python: strings, números, e etc...
import csv #modulo para leitura de csv
import sys #impresso do sistema
import math #para calculo matematico simples
import os #ajuda a junatar linhas impressas
from math import log
from kFold.kFoldCrossValidation import * # modulo de k fold cross validation em outra pasta



#    ___                                    _              _   __ _                     
#   / __\   _ _ __   ___ ___   ___  ___    /_\  _   ___  _(_) / /(_) __ _ _ __ ___  ___ 
#  / _\| | | | '_ \ / __/ _ \ / _ \/ __|  //_\\| | | \ \/ / |/ / | |/ _` | '__/ _ \/ __|
# / /  | |_| | | | | (_| (_) |  __/\__ \ /  _  \ |_| |>  <| / /__| | (_| | | |  __/\__ \
# \/    \__,_|_| |_|\___\___/ \___||___/ \_/ \_/\__,_/_/\_\_\____/_|\__,_|_|  \___||___/
                                                                                      


#metodo que extrai dados do csv e retorna dicionario data
def carrega_csv(nome_arquivo):
	caminho = os.path.normpath(os.getcwd() + nome_arquivo)
	arquivo = csv.reader(open(caminho))
	linhas = []
	#percorre arquivo 
	for l in arquivo:
		linhas.append(l)

	headers = linhas[0]#pega o cabecalho do data set 
	#ppara percorrer lista de atributos
	indice_nome, nome_indice =  get_nome_cabecalho_mapa_indice(headers)#dado um nome de um cabecalho retorna o indice e vice e versa
	#dicionario que armazena o data set com chaves como: o cabecalho, linhas(exemplos) e indices para nomes
	data = {
		'header': headers,
		'linhas': linhas[1:],
		'nome_indice': nome_indice,
		'indice_nome': indice_nome	
	}
	return data

#Cria um mapa Dado um cabecalho tem se um indice e vice e verca
def get_nome_cabecalho_mapa_indice(headers):
	nome_indice = {}
	indice_nome = {}
	for i in range(0, len(headers)):
		nome_indice[headers[i]] = i
		indice_nome[i] = headers[i]
	return indice_nome, nome_indice	

#projecao das colunas para trabalhar como se fosse umma lista, percorre o data set e pega as colunas desejadas na configuracao
def projeta_colunas(data, colunas_projeta):
	#lista com cabeçalhos e linhas ldata linha, rdata Headers
	h_data = list(data['header'])
	l_data = list(data['linhas'])
	#todas as colunas
	todas_col = list(range(0, len(h_data)))
	# indice das colunas que serao porjetadas 
	projeta_colunas_idx = [data['nome_indice'][nome] for nome in colunas_projeta]
	#seleciona de todas as colunas aquelas que serao porjetadas para remover o resto
	remove_colunas = [col_idx for col_idx in todas_col if col_idx not in projeta_colunas_idx]
	#ordena e remove as colunas nao mencionadas no arquivo configuracao
	for deleta_col in sorted(remove_colunas, reverse=True):
		del h_data[deleta_col]
		for l in l_data:
			del r[deleta_col]
	#retorna um mapa de indice pra cada coluna
	indice_nome, nome_indice = get_nome_cabecalho_mapa_indice(h_data)
	#retorna o data set
	return {'header': h_data, 'linhas': l_data,
			'nome_indice': nome_indice,
			'indice_nome': indice_nome}

#retorna mapa de valor sem repticoes dentro do data set para uso do id3
def get_valor_unico(data):
	indice_nome = data['indice_nome']
	indices = indice_nome.keys()
	mapa_de_valor = {}	
	#cria uma posicao para cada indice dentro de mapa valor
	for indice in iter(indices):
		mapa_de_valor[indice_nome[indice]] = set()
# percorre  linhas e constroi mapa de valor de acordo com indice
	for data_linha in data['linhas']:
		for indice in indice_nome.keys():
			atributo_nome = indice_nome[indice]
			valor = data_linha[indice]
			#caso não esteja no mapa adiciona
			if valor not in mapa_de_valor.keys():
				mapa_de_valor[atributo_nome].add(valor)
	return mapa_de_valor					

#retornar os rotulos das clases
def get_classes(data, atributo_alvo):
	linhas = data['linhas']
	#retorna o indice do atributo alvo 
	id_coluna = data['nome_indice'][atributo_alvo]
	#dicionario com valor das classes
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

#    _______  ____
#   /  _/ _ \|_  /
#  _/ // // //_ < 
# /___/____/____/ 
                

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

erro = 0
def count_erro(raiz, teste, atributo_alvo):
	global erro
	erro = 0
	exemplos = teste['linhas']
	indices = teste['nome_indice']
	def percorre(no, exemplo, indices, atributo_alvo):
		global erro
		if 'classe' in no:
			if no['classe'] != exemplo[indices[atributo_alvo]]:
				erro+=1
		elif 'atributo' in no:
				sub_chave = exemplo[indices[no['atributo']]]
				percorre(no['nodes'][sub_chave], exemplo, indices, atributo_alvo)
	for exemplo in exemplos:
		 percorre(raiz, exemplo, indices, atributo_alvo)
	return erro

node_tree = []
filhos = []
def anda_node(raiz):
	global node_tree
	global filhos
	if 'classe' in raiz:
		filhos = raiz
	else:
		node_tree = raiz['nodes']

#PODA POR ERRO
def poda(raiz):
	global node_tree
	remove_no = node_tree
	monta_arvore(remove_no, raiz)
	return raiz


folha = 0
nozin = 0

#Funçao que atrzves do no raiz imprime as regras da arvore
def imprime_lindamente_arvore_modificada(raiz):
	pilha = []
	regras = set()
	def percorre(no, pilha, regras):
		global folha
		global nozin
		global filhos
		global node_tree
		if 'classe' in no:
			pilha.append(' \tTHEN: '+no['classe'])
			regras.add(''.join(pilha))
			pilha.pop()
			filhos.append(no['classe'])
			folha+=1
		elif 'atributo' in no:
			nodata = 'IF ' if not pilha else ' -> '
			pilha.append(nodata+no['atributo']+'=')
			
			nozin+=1
			for sub_chave in no['nodes']:
				pilha.append(sub_chave)
				percorre(no['nodes'][sub_chave], pilha, regras)
				node_tree.append(no['atributo'])
				pilha.pop()
			pilha.pop()
	percorre(raiz, pilha, regras)
	print(os.linesep.join(regras))
	return folha,nozin
#                  _       
#  _ __ ___   __ _(_)_ __  
# | '_ ` _ \ / _` | | '_ \ 
# | | | | | | (_| | | | | |
# |_| |_| |_|\__,_|_|_| |_|
                         


def main():
	#pega o arquivo de configuracao  e carrega o data set 
	argv = sys.argv
	print("Command line args {}: ".format(argv))
	config=configuracao(argv[1])
	data = carrega_csv(config['data_file'])
	copia_original = data.copy()
	#Kfolds Cross Validation
	k = config['kFolds']
	n_exemplos = config['n_exemplos']
	folds = cross_validation_part(data['linhas'], k, n_exemplos)
	treinamento=[]
	tamanho_folds = len(folds)
	tm_fold = n_exemplos/k
	erroFolds=[]*tamanho_folds
	#apos ter splitado os dados testa o fold e avalia o erro
	for fold in folds:
		data['linhas'] = fold
		teste = data.copy()
		idx_fold = folds.index(fold)
		for i in range(len(folds)):
			if i is not idx_fold:
				treinamento +=folds[i] 
		data['linhas'] = treinamento
		#aplica o id3 no conjunto de treinamento 
		raiz = {}
		data = projeta_colunas(data, config['projecao_colunas'])
		atributo_alvo = config['atributo_alvo']
		restantes = set(data['header'])
		restantes.remove(atributo_alvo)
		unicos = get_valor_unico(data)
		raiz = id3(data, unicos, restantes, atributo_alvo)
		#contabiliza erro para arvore gerada
		erro = count_erro(raiz, teste, atributo_alvo)
		erroFolds.append(erro/tm_fold)

	#calcula a media de erro do folds e  erro padrao
	salva_raiz = raiz
	media_erro = sum(erroFolds)/k
	erro_padrao = math.sqrt((media_erro*(1-media_erro))/n_exemplos)
	# intervalo para 95% de confianca para estimativa do erro verdadeiro
	min_range = media_erro-(1.96*erro_padrao)
	max_range = media_erro+(1.96*erro_padrao)
	#imprime_lindamente_arvore(raiz)
	print("-----------------------------******************DESCRICAO DE ERROS NO  K FOLD CROSS VALIDATION*************------------------------------------")

	media_erro=round(media_erro,4)
	print("Media erro:{0}".format(media_erro))
	min_range=round(min_range,4)
	max_range=round(max_range,4	) 
	print("Intervalo de de:{0}<ERRO VERDADEIRO<{1}".format(min_range,max_range))
	#Cria aletaoriamente folds de treinamento teste e validacao
	conjunto_aleatorio = slplit_data_set(copia_original['linhas'], 3) 
	treinamento = conjunto_aleatorio[0]
	teste = conjunto_aleatorio[1]
	validacao = conjunto_aleatorio[2]
	#faz a poda
	poda(raiz)
	folhas, nos = imprime_lindamente_arvore_modificada(salva_raiz)
	print("Numero de folhas:{0}. Numero de nos internos:{1}".format(folhas, nos))
	
if __name__ == "__main__": main()