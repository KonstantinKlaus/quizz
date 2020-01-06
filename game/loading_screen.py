import threading
import time


class LoadingScreen:
    loading = False

    def __init__(self):
        pass

    def loading_screen(self, info: ""):
        # start loading thread
        self.loading = True
        threading.Thread(target=self.loading, ).start()

    def loading_screen_set_info(self, info):
        pass

    def loading(self):
        while self.loading:
            time.sleep(0.2)
