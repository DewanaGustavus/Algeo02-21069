import numpy as np
import math

def vectorsatuan(vector):
    sum = 0
    for val in vector:
        sum += math.pow(val, 2)
    sum = math.sqrt(sum)
    vectorsatuan = (vector/sum)
    return vectorsatuan

def euclid_distance(A, B):
    dist = 0
    for i in range(len(A)):
        dist += math.pow(A[i] - B[i], 2)
    return dist

def length(A):
    sum = 0

    for i in A:
        sum += math.pow(i, 2)

    return sum

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
                eigenvector = [tempval]
            else:
                starttempval = tempval
                for k in range(i):
                    tempval = (tempval - (((np.dot(eigenvector[k], starttempval)) / length(eigenvector[k])) * eigenvector[k]))

                for j in range(len(tempval)):
                    sum += math.pow(tempval[j], 2)
                sum = math.sqrt(sum)
                tempval = (tempval / sum)
                eigenvector = np.append(eigenvector, [tempval], axis=0)
                
        eigenvector = np.transpose(eigenvector)
        inverse = np.transpose(eigenvector)

        if ctr == 1:
            temp = np.transpose(eigenvector)
        else:
            temp = np.matmul(temp, np.transpose(eigenvector))
        A = np.matmul(inverse, A)
        A = np.matmul(A, eigenvector)
        
        A = np.transpose(A)
        ctr+=1

    return A, temp

def getEigenValue(A):
    eigenvalue = [A[0][0]]
    for i in range(1,len(A)):
        eigenvalue = np.append(eigenvalue, [A[i][i]], axis = 0)
    return eigenvalue

def getW(A, B, K):
    temp = np.dot(vectorsatuan(A), B)
    w = np.array([temp for i in range(K)])
    return w

def training(daftarface):
    # mengubah matrix jadi M x N^2 , harus di loop untuk setiap gambar
    Xm = np.array([np.array(x).flatten() for x in daftarface])
    
    # matrix berupa m x N^2 karena menggunakan append
    # ubah ke N^2 x M
    Xm = np.transpose(Xm)
    # membentuk mean    
    psi = np.array([sum(x)/len(x) for x in Xm])

    # kurangi semua matriks X menjadi a
    # transpose sementara matrixnya agar dapat dikurangi dengan mean
    Xm = np.transpose(Xm)
    Xm = np.array([np.subtract(x, psi) for x in Xm])
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
    Omega = np.array([getW(eigenvector[i], A_normal[i], K) for i in range(len(C_aksen))]) # eigenfaces baru
    # Omega telah terbentuk

    return C_aksen, psi, Omega

def indeks_gambar_terdekat(imagematrix, K, psi, C_aksen, Omega):
    matrix = np.array(imagematrix).flatten()
    matrix = np.subtract(matrix, psi)

    # dotkan uj dengan ai
    w_new = getW(matrix, matrix, K)

    # looping setiap Omega dataset dan cari yang paling minim selisihnya
    dist = [euclid_distance(w_new, Omega[i]) for i in range(len(C_aksen))]
    minimum = min(dist)
    minidx = dist.index(minimum)
    return minidx