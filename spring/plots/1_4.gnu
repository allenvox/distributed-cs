set terminal pngcairo enhanced size 1280,800
set output "img/1_4.png"
set title "Среднее время восстановления T(n)"
set xlabel "Количество машин (n)"
set ylabel "T, часов"
set grid

set logscale y 2
set format y "%.2f"
set ytics 0.5
set xtics 10

plot "data/1_4.txt" using 1:($2 == 1 ? $3 : NaN) with linespoints title "μ=1", \
     "" using 1:($2 == 2 ? $3 : NaN) with linespoints title "μ=2", \
     "" using 1:($2 == 4 ? $3 : NaN) with linespoints title "μ=4", \
     "" using 1:($2 == 6 ? $3 : NaN) with linespoints title "μ=6"