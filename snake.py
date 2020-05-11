from tkinter import Tk, Canvas
import random

# Создание окна
root = Tk()
# ширина экрана
WIDTH = 800
# высота экрана
HEIGHT = 600
# Размер сегмента змейки
SEG_SIZE = 20
# Переменная отвечающая за состояние игры
IN_GAME = True
# Устанавливаем название окна
root.title("Змейка")


# Вспомогательные функции

#Создает яблоко, которое нужно съесть
def create_block():
    global BLOCK
    posx = SEG_SIZE * random.randint(1, (WIDTH-SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT-SEG_SIZE) / SEG_SIZE)
    # Яблоко это кружочек красного цвета
    BLOCK = c.create_oval(posx, posy,
                          posx+SEG_SIZE, posy+SEG_SIZE,
                          fill="red")

#Управляет игровым процессом
def main():
    global IN_GAME
    if IN_GAME:
        # Двигаем змейку
        s.move()
        # Двигаем змейку
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords
        # Проверка на столкновение с краями игрового поля
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False
        #Поедание яблоко
        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            create_block()
        # Сесть себя
        else:
            # Проходим по всем сегментам змеи
            for index in range(len(s.segments)-1):
                if head_coords == c.coords(s.segments[index].instance):
                    IN_GAME = False
        root.after(100, main)
    # Если Не IN_GAME то остановить игру и распечатать сообщение
    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')

#Сегмент одиночной змеи
class Segment(object):
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y,
                                           x+SEG_SIZE, y+SEG_SIZE,
                                           fill="white")

#класс Змея 
class Snake(object):
    def __init__(self, segments):
        self.segments = segments
        # список доступных направлений движения змейки
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}
        # изначально змейка двигается вправо
        self.vector = self.mapping["Right"]

    #Перемещает змею с указанным вектором
    def move(self):
        # перебираем все сегменты кроме первого
        for index in range(len(self.segments)-1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index+1].instance)
            # задаем каждому сегменту позицию сегмента стоящего после него
            c.coords(segment, x1, y1, x2, y2)
        # получаем координаты сегмента перед "головой"
        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        # помещаем "голову" в направлении указанном в векторе движения
        c.coords(self.segments[-1].instance,
                 x1+self.vector[0]*SEG_SIZE, y1+self.vector[1]*SEG_SIZE,
                 x2+self.vector[0]*SEG_SIZE, y2+self.vector[1]*SEG_SIZE)

    #Добавляет сегмент к змее
    def add_segment(self):
        # определяем последний сегмент
        last_seg = c.coords(self.segments[0].instance)
        # определяем координаты куда поставить следующий сегмент
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        # добавляем змейке еще один сегмент в заданных координатах
        self.segments.insert(0, Segment(x, y))

    #Изменяет направление движения змейки
    def change_direction(self, event):
        # event передаст нам символ нажатой клавиши
        # и если эта клавиша в доступных направлениях 
        # изменяем направление
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def reset_snake(self):
        for segment in self.segments:
            c.delete(segment.instance)


def set_state(item, state):
    c.itemconfigure(item, state=state)


def clicked(event):
    global IN_GAME
    s.reset_snake()
    IN_GAME = True
    c.delete(BLOCK)
    c.itemconfigure(restart_text, state='hidden')
    c.itemconfigure(game_over_text, state='hidden')
    start_game()


def start_game():
    global s
    create_block()
    s = create_snake()
    # Реакция на нажатие клавиши
    c.bind("<KeyPress>", s.change_direction)
    main()

# создаем набор сегментов 
# и собственно змейку
def create_snake():
    segments = [Segment(SEG_SIZE, SEG_SIZE),
                Segment(SEG_SIZE*2, SEG_SIZE),
                Segment(SEG_SIZE*3, SEG_SIZE)]
    return Snake(segments)




# создаем экземпляр класса Canvas 
#и заливаем все зеленым цветом
c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#004491")
c.grid()
# Наводим фокус на Canvas, чтобы мы могли ловить нажатия клавиш
c.focus_set()
game_over_text = c.create_text(WIDTH/2, HEIGHT/2, text="Конец Игры!",
                               font='Arial 20', fill='red',
                               state='hidden')
restart_text = c.create_text(WIDTH/2, HEIGHT-HEIGHT/3,
                             font='Arial 30',
                             fill='white',
                             text="Нажмите Сюда Для Перезапуска Игры",
                             state='hidden')

c.tag_bind(restart_text, "<Button-1>", clicked)
start_game()
root.mainloop()
