

set terminal pngcairo enhanced size 1280,800
set output "T_plot.png"

set title "Среднее время восстановления T(n)"
set xlabel "Количество машин (n)"
set ylabel "T, часов"
set grid

# Логарифмическая шкала по основанию 2
set logscale y 2

# Форматирование меток оси Y в степенях двойки
set format y "%.2f"
set ytics 0.5

plot "T_results.txt" using 1:($2 == 1 ? $3 : NaN) with linespoints title "μ=1", \
     "" using 1:($2 == 2 ? $3 : NaN) with linespoints title "μ=2", \
     "" using 1:($2 == 4 ? $3 : NaN) with linespoints title "μ=4", \
     "" using 1:($2 == 6 ? $3 : NaN) with linespoints title "μ=6"