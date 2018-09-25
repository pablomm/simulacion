file = "pi.txt";
#http://www.geom.uiuc.edu/~huberty/math5337/groupe/digits.html
l=10000
#file.info(file)$size
s = readChar(file,l);
ocurrencias = c()
for(i in 0:9){
  ocurrencias[[i+1]]=lengths(regmatches(s, gregexpr(as.character(i), s)));
}
plot(0:9,ocurrencias,ylim = c(0,max(ocurrencias)))
ji2 = 0
e = l/10
for(i in 1:10){
  ji2 = ji2 + (e - ocurrencias[i])^2/e
}
print(1-pchisq(ji2,9))
l = 20000
s = readChar(file,l);
pairs = as.numeric(substring(s, first = 1:(nchar(s) - 1), last = 2:nchar(s)))[seq(1,nchar(s)-1,2)]
ocurrencias2 = c()
for(i in 0:99){
  ocurrencias2[[i+1]]=sum(pairs == i)
}
Mocurrencias2 = matrix(ocurrencias2,10,10)

ji2 = 0
e = l/100
for(i in 1:100){
  ji2 = ji2 + (e - ocurrencias2[i])^2/e
}
plot(0:99,ocurrencias2,ylim=c(0,max(ocurrencias2)))
print(1-pchisq(ji2,99))