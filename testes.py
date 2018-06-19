
def estudoFor():
	erro = 0.083
	for i in range(2560):
		i = (i+2560)
		erro = erro + 0.000001
		print("{0},{1}".format(i, 1-erro))

def main():
	estudoFor()
if __name__ == "__main__": main()