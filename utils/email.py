import threading


class EmailThread(threading.Thread):
    """Thread class to send emails."""

    def __init__(self, email_obj):
        threading.Thread.__init__(self)
        self.email_obj = email_obj

    def run(self):
        self.email_obj.send()
