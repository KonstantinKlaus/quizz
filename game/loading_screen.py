import threading

import pygame

from game.constants import BLACK, WHITE


class LoadingScreen:
    is_loading = False

    angle = 0

    info = ""

    def __init__(self, game):
        self.info = None
        self.job = None
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.game = game

    def exit(self):
        self.is_loading = False

    def loading_screen_set_info(self, info):
        self.info = info

    def loading(self, task, params=(), info=""):
        self.info = info
        self.is_loading = True
        self.start_task(task, params)

        while self.is_loading:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.clock.tick(30)

    def start_task(self, task, params):
        # start work thread
        self.is_loading = True
        self.job = threading.Thread(target=task, args=params)
        self.job.start()

    def on_loop(self):
        # increase angle
        self.angle += 10
        # ensure angle does not increase indefinitely
        self.angle %= 360

        # check if thread still running
        if not self.job.isAlive():
            self.exit()

    def on_render(self):
        self.screen.fill(WHITE)

        (width, height) = self.screen.get_size()

        font = pygame.font.Font('freesansbold.ttf', int(0.15 * height))

        font2 = pygame.font.Font('freesansbold.ttf', int(0.055 * height))

        info = font2.render(self.info, True, BLACK)

        q = font.render("Q", True, BLACK)

        # create a new, rotated Surface
        rot_q = pygame.transform.rotate(q, self.angle)
        # and blit it to the screen
        self.screen.blit(rot_q, (0.5 * width - rot_q.get_width() // 2, 0.5 * height - rot_q.get_height() // 2))
        self.screen.blit(info, (0.5 * width - info.get_width() // 2, 0.65 * height - info.get_height() // 2))
        pygame.display.update()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.is_loading = False
            self.game.end_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_loading = False
                self.game.end_game()
