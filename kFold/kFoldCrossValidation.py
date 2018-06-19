from random import randrange
from random import seed # para montar os folds radomicamnete 
#Divide data set em k folds
def cross_validation_part(data, folds, n):
	seed(42)
	fold_tamanho=int(n/folds)
	copia=data
	split=list()
	for i in range(folds):
		fold = list()
		while len(fold) < fold_tamanho:
			index = randrange(len(copia))
			fold.insert(i, copia.pop(index))
		split.append(fold)
	return split

def cross_validation_part_poda(data, folds, n):
	seed(42)
	fold_tamanho=int(n/folds)
	copia=data
	split=list()
	for i in range(folds):
		fold = list()
		while len(fold) < fold_tamanho:
			index = randrange(len(copia))
			fold.insert(i, copia.pop(index))
		split.append(fold)
	return split