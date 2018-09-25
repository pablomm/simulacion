file = "pi.txt";
#http://www.geom.uiuc.edu/~huberty/math5337/groupe/digits.html
l=file.info(file)$size
s = readChar(file,l);
ocurrencias = c()
for(i in 0:9){
  ocurrencias[[i+1]]=lengths(regmatches(s, gregexpr(as.character(i), s)));
}
plot(0:9,ocurrencias,ylim = c(0,max(ocurrencias)))
ji2 = c()
for(i in 0:9){
  
}