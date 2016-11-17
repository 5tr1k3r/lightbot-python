from collections import namedtuple

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from lightbot import game


# noinspection PyShadowingNames
class Vertex:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __call__(self):
        return self.x, self.y, self.z


# noinspection PyShadowingNames
class LightbotOpenGLWindow:
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    SCALE = 1

    width = 5
    height = 4

    Floor = namedtuple('Floor', 'vertices, edges, big_rect')

    def __init__(self):
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

        self.ground = self._make_floor(level=0)
        self.second_floor = self._make_floor(level=1)

        self.start_game_cycle()

    def _make_floor(self, level):
        vertices = []
        edges = []

        for x in range(self.width + 1):
            for y in range(self.height + 1):
                vertices.append(Vertex(x, y, level))
        # print(self.vertices)

        big_rect = (0,
                    vertices.index(Vertex(0, self.height, level)),
                    vertices.index(Vertex(self.width, self.height, level)),
                    vertices.index(Vertex(self.width, 0, level)))

        for i in range(1, self.height):
            x = vertices.index(Vertex(0, i, level))
            y = vertices.index(Vertex(self.width, i, level))
            edges.append((x, y))

        for i in range(1, self.width):
            x = vertices.index(Vertex(i, 0, level))
            y = vertices.index(Vertex(i, self.height, level))
            edges.append((x, y))

        return self.Floor(vertices, edges, big_rect)

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
            self._process_events()
            self._clear_screen()

            # All custom draw functions should go here.
            self._draw_floor(self.ground)
            self._draw_floor(self.second_floor)
            self.draw_current_state()

            self._update_screen()

    def draw_current_state(self):
        pass

    @staticmethod
    def _draw_floor(floor):
        # self._draw_text(0, 0, 0, 'hey')

        glBegin(GL_QUADS)
        glColor3f(0.2, 0.4, 0.4)
        for vertex in floor.big_rect:
            glVertex3fv(floor.vertices[vertex]())
        glEnd()

        glBegin(GL_LINES)
        glColor3f(0, 0, 0)
        for edge in floor.edges:
            for vertex in edge:
                glVertex3fv(floor.vertices[vertex]())
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
