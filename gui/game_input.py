#pyautogui is BSD-3
import pyautogui

import time
# from pywinauto.application import Application


class GameInput:
    def __init__(self):
        # split screen into squares
        self.input = ['enter', 'enter', 'up', 'enter', 'down', 'enter', 'enter']  # grid, columns first
        # self.input = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        # self.input = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        # transform into grid
        """
        enter      up   enter
        left    enter   right
        enter    down   enter
        """
        self.dim_x = 7
        self.dim_y = 1
        # self.grid_length = (length)/self.dim_x
        # self.grid_height = (height)/self.dim_y
        # input timer
        self.last_time = time.time()

    def coordinate_input(self, coordinate, length, height):
        # print("getting coordinate for game")
        grid_length = length / self.dim_x
        grid_height = height / self.dim_y
        # coordinate is in the form of x, y in int
        if time.time() - self.last_time > 1:
            self.last_time = time.time()
            chosen_num = 0
            for i in range(self.dim_x):  # length
                for j in range(self.dim_y):  # width
                    # print(f"i {i} j {j}")
                    # print(f"grid length {grid_length}")
                    # print(f"grid height {grid_height}")
                    grid_x_max = grid_length * (i + 1)
                    grid_x_min = grid_length * i
                    grid_y_max = grid_height * (j + 1)
                    grid_y_min = grid_height * j
                    # print("a")
                    if grid_x_min < coordinate[0] < grid_x_max and grid_y_min < coordinate[1] < grid_y_max:
                        chosen_num = j * self.dim_x + i
            chosen_key = self.input[chosen_num]
            print(f"chosen key: {chosen_key}")
            # if chosen_key == 'enter':
            #     pyautogui.click()
            # else:
            pyautogui.press(chosen_key)


if __name__ == "__main__":
    game_input = GameInput(pyautogui.size()[0], pyautogui.size()[1])
    time.sleep(1)
    game_input.coordinate_input(pyautogui.position())
