import threading
import time

from game.constants import *


class LoadingScreen:
    loading = False

    angle = 0

    def __init__(self, game):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.game = game

    def exit(self):
        self.loading = False

    def loading_screen(self, info=""):
        self.screen.fill(WHITE)

        # start loading thread
        self.loading = True
        threading.Thread(target=self.is_loading, ).start()

    def loading_screen_set_info(self, info):
        pass

    def is_loading(self):
        while self.loading:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.clock.tick(30)

    def on_loop(self):
        # increase angle
        self.angle += 10
        # ensure angle does not increase indefinitely
        self.angle %= 360

    def on_render(self):
        (width, height) = self.screen.get_size()

        # font = pygame.font.Font('freesansbold.ttf', int(0.15 * height))
        #
        # q = font.render("Q", True, BLACK)
        #
        # # create a new, rotated Surface
        # rot_q = pygame.transform.rotate(q, self.angle)
        # # and blit it to the screen
        # self.screen.blit(rot_q, (0.5 * width - rot_q.get_width() // 2, 0.5 * height - rot_q.get_height() // 2))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.loading = False
            self.game.end_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.loading = False
                self.game.end_game()

