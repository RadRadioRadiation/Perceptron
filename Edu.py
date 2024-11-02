from data import float_to_2f, Read_WeightsFile, forLayers
from data import Layer0, Layer1, Layer2, Layer3, size_matrix, L_error1, L_error2, L_error3, exp
import math, time

start_time = time.time()

def format_time(seconds):
    hours, rem = divmod(seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return f'{int(hours)} часов, {int(minutes)} минут, {seconds:.2f} секунд'


Weights01 = Read_WeightsFile('Weights/Weights01.txt', len(Layer0), len(Layer1)-1)
Weights12 = Read_WeightsFile('Weights/Weights12.txt', len(Layer1), len(Layer2)-1)
Weights23 = Read_WeightsFile('Weights/Weights23.txt', len(Layer2), len(Layer3)-1)




def Read_Tests(test_papka_n, test_n):
    file = open('Tests/' + str(test_papka_n) + '/' + str(test_papka_n) + '_' + str(test_n + 1) + '.txt', 'r')
    s = file.read()
    s = s.split('\n')

    file.close()
    return s



def Read_TestLaeyer(test_papka_n, test_n):
    Layer = [0] * (size_matrix ** 2 + 1) #101
    Layer[size_matrix ** 2] = 1 

    for i in range(size_matrix):
        for j in range(size_matrix):
            Layer[j + i * size_matrix + 1] = float(mas_Tests[test_papka_n][test_n][i][j])

    return Layer



    


def find_Error_Output(test_papka_n):

    Correct_ans = [0.1] * 10
    Correct_ans[test_papka_n] = 0.9

    for i in range(len(Layer3) - 1):
        L_error3[i] = Correct_ans[i] - Layer3[i]



def find_Error(L_pre, W, L_next):
    for i in range(len(L_pre) - 1):
        L_pre[i] = 0
        for j in range(len(L_next) - 1):
            L_pre[i] += float(L_next[j]) * float(W[i][j])

    return L_pre


def Change_Weights(L_pre, W, L_next, L_error):
    for i in range(len(L_next) - 1):
        for j in range(len(L_pre)):
            W[j][i] += exp * L_error[i] * L_next[i] * (1 - L_next[i]) * L_pre[j]

    return W



N_tests = 32

#Создаём массив, который хранит все значения тестовых файлов
mas_Tests = [0] * 10
for i in range(10):
    mas_Tests[i] = [0] * N_tests
for test_papka_n in range(10):
    for test_n in range(N_tests):
        mas_Tests[test_papka_n][test_n] = Read_Tests(test_papka_n, test_n)





#ошибка обучения
err = 100
err_pre = 0

steps = 0
err_eps = 0.01
while err >= err_eps:
    err_pre = err
    err = 0
    for test_papka_n in range(10):
        for test_n in range(N_tests):

            #получаем все значения с теста
            Layer0 = Read_TestLaeyer(test_papka_n, test_n)

            #пробегаем по всем слоям
            Layer1 = forLayers(Layer0, Weights01, Layer1)
            Layer2 = forLayers(Layer1, Weights12, Layer2)
            Layer3 = forLayers(Layer2, Weights23, Layer3)


            #находим ошибку последнего слоя
            find_Error_Output(test_papka_n)

            #ДОП сумируем ошибки ВСЕХ тестов //складывать квадратично!!!
            for i in range(len(L_error3)):
                err += L_error3[i] ** 2

            #находим ошибки остальных слоёв
            L_error2 = find_Error(L_error2, Weights23, L_error3)
            L_error1 = find_Error(L_error1, Weights12, L_error2)


            #изменяем веса
            Weights23 = Change_Weights(Layer2, Weights23, Layer3, L_error3)
            Weights12 = Change_Weights(Layer1, Weights12, Layer2, L_error2)
            Weights01 = Change_Weights(Layer0, Weights01, Layer1, L_error1)

    steps += 1
    print(f'steps = {steps};          err = {err:.10f};          progress = {err - err_pre:.10f}')



#Сохранение весов
file_W01 = open('Weights/Weights01.txt', 'w')
file_W12 = open('Weights/Weights12.txt', 'w')
file_W23 = open('Weights/Weights23.txt', 'w')

def Save_Weights(file, L_pre, W, L_next):
    for i in range(len(L_pre)):
        for j in range(len(L_next)-1):
            file.write(str(W[i][j]) + '\n')
    file.close()

Save_Weights(file_W01, Layer0, Weights01, Layer1)
Save_Weights(file_W12, Layer1, Weights12, Layer2)
Save_Weights(file_W23, Layer2, Weights23, Layer3)


print('Обучение завершено успешно!')


end_time = time.time()
print(f'Время выполнения: {format_time(end_time - start_time)}')

file_EDUinfo = open('EDUinfo.txt', 'w')
file_EDUinfo.write(f'''Информация о последнем обучении:
Предел обучения = {err_eps}
Коэфицент обучения = {exp}
Количество шагов = {steps - 1}
Время обучения = {format_time(end_time - start_time)}
''')
file_EDUinfo.close()