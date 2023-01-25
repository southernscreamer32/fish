import pyautogui, time


class GameInput():
    def __init__(self, length, height):
        # split screen into squares
        self.input = ['enter', 'left', 'enter', 'up', 'enter', 'down', 'enter', 'right', 'enter']   # grid, columns first
        # transform into grid
        """
        enter      up   enter
        left    enter   right
        enter    down   enter
        """
        self.dim_x = 3
        self.dim_y = 3
        self.grid_length = length/self.dim_x
        self.grid_height = height/self.dim_y

    def coordinate_input(self, coordinate):
        # coordinate is in the form of x, y in int
        chosen_num = 0
        for i in range(self.dim_x): #length
            for j in range(self.dim_y): #width
                grid_x_max = self.grid_length*(i+1)
                grid_x_min = self.grid_length*i
                grid_y_max = self.grid_height*(j+1)
                grid_y_min = self.grid_height*j
                if grid_x_min < coordinate[0] and coordinate[0] < grid_x_max and grid_y_min < coordinate[1] and coordinate[1] < grid_y_max:
                    chosen_num = i*self.dim_x+j
        chosen_key = self.input[chosen_num]
        pyautogui.press(chosen_key)

if __name__ == "__main__":
    game_input = GameInput(pyautogui.size()[0], pyautogui.size()[1])
    time.sleep(1)
    game_input.coordinate_input(pyautogui.position())
