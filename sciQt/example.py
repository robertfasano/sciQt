from sciQt import Dashboard, UnitEdit, DictMenu, ParameterTable, Frame

class MyDashboard(Dashboard):
    def __init__(self):
        Dashboard.__init__(self, title='My Dashboard')

    def buildUI(self):
        frame = Frame(self.layout)                ## create frame for text
        edit = UnitEdit()        ## add unitful line edit
        frame.addWidget(edit)

        menu = DictMenu('File', {'Hello': lambda: print('Hello world!')})   ## create menu
        self.menuBar().addMenu(menu)

        self.table = ParameterTable({'voltage': 0, 'phase': 3.14})
        self.layout.addWidget(self.table)

        self.show()

if __name__ == '__main__':
    dashboard = MyDashboard()
