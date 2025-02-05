set terminal pngcairo enhanced size 1280,800
set output "img/1_6.png"
set title "Среднее время восстановления T(n)"
set xlabel "Количество машин (n)"
set ylabel "T, часов"
set grid

#set logscale y 2
set format y "%.2f"
set ytics 0.01
set yrange [0.001:0.1]
set xtics 10

plot "data/1_6.txt" using 1:($2 == 1 ? $3 : NaN) with linespoints title "m=1", \
     "" using 1:($2 == 2 ? $3 : NaN) with linespoints title "m=2", \
     "" using 1:($2 == 3 ? $3 : NaN) with linespoints title "m=3", \
     "" using 1:($2 == 4 ? $3 : NaN) with linespoints title "m=4"
