import subprocess
from subprocess import CalledProcessError

class Notify(object):
    """wraps notification messages around a set of programs"""
    def __init__(self, app=None):
        super(Notify, self).__init__()
        self.zenity = {
            'path': '/usr/bin/zenity',
            'arguments': '--warning --text'
        }
        self.notify_send = {
            'path': '/usr/bin/notify-send',
            'arguments': '-u critical'
        }
        self.NOTIFIER = {'zenity': self.zenity, 'notify_send': self.notify_send,}
        if app is not None:
            self.app = self.NOTIFIER[app]
        else:
            self.app = self.__detect_app__()

    def notify(self, text=None):
        """calls the program with a message"""
        app = self.app
        if text is None:
            text = ""
        args = app['arguments'].split()
        args.append(text)

        p = subprocess.Popen([app['path']] + args)

    def __detect_app__(self):
        """returns the first found application"""
        for app in self.NOTIFIER.keys():
            try:
                subprocess.call(self.NOTIFIER[app]['path'])
            except CalledProcessError as e:
                print("{} not found. {}".format(app, e))
            else:
                return self.NOTIFIER[app]
