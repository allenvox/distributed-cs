set terminal pngcairo enhanced size 1280,800
set output "img/1_3.png"
set title "Среднее время наработки до отказа Θ(n)"
set xlabel "Количество машин (n)"
set ylabel "Θ, часов"
set grid

set logscale y 10
set format y "10^{%L}"
set ytics 10
set xtics 1

plot "data/1_3.txt" using 1:($2 == 1 ? $3 : NaN) with linespoints title "m=1", \
     "" using 1:($2 == 2 ? $3 : NaN) with linespoints title "m=2", \
     "" using 1:($2 == 3 ? $3 : NaN) with linespoints title "m=3", \
     "" using 1:($2 == 4 ? $3 : NaN) with linespoints title "m=4"
