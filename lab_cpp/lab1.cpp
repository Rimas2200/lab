#include <cmath>
#include <random>
#include <iostream>
#include <functional>

namespace stat_mod_1 {

const int MIN_ITER_COUNT = 10000;

std::random_device rd;
std::mt19937 gen(rd());
std::uniform_real_distribution<> urd(0, 1);

double uniform() {
    return urd(gen);
}

// св
int random_value() {
    double a = uniform();
    double p = 1.0 / 8.0;       // P(0)
    int n = 0;
    while (a > p) {
        a -= p;
        n++;
        p *= 7.0 / 8.0; // рекуррентно: P(n+1) = P(n) * 7/8
    }
    return n;
}

// функция вычисления ожидания
double expected_value(std::function<double()> rand_distr, double precision, int min_iter_count = MIN_ITER_COUNT) {
    double sum = 0;
    double square_sum = 0;
    int n = 0;
    bool is_precision_obtained = false;
    while (!is_precision_obtained) {
        double r = rand_distr();
        sum += r;
        square_sum += r * r;
        n++;

        if (n < min_iter_count) continue;

        double dispersion = (1.0 / (n - 1)) * square_sum - (1.0 / (n * (n - 1))) * sum * sum;
        double estimated_iter_count = 9 * dispersion / (precision * precision);

        is_precision_obtained = (n > estimated_iter_count);
    }
    return sum / n;
}

// S1 и S2
double calculated_value_1() {
    auto rv = []() -> double {
        int n = random_value();
        return (double)n;
    };
    return expected_value(rv, 0.1);
}

double calculated_value_2() {
    auto rv = []() -> double {
        int n = random_value();
        return 2.0 * sqrt((double)n);
    };
    return expected_value(rv, 0.01);
}

} // namespace stat_mod_1

int main() {
    std::cout << "Random value: " << stat_mod_1::random_value() << std::endl;
    std::cout << "S1 = " << stat_mod_1::calculated_value_1() << std::endl;
    std::cout << "S2 = " << stat_mod_1::calculated_value_2() << std::endl;
    return 0;
}
