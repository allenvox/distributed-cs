set terminal pngcairo enhanced size 1280,800
set output "img/1_5.png"
set title "Среднее время восстановления T(n)"
set xlabel "Количество машин (n)"
set ylabel "T, часов"
set grid

set logscale y 10
set format y "%.5f"
set ytics 0.1
set yrange [0.000001:0.15]
set xtics 10

plot "data/1_5.txt" using 1:($2 == 1e-05 ? $3 : NaN) with linespoints title "λ=1e-5", \
     "" using 1:($2 == 1e-06 ? $3 : NaN) with linespoints title "λ=1e-6", \
     "" using 1:($2 == 1e-07 ? $3 : NaN) with linespoints title "λ=1e-7", \
     "" using 1:($2 == 1e-08 ? $3 : NaN) with linespoints title "λ=1e-8", \
     "" using 1:($2 == 1e-09 ? $3 : NaN) with linespoints title "λ=1e-9"
