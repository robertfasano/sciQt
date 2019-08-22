from PyQt5.QtGui import QPalette, QColor

light_color = QColor('#FFFFFF')
dark_color = QColor('#172B4D')

palette = QPalette()

for target in [QPalette.Base,
               QPalette.Window,
               QPalette.HighlightedText]:
    palette.setColor(target, light_color)
for target in [QPalette.WindowText,
               QPalette.Text,
               QPalette.ButtonText,
               QPalette.Highlight]:
    palette.setColor(target, dark_color)
