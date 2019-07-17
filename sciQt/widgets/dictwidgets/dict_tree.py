from PyQt5.QtWidgets import (QWidget, QAbstractItemView, QVBoxLayout,
        QMenu, QAction, QTreeWidget, QTreeWidgetItem, QHeaderView, QPushButton)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import *
# from emergent.utilities.containers import State
# from emergent.dashboard.structures.dict_menu import DictMenu
from functools import partial

class DictTree(QTreeWidget):
    def __init__(self, data={}):
        super().__init__()
        self.setColumnCount(2)
        header_item = QTreeWidgetItem(['Parameter', 'Value'])
        self.setHeaderItem(header_item)
        self.set_model(data)
        self.expand()
        self.resizeColumnToContents(0)
        
        ## editing
        self.editorOpen = False
        self.current_item = None
        self.last_item = None
        self.itemDoubleClicked.connect(self.open_editor)
        self.itemSelectionChanged.connect(self.close_editor)

    def add_node(self, parent, name):
        leaf = QTreeWidgetItem([name])
        parent.addChild(leaf)
        return leaf

    def get_model(self, model=None, parent=None):
        items = []
        if model is None:
            model = {}
            for i in range(self.topLevelItemCount()):
                items.append(self.topLevelItem(i))
        else:
            for i in range(parent.childCount()):
                items.append(parent.child(i))
        if items == []:
            return parent.text(1)
        for item in items:
            name = item.text(0)
            model[name] = self.get_model({}, item)
        return model


    def set_model(self, model, top_level=True, parent=None):
        for key in model:
            leaf = QTreeWidgetItem([key])
            if top_level:
                self.insertTopLevelItems(self.topLevelItemCount(), [leaf])
            else:
                parent.addChild(leaf)
            if isinstance(model[key], dict):
                self.set_model(model[key], top_level=False, parent=leaf)
            else:
                leaf.setText(1, str(model[key]))

    def get_subtree_nodes(self, item):
        nodes = []
        nodes.append(item)
        for i in range(item.childCount()):
            nodes.extend(self.get_subtree_nodes(item.child(i)))
        return nodes

    def get_all_items(self):
        all_items = []
        for i in range(self.topLevelItemCount()):
            top_item = self.topLevelItem(i)
            all_items.extend(self.get_subtree_nodes(top_item))
        return all_items

    def expand(self):
        items = self.get_all_items()
        for item in items:
            item.setExpanded(True)

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.close_editor()

    def open_editor(self):
        ''' Allow the currently-selected node to be edited. '''
        self.current_item = self.currentItem()
        self.currentValue = self.current_item.text(1)
        col = self.currentIndex().column()
        if col == 0:
            return
        if col in [1]:
            self.openPersistentEditor(self.currentItem(), col)
            self.editorOpen = 1

    def close_editor(self):
        ''' Disable editing after the user clicks another node. '''
        self.last_item = self.current_item
        self.current_item = self.currentItem()
        if self.editorOpen:
            self.last_item.setText(1,self.currentValue)
        self.closePersistentEditor(self.last_item, 1)
        self.editorOpen = 0
