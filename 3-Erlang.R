
# Semana 1 - Ejercicio 3. Distribucion Erlang

# Apartados 1 y 2 en papel

# Apartado 3 - Implementacion

rerlang <- function(n, k, lambda=1.) {
  #
  # Genera muestras distribuidas segun la distribucion de Erlang(k,lambda)
  # Args:
  #    n : Numero de muestras
  #    k : Parametro k de la distribucion
  #    lambda : Parametro lambda de la distribucion
  
  # Matrix kxn de muestras u(0,1)
  uniformes = matrix(runif(n*k), nrow=k, ncol=n)
  
  # Reducimos la matrix a un vector multiplicando las columnas
  # Y transformamos para que sea Erlang(k,lambda)
  erlangs = (-1./lambda) * log(apply(uniformes, 2, prod))
  
  return (erlangs)
}

# Generamos muestras de Erlangs usando nuestro generador y dibujamos histograma
n <- 1000 # Numero de muestras a generar
k <- 10
lambda <- 0.8

muestra <- rerlang(n,k,lambda)

# Dibujamos histograma de la muestra
hist(muestra, prob=T, breaks = 20,
     main=paste('Distribution Erlang(',k,', ',lambda,')', sep=''))

# Dibujamos la función de densidad de erlang sobre el histograma
xfit <- seq(0, max(muestra)+1, length = 100) 
yfit <- dgamma(xfit, shape=k, rate = lambda)
lines(xfit, yfit, col = "blue", lwd = 2)



