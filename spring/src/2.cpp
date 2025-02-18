#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>
#include <iomanip>
#include <stdexcept>

using namespace std;

// Оперативная надежность R*(t)
double calculateRStar(double lambda, int n, double t) {
    if (lambda <= 0 || n <= 0 || t < 0) 
        throw invalid_argument("Incorrect parameters for R*(t)");
    return exp(-lambda * n * t);
}

// Оперативная восстановимость U*(t)
double calculateUStar(double mu, int m, double t) {
    if (mu <= 0 || m <= 0 || t < 0) 
        throw invalid_argument("Incorrect parameters for U*(t)");
    return 1 - exp(-mu * m * t);
}

// Коэффициент готовности S
double calculateS(double lambda, double mu, int n, int m) {
    if (lambda <= 0 || mu <= 0 || n <= 0 || m <= 0) 
        throw invalid_argument("Incorrect parameters for S");
    return (mu * m) / (lambda * n + mu * m);
}

int main(int argc, char* argv[]) {
    int N = 10, m = 1, t_max = 24;
    double lambda = 0.024, mu = 0.71;

    ofstream Rfile("data/2_1.txt");
    Rfile << "t\tR*(t) n=8\tR*(t) n=9\tR*(t) n=10\n";
    for (int t = 0; t <= 24; t += 2) {
        Rfile << t << "\t"
              << calculateRStar(lambda, 8, t) << "\t"
              << calculateRStar(lambda, 9, t) << "\t"
              << calculateRStar(lambda, 10, t) << "\n";
    }
    Rfile.close();

    ofstream Ufile("data/2_2.txt");
    Ufile << "t\t";
    for (int n = 10; n <= 16; ++n) Ufile << "U*(t) n=" << n << "\t";
    Ufile << "\n";
    for (int t = 0; t <= 24; t += 2) {
        Ufile << t;
        for (int n = 10; n <= 16; ++n) {
            Ufile << "\t" << calculateUStar(mu, m, t);
        }
        Ufile << "\n";
    }
    Ufile.close();

    ofstream Sfile("data/2_3.txt");
    Sfile << "n\tS\n";
    for (int n = 11; n <= 16; ++n) {
        Sfile << n << "\t" << fixed << setprecision(3) 
              << calculateS(lambda, mu, n, m) << "\n";
    }
    Sfile.close();

    ofstream Rscript("plots/2_1.gnu");
    Rscript << "set terminal pngcairo enhanced font 'Arial,12'\n"
            << "set output 'img/2_1.png'\n"
            << "set title 'Зависимость R*(t) для различных n'\n"
            << "set xlabel 'Время t (часы)'\n"
            << "set ylabel 'R*(t)'\n"
            << "set grid\n"
            << "plot 'data/2_1.txt' using 1:2 with linespoints title 'n=8', \\\n"
            << "     '' using 1:3 with linespoints title 'n=9', \\\n"
            << "     '' using 1:4 with linespoints title 'n=10'\n";
    Rscript.close();

    ofstream Uscript("plots/2_2.gnu");
    Uscript << "set terminal pngcairo enhanced font 'Arial,12'\n"
            << "set output 'img/2_2.png'\n"
            << "set title 'Зависимость U*(t) для различных n'\n"
            << "set xlabel 'Время t (часы)'\n"
            << "set ylabel 'U*(t)'\n"
            << "set grid\n"
            << "plot for [col=2:8] 'data/2_2.txt' using 1:col with lines title columnheader\n";
    Uscript.close();

    cout << "Время тряски посчитано. Next execute 2_plots.sh\n";
    return 0;
}
