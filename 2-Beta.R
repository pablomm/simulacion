
# Semana 1 - Ejercicio 2. Generacion Distribucion beta.

# Apartado 1 - Dibujar distribucion y densidad de beta(2,4)

# Funcion de densidad de la Beta(2,4) 
f <- Vectorize(function(x) { if (x > 0 && x <  1) (20 * x*(1 - x)**3) else 0})

# Funcion de distribucion
Fbeta24 <- Vectorize(function(x) { if (x < 0 ) 0 
                                 else if (x>1) 1 
                                 else (-4*x**5+15*x**4-20*x**3+10*x**2)
        })

xfit <- seq(0,1,length=200) # Grid para dibujar funciones
plot(xfit, f(xfit),type="l", lwd=2, main="Densidad Beta(2,4)")
# En rojo encima linea discontinua con la proporcionada por R
lines(xfit,dbeta(xfit,2,4), type="l", lty=2, col="red")

plot(xfit, Fbeta24(xfit),type="l", lwd=2, main="Distribucion Beta(2,4)")
# En verde encima linea discontinua con la proporcionada por R
lines(xfit,pbeta(xfit,2,4), type="l", lty=2, col="green")


# Apartado 2 - Algoritmo de Aceptacion/Rechazo

aceprech <- function(n, f, cte=1, rh=runif, dh=dunif) {
  #
  # Metodo de aceptacion/rechazo generico
  #   Args:
  #      n: Numero de muestras a generar
  #      f: Funcion de densidad de la variable a generar
  #      cte: Constante c, mayor que 1, para escalar h. Por defecto 1. La probabilidad 
  #          de aceptacion sera 1/cte.
  #      rh: Generador aleatorio de numeros de acuerdo a la distribucion h.
  #          Debe aceptar como unico parametro el numero de muestras a generar.
  #      dh: Funcion de densidad para aceptar/rechazar las muestras,
  #         debe cumplirse que f(x) <= c*h(x).
  #         Por defecto toma la densidad uniforme
  
  muestras = c()
  
  # Guardamos datos de aceptados y rechazados
  rechazados <<- 0
  aceptados <<- 0
  
  # Funcion de Aceptacion/Rechazo
  g <- function(x) { return (f(x) / (cte * dh(x))) }
  
  for (i in 1:n) {
    accept = F
    
    rechazados <<- rechazados - 1
    while(!accept) {
      
      # Muestra variable y
      y <- rh(1)
      
      # Tirada uniforme para aceptar/rechazar
      u <- runif(1)
      accept <- u <= g(y)
      
      rechazados <<- rechazados + 1
    
    }
    aceptados <<- aceptados + 1
    muestras[[i]] <- y
  }
  
  return (muestras)
}

cte <- 2.109375 + 0.00001 # Constante del metodo de aceptacion
# Maximo de la f calculada numericamente + un margen de error

# Funcion para generar muestras Beta(2,4)
generadorBeta24 <- function(n) {aceprech(n,cte=cte, f)}


# Apartado 3 - Probar y analizar algoritmo

n <- 1000 # Numero de muestras a generar


# Muestra de funcion beta generada mediante el metodo de aceptacion/rechazo generico
muestra <- generadorBeta24(n)

# El porcentaje de aceptados esperado sera de 1/cte
# En nuestro caso 0.474
print(paste("Porcentaje de aceptados: ", 1- rechazados/(aceptados+rechazados)))



# Apartado 4 - Validar algoritmo

# Dibujamos histograma de la muestra y la funcion de densidad sobrepuesta
hist(muestra, prob=T, main='Distribucion Beta(2,4)', ylim = c(0,2.5), xlim=c(0,1))
xfit <- seq(0, 1, length = 100) 
yfit <- dbeta(xfit, shape1=2, shape2=4)
lines(xfit, yfit, col = "blue", lwd = 2)

qqplot(muestra, qbeta(seq(0,1,length = n), shape1 = 2, shape2 = 4))


abline(0,1, col='red')

# Test de kolmogorov
print(ks.test(muestra, 'pbeta', shape1=2, shape2=4))

# Un valor del estadistico cercano a 0 nos da evidencias bastante razonables 
# de que esta generado por una beta (Hipotesis alternativa)

# Apartado 5 - Metodo de la inversa

# No podemos computar explicitamente la funcion inversa, pues no tiene expresion analitica
# Asi que calcularemos de manera numerica la funcion de distribucion inversa 
# resolviendo la solucion a y = F(x) en el intervalo (0,1)

Finversa = Vectorize(function (y) uniroot((function (x) Fbeta24(x) - y), lower = 0, upper = 1)$root)

plot(xfit, Finversa(seq(0,1,length=100)), lwd=2, type="l", main="Funcion Distribucion inversa")


generadorBeta24_inversa <- function(n) { Finversa(runif(n))}

# Puede tardar para valores de n grande
muestraInversa <- generadorBeta24_inversa(n)
hist(muestraInversa, prob=T, xlim=c(0,1), ylim=c(0,2.2))
lines(xfit, yfit, col = "blue", lwd = 2) # Funcion densidad

# Tambien podemos calcular la ecdf a partir de los datos de la muestra
ecdfmuestra <- ecdf(muestra)
# La inversa puede ser computado con los cuantiles de la ecdf
InversaEcdf <- Vectorize(function(x) { quantile(ecdfmuestra, x) })
generadorBeta24Ecdf <- function(n) { InversaEcdf(runif(n))}
muestraEcdf <- generadorBeta24Ecdf(n)
# Ploteamos la muestra generada a partir de la Ecdf
hist(muestraEcdf, prob=T, xlim=c(0,1), ylim=c(0,2.2))
lines(xfit, yfit, col = "blue", lwd = 2) # Funcion densidad

# Para la funcion inversa, tanto calculada a partir de la ecdf como resolviendo 
# numericamente y=F(x) podrian haberse calculado los valores en una malla en (0,1)
# y haberse interpolado con splines para que una vez construidas la evaluacion sea
# rapida, pero tampoco merece la pena complicarse tanto para el ejercicio


