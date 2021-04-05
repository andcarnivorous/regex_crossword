import pygame

DIF = 500 / 9


class Drawer(object):

    def __init__(self, screen, font1, font2, x, y):
        self.screen = screen
        self.font1 = font1
        self.font2 = font2
        self.x = x
        self.y = y

    def draw_instruction(self):
        text1 = self.font2.render("ENTER STRINGS MATCHING THE REGEX ON BOTH AXIS", 1, (0, 0, 0))
        text2 = self.font2.render("ENTER LETTERS AND USE ARROW KEYS TO MOVE", 1, (0, 0, 0))
        self.screen.blit(text1, (30, 720))
        self.screen.blit(text2, (30, 740))

    def draw_result(self):
        text1 = self.font1.render("FINISHED PRESS R or D", 1, (0, 0, 0))
        self.screen.blit(text1, (20, 570))

    def draw_val(self, val):
        text1 = self.font1.render(str(val), 1, (0, 0, 0))
        self.screen.blit(text1, (self.x * DIF + 15, self.y * DIF + 15))

    def draw_box(self):
        #  Highlight the cell selected
        for i in range(2):
            pygame.draw.line(self.screen, (255, 0, 0), (self.x * DIF-3, (self.y + i)*DIF), (self.x * DIF + DIF + 3, (self.y + i)*DIF), 7)
            pygame.draw.line(self.screen, (255, 0, 0), ((self.x + i) * DIF, self.y * DIF), ((self.x + i) * DIF, self.y * DIF + DIF), 7)

    def update_xy(self, x, y):
        self.x = x
        self.y = y

    def draw_expressions(self, rows, cols):
        for i in range(len(rows)):
            for j in range(len(cols)):
                expression = self.font1.render(cols[i], 1, (15, 10, 15))
                self.screen.blit(expression, (250, (i * DIF)+15))

                expression = self.font1.render(rows[i], 1, (15, 10, 15))
                expression = pygame.transform.rotate(expression, 270)
                i += 10
                self.screen.blit(expression, ((i * DIF)+15, (DIF*len(rows)) + 10))
                i -= 10

    def draw(self, limit, grid):
        for i in range(limit):
            for j in range(limit):
                if grid[i][j] != 0:
                    i += 10
                    j += 0
                    # Fill blue color in already numbered grid
                    pygame.draw.rect(self.screen, (0, 153, 153), (i * DIF, j * DIF, DIF + 1, DIF + 1))

                    # Fill gird with default numbers specified
                    text1 = self.font1.render(str(grid[i-10][j]), 1, (0, 0, 0))
                    self.screen.blit(text1, (i * DIF + 15, j * DIF + 15))
                    i -= 10
                    j -= 0
        # Draw lines horizontally and verticallyto form grid
        for i in range(limit+1):
            if i % 3 == 0:
                thick = 1
            else:
                thick = 1
            pygame.draw.line(self.screen, (0, 0, 0), (555, i * DIF), (555 + (DIF * limit), i * DIF), thick)
            i += 10
            pygame.draw.line(self.screen, (0, 0, 0), (i * DIF, 0), (i * DIF, DIF*limit), thick)

    def get_cord(self, pos):

        x = pos[0]//DIF

        y = pos[1]//DIF
        self.update_xy(x, y)
