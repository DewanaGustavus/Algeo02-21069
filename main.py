import numpy as np
import math

def QR(A):
    ctr = 1
    while ctr != 10000:
        A = np.transpose(A)
        # looping menghitung matrix
        for i in range(len(A)):
            tempval = A[i]
            sum = 0
            if i == 0:
                for j in range(len(tempval)):
                    sum += math.pow(tempval[j], 2)
                sum = math.sqrt(sum)
                tempval = (tempval / sum)
                Q = [tempval]
            else:
                starttempval = tempval
                for k in range(i):
                    tempval = (tempval - ((np.dot(Q[k], starttempval)) * Q[k]))

                for j in range(len(tempval)):
                    sum += math.pow(tempval[j], 2)
                sum = math.sqrt(sum)
                tempval = (tempval / sum)
                Q = np.append(Q, [tempval], axis=0)
                
        Q = np.transpose(Q)
        inverse = np.transpose(Q)
        A = np.matmul(inverse, A)
        A = np.matmul(A, Q)
        A = np.transpose(A)
        ctr+=1
    
    return A

def getEigenValue(A):
    for i in range(len(A)):
        for j in range(len(A)):
            if i == j:
                if i == 0:
                    eigenvalue = [A[i][j]]
                else:
                    eigenvalue = np.append(eigenvalue, [A[i][j]], axis=0)
    return eigenvalue

def maxVal(A):
    temp = A[0]
    for i in range(len(A)):
        if temp < A[i]:
            temp = A[i]
    
    return temp

# mengubah matrix jadi N^2, harus di loop untuk setiap gambar
first = True

for x in daftarface:
    x = x.flatten()
    if (first):
        first = False
        Xm = x
    else:
        Xm = np.append(Xm, x, axis = 0)

# matrix m x N^2
# ubah ke N^2 x M
Xm = np.transpose(Xm)
# cari mean
first2 = True
for i in range(len(Xm)):
    sum = 0
    ctr = 0
    for j in range(len(Xm[0])):
        sum += Xm[i][j]
        ctr += 1
    sum = sum/ctr
    if (first2):
        psi = sum
        first2 = False
    else:
        psi = np.append(psi, sum)
# terbentuk mean

# kurangi semua matriks X menjadi a
# transpose sementara matrixnya agar dapat dikurangi dengan mean
Xm = np.transpose(Xm)
for i in range(len(Xm)):
    np.subtract(Xm[i], psi)
# Xm sudah menjadi am
# transpose kembali ke awal 
Xm = np.transpose(Xm)
# matrix M x N^2
Xmt = np.transpose(Xm)

# cari matrix C'
C = np.multiply(Xmt, Xm)

# mencari nilai eigen dari C
# ambil nilai eigen max dari segala kemungkinan
maxEigen = maxVal(getEigenValue(QR(C)))

# misalkan K sehingga K < M
K = len(C) - 1




a = np.append(a, [1,2,3,4])
a = a.flatten()
for i in range(len(a)):
    print(a[i])

# append matrixnya sementara
# transpose matrixnya biar jadi N^2 x M

p2 = np.roots([1, -23, 185, -625, 894, -432])
print ("Roots of P2 : ", p2)
p = np.array([x, 0, 0], [0, x, 0], [0, 0, x])
print(p)
p1 = np.poly1d([1, -1])
p2 = np.poly1d([1, -17])
print(np.roots(np.polymul(p1, p2)))

# pakai metode QR yang diimplementasikan sendiri
# untuk mempermudah perhitungan, maka kita transposekan matrixnya terlebih dahulu

