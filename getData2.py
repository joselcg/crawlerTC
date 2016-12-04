#-*- coding: utf-8 -*- 

from bs4 import BeautifulSoup
import requests
import os
import urllib
import xlsxwriter

#427 paginas de lotes

#Create an new Excel file and add a workshett
workbook = xlsxwriter.Workbook('articulos2.xlsx');
worksheet = workbook.add_worksheet()

worksheet.set_column('A:A', 20)
worksheet.set_column('B:B', 20)
worksheet.set_column('C:C', 100)


for k in range(427): 
	numero = str(k + 1)
	url = "http://www.todocoleccion.net/catalogo-coleccionismo-antiguedades-ventas-subastas-I=c-0-Ultima_Modificacion-" + numero + "-2-DESC-vs-2146807048"
	print url
	req = requests.get(url)

	statusCode = req.status_code
	
	#Pasamos el contenido HTML de la web a un objeto BeautifulSOup()
	html = BeautifulSoup(req.text)

	#Obtenemos todos los divs donde estan los articulos
	articulos = html.find_all('div',{'class':'lote-item-info-content'})
	
	#Recorremos todos los articulos
	for i, articulo in enumerate(articulos):
		url2 = articulo.find('a',{'class':'lote-titulo-enlace nombre block'})
		url2 = "http://todocoleccion.net" + str(url2.get('href').encode('ascii', 'ignore'))
		req2 = requests.get(url2.encode('ascii', 'ignore'))
		html2 = BeautifulSoup(req2.text)
		titulo = html2.find('p',{'class':'lead'})
		if titulo is not None:
			titulo = html2.find('p',{'class':'lead'}).getText() 
		precio = html2.find('span',{'class':'lote-precio precio_directa margin-right'})
		if precio is None:
			precio = html2.find('span',{'class':'precio-subasta lote-precio'})
			if precio is not None:
				precio = html2.find('span',{'class':'precio-subasta lote-precio'}).getText()
		else:
			precio = html2.find('span',{'class':'lote-precio precio_directa margin-right'}).getText()
		descripcion = html2.find('span',{'itemprop':'description'})
		if descripcion is not None:
			descripcion = descripcion.getText()	
	
		#Imprimimos el Titulo
		#print "%d - %s - %s - %s" %(i+1, titulo, precio, descripcion)
		#Escribimos en la hoja excel
		l = 0
		if k > 0:
			l = (k*30) + i + 2
		else:
			l = i + 2
			
		worksheet.write('A' + str(l), str(l-1))
		worksheet.write('B' + str(l), titulo)
		worksheet.write('C' + str(l), precio)
		worksheet.write('D' + str(l), descripcion)
		#Creamos el directorio para guardar las imagenes
		#os.mkdir(str(l-1))
		#page_images = [image["src"] for image in html2.findAll("img")]
		#cadena = "cloud"
		#j = 1 
		#for img in page_images:
		#	imagen = (str(img.encode('ascii','ignore')))
		#	if  cadena in imagen :
		#		urllib.urlretrieve(imagen, './' + str(l-1) + '/' + str(j) + '.jpg')
		#		j += 1

workbook.close()
	

