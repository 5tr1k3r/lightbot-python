"""Main module for the project."""
import os
import sys

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame import locals as pyloc

from lightbot import game


# noinspection PyShadowingNames
class Vertex:
    """Implement a Vertex class.
    We can check equality of Vertices.
    """
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __call__(self):
        return self.x, self.y, self.z


class Floor:
    """Construct a floor object of a given size (in cells) and a given elevation.
    It is represented by:
    - all its vertices (a list of Vertex objects)
    - a big rectangle that covers the whole area (a tuple with 4 indices of vertices)
    - all the inner edges, e.g. 3x2 floor has 3 those edges
      each edge is a tuple with 2 indices of vertices
    """
    def __init__(self, width, height, level):
        self.level = level

        self.vertices = []
        for x in range(width + 1):
            for y in range(height + 1):
                self.vertices.append(Vertex(x, y, level))

        self.big_rect = (0,
                         self.vertices.index(Vertex(0, height, level)),
                         self.vertices.index(Vertex(width, height, level)),
                         self.vertices.index(Vertex(width, 0, level)))

        self.edges = []
        for i in range(1, height):
            x = self.vertices.index(Vertex(0, i, level))
            y = self.vertices.index(Vertex(width, i, level))
            self.edges.append((x, y))
        for i in range(1, width):
            x = self.vertices.index(Vertex(i, 0, level))
            y = self.vertices.index(Vertex(i, height, level))
            self.edges.append((x, y))


# noinspection PyShadowingNames
class LightbotOpenGLWindow:
    """A basic pygame-opengl window class."""
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    DESIRED_FPS = 100

    width = 5
    height = 4

    def __init__(self):
        self.init_window()
        self.set_default_camera_position()

        self.ground = Floor(self.width, self.height, level=0)
        self.second_floor = Floor(3, 3, level=1)

        self.start_game_cycle()

    def init_window(self):
        """Initialization and first few important OpenGL functions."""
        if sys.platform in ["win32", "win64"]:
            os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        display = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        pygame.display.set_mode(display, pyloc.DOUBLEBUF | pyloc.OPENGL)
        # THIS STUFF MAKES THINGS OPAQUE/SOLID!
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        # glEnable(GL_MULTISAMPLE)
        # glEnable(GL_LINE_SMOOTH)

    def set_default_camera_position(self):
        """Trying to make it look like original lightbot's isometric perspective."""
        glLoadIdentity()
        gluPerspective(45, self.WINDOW_WIDTH / self.WINDOW_HEIGHT, 0.1, 50.0)
        glTranslatef(-2, 0, -7)
        glRotatef(-35.264, 1, 0, 0)
        glRotatef(-45.0, 0, 0, 1)
        glRotatef(5, 0, 0, 1)
        glRotatef(-4, 1, 0, 0)

    def start_game_cycle(self):
        """Quite self-explanatory. Process events, prepare for drawing, do drawing.
        Should add game logic in there somewhere.
        """
        while True:
            self._process_events()
            self._clear_screen()

            # All custom draw functions should go here.
            self._draw_floor(self.ground, grid=True)
            self._draw_floor(self.second_floor, grid=True,
                             color=(0.5, 0.5, 0.5))
            self._draw_current_state()

            self._update_screen()

    def _process_events(self, log=None):
        """Events are keyboard and mouse button presses, mouse movement
        and other stuff like resizing the window.
        """
        # Here we check which keys are held down
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:             # LEFT - Rotate camera left
            glRotatef(1, -1, 0, 0)
        if keys[pygame.K_RIGHT]:            # RIGHT - Rotate camera right
            glRotatef(1, 1, 0, 0)
        if keys[pygame.K_DOWN]:             # DOWN - Rotate camera down
            glRotatef(1, 0, -1, 0)
        if keys[pygame.K_UP]:               # UP - Rotate camera up
            glRotatef(1, 0, 1, 0)
        if keys[pygame.K_PAGEUP]:           # PageUp - Zoom out
            glScalef(0.98, 0.98, 0.98)
        if keys[pygame.K_PAGEDOWN]:         # PageDown - Zoom in
            glScalef(1.02, 1.02, 1.02)
        if keys[pygame.K_SPACE]:            # SPACE - Pause
            self.pause()

        # Get event queue and check it for a few specific events
        for event in pygame.event.get():
            esc_is_pressed = (event.type == pygame.KEYDOWN and
                              event.key == pygame.K_ESCAPE)
            home_is_pressed = (event.type == pygame.KEYDOWN and
                               event.key == pygame.K_HOME)

            if event.type == pygame.QUIT or esc_is_pressed:
                pygame.quit()               # ESC - quit the game
                quit()
            if home_is_pressed:             # HOME - default camera position
                self.set_default_camera_position()

            if log:
                print(event)

    @staticmethod
    def pause():
        """A dummy function for the future."""
        pass

    @staticmethod
    def _clear_screen():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def _update_screen(self):
        pygame.display.flip()
        pygame.time.wait(1000 // self.DESIRED_FPS)

    def _draw_current_state(self):
        pass

    def _draw_floor(self, floor, grid=None, color=None):
        # self._draw_text(0, 0, 0, 'hey')
        if not color:
            color = (0.2, 0.4, 0.4)
        self._draw_rect(floor.vertices, floor.big_rect, color)

        if grid:
            line_color = (0, 0, 0)
            self._draw_lines(floor.vertices, floor.edges, line_color)

    @staticmethod
    def _draw_rect(vertices, rect, color):
        glBegin(GL_QUADS)
        glColor3f(*color)
        for vertex in rect:
            glVertex3fv(vertices[vertex]())
        glEnd()

    @staticmethod
    def _draw_lines(vertices, edges, color):
        glBegin(GL_LINES)
        glColor3f(*color)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex]())
        glEnd()

    @staticmethod
    def _draw_text(x, y, z, text):
        position = (x, y, z)
        font = pygame.font.Font(None, 32)
        color = (255, 255, 255, 255)
        background = (0, 0, 0, 255)
        text_surface = font.render(text, True, color, background)
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        glRasterPos3d(*position)
        glDrawPixels(text_surface.get_width(), text_surface.get_height(),
                     GL_RGBA, GL_UNSIGNED_BYTE, text_data)


if __name__ == '__main__':
    board = game.Board('board.txt')
    window = LightbotOpenGLWindow()
