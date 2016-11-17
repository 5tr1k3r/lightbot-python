import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from lightbot import game


class Vertex:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __call__(self):
        return self.x, self.y, self.z


class LightbotOpenGLWindow:
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    SCALE = 1

    width = 5
    height = 4

    def __init__(self):
        self.vertices = []
        self.edges = []
        self.big_square = None

        pygame.init()
        display = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        gluPerspective(45, self.WINDOW_WIDTH / self.WINDOW_HEIGHT, 0.1, 50.0)
        glTranslatef(-2, 0, -7)
        glRotatef(-35.264, 1.0, 0.0, 0.0)
        glRotatef(-45.0, 0.0, 0.0, 1.0)
        glRotatef(5, 0, 0, 1)
        glRotatef(-4, 1, 0, 0)
        # glEnable(GL_DEPTH_TEST)         # THIS STUFF MAKES THINGS OPAQUE/SOLID!!!!!

        self._prepare_ground()

        self.start_game_cycle()

    def _prepare_ground(self):
        floor_height = 0

        for x in range(self.width + 1):
            for y in range(self.height + 1):
                self.vertices.append(Vertex(x, y, floor_height))
        # print(self.vertices)

        self.big_square = (0,
                           self.vertices.index(Vertex(0, self.height, 0)),
                           self.vertices.index(Vertex(self.width, self.height, 0)),
                           self.vertices.index(Vertex(self.width, 0, 0)))
        print(self.big_square)

        for i in range(1, self.height):
            x = self.vertices.index(Vertex(0, i, 0))
            y = self.vertices.index(Vertex(self.width, i, 0))
            self.edges.append((x, y))

        for i in range(1, self.width):
            x = self.vertices.index(Vertex(i, 0, 0))
            y = self.vertices.index(Vertex(i, self.height, 0))
            self.edges.append((x, y))

    @staticmethod
    def _process_events(log=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glRotatef(-1, 1, 0, 0)

            if log:
                print(event)

    @staticmethod
    def _clear_screen():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    @staticmethod
    def _update_screen():
        pygame.display.flip()
        pygame.time.wait(10)

    def start_game_cycle(self):
        while True:
            self._process_events(log=True)
            self._clear_screen()

            # All custom draw functions should go here.
            self.draw_basic_board()
            self.draw_current_state()

            self._update_screen()

    def draw_current_state(self):
        pass

    def draw_basic_board(self):
        self._draw_text(0, 0, 0, 'hey')

        glBegin(GL_QUADS)
        glColor3f(0.2, 1, 0.4)
        for vertex in self.big_square:
            glVertex3fv(self.vertices[vertex]())
        glEnd()

        glBegin(GL_LINES)
        glColor3f(0, 0, 0)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex]())
        glEnd()

    @staticmethod
    def _draw_text(x, y, z, text):
        position = (x, y, z)
        font = pygame.font.Font(None, 32)
        text_surface = font.render(text, True, (255, 255, 255, 255), (0, 0, 0, 255))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        glRasterPos3d(*position)
        glDrawPixels(text_surface.get_width(), text_surface.get_height(),
                     GL_RGBA, GL_UNSIGNED_BYTE, text_data)


if __name__ == '__main__':
    board = game.Board('board.txt')
    window = LightbotOpenGLWindow()
