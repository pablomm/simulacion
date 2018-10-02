
# Semana 3 - Simulacion de montecarlo

montecarlo <- function(f, n=10000,xlim=c(0,1), ylim=c(0,1), plt=F) {
  # Integra la funcion f en el intervalo xlim usando el metodo de 
  # montecarlo, calculando la proporcion de puntos generados debajo
  # de la curva.
  #
  # f: Funcion a integrar
  # n: Numero de pares uniformes a generar
  # xlim: Intervalo donde integrar la funcion
  # ylim: Rango de funciones a integrar, para ser optimo deberia ser
  #       (min(f), max(f)) en el intervalo de integracion.
  # Devuelve un vector con:
  #    - La integral aproximada como la razon de puntos debajo de la curva
  #    - Puntos x generados
  #    - Puntos y generados
  #    - Array con indices de los puntos aceptados
  
  x = runif(n, xlim[1], xlim[2])
  y = runif(n, ylim[1], ylim[2])

  # Calculamos los puntos donde 
  values <- sapply(x,f)
  z <- ((values >= y))
  integral <- length(z[z == TRUE])/n
  
  if(plt) {
    colores <- rep("gainsboro", n)
    colores[z == T] = "black"
    
    plot(x,y,col=colores, main=paste("Integral:", integral))
    xfit = seq(xlim[1], xlim[2],0.01)
    lines(xfit, sapply(xfit, f))
  }
  
  return (integral)
  
}

# Segundo metodo de integracion

integra <- function(g, n=1000, xlim=c(0,1), rf=runif, df=dunif) {
  # Calcula la integral de g como E[g(X)/f(X)]
  # teniendo X la funcion de densidad f
  # Args:
  #      g:  Funcion a integrar
  #      n:  Numero de muestras aleatorias a generar
  #      xlim: Intervalo de integracion
  #      rf: Funcion para generar muestras de X
  #      pf: Funcion de densidad de X
  
  muestras <- rf(n)
  h <- function(x) g(x)/df(x)
  
  values <- sapply(muestras, h)
  
  return (mean(values))
}

n <- 100
par(mfrow=c(1,1))
# Integral de sin(x)
res <- montecarlo(sin,n,xlim=c(0,pi),plt=T)  

# Integral de x^2
f <- function(x) x**2 
print(montecarlo(f,n,plt=T)) # Metodo 1
print(integra(f,n)) # Metodo 2


# Comparamos la variabilidad de cada uno de los 2 metodos
k <- 100 # Numero de simulaciones de la integral

metodo1 <- replicate(k, montecarlo(f,n))
metodo2 <- replicate(k, integra(f,n))

par(mfrow=c(1,2))
hist(metodo1, prob=T)
hist(metodo2, prob=T)

