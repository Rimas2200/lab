% Задание 1
fplot(@(x) (x^2 - x - 6) / abs(x - 3), [-5, 5]);
fplot(@(x) (abs(cos(x))*tan(x)), [-5, 5]);

%Задаание 2
t = linspace(0, 2*pi, 100);
x = 3 * cos(t);
y = 3 * sin(t);
plot(x, y);

%Задание 3
theta = linspace(0, 2*pi, 100);
r = 2 * sin(3 * theta);
polar(theta, r);

%Задание 4
t = linspace(0, 2*pi, 100);
s = linspace(0, 3, 50);

%функция для создания сетки координат
%создает две матрицы: одну для значений t и другую для значений s
[T, S] = meshgrid(t, s);

x = 3 * S .* cos(T); %точка перед умножением нужна для поэлементного умножения
y = 3 * S .* sin(T);
z = S;

plot3(x, y, z);
