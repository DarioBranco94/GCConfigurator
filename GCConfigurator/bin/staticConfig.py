#
# Copyright (c) 2019-2020 by University of Campania "Luigi Vanvitelli".
# Developers and maintainers: Salvatore Venticinque, Dario Branco.
# This file is part of GreenCharge
# (see https://www.greencharge2020.eu/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#


import time

from datetime import datetime

from PyQt5 import uic, QtCore,QtGui, QtWidgets, QtXml
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtGui import QIcon


from numpy import *
import csv
import os
import staticConfig as sC



class XmlHandler(QtXml.QXmlDefaultHandler):
    def __init__(self, root):
        QtXml.QXmlDefaultHandler.__init__(self)
        self._root = root
        self._item = None
        self._text = ''
        self._error = ''

    def startElement(self, namespace, name, qname, attributes):
        if qname == 'house' or qname == 'device'  or qname == 'chargingStation' or qname == 'ecar' or qname == 'heatercooler' or qname == 'battery' or qname == 'backgroundload':
            if self._item is not None:
                self._item = QtWidgets.QTreeWidgetItem(self._item)
            else:
                self._item = QtWidgets.QTreeWidgetItem(self._root)
            self._item.setData(0, QtCore.Qt.UserRole, qname)
            if( qname == 'chargingStation'):
                self._item.setText(0, "Charging Station "+attributes.value('id'))
            if( qname == 'house'):
                self._item.setText(0, "House "+attributes.value('id'))
            if qname == 'house' :
                self._item.setExpanded(True)
                self._item.setIcon(0, QIcon('../res/GUI/images/icons8-cottage-80.png'))
            if(qname == 'chargingStation'):
                self._item.setExpanded(True)
                self._item.setIcon(0, QIcon('../res/GUI/images/icons8-batteria-per-auto-80.png'))
            elif qname == 'device':
                self._item.setText(1, attributes.value('type'))
                self._item.setIcon(0, QIcon('../res/GUI/images/icons8-elettrico-80.png'))
            elif qname == 'ecar':
                self._item.setText(1, attributes.value('type'))
                self._item.setIcon(0, QIcon('../res/GUI/images/icons8-carpool-80.png'))

          
        self._text = ''
        return True

    def endElement(self, namespace, name, qname):
        if qname == 'name':
            if self._item is not None:
                self._item.setText(0, self._text)
        elif qname == 'type':
            if self._item is not None:
                self._item.setText(2, self._text)
        elif qname == 'id':
            if self._item is not None:
                self._item.setText(1, self._text)
        elif qname == 'house' or qname == 'device'  or qname == 'chargingStation' or qname == 'ecar' or qname == 'heatercooler' or qname == 'battery' or qname == 'backgroundload':
            self._item = self._item.parent()
            
        return True

    def characters(self, text):
        self._text += text
        return True

    def fatalError(self, exception):
        print('Parse Error: line %d, column %d:\n  %s' % (
              exception.lineNumber(),
              exception.columnNumber(),
              exception.message(),
              ))
        return False

    def errorString(self):
        return self._error


class XmlHandlerGeneral(QtXml.QXmlDefaultHandler):
    def __init__(self, root):
        QtXml.QXmlDefaultHandler.__init__(self)
        self._root = root
        self._item = None
        self._text = ''
        self._error = ''

    def startElement(self, namespace, name, qname, attributes):
        if qname == 'house' or qname == 'device'  or qname == 'chargingStation' or qname == 'ecar' or qname == 'heatercooler' or qname == 'battery' or qname == 'backgroundload':
            if self._item is not None:
                self._item = QtWidgets.QTreeWidgetItem(self._item)
            else:
                self._item = QtWidgets.QTreeWidgetItem(self._root)
            self._item.setData(0, QtCore.Qt.UserRole, qname)
            if( qname == 'chargingStation'):
                self._item.setText(0, "Charging Station "+attributes.value('id'))
            if( qname == 'house'):
                self._item.setText(0, "House "+attributes.value('id'))
            if qname == 'house' :
                self._item.setExpanded(True)
                self._item.setIcon(0, QIcon('../res/GUI/images/icons8-cottage-80.png'))
            if(qname == 'chargingStation'):
                self._item.setExpanded(True)
                self._item.setIcon(0, QIcon('../res/GUI/images/icons8-batteria-per-auto-80.png'))
            elif qname == 'device':
                self._item.setText(1, attributes.value('type'))
                self._item.setIcon(0, QIcon('../res/GUI/images/icons8-elettrico-80.png'))
            elif qname == 'ecar':
                None
            else:
                None

          
        self._text = ''
        return True

    def endElement(self, namespace, name, qname):
        if qname == 'name':
            if self._item is not None:
                self._item.setText(0, self._text)
        elif qname == 'type':
            if self._item is not None:
                self._item.setText(2, self._text)
        elif qname == 'id':
            if self._item is not None:
                self._item.setText(1, self._text)
        elif qname == 'house' or qname == 'device' or qname == 'chargingStation':
            self._item = self._item.parent()
        elif qname == 'ecar':
            None
        else:
            None
        return True

    def characters(self, text):
        self._text += text
        return True

    def fatalError(self, exception):
        print('Parse Error: line %d, column %d:\n  %s' % (
              exception.lineNumber(),
              exception.columnNumber(),
              exception.message(),
              ))
        return False

    def errorString(self):
        return self._error



class XmlHandlerEcar(QtXml.QXmlDefaultHandler):
    def __init__(self, root):
        QtXml.QXmlDefaultHandler.__init__(self)
        self._root = root
        self._item = None
        self._text = ''
        self._error = ''

    def startElement(self, namespace, name, qname, attributes):
        if qname == 'house' or qname == 'chargingStation' or qname == 'ecar':
            if self._item is not None:
                self._item = QtWidgets.QTreeWidgetItem(self._item)
            else:
                self._item = QtWidgets.QTreeWidgetItem(self._root)
            self._item.setData(0, QtCore.Qt.UserRole, qname)
            if( qname == 'chargingStation'):
                self._item.setText(0, "Charging Station "+attributes.value('id'))
            if( qname == 'house'):
                self._item.setText(0, "House "+attributes.value('id'))
            if qname == 'house' :
                self._item.setExpanded(True)
                self._item.setIcon(0, QIcon('../res/GUI/images/icons8-cottage-80.png'))
            if(qname == 'chargingStation'):
                self._item.setExpanded(True)
                self._item.setIcon(0, QIcon('../res/GUI/images/icons8-batteria-per-auto-80.png'))
            elif qname == 'ecar':
                self._item.setText(1, attributes.value('type'))
                self._item.setIcon(0, QIcon('../res/GUI/images/icons8-carpool-80.png'))
            elif qname == 'heatercooler' or qname == 'battery' or qname == 'backgroundload':
                self._item.setText(1, attributes.value('type'))
                self._item.setIcon(0, QIcon('../res/GUI/images/icons8-carpool-80.png'))

          
        self._text = ''
        return True

    def endElement(self, namespace, name, qname):
        if qname == 'name':
            if self._item is not None:
                self._item.setText(0, self._text)
        elif qname == 'type':
            if self._item is not None:
                self._item.setText(2, self._text)
        elif qname == 'id':
            if self._item is not None:
                self._item.setText(1, self._text)
        elif qname == 'house' or qname == 'chargingStation' or qname == 'ecar':
            self._item = self._item.parent()
            
        return True

    def characters(self, text):
        self._text += text
        return True

    def fatalError(self, exception):
        print('Parse Error: line %d, column %d:\n  %s' % (
              exception.lineNumber(),
              exception.columnNumber(),
              exception.message(),
              ))
        return False

    def errorString(self):
        return self._error
