from data import float_to_2f
from data import Layer0, Layer1, Layer2, Layer3
from random import uniform



file_W01 = open('Weights/Weights01.txt', 'w')
file_W12 = open('Weights/Weights12.txt', 'w')
file_W23 = open('Weights/Weights23.txt', 'w')



def Save_Weights(file, L_pre, L_next):
    for i in range(len(L_pre)):
        for j in range(len(L_next)-1):
            file.write(str(uniform(-1,1)) + '\n')
    file.close()


Save_Weights(file_W01, Layer0, Layer1)
Save_Weights(file_W12, Layer1, Layer2)
Save_Weights(file_W23, Layer2, Layer3)


print('Новые веса были успешно записаны!')