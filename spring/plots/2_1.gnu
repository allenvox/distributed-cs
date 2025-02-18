set terminal pngcairo enhanced font 'Arial,12'
set output 'img/2_1.png'
set title 'Зависимость R*(t) для различных n'
set xlabel 'Время t (часы)'
set ylabel 'R*(t)'
set grid
plot 'data/2_1.txt' using 1:2 with linespoints title 'n=8', \
     '' using 1:3 with linespoints title 'n=9', \
     '' using 1:4 with linespoints title 'n=10'
