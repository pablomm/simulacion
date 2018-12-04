

for i in $(ls | grep -i 'diferencias' ); do
 echo item: $i;
 python $i &
done
