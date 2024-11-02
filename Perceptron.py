from data import *

# mb1 -> draw; mb2 -> remove
# X -> установка всех значение клеток на 0



font = pygame.font.SysFont('Arial', 15)
class Output:
    def __init__(self, index):
        self.rect = pygame.Rect(600, 50 + index * 50, 40, 40)
        self.rect_in = pygame.Rect(602, 52 + index * 50, 36, 36)
        self.color = (200, 200, 200)
        self.color_in = (0, 0, 0)
        self.value = 0
        self.text = font.render(str(self.value), True, (255, 255, 255))


    def change_value(self, num):
        self.value = float(num)


    def draw(self, index):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.color_in, self.rect_in)

        self.text = font.render(float_to_2f(self.value), True, (255, 255, 255))
        screen.blit(self.text, (660, 60 + index * 50))

        self.text = font.render(str(index), True, (255, 255, 255))
        screen.blit(self.text, (570, 60 + index * 50))



List_Output = [0] * 10
for i in range(10):
    List_Output[i] = Output(i)




#смещение
for i in range(size_matrix):
    for j in range(size_matrix):
        Cells[i][j].rect.x -= 100


Weights01 = Read_WeightsFile('Weights/Weights01.txt', 101, 64)
Weights12 = Read_WeightsFile('Weights/Weights12.txt', 65, 16)
Weights23 = Read_WeightsFile('Weights/Weights23.txt', 17, 10)




while True:
    screen.fill((0, 0, 0))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()


        if e.type == pygame.MOUSEBUTTONDOWN:
            which_button_down = 1 if e.button == 1 else 2
            motion = True
            
        if e.type == pygame.MOUSEBUTTONUP:
            motion = False
            which_button_down = 0
            
            #Обновляем проверку(нужно чтобы при нажатии не было зацикливания)
            for i in range(size_matrix):
                for j in range(size_matrix):
                    Cells[i][j].isclicked = False

        if motion and e.type == pygame.MOUSEMOTION:
            x, y = e.pos
            for i in range(size_matrix):
                for j in range(size_matrix):
                    if Cells[i][j].rect.x < x < Cells[i][j].rect.right and Cells[i][j].rect.y < y < Cells[i][j].rect.bottom:
                        if which_button_down == 1:
                            Cells[i][j].click()
                        if which_button_down == 2:
                            Cells[i][j].remove()

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_x:
                for i in range(size_matrix):
                    for j in range(size_matrix):
                        Cells[i][j].remove()


    for i in range(size_matrix):
        for j in range(size_matrix):
            Layer0[j + i * size_matrix + 1] = Cells[i][j].value

    #пробегаем по всем слоям
    forLayers(Layer0, Weights01, Layer1)
    forLayers(Layer1, Weights12, Layer2)
    forLayers(Layer2, Weights23, Layer3)


    for i in range(10):
        List_Output[i].change_value(Layer3[i])

    max_value = 0
    index_max_value = 0
    for i in range(10):
        List_Output[i].color_in = (0, 0, 0)
        if max_value <= List_Output[i].value:
            max_value = List_Output[i].value
            index_max_value = i

    List_Output[index_max_value].color_in = (200, 200, 200)


    #Отрисовка
    for i in range(size_matrix):
        for j in range(size_matrix):
            Cells[i][j].draw()

    for i in range(10):
        List_Output[i].draw(i)

    pygame.display.update()
    clock.tick(60)