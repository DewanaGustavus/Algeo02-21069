import numpy as np
import math

def QR(A, eigenvector):
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
                eigenvector = [tempval]
            else:
                starttempval = tempval
                for k in range(i):
                    tempval = (tempval - ((np.dot(eigenvector[k], starttempval)) * eigenvector[k]))

                for j in range(len(tempval)):
                    sum += math.pow(tempval[j], 2)
                sum = math.sqrt(sum)
                tempval = (tempval / sum)
                eigenvector = np.append(eigenvector, [tempval], axis=0)
                
        eigenvector = np.transpose(eigenvector)
        inverse = np.transpose(eigenvector)
        A = np.matmul(inverse, A)
        A = np.matmul(A, eigenvector)
        
        A = np.transpose(A)
        ctr+=1

    return A, eigenvector

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
maxEigen = maxVal(getEigenValue(eigenvectorR(C)))

# misalkan K sehingga K < M
K = len(C) - 1



# A = [[3, -4, -2], [-1, 4, 1], [2, -6, -1]]
# eigenvector = [[]]
# n, m = np.shape(A) 
# A = np.random.rand(n, 30)
# A, eigenvector = np.linalg.qr(A)

# print(eigenvector)
# print("")
