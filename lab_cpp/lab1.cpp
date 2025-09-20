#include <cmath>
#include <random>
#include <iostream>
#include <functional>

namespace stat_mod_1 {

// Минимальное число итераций при вычислении мат. ожидания
const int MIN_ITER_COUNT = 10000;

// Генератор случайных чисел (Mersenne Twister)
// и равномерное распределение на отрезке [0; 1)
std::random_device rd;
std::mt19937 gen(rd());
std::uniform_real_distribution<> urd(0, 1);

// Функция, возвращающая равномерно распределённое случайное число [0; 1)
double uniform() {
    return urd(gen);
}

// Генерация случайной величины X
// Закон распределения: 
//   P(X = 0) = 1/8
//   P(X = 1) = 7/8 * 1/8
//   P(X = 2) = (7/8)^2 * 1/8

// То есть это геометрическое распределение с p = 1/8
int random_value() {
    double a = uniform();  // берём число от 0 до 1
    double p = 1.0 / 8.0;  // начальная вероятность P(0)
    int n = 0;             // значение случайной величины
    while (a > p) {
        a -= p;            // вычитаем вероятность
        n++;               // переходим к следующему значению
        p *= 7.0 / 8.0;    // P(n+1) = P(n) * (7/8)
    }
    return n;
}

// Метод Монте-Карло для вычисления матожидания
// rand_distr - генератор значений случайной величины
// precision - требуемая точность результата
// min_iter_count - минимальное количество итераций
double expected_value(std::function<double()> rand_distr,
                      double precision,
                      int min_iter_count = MIN_ITER_COUNT) {
    double sum = 0;          // накопленная сумма значений
    double square_sum = 0;   // накопленная сумма квадратов
    int n = 0;               // количество сгенерированных значений
    bool is_precision_obtained = false;

    while (!is_precision_obtained) {
        double r = rand_distr();
        sum += r;
        square_sum += r * r;
        n++;

        // пока не достигли минимального числа итераций, не проверяем точность
        if (n < min_iter_count) continue;

        // Оценка дисперсии выборки
        double dispersion = (1.0 / (n - 1)) * square_sum
                          - (1.0 / (n * (n - 1))) * sum * sum;

        // Оценка требуемого числа итераций для достижения precision
        double estimated_iter_count = 9 * dispersion / (precision * precision);

        // Проверяем, достаточно ли выборки
        is_precision_obtained = (n > estimated_iter_count);
    }

    // Возвращаем среднее
    return sum / n;
}

// Функции для расчётов S1 и S2
// S1 = M[X], где X — случайная величина (целое число)
double calculated_value_1() {
    auto rv = []() -> double {
        int n = random_value();
        return static_cast<double>(n);  // просто значение X
    };
    return expected_value(rv, 0.1);
}
// S2 = M[2 * sqrt(X)], где X — случайная величина
double calculated_value_2() {
    auto rv = []() -> double {
        int n = random_value();
        return 2.0 * sqrt(static_cast<double>(n));
    };
    return expected_value(rv, 0.01);
}

}

int main() {
    // Случайное значение X
    std::cout << "Random value: " << stat_mod_1::random_value() << std::endl;

    // Вычисляем S1 и S2 с заданной точностью
    std::cout << "S1 = " << stat_mod_1::calculated_value_1() << std::endl;
    std::cout << "S2 = " << stat_mod_1::calculated_value_2() << std::endl;

    return 0;
}
