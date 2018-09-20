
# Semana 1 - Ejercicio 1. Box-Muller

# Apartado 1 en papel

# Apartado 2 - Implementacion Box-Muller

boxmuller <- function(n, mu=0., sd=1., epsilon=1e-10) {
  #
  # Generador de muestras normales utilizando el metodo de Box-Muller
  # Args:
  #    n : Numero de muestras a generar
  #    mean: Media de la normal
  #    sd: Desviacion tipica
  
  # Generamos u1 en el intervalo (epsilon,1) en vez de (0,1)
  # para evitar un posible -inf (aunque improbable)
  u1 <- runif(n, epsilon,1)
  u2 <- runif(n)
  
  # Muestras normal(0,1)
  z <- sqrt(-2 * log(u1)) * cos(2 * pi * u2)
  # z <- sqrt(-2 * log(u1)) * sin(2 * pi * u2)
  
  # Desestandarizamos la normal
  normal <- sd*z + mu
  
 return (normal) 
}

# Apartado 3 - Validacion

# Generamos muestras de normales usando nuestro generador y dibujamos histograma
n <- 1e4 # Numero de muestras a generar
mu <- 0 # Media de la normal
sd <- 1 # Desviacion estandar

muestra <- boxmuller(n,mu,sd)

# Limite del grafico
limite <- max(-1*min(muestra), max(muestra))+1 - mu

# Dibujamos histograma de la muestra
hist(muestra, prob=T, breaks = 20, xlim = c(mu-limite,mu+ limite),
     ylim=c(0, 1./(sd*sqrt(2*pi))),
     main=paste('Distribucion Normal(',mu,', ',sd,')', sep=''))

# Dibujamos la función de densidad de erlang sobre el histograma
xfit <- seq(mu-limite, mu+limite, length = 100) 
yfit <- dnorm(xfit,mean=mu, sd=sd )
lines(xfit, yfit, col = "blue", lwd = 2)


# QQplot de la muestra normal propia
qqnorm(muestra)

# Ajustamos una recta de regresion lineal
# Al estar generados por la misma distribucion deberan tener una 
# correlacion cercana a 1, por tanto el qqplot debera modelizarse
# sobre la recta y=x
abline(a=0, b=1, col='red')

# Test de kolmogorov
# Con la opcion two sided, para comprobar si la distribucion es igual
# Un valor del estadistico cercano a 0 nos dara evidencias para afirmar
# que nuestra muestra se distribuye de forma normal
print(ks.test(muestra,'pnorm', mu, sd))

# Apartado 4 - Normal(10,2)

# Cambiar los parametros mu y sd del apartado anterior y reejecutar

