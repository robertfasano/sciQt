from sciQt import Dashboard, UnitEdit, DictMenu,  DictTable, Frame, TTLTable, DictTree
from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QWidget

class MyDashboard(Dashboard):
    def __init__(self):
        Dashboard.__init__(self, title='My Dashboard')

    def buildUI(self):
        menu = DictMenu('File', {'Hello': lambda: print('Hello world!')})   ## create menu
        self.menuBar().addMenu(menu)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        ## dict widgets tab
        self.dict_tab = QWidget()
        self.dict_tab.setLayout(QVBoxLayout())

        self.table = DictTable({'voltage': 0, 'phase': 3.14})
        self.dict_tab.layout().addWidget(self.table)

        tree = DictTree({'levelA': {'level2': {'level3': {'level4': 0}}}, 'level B': 1, 'levelC': {'levelC2': 'y'}})
        self.dict_tab.layout().addWidget(tree)
        self.tabs.addTab(self.dict_tab, 'Dictionary')

        ## unit widgets tab
        self.units_tab = QWidget()
        self.units_tab.setLayout(QVBoxLayout())
        self.units_tab.layout().addWidget(UnitEdit())
        self.tabs.addTab(self.units_tab, 'Units')

        ## color tab
        self.color_tab = QWidget()
        self.color_tab.setLayout(QVBoxLayout())
        from sciQt.widgets.labeled_widgets import LabeledComboBox
        from sciQt.widgets.color import ColorLabel, load_palette_options
        def update_label_color(text):
            color_label.setColor(text)

        color_edit = LabeledComboBox('Text color', load_palette_options())
        color_label = ColorLabel('colored label')
        color_edit.currentTextChanged.connect(update_label_color)
        color_edit.box.setCurrentIndex(1)
        self.color_tab.layout().addWidget(color_edit)
        self.color_tab.layout().addWidget(color_label)

        self.tabs.addTab(self.color_tab, 'Color')

if __name__ == '__main__':
    dashboard = MyDashboard()
