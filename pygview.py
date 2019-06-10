#!/usr/bin/env python

####

import pygame

class PygView(object):
    """Pygame interface"""

    CURSORKEYS = slice(273, 277)
    QUIT_KEYS = pygame.K_ESCAPE, pygame.K_q
    EVENTS = 'up', 'down', 'right', 'left', 'drag'

    def __init__(self, controller, config):

        self.controller = controller
        self.width = config.width
        self.height = config.height
        self.back_color = config.back_color
        self.fps = config.fps
        self.font_color = config.font_color

        pygame.init()
        flags = pygame.DOUBLEBUF | [0, pygame.FULLSCREEN][config.fullscreen]
        self.canvas = pygame.display.set_mode((self.width, self.height), flags)
        pygame.display.set_caption(config.title)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(config.visibmouse)
        self.font = pygame.font.Font(None, self.height // config.font_ratio)


    @property
    def frame_duration_secs(self):

        return 0.001 * self.clock.get_time()


    def run(self):
        """Main loop"""

        running = True
        while running:
            self.clock.tick_busy_loop(self.fps)
            running = self.controller.dispatch(self.get_events())
            self.flip()
        else:
            self.quit()


    def get_events(self):

        keys = pygame.key.get_pressed()[PygView.CURSORKEYS]
        move_events = [e for e, k in zip(PygView.EVENTS, keys) if k]
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            move_events += {'drag'}

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit', move_events
            if event.type == pygame.KEYDOWN:
                if event.key in PygView.QUIT_KEYS:
                    return 'quit', move_events
                else:
                    return 'other_key', move_events
        else:
            return None, move_events


    def rectangle(self, xywh, color, border=0):

        pygame.draw.rect(self.canvas, color, xywh, border)


    def draw_text(self, text, colour=None, size=None, pos=None):
        if colour is None:
            fw, fh = self.font.size(text)
            surface = self.font.render(text, True, self.font_color)
            self.canvas.blit(surface, ((self.width - fw) // 2, (self.height - fh) // 2))
            return

        font = pygame.font.SysFont("Noto Mono", size, True)
        surface = font.render(text, True, colour)
        self.canvas.blit(surface, pos)

    def flip(self):

        pygame.display.flip()
        self.canvas.fill(self.back_color)


    def quit(self):

        pygame.quit()