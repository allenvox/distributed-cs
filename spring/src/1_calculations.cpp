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

void theta_1() {
    int N = 65536, m = 1;
    double lambda = 1e-5;
    vector<int> muValues = {1, 10, 100, 1000};
    vector<int> nValues = {65526, 65527, 65528, 65529, 65530, 65531, 65532, 65533, 65534, 65535, 65536};
    ofstream thetaFile("./data/1_1.txt");
    for (int mu : muValues) {
        for (int n : nValues) {
            double theta = calculateTheta(N, lambda, m, mu, n);
            thetaFile << n << " " << mu << " " << theta << endl;
        }
    }
    thetaFile.close();
}

void theta_2() {
    int N = 65536, m = 1, mu = 1;
    vector<double> lambdas = {1e-5, 1e-6, 1e-7, 1e-8, 1e-9};
    vector<int> nValues = {65526, 65527, 65528, 65529, 65530, 65531, 65532, 65533, 65534, 65535, 65536};
    ofstream thetaFile("./data/1_2.txt");
    for(double lambda : lambdas) {
        for (int n : nValues) {
            double theta = calculateTheta(N, lambda, m, mu, n);
            thetaFile << n << " " << lambda << " " << theta << endl;
        }
    }
    thetaFile.close();
}

void theta_3() {
    int N = 65536, mu = 1;
    double lambda = 1e-5;
    vector<int> ms = {1, 2, 3, 4};
    vector<int> nValues = {65526, 65527, 65528, 65529, 65530, 65531, 65532, 65533, 65534, 65535, 65536};
    ofstream thetaFile("./data/1_3.txt");
    for(int m : ms) {
        for (int n : nValues) {
            double theta = calculateTheta(N, lambda, m, mu, n);
            thetaFile << n << " " << m << " " << theta << endl;
        }
    }
    thetaFile.close();
}

void t_4() {
    int N = 1000, m = 1;
    double lambda = 1e-3;
    vector<int> muValues = {1, 2, 4, 6};
    vector<int> nValues = {900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000};
    ofstream tFile("./data/1_4.txt");
    for (int mu : muValues) {
        for (int n : nValues) {
            double t = calculateT(N, lambda, m, mu, n);
            tFile << n << " " << mu << " " << t << endl;
        }
    }
    tFile.close();
}

void t_5() {
    int N = 8192, m = 1, mu = 1;
    vector<double> lambdas = {1e-5, 1e-6, 1e-7, 1e-8, 1e-9};
    vector<int> nValues = {8092, 8102, 8112, 8122, 8132, 8142, 8152, 8162, 8172, 8182, 8192};
    ofstream tFile("./data/1_5.txt");
    for (double lambda : lambdas) {
        for (int n : nValues) {
            double t = calculateT(N, lambda, m, mu, n);
            tFile << n << " " << lambda << " " << t << endl;
        }
    }
    tFile.close();
}

void t_6() {
    int N = 8192, mu = 1;
    double lambda = 1e-5;
    vector<int> ms = {1, 2, 3, 4};
    vector<int> nValues = {8092, 8102, 8112, 8122, 8132, 8142, 8152, 8162, 8172, 8182, 8192};
    ofstream tFile("./data/1_6.txt");
    for (int m : ms) {
        for (int n : nValues) {
            double t = calculateT(N, lambda, m, mu, n);
            tFile << n << " " << m << " " << t << endl;
        }
    }
    tFile.close();
}

int main() {
    theta_1();
    theta_2();
    theta_3();
    t_4();
    t_5();
    t_6();
    cout << "all done\n";
    return 0;
}
