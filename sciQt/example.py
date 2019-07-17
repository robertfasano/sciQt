from sciQt import Dashboard, UnitEdit, DictMenu,  DictTable, Frame, TTLTable, DictTree

class MyDashboard(Dashboard):
    def __init__(self):
        Dashboard.__init__(self, title='My Dashboard')

    def buildUI(self):
        frame = Frame(self.layout)                ## create frame for text
        edit = UnitEdit()        ## add unitful line edit
        frame.addWidget(edit)

        menu = DictMenu('File', {'Hello': lambda: print('Hello world!')})   ## create menu
        self.menuBar().addMenu(menu)

        self.table = DictTable({'voltage': 0, 'phase': 3.14})
        self.layout.addWidget(self.table)

        tree = DictTree({'levelA': {'level2': {'level3': {'level4': 0}}}, 'level B': 1, 'levelC': {'levelC2': 'y'}})
        self.layout.addWidget(tree)

if __name__ == '__main__':
    dashboard = MyDashboard()
