from PyQt5.QtWidgets import QApplication

def Application():
    app = QApplication.instance()
    if app is None:
        app = QApplication([" "])         # Create an instance of the application
    return app
