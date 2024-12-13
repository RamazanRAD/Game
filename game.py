import tkinter as tk
from random import randint


class Game:
    def __init__(self, canvas):
        """Инициализация игры."""
        self.canvas = canvas
        self.snake_coords = [[14, 14]]
        self.apple_coords = [randint(0, 29) for _ in range(2)]
        self.vector = {
            "Up": (0, -1),
            "Down": (0, 1),
            "Left": (-1, 0),
            "Right": (1, 0),
        }
        self.direction = self.vector["Right"]
        self.canvas.focus_set()
        self.canvas.bind("<KeyPress>", self.set_direction)
        self.game_loop()

    def set_apple(self):
        """Устанавливает новое положение яблока."""
        self.apple_coords = [randint(0, 29) for _ in range(2)]
        if self.apple_coords in self.snake_coords:
            self.set_apple()

    def set_direction(self, event):
        """Устанавливает направление движения змейки."""
        if event.keysym in self.vector:
            self.direction = self.vector[event.keysym]

    def draw(self):
        """Отрисовывает текущий кадр игры."""
        self.canvas.delete(tk.ALL)
        x_apple, y_apple = self.apple_coords
        self.canvas.create_rectangle(
            x_apple * 10, y_apple * 10,
            (x_apple + 1) * 10, (y_apple + 1) * 10,
            fill="red", width=0
        )
        for x, y in self.snake_coords:
            self.canvas.create_rectangle(
                x * 10, y * 10,
                (x + 1) * 10, (y + 1) * 10,
                fill="green", width=0
            )

    @staticmethod
    def coord_check(coord):
        """Возвращает координаты на интервале [0, 29]."""
        if coord > 29:
            return 0
        if coord < 0:
            return 29
        return coord

    def game_loop(self):
        """Главный игровой цикл."""
        self.draw()
        x, y = self.snake_coords[0]
        x += self.direction[0]
        y += self.direction[1]
        x = self.coord_check(x)
        y = self.coord_check(y)

        if [x, y] == self.apple_coords:
            self.set_apple()
        elif [x, y] in self.snake_coords:
            self.snake_coords = []
        else:
            self.snake_coords.pop()

        self.snake_coords.insert(0, [x, y])
        self.canvas.after(100, self.game_loop)


if __name__ == "__main__":
    root = tk.Tk()
    canvas = tk.Canvas(root, width=300, height=300, bg="black")
    canvas.pack()
    game = Game(canvas)
    root.mainloop()