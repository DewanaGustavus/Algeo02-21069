import numpy as np
import math

def euclid_distance(A, B):
    dist = 0
    for i in range(len(A)):
        dist += math.pow(A[i] - B[i], 2)
    return dist

def QR(A):
    ctr = 1
    while ctr != 5:
        A = np.transpose(A)
        # looping menghitung matrix
        for i in range(len(A)):
            tempval = A[i]
            sum = 0
            if i == 0:
                for j in range(len(tempval)):
                    sum += math.pow(tempval[j], 2)
                sum = float(math.sqrt(sum))
                tempval1 = (tempval / sum)
                eigenvector = [tempval1]
            else:
                starttempval = tempval
                for k in range(i):
                    tempval = (tempval - ((np.dot(eigenvector[k], starttempval)) * eigenvector[k]))

                for j in range(len(tempval)):
                    sum += math.pow(tempval[j], 2)
                sum = float(math.sqrt(sum))
                tempval = (tempval / sum)
                eigenvector = np.append(eigenvector, [tempval], axis=0)

        A = np.transpose(A)        
        eigenvector = np.transpose(eigenvector)
        inverse = np.transpose(eigenvector)

        if ctr == 1:
            temp = np.transpose(eigenvector)
        else:
            temp = np.matmul(temp, np.transpose(eigenvector))
        A = np.matmul(inverse, A)
        A = np.matmul(A, eigenvector)
        
        ctr+=1

    return A, temp

def getEigenface(A, eigvec):
    eigvec = np.transpose(eigvec)
    temp = np.array([np.matmul(A, eigvec[i]) for i in range(len(eigvec))])
    eigenface = np.transpose(temp)
    return eigenface

def getOmega(A, B, K):
    for i in range(len(A)): # looping seluruh gambar
        temp = A[i]
        for k in range(K+1):
            tempw = np.dot(B[k], temp)
            if k == 0:
                l1 = [tempw]
            else:
                l1 = np.append(l1, [tempw], axis=0)
        if i == 0:
            Omega = [l1]
        else:
            Omega = np.append(Omega, [l1], axis=0)

    return Omega

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
    C_aksen = np.matmul(A_normal, A_transpose)
    
    # mencari eigenvector
    # eigenface berupa tiap kolom pada eigenvector/tiap baris pada eigenvector yang di transpose
    C_aksen, eigenvector = QR(C_aksen)
    # transposekan eigenvector agar eigenface bisa diambil per baris
    eigenface = getEigenface(A_transpose, eigenvector)

    # misalkan K sehingga K < M
    K = len(C_aksen) - 1
    
    eigenfaceT=np.transpose(eigenface)
    Omega = getOmega(A_normal, eigenfaceT, K)
    # Omega telah terbentuk

    hasiltraining = [K, C_aksen, psi, Omega, eigenface]
    return hasiltraining

def indeks_gambar_terdekat(imagematrix, datatraining):
    K, C_aksen, psi, Omega, eigenface = datatraining
    matrix = np.array(imagematrix).flatten()
    matrix = np.subtract(matrix, psi)
    
    # dotkan uj dengan ai
    eigenface = np.transpose(eigenface)
    
    for k in range(K+1):
        tempw = np.dot(eigenface[k], matrix)
        if k == 0:
            l1 = [tempw]
        else:
            l1 = np.append(l1, [tempw], axis=0)
    
    # looping setiap Omega dataset dan cari yang paling minim selisihnya
    dist = [euclid_distance(l1, Omega[i]) for i in range(len(C_aksen))]
    minimum = min(dist)
    
    tolerance=0
    for i in dist:
        tolerance+=i
    tolerance=(tolerance/len(C_aksen))*0.1
    
    if minimum < tolerance :
        minidx = dist.index(minimum)
        return minidx
    else :
        return -1
