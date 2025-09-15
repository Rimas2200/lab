%Karpenko.D Usov.D
matrix = [2 -1 0 1; 3 -2 1 4;1 0 0 2; -2
5 2 1];
det_matrix = det(matrix)

matrix = [1 -3 2 0; 0 -2 4 -1; 1 0 0 2; -
4 5 2 1];
det_matrix = det(matrix)

 matrix = [0 -1 0 1; 4 -2 1 4; 3 0 0 2; -2
5 2 1];
det_matrix = det(matrix)

%nomer 2
matrix = [3 2 -1; 1 -3 2; 7 2 0];
inv_matrix = inv(matrix)

matrix = [1 1 -1; 8 3 -6; -4 -1 3];
inv(matrix)

matrix = [3 -1 2; 2 -1 -1; 4 -2 -2];
inv(matrix)

matrix = [3 4 2; 2 -1 -3; 1 5 1];
inv(matrix)

matrix = [3 4 2; 2 -1 -3; 1 5 1];
matrix_inv = inv(matrix)
matrix * matrix_inv

A = [1 2 10; 2 4 -1; 1 1 -3];
B = [-15; 12; 9];
A^(-1)*B

A = [1 2 1; 4 -3 4; 2 7 -1];
B = [4; 5; 8];
A^(-1)*B

A = [2 -3 1; 3 2 -3; 4 1 -3];
b = [2;-3;-4];
A^(-1)*b
c =  A^(-1)*b;
A * c
 
   