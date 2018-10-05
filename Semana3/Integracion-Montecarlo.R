
# Semana 3 - Simulacion de montecarlo
# Grupo 1 - Luis Jariego, Pablo Marcos, Roberto Alcover y Santiago Cerezo

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

metodo1 <- replicate(k, montecarlo(f,n)   )
metodo2 <- replicate(k, integra(f,n))
metodo <- replicate(100, runif)


par(mfrow=c(1,2))
print("Comparacion metodo montecarlo vs naive montecarlo, desviaciones:")
print(sd(metodo1))
print(sd(metodo2))
hist(metodo1, prob=T)
hist(metodo2, prob=T)

# Integramos el coseno pero calculando la esperanza de la uniforme y la beta
alfa <- 2
beta <- 2
rf <- function(n) { rbeta(n, shape1 = alfa, shape2 = beta)}
df <- function(x) { dbeta(x, shape1 = alfa, shape2 = beta)}

f <- function(x) { sin(x*pi)}


# Pintamos la funcion de densidad beta y la funcion a integrar
xfit = seq(0,1,0.01)

par(mfrow=c(1,1))
plot(xfit, sapply(xfit, f), type="l", lwd=2, ylim=c(0,2))
lines(xfit, sapply(xfit, df), lwd=2, col="red")
legend("topright", legend=c("sin(x*pi)", paste("beta(",alfa,",",beta,")")),
       col=c("black", "red"),lty=c(1,1))

par(mfrow=c(1,2))
metodo2_uniforme <- replicate(k, integra(f, n))
metodo2_beta <- replicate(k, integra(f, n, rf=rf,df=df))

print("Desviaciones estandar con uniforme vs beta")
sd1 <- sd(metodo2_uniforme)
sd2 <- sd(metodo2_beta)
hist(metodo2_uniforme, prob=T, main=paste("Unif sd=",sd1))
hist(metodo2_beta, prob=T, main=paste("Beta sd=",sd2))

# Veamos como afecta a la desviacion el numero de muestras
desviaciones_beta <- c()
desviaciones_unif <- c()
i <- 1
sims = c(100,500,1000, 5000, 10000)
for (n in sims){
  metodo2_beta <- replicate(k, integra(f, n, rf=rf,df=df))
  metodo2_uniforme <- replicate(k, integra(f, n))
  desviaciones_beta[[i]] <- sd(metodo2_beta)
  desviaciones_unif[[i]] <- sd(metodo2_uniforme)
  i <- i+1
}
par(mfrow=c(1,1))
xfit = seq(0, 1e4,length=100)
#plot(xfit, 1/sqrt(xfit), type="l", col="red", lwd=2, main="Comparacion convergencia")
plot(desviaciones_unif, desviaciones_beta, type="o", main="Comparacion convergencia", lwd=2)
plot(sims, desviaciones_beta/desviaciones_unif, type="o", main="Comparacion convergencia sd_beta/sd_unif", lwd=2)

