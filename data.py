import pygame, sys, math
pygame.init()

def float_to_2f(num):
    return '%.2f' %float(num)


#коэф обучения
exp = 0.01



# Layers: 100 + 1 -> 64 + 1 -> 16 + 1 -> 10  // +1 - нейрон смещения
# Weights01 = 101 * 64 = 6464
# Weights12 = 65 * 16 = 1040
# Weights23 = 17 * 10 = 170


size_matrix = 10
Layer0 = [0] * (size_matrix ** 2 + 1) #101
Layer0[len(Layer0) - 1] = 1      #нейрон смещения
Layer1 = [0] * 65
Layer1[len(Layer1) - 1] = 1      #нейрон смещения
Layer2 = [0] * 17
Layer2[len(Layer2) - 1] = 1      #нейрон смещения
Layer3 = [0] * 11


L_error1 = [0] * (len(Layer1) - 1)
L_error2 = [0] * (len(Layer2) - 1)
L_error3 = [0] * (len(Layer3) - 1)


#функция возвращает двойной список со всеми весами из файла
def Read_WeightsFile(file_name, size_pre, size_next):

    file = open(file_name, 'r')
    s = file.read()
    s = s.split('\n')

    #создание пустого двойного массива
    Weights = [0] * size_pre
    for i in range(size_pre): 
        Weights[i] = [0] * size_next


    #заполнение двойного массива
    for i in range(size_pre):
        for j in range(size_next):
            Weights[i][j] = float(s[j + i * size_next])

    file.close()
    return Weights


#функция проходит по всем слоям
def forLayers(L_pre, W, L_next):
    for i in range(len(L_next) - 1):
        L_next[i] = 0
        for j in range(len(L_pre)):
            L_next[i] += float(L_pre[j]) * float(W[j][i])

        L_next[i] = 1 / (1 + math.exp(-1 * L_next[i]))

    return L_next







WW = 800
WH = 600


screen = pygame.display.set_mode((WW, WH))
clock = pygame.time.Clock()

#Класс клетка
class Cell:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, cell_size, cell_size)
        self.color = (90, 90, 90)
        self.value = 0

    def click(self):
        self.value = 1
        self.color = (250, 250, 250)

    def remove(self):
        self.value = 0
        self.color = (90, 90, 90)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)



cell_size = 29

#Создание массива
Cells = [0] * size_matrix
for i in range(size_matrix): 
    Cells[i] = [0] * size_matrix


#Заполнение массива
for i in range(size_matrix):
    for j in range(size_matrix):
        Cells[i][j] = Cell((cell_size + 1) * j + 250, (cell_size + 1) * i + 150)



motion = False
which_button_down = 0