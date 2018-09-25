
#NORMAL

tam = 10000
n = 100
mean = 0
sd = 1

newmean = n*mean
newsd = sd*sqrt(n)

z = c()
for (i in 1:tam){
  x = rnorm(n, mean=mean, sd=sd)
  y = sum(x)
  z = c(z,y)
}

# Limite del grafico
infimo <- min(z)-5
maximo <- max(z)+5

# Dibujamos histograma de la muestra
hist(z, prob=T, breaks = 30, xlim = c(infimo,maximo))

# Dibujamos la función de densidad de erlang sobre el histograma
xfit <- seq(infimo, maximo, length = 100)
yfit <- dnorm(xfit, mean=newmean, newsd)
lines(xfit, yfit, col = "blue", lwd = 2)

#TESTS
# QQplot de la muestra normal propia, primero estandarizamos la variable
est = (z-newmean)/newsd
qqnorm(est)

# Ajustamos una recta de regresion lineal
# Al estar generados por la misma distribucion deberan tener una 
# correlacion cercana a 1, por tanto el qqplot debera modelizarse
# sobre la recta y=x
abline(a=0, b=1, col='red')

# Test de kolmogorov
# Con la opcion two sided, para comprobar si la distribucion es igual
# Un valor del estadistico cercano a 0 nos dara evidencias para afirmar
# que nuestra muestra se distribuye de forma normal
print(ks.test(z,'pnorm', newmean, newsd))
