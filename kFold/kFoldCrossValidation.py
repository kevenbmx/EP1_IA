from random import randrange

#Divide data set em k folds
def cross_validation_part(data, folds, n):
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