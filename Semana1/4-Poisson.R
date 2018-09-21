
# Semana 1 - Ejercicio 4. Poisson

# Para generar la poisson simularemos la llegada de eventos 
# Sumando los tiempos distribuidos de forma exponencial
# Para generar el valor de la dist de poisson contaremos
# El numero de eventos que han ocurrido en 1 unidad de tiempo
generador <- function(n,lambda=1) {
  #
  # Generador de v.a. distribuida Poisson(lambda)
  # Args:
  #   n : Numero de muestras a generar
  #   lambda: Parametro lambda de la distribucion
  
  muestra <- c()
  rate <- exp(-lambda)
  
  for(i in 1:n) {
    s <- 1 # Tiempo transcurrido
    a <- -1 # Numero de eventos ocurridos
    while(s >= rate) {
      
      s = s * runif(1)
      a = a + 1
    }
    muestra[[i]] <- a
  }
  
  return (muestra)
}

n <- 10000 # Numero de muestras a generar
lambda <- 7 # Parametro lambda de la poisson

muestra <- generador(n,lambda)

# Tanto la media como la muestra de la poblacion es lambda
# Por tanto la media y varianza muestral son estimadores insesgados
# de lambda
print(mean(muestra))
print(var(muestra))

# Histograma de la muestra y funcion de masa de la poisson
histograma <- hist(muestra, prob=T, main=paste("Poisson(",lambda,")", sep=""))

plot(histograma$breaks[-length(histograma$breaks)], histograma$density,type='h',
     main=paste("Poisson(",lambda,")",sep=""),xlab = "",ylab="")
points(histograma$breaks[-length(histograma$breaks)], histograma$density, pch=16)
# Dibujamos distribucion
points(histograma$breaks[-length(histograma$breaks)], 
     dpois(histograma$breaks[-1], lambda = lambda), col='red')

legend("topright",legend=c("Generated", "Theorical"),col=c("black", "red"), inset=0.1, 
       pch=c(16,1))





