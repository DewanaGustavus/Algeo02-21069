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

# mengubah matrix jadi M x N^2 , harus di loop untuk setiap gambar
first = True

for x in daftarface:
    x = np.array(x)
    x = x.flatten()
    if (first):
        first = False
        Xm = x
    else:
        Xm = np.append(Xm, x, axis = 0)

# matrix berupa m x N^2 karena menggunakan append
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
    Xm[i] = np.subtract(Xm[i], psi)
# Xm sudah menjadi am

A_normal = Xm
# matrix M x N^2
A_transpose = np.transpose(A_normal)

# cari matrix C'
C_aksen = np.multiply(A_transpose, A_normal)

# mencari eigenvector
# eigenface berupa tiap kolom pada eigenvector/tiap baris pada eigenvector yang di transpose
eigenvector = [[]]
C_aksen, eigenvector = QR(C_aksen, eigenvector)

# transposekan eigenvector agar eigenface bisa diambil per baris
eigenvector = np.transpose(eigenvector)

# misalkan K sehingga K < M
K = len(C_aksen) - 1
for i in range(len(C_aksen)):
    # looping sigma perkalian wj dengan uj
    sum = 0
    # looping sebanyak K
    for j in range(K):
        u = eigenvector[i]

        # looping untuk menghitung vektor satuan dari eigenvector
        sumtemp = 0
        for k in range(len(u)):
            sumtemp += math.pow(u[k], 2)
        sumtemp = math.sqrt(sumtemp)
        u = (u/sumtemp)

        # dotkan uj dengan ai
        temp = np.dot(u, A_normal[i]) # nilai wi

        if (j == 0):
            w = [temp]
        else:
            w = np.append(w, [temp])
    # memasukkan eigenfaces baru, misalkan Omega
    if (i == 0):
        Omega = [w]
    else:
        Omega = np.append(Omega, [w], axis=0)
# Omega telah terbentuk


# BAGIAN TESTING #

# input gambar tes
input = np.array(input)
input = input.flatten()
input = np.subtract(input, psi)

for j in range(K):
    u = input

    # looping untuk menghitung vektor satuan dari eigenvector
    sumtemp = 0
    for k in range(len(u)):
        sumtemp += math.pow(u[k], 2)
    sumtemp = math.sqrt(sumtemp)
    u = (u/sumtemp)

    # dotkan uj dengan ai
    temp = np.dot(u, input) # nilai wi

    if (j == 0):
        w_new = [temp]
    else:
        w_new = np.append(w_new, [temp])

# looping setiap Omega dataset dan cari yang paling minim selisihnya
for i in range(len(C_aksen)):
    sum = 0
    for j in range(K):
        sum += math.pow(w_new[j] - Omega[i][j], 2)

    if i == 0:
        min = sum
        idxmin = 0
    else:
        if min > sum:
            min = sum
            idxmin = i  # idxmin adalah index foto yang paling mendekati input