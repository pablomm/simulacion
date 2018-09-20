
# Semana 1 - Ejercicio 4. Poisson

# Para generar la poisson simularemos la llegada de eventos 
# Sumando los tiempos distribuidos de forma exponencial
# Para generar el valor de la dist de poisson contaremos
# El numero de eventos que han ocurrido en 1 unidad de tiempo
poisson <- function(n,lambda=1) {
  #
  # Generador de v.a. distribuida Poisson(lambda)
  # Args:
  #   n : Numero de muestras a generar
  #   lambda: Parametro lambda de la distribucion
  
  muestra <- c()
  
  for(i in 1:n) {
    s <- 0 # Tiempo transcurrido
    a <- -1 # Numero de eventos ocurridos
    while(s <= 1) {
      
      s = s + (-1/lambda)* log(runif(1))
      a = a + 1
    }
    muestra[[i]] <- a
  }
  
  return (muestra)
}

n <- 10000
lambda <- 5

muestra <- generador(n,lambda)
hist(muestra, prob=T)
x <- seq(0, max(muestra),1)
points(x,dpois(x, lambda), col="red")



