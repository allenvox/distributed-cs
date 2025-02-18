set terminal pngcairo enhanced font 'Arial,12'
set output 'img/2_2.png'
set title 'Зависимость U*(t) для различных n'
set xlabel 'Время t (часы)'
set ylabel 'U*(t)'
set grid
plot for [col=2:8] 'data/2_2.txt' using 1:col with lines title columnheader
