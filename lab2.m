%задание 1
matrix_A = [1 2 1; 4 -3 4; 2 7 -1];
matrix_B = [4; 5; 8];

A1 = matrix_A; A1(:,1) = matrix_B;
A2 = matrix_A; A2(:,2) = matrix_B;
A3 = matrix_A; A3(:,3) = matrix_B;

d(1) = det(A1);
d(2) = det(A2);
d(3) = det(A3)

matrix_A = [2 -3 1; 3 2 -3; 4 1 -3];
matrix_B = [2; -3; -4];

A1 = matrix_A; A1(:,1) = matrix_B;
A2 = matrix_A; A2(:,2) = matrix_B;
A3 = matrix_A; A3(:,3) = matrix_B;

d(1) = det(A1);
d(2) = det(A2);
d(3) = det(A3)

%задание 2
matrix_A = [4 1 -1; 1 -3 2; 6 -5 3];
matrix_B = [6; 1; 8];
C = rref([matrix_A matrix_B]);
N = size(C);
X = C(:, N(2));
matrix_A*X-matrix_B

matrix_A = [5 8 -3; 1 3 1; 4 5 -4];
matrix_B = [8; 5; 3];
C = rref([matrix_A matrix_B]);
N = size(C);
X = C(:, N(2));
matrix_A*X-matrix_B

%задание 3
matrix_A = [1 1 1 1; 2 -2 3 -3; 9 9 4 4; 3 -3 2 -2];
matrix_B = [2; 3; 9; 4];
X = matrix_A^(-1)*matrix_B;
matrix_A*X

matrix_A = [1 1 1 1; 1 -1 4 -4; 16 16 1 1; 16 -16 4 -4];
matrix_B = [1; -4; -6; 7];
X = matrix_A^(-1)*matrix_B;
matrix_A*X
