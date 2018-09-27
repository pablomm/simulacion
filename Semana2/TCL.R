
par(mfrow = c(3, 3))

# TCL
tcl <- function(tam, n, gen, mean, sd, name) {
  sn = c()
  x = matrix(gen(tam*n), tam, n)

  for(i in 1:tam){
    if (i %% 500 == 0) {
    d <- density(x[i,])
    if (i == 500) plot(d, main = paste("Densidades variables", name))
    else lines(d)
    }
  }

  sn = apply(x, 1, mean)
  
  # Estandarizamos la variable
  z = sqrt(n)*(sn - mean)/sd
  
  # Limite del grafico
  infimo <- min(z)-1
  maximo <- max(z)+1
  
  # Dibujamos histograma de la muestra
  hist(z, prob=T, breaks = 30, xlim = c(infimo,maximo), main=paste("Histograma del TCL with n=", n, "para suma de variables" , name))
  
  # Dibujamos la funci??n de densidad de erlang sobre el histograma
  xfit <- seq(infimo, maximo, length = 100)
  yfit <- dnorm(xfit, 0, 1)
  lines(xfit, yfit, col = "blue", lwd = 2)
  
  #TESTS
  # QQplot de la muestra normal propia
  qqnorm(z, main = paste("Q-Q plot para suma de variables", name))
  
  # Ajustamos una recta de regresion lineal
  # Al estar generados por la misma distribucion deberan tener una 
  # correlacion cercana a 1, por tanto el qqplot debera modelizarse
  # sobre la recta y=x
  abline(a=0, b=1, col='red')
  
  # Test de kolmogorov
  # Con la opcion two sided, para comprobar si la distribucion es igual
  # Un valor del estadistico cercano a 0 nos dara evidencias para afirmar
  # que nuestra muestra se distribuye de forma normal
  print(ks.test(z,'pnorm', 0, 1))
}

tam = 10000
n = 100

# Normal
mean = 0
sd = 1

tcl(tam, n, function(n){ rnorm(n, mean, sd) }, mean, sd, "Normal")

# Gamma
k = 1
lambda = 1/2
mean = k/lambda
sd = sqrt(k/lambda**2)

tcl(tam, n, function(n){ rgamma(n, shape=k, rate=lambda)}, mean, sd, "Gamma")

# Beta
a = 2
b = 2
mean = a/(a+b)
sd = sqrt((a*b)/((a+b)**2 * (a+b+1)))

tcl(tam, n, function(n){ rbeta(n, shape1=a, shape2=b)}, mean, sd, "Beta")
