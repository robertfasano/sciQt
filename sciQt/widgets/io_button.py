from abc import abstractmethod
from PyQt5.QtWidgets import QPushButton, QDialog

class IOButton(QPushButton):
    ''' A template for a button representing an i/o event. '''
    def __init__(self, channel, size=(75, 30), inactive_color = '#999999', active_color = '#00CCCC'):
        QPushButton.__init__(self)
        self.channel = channel
        self.setFixedSize(*size)

        self.setProperty('active', False)
        style = f'''
        QPushButton:flat[active=true]{{background-color: {active_color}; border:1px solid black;}}
        QPushButton:flat[active=false]{{background-color: {inactive_color}; border:1px solid black;}}
        '''
        self.setStyleSheet(style)
        self.setFlat(True)
        self.setAutoFillBackground(True)

    @abstractmethod
    def get_state(self):
        raise NotImplementedError

    @abstractmethod
    def set_state(self, state):
        raise NotImplementedError

    @abstractmethod
    def create_event(self):
        raise NotImplementedError

    @abstractmethod
    def isActive(self):
        raise NotImplementedError

    class Dialog(QDialog):
        @abstractmethod
        def __init__(self, parent):
            raise NotImplementedError

        @abstractmethod
        def get_event(self):
            raise NotImplementedError
