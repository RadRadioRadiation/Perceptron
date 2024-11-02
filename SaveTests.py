from data import *

# num 0 - 9 -> Запись в файл и установка всех значение клеток на 0
# L -> Показать значения
# X -> установка всех значение клеток на 0
# mb1 -> draw; mb2 -> remove



def SaveCells(num):
    file_last = open('Tests/' + str(num) + '/last' + str(num) + '.txt', 'r')
    num_last = int(file_last.read()) + 1
    file_last.close()

    file_save = open('Tests/' + str(num) + '/' + str(num) + '_' + str(num_last) + '.txt', 'w')

    s = ''
    for i in range(size_matrix):
        for j in range(size_matrix):
            s += str(Cells[i][j].value)
        s += '\n'

    file_save.write(s)

    file_last = open('Tests/' + str(num) + '/last' + str(num) + '.txt', 'w')
    file_last.write(str(num_last))
    file_last.close()
    print(f'Успешно сохранено! Last[{num}] = {num_last}')



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

            #load
            if e.key == pygame.K_l:
                pass

            elif e.key == pygame.K_0:
                SaveCells(0)
            elif e.key == pygame.K_1:
                SaveCells(1)
            elif e.key == pygame.K_2:
                SaveCells(2)
            elif e.key == pygame.K_3:
                SaveCells(3)
            elif e.key == pygame.K_4:
                SaveCells(4)
            elif e.key == pygame.K_5:
                SaveCells(5)
            elif e.key == pygame.K_6:
                SaveCells(6)
            elif e.key == pygame.K_7:
                SaveCells(7)
            elif e.key == pygame.K_8:
                SaveCells(8)
            elif e.key == pygame.K_9:
                SaveCells(9)




    #Отрисовка
    for i in range(size_matrix):
        for j in range(size_matrix):
            Cells[i][j].draw()

    pygame.display.update()
    clock.tick(60)