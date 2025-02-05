#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>

using namespace std;

double calculateTheta(int N, double lambda, int m, double mu, int n1) {
    double theta = 0.0;
    if (n1 != N) {
        for (int j = n1 + 1; j <= N; ++j) {
            double product = 1.0;
            for (int l = n1; l < j; ++l) {
                product *= mu / (l * lambda);
            }
            theta += (1.0 / (j * lambda)) * product;
        }
        theta += 1.0 / (n1 * lambda);
    } else {
        theta = 1.0 / (N * lambda);
    }
    return theta;
}

double calculateT(int N, double lambda, int m, double mu, int n1) {
    auto mu_l = [N, m, mu](int l) -> double {
        return (l >= N - m && l <= N) ? (N - l) * mu : m * mu;
    };

    if (n1 == 1) {
        return 1.0 / mu;
    }
    double product1 = 1.0;
    for (int l = 1; l <= n1 - 1; l++) {
        product1 *= (l * lambda) / mu_l(l);
    }
    product1 /= mu;
    double sum = 0.0;
    for (int j = 1; j < n1 - 1; j++) {
        double product2 = 1.0;
        for (int l = j; l <= n1 - 1; l++) {
            product2 *= (l * lambda) / mu_l(l);
        }
        sum += product2 / (j * lambda);
    }
    return product1 + sum;
}

void thetas() {
    int N = 65536, m = 1;
    double lambda = 1e-5;
    vector<int> muValues = {1, 10, 100, 1000};
    vector<int> nValues = {65527, 65528, 65529, 65530, 65531, 65532, 65533, 65534, 65535, 65536};
    ofstream thetaFile("theta_results.txt");
    if (!thetaFile.is_open()) {
        cerr << "failed opening file\n";
        return;
    }
    for (int mu : muValues) {
        for (int n : nValues) {
            double theta = calculateTheta(N, lambda, m, mu, n);
            thetaFile << n << " " << mu << " " << theta << endl;
        }
    }
    thetaFile.close();
    cout << "thetas generated\n";
}

void ts() {
    int N = 1000, m = 1;
    double lambda = 1e-3;
    vector<int> muValues = {1, 2, 4, 6};
    vector<int> nValues = {900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000};
    ofstream tFile("t_results.txt");
    if (!tFile.is_open()) {
        cerr << "failed opening file\n";
        return;
    }
    for (int mu : muValues) {
        for (int n : nValues) {
            double t = calculateT(N, lambda, m, mu, n);
            tFile << n << " " << mu << " " << t << endl;
        }
    }
    tFile.close();
    cout << "ts generated\n";
}

int main() {
    thetas();
    ts();
    cout << "done\n";
    return 0;
}
