
# Semana 1. Digitos de pi y distribucion uniforme
# Nombre del archivo
file = "pi.txt";

# Funcion auxiliar para trozear la cadena leida en bloques
splitInParts <- function(string, size){
  pat <- paste0('(?<=.{',size,'})')
  strsplit(string, pat, perl=TRUE)
}

contarOcurrencias <- function(file, n, g=1, isString=F) {
  #
  # Funcion para contar digitos de pi en bloques
  #
  #   file: Nombre del fichero a leer los digitos o string con digitos
  #   n : Numero de digitos a leer
  #   g: Tam de los bloques de digitos, por ejemplo
  #       si g=2 pi-3 se trocearia como 14 15 92 65 35 ...
  #   isString : Si F se asume que se ha pasado el nombre del fichero,
  #              si es T se asume que se ha pasado la cadena leida
 
  if (!isString) { # Si no es string asumimos que se pasa nombre de fichero
    s <- readChar(file, n)
  } else {
    # Si isString se pasa de argumento la cadena leida ya
    s <- file[1:n]
  }
  s <- splitInParts(s, g)
  s <- lapply(s, as.numeric)
  s <- s[[1]]
  m <- 10**g - 1
  ocurrencias <- c()
  
  
  for(i in 0:m){
    ocurrencias[[i+1]] <- sum(s == i)
  }
  
  
  return (ocurrencias)
} 

testUniforme <- function(ocurrencias) {
  # Test de chi^2 para probar la uniformidad de una muestra
  # dada la frecuencia de un muestra
  
  # Numero de grupos
  n <- length(ocurrencias)
  # Valor esperado si fuera uniforme
  E = sum(ocurrencias)/n

  chi2 <- sum((E - ocurrencias)**2/E)
  
  # Devolvemos el valor de la ji^2
  dchisq(chi2,n-1)
  
}
# Apartados a) y b)
# Link con digitos de pi
# http://www.geom.uiuc.edu/~huberty/math5337/groupe/digits.html
# Para limpiar el fichero, suponiendo que tenemos el fichero en pi_aux.txt
# empleamos cat pi_aux.txt | tr -d "\t" > pi.txt

# Apartado c)

# Mil primeros digitos
n <- 10000
grupos <- 1

# Contamos frecuencias en 1000 primeros digitos de pi
ocurrencias <- contarOcurrencias(file, n, 10**(grupos-1))

# Bar plot con las ocurrencias
barplot(ocurrencias,names.arg=as.character(0:(10**grupos -1)) ,
        main = paste("Distribucion de",n,"digitos de pi en grupos de",grupos))

# Obtenido un p-valor de 0.08235065
print(testUniforme(ocurrencias))


# Apartado d)
n <- 20000
grupos <- 2

# Frecuencia primeras 10.000 parejas
ocurrencias <- contarOcurrencias(file, n, grupos)

# Bar plot con las ocurrencias
barplot(ocurrencias,names.arg=as.character(0:(10**grupos -1)) ,
        main = paste("Distribucion de",n,"digitos de pi en grupos de",grupos))

# Matriz con ocurrencias de las 100 parejas
mat <- matrix(ocurrencias,10**(grupos-1),10**(grupos-1))
print(mat)

# Obtenido un p-valor de 0.01192965
print(testUniforme(ocurrencias))


# Apartado e)

s <- readChar(file, 1e6) # Leemos un millon de digitos de pi
