set terminal pngcairo enhanced size 1280,800
set output "img/1_1.png"
set title "Среднее время наработки до отказа Θ(n)"
set xlabel "Количество машин (n)"
set ylabel "Θ, часов"
set grid

set logscale y 2
set format y "%.0f"
set ytics 4
set yrange [1:280000]
set xtics 1

plot "data/1_1.txt" using 1:($2 == 1 ? $3 : NaN) with linespoints title "μ=1", \
     "" using 1:($2 == 10 ? $3 : NaN) with linespoints title "μ=10", \
     "" using 1:($2 == 100 ? $3 : NaN) with linespoints title "μ=100", \
     "" using 1:($2 == 1000 ? $3 : NaN) with linespoints title "μ=1000"