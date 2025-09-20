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

// Подынтегральная функция f(y, z, b)
// Определена кусочно:
//    если y < b, то f(y,z,b) = z
//    иначе f(y,z,b) = z^2
double f(double y, double z, double b) {
    if (y < b) return z;
    return z * z;
}

// Вычисление кратного интеграла методом Монте-Карло
// Область интегрирования задаётся через случайные переменные:
//   x ∈ [0; a]
//   y ∈ [−x; x]
//   z ∈ [0; y^2]
// Подынтегральное выражение: cos(x) * f(y, z, b)
// Нормировка производится произведением длин интервалов:
//   (a) по x,
//   (2x) по y,
//   (y^2) по z
double multiple_integral_value(double a, double b) {
    auto rand_value = [=]() -> double {
        // Случайное значение x в [0; a]
        double x = a * uniform();

        // Случайное значение y в [−x; x]
        double y = -x + 2 * x * uniform();

        // Случайное значение z в [0; y^2]
        double z = y * y * uniform();

        // Подынтегральное выражение
        double val = cos(x) * f(y, z, b);

        // Нормировка по объёму области интегрирования
        return val * (a * 2 * x * (y * y));
    };

    // вычисляем матожидание с заданной точностью
    return expected_value(rand_value, 0.001);
}
}

int main() {
    double a = 5.0;  // параметр a
    double b = 2.0;  // параметр b

    std::cout << "Integral value (a = " << a
              << ", b = " << b << "): "
              << stat_mod_1::multiple_integral_value(a, b)
              << std::endl;

    return 0;
}
