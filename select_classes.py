from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
import classifier



class all_classes(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.chosen = []
        self.setAcceptDrops(True)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            data = QMimeData()
            drag.setMimeData(data)
            drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        tree = event.source() 
        if tree == self:
            return

        widget = tree.currentItem() 
        base_index = tree.indexOfTopLevelItem(widget)
        class_index = tree.indexOfTopLevelItem(widget.parent())

        if base_index == -1:
            base = widget.parent()
            base.removeChild(widget)
            tree.chosen.remove(widget.text(1))
            if base.childCount() == 0:
                base_index = tree.indexOfTopLevelItem(base)
                tree.takeTopLevelItem(base_index)

        elif class_index == -1:
            base = widget
            base_index = tree.indexOfTopLevelItem(base)
            for index in range(base.childCount()):
                tree.chosen.remove(base.child(index).text(1))
            tree.takeTopLevelItem(base_index)


class selected_classes(all_classes):
    def __init__(self):
        super().__init__()

    def dropEvent(self, event):
        base_in_tree = None
        tree = event.source()
        if tree == self:
            return

        widget = tree.currentItem()
        base_index = tree.indexOfTopLevelItem(widget)
        class_index = tree.indexOfTopLevelItem(widget.parent())

        if base_index == -1:
            base = widget.parent()
            if widget.text(1) not in self.chosen:
                self.chosen.append(widget.text(1))
                base_in_tree = self.findItems(base.text(0), Qt.MatchExactly)
                if not base_in_tree:
                    self.addTopLevelItem(QTreeWidgetItem([base.text(0)]))
                base_in_tree = self.findItems(base.text(0), Qt.MatchExactly)
                base_in_tree[0].addChild(QTreeWidgetItem([widget.text(0), widget.text(1)]))

        elif class_index == -1:
            base = widget
            base_in_tree = self.findItems(base.text(0), Qt.MatchExactly)
            if not base_in_tree:
                self.addTopLevelItem(QTreeWidgetItem([base.text(0)]))
                base_in_tree = self.findItems(base.text(0), Qt.MatchExactly)
                for index in range(base.childCount()):
                    base_in_tree[0].addChild(QTreeWidgetItem([base.child(index).text(0), base.child(index).text(1)]))
                    self.chosen.append(base.child(index).text(1))
            else:
                for index in range(base.childCount()):
                    if base.child(index).text(1) not in self.chosen:
                        self.chosen.append(base.child(index).text(1))
                        base_in_tree[0].addChild(QTreeWidgetItem([base.child(index).text(0), base.child(index).text(1)]))
        if base_in_tree:
            base_in_tree[0].sortChildren(1, Qt.AscendingOrder)


class polygon_classes(all_classes):
    def __init__(self):
        super().__init__()

        self.setColumnCount(3)
        self.setHeaderLabels(['Name', 'Code', 'Points'])
        self.pairlist = []
        self.make_tuple()
        #self.fill_fromhdf()

    def fill_fromhdf(self, hdf):
        self.clear()
        for cclass in hdf.attrs[classifier.hdfs.CLASSES.value]:
            #print(type(cclass))
            name = self.get_name(int(cclass))
            #print(name)
            self.addTopLevelItem(QTreeWidgetItem([name, cclass]))
            #print(cclass)
            #self.addTopLevelItem(QTreeWidgetItem([base.text(0)]))
        #for base in classifier.bases.name():
        #    print(base)
        #self.itemEntered.connect()

    #def fill_fromhdf2(self, hdf):
    #    for item in hdf.

    def make_tuple(self):
        codelist = classifier.classes.code()
        namelist = classifier.classes.name()

        for code, name in zip(codelist, namelist):
            self.pairlist.append((code, name))
            #print(type(code))
       #print(self.pairlist)
    
    def get_name(self, code):
        for pair in self.pairlist:
            if pair[0] == code:
                return pair[1]


#    def current_base(self, item, column):
        


