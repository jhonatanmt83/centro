#encoding: utf-8
import os
texto = "borrados.txt"
archi=open(texto,'r')
linea=archi.readline()
while linea!="":
	#os.system("git rm " + linea)
	linea = linea.replace(" ", "\ ")
	os.system("git rm " + linea)
	linea=archi.readline()
archi.close()
