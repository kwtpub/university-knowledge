#include <iostream>
#include <cmath>
using namespace std;

int main() {
    int x;
    double eps;
    cout << "Введите x: ";
    cin >> x;
    cout << "Введите eps: ";
    cin >> eps;

    int N = 1;
    double sum = 1; // Первый член ряда (n=0)
    double exept = (exp(x) + exp(-x)) / 2;
    double diff = fabs(sum - exept);

    while (diff > eps) {
        // Числитель: x^{2N}
        double argx = pow(x, 2 * N);

        // Знаменатель: (2N)!
        double factorial = 1;
        for (int j = 1; j <= 2 * N; ++j) {
            factorial *= j;
        }

        // Слагаемое ряда
        double slog = argx / factorial;

        // Увеличиваем сумму
        sum += slog;

        // Пересчитываем разницу с эталонным значением
        diff = fabs(sum - exept);

        // Переходим к следующему члену ряда
        N++;
    }

    cout << "SUM = " << sum << "\nCOUNT = " << N << "\nDIFF = " << diff << endl;
    return 0;
}
