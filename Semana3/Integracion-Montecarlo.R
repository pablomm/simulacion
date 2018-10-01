
# Semana 3 - Simulacion de montecarlo

montecarlo <- function(f, n=10000,xlim=c(0,1), ylim=c(0,1)) {
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
  
  return (list(integral=length(z[z == TRUE])/n,x=x,y=y,aceptados=z))
  
}

# Integramos la funcion x**2
n <- 10000

f <- function(x) x**2 # Integral de x^2
res <- montecarlo(f,n)

#f <- function(x) sin(x) # Integral de sin(x)
#res <- montecarlo(f,n,xlim=c(0,pi))

# Pintamos los puntos aceptados en verde, los rechazados en azul
colores <- rep("gainsboro", n)
colores[res$aceptados == T] = "black"

plot(res$x,res$y,col=colores, main=paste("Integral:", res$integral))

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

# Integramos por el segundo metodo x**2
n <- 100000
f <- function(x) x**2 # Integral de x**2
res <- integra(f,n)

print(res)




