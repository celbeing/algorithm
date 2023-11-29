#슈트라센 알고리즘(행렬 곱)

#입력받은 두 행렬은 같은 크기의 2^n*2^n 정사각행렬로 변환한다.
#모자라는 원소는 모두 0으로 채운다.

#각 행렬을 같은 크기의 4개의 행렬로 나누어 연산을 실시한다.
#C11 = A11*B11 + A12*B21
#C12 = A11*B12 + A12*B22
#C21 = A21*B11 + A22*B21
#C22 = A21*B12 + A22*B22 (총 연산 곱셈 8회, 덧셈 4회)

#M1 = (A11 + A22)*(B11 + B22)
#M2 = (A21 + A22)*B11
#M3 = A11*(B12 - B22)
#M4 = A22*(B21 - B11)
#M5 = (A11 + A12)*B22
#M6 = (A21 - A11)*(B11 + B12)
#M7 = (A12 - A22)*(B21 + B22) (곱셈 7회, 덧셈 10회)
#C11 = M1 + M4 - M5 + M7
#C12 = M3 + M5
#C21 = M2 + M4
#C22 = M1 - M2 + M3 + M6 (총 연산 곱셈 7회, 덧셈 18회)

#행렬에서는 곱셈이 훨씬 더 많은 시간을 필요로 하기 때문에
#덧셈 횟수가 16회 늘어났다고 해도 곱셈 횟수를 1회 줄인 것이 효율적이다.
#하지만 n이 작은 경우에는 덧셈 횟수가 너무 많아지므로
#일반적인 행렬 곱셈이 더 빠르다.

import sys
input = sys.stdin.readline

#행렬의 크기를 2^n*2^n으로 확장
def set_matrix(A,B):
    n = 1
    k = max(len(A),len(A[0]),len(B),len(B[0]))
    while n < k:
        n*=2
    newA = [[0 for _ in range(n)] for __ in range(n)]
    newB = [[0 for _ in range(n)] for __ in range(n)]
    for i in range(len(A)):
        for j in range(len(A[0])):
            newA[i][j] = A[i][j]
    for i in range(len(B)):
        for j in range(len(B[0])):
            newB[i][j] = B[i][j]
    return newA,newB

#행렬의 합
def sum_matrix(A,B):
    n = len(A)
    C = [[0 for _ in range(n)] for __ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C

#행렬의 차
def sub_matrix(A,B):
    n = len(A)
    C = [[0 for _ in range(n)] for __ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
    return C

#행렬을 4개의 부분으로 나누기
def cut_matrix(M):
    n = len(M) // 2
    M11 = [[0 for _ in range(n)] for __ in range(n)]
    M12 = [[0 for _ in range(n)] for __ in range(n)]
    M21 = [[0 for _ in range(n)] for __ in range(n)]
    M22 = [[0 for _ in range(n)] for __ in range(n)]
    for i in range(n):
        for j in range(n):
            M11[i][j] = M[i][j]
            M12[i][j] = M[i][j+n]
            M21[i][j] = M[i+n][j]
            M22[i][j] = M[i+n][j+n]
    return M11,M12,M21,M22

#4개의 부분 행렬을 하나로 합치기
def glue_matrix(C11,C12,C21,C22):
    n = len(C11)
    M = [[0 for _ in range(n*2)] for __ in range(n*2)]
    for i in range(n):
        for j in range(n):
            M[i][j] = C11[i][j]
            M[i][j+n] = C12[i][j]
            M[i+n][j] = C21[i][j]
            M[i+n][j+n] = C22[i][j]
    return M

#행렬의 곱
def mul_matrix(A,B):
    n = len(A)
    if n == 1:
        C = [[0]]
        C[0][0] = A[0][0]*B[0][0]
        return C
    else:
        A11,A12,A21,A22 = cut_matrix(A)
        B11,B12,B21,B22 = cut_matrix(B)
        M1 = mul_matrix(sum_matrix(A11,A22),sum_matrix(B11,B22))
        M2 = mul_matrix(sum_matrix(A21,A22),B11)
        M3 = mul_matrix(A11,sub_matrix(B12,B22))
        M4 = mul_matrix(A22,sub_matrix(B21,B11))
        M5 = mul_matrix(sum_matrix(A11,A12),B22)
        M6 = mul_matrix(sub_matrix(A21,A11),sum_matrix(B11,B12))
        M7 = mul_matrix(sub_matrix(A12,A22),sum_matrix(B21,B22))

        C11 = sum_matrix(sub_matrix(sum_matrix(M1,M4),M5),M7)
        C12 = sum_matrix(M3,M5)
        C21 = sum_matrix(M2,M4)
        C22 = sum_matrix(sum_matrix(sub_matrix(M1,M2),M3),M6)
        return glue_matrix(C11,C12,C21,C22)

#원래 크기로 되돌리기
def trim_matrix(A,row,col):
    M = [[0 for _ in range(col)] for __ in range(row)]
    for i in range(row):
        for j in range(col):
            M[i][j] = A[i][j]
    return M

rowA,colA,rowB,colB = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(rowA)]
B = [list(map(int,input().split())) for _ in range(rowB)]
newA,newB = set_matrix(A,B)
print(trim_matrix(mul_matrix(newA,newB),rowA,colB))