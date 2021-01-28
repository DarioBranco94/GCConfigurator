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
import datetime

from PyQt5 import uic, QtCore,QtGui, QtWidgets, QtXml
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QListWidgetItem,QMessageBox
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from numpy import *
import csv
import random
from lxml import etree as ET
import os
import staticConfig as sC
from xml.etree import ElementTree
from xml.dom import minidom
from shutil import copy2
from multiprocessing import Process, Pool
import psutil
import asyncio
import threading
import pdb




def runner():
    scheduler = sche.scheduler("scheduler@greencharge.eu", "branco25")
    sched = scheduler.start()
    sched.result()
    #self.editStartTime.text()



    for i in range(4):
        abilit = 0
        es.date = "01/01/01 00:00:00"
        es.datetime_object = datetime.datetime.strptime("01/01/01 00:00:00", '%m/%d/%y %H:%M:%S')
        #external = es.ExternalSourceAgent("externalSource@greencharge.eu", "branco25","../xml/neighborhood.xml","../xml/loads.xml")
        external = es.ExternalSourceAgent("externalSource@greencharge.eu", "branco25","../xml/neighborhood.xml", "../xml/loads.xml")
        ex = external.start()
        ex.result()
        external.stop()
        setupmodule = sm.setupModule("setupmodule@greencharge.eu", "branco25")
        setupmodule.start()
        while(abilit == 0):
            None
        while(setupmodule.is_alive()):
            setupmodule.stop()
    while(scheduler.is_alive()):
        scheduler.stop()








class splashUi(QtWidgets.QMainWindow):

        def __init__(self, parent = None):
            super(splashUi,self).__init__(parent)
            uic.loadUi('../res/GUI/splashscreen.ui', self)

class backgroundUi(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(backgroundUi, self).__init__(parent)
        uic.loadUi('../res/GUI/background.ui', self)
        self.parent = parent
        self.grandparent = self.parent.parent.parent
        print(len(self.parent.idArray))

        with open('../res/csv_files/deviceRepositoryData.csv', "r") as fileInput:
            reader = csv.reader(fileInput)
            lines = []
            for line in reader:
                if (self.parent.treeWidget.selectedItems()[0].text(0) == line[0]):
                    lines.append(line[2])
        splitted = lines[0].split(";")
        onlyname = []
        for i in range(len(splitted) - 1):
            onlyname = splitted[i].split("/")
            self.comboBox.addItem(onlyname[len(onlyname) - 1])

    def accept(self):

        def calculateTime(file):
            dirPath2 = "../Inputs/" + file
            f = open(dirPath2)
            csv_f = csv.reader(f)
            data = []
            count = 0
            for row in csv_f:
                data.append(row[0].split()[0])
                count += 1
            f.close()
            delta = int(data[-1]) - int(data[0])
            return delta

        for i in self.parent.idArray:
            entry = []
            entry.append(i)
            entry.append(self.comboBox.currentText())
            with open('../res/csv_files/eventbackground.csv', mode='a') as device_data:
                device_writer = csv.writer(device_data, delimiter=',')
                device_writer.writerow(entry)
                icon = QIcon("../res/GUI/images/icons8-checkmark-80")
                item = self.grandparent.treeWidget_2.findItems(i, Qt.MatchExactly | Qt.MatchRecursive, 1)
                item[0].setIcon(3, icon)
                item[0].setText(3, "  ")
        self.grandparent.showLoads()
        self.parent.close()
        self.parent.parent.close()
        self.close()

class backgroundUiSingle(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(backgroundUiSingle, self).__init__(parent)
        uic.loadUi('../res/GUI/background.ui', self)
        self.parent = parent

        with open('../res/csv_files/deviceRepositoryData.csv', "r") as fileInput:
            reader = csv.reader(fileInput)
            lines = []
            for line in reader:
                if (self.parent.treeWidget_2.selectedItems()[0].text(0) == line[0]):
                    lines.append(line[2])
        splitted = lines[0].split(";")
        onlyname = []
        for i in range(len(splitted) - 1):
            onlyname = splitted[i].split("/")
            self.comboBox.addItem(onlyname[len(onlyname) - 1])

    def accept(self):

        def calculateTime(file):
            dirPath2 = "../Inputs/" + file
            f = open(dirPath2)
            csv_f = csv.reader(f)
            data = []
            count = 0
            for row in csv_f:
                data.append(row[0].split()[0])
                count += 1
            f.close()
            delta = int(data[-1]) - int(data[0])
            return delta

        entry = []
        entry.append(self.parent.treeWidget_2.selectedItems()[0].text(1))
        entry.append(self.comboBox.currentText())
        with open('../res/csv_files/eventbackground.csv', mode='a') as device_data:
            device_writer = csv.writer(device_data, delimiter=',')
            device_writer.writerow(entry)
            icon = QIcon("../res/GUI/images/icons8-checkmark-80")
            self.parent.treeWidget_2.selectedItems()[0].setIcon(3, icon)
            self.parent.treeWidget_2.selectedItems()[0].setText(3, "  ")
        self.parent.showLoads()

        self.close()

class heaterCooler(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(heaterCooler, self).__init__(parent)
        uic.loadUi('../res/GUI/heatercooler.ui', self)
        self.parent = parent
        self.grandparent = self.parent.parent.parent
        print(len(self.parent.idArray))

        with open('../res/csv_files/deviceRepositoryData.csv', "r") as fileInput:
            reader = csv.reader(fileInput)
            lines = []
            for line in reader:
                if (self.parent.treeWidget.selectedItems()[0].text(0) == line[0]):
                    lines.append(line[2])
        splitted = lines[0].split(";")
        onlyname = []
        for i in range(len(splitted) - 1):
            onlyname = splitted[i].split("/")
            self.comboBox.addItem(onlyname[len(onlyname) - 1])

    def accept(self):

        def calculateTime(file):
            dirPath2 = "../Inputs/" + file
            f = open(dirPath2)
            csv_f = csv.reader(f)
            data = []
            count = 0
            for row in csv_f:
                data.append(row[0].split()[0])
                count += 1
            f.close()
            delta = int(data[-1]) - int(data[0])
            return delta

        for i in self.parent.idArray:
            entry = []
            entry.append(i)
            entry.append(self.comboBox.currentText())
            print(i)
            with open('../res/csv_files/eventHC.csv', mode='a') as device_data:
                device_writer = csv.writer(device_data, delimiter=',')
                device_writer.writerow(entry)
                icon = QIcon("../res/GUI/images/icons8-checkmark-80")
                item = self.grandparent.treeWidget_2.findItems(i, Qt.MatchExactly | Qt.MatchRecursive, 1)
                item[0].setIcon(3, icon)
                item[0].setText(3, "  ")
        self.grandparent.showLoads()
        self.parent.close()
        self.parent.parent.close()
        self.close()



class heaterCoolerSingle(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(heaterCoolerSingle, self).__init__(parent)
        uic.loadUi('../res/GUI/heatercooler.ui', self)
        self.parent = parent

        with open('../res/csv_files/deviceRepositoryData.csv', "r") as fileInput:
            reader = csv.reader(fileInput)
            lines = []
            for line in reader:
                if (self.parent.treeWidget_2.selectedItems()[0].text(0) == line[0]):
                    lines.append(line[2])
        splitted = lines[0].split(";")
        onlyname = []
        for i in range(len(splitted) - 1):
            onlyname = splitted[i].split("/")
            self.comboBox.addItem(onlyname[len(onlyname) - 1])

    def accept(self):

        def calculateTime(file):
            dirPath2 = "../Inputs/" + file
            f = open(dirPath2)
            csv_f = csv.reader(f)
            data = []
            count = 0
            for row in csv_f:
                data.append(row[0].split()[0])
                count += 1
            f.close()
            delta = int(data[-1]) - int(data[0])
            return delta

        entry = []
        entry.append(self.parent.treeWidget_2.selectedItems()[0].text(1))
        entry.append(self.comboBox.currentText())
        with open('../res/csv_files/eventHC.csv', mode='a') as device_data:
            device_writer = csv.writer(device_data, delimiter=',')
            device_writer.writerow(entry)
            icon = QIcon("../res/GUI/images/icons8-checkmark-80")
            self.parent.treeWidget_2.selectedItems()[0].setIcon(3, icon)
            self.parent.treeWidget_2.selectedItems()[0].setText(3, "  ")
        self.parent.showLoads()
        self.close()




class selectTypeDevice(QtWidgets.QDialog):
        def __init__(self, parent = None):
            super(selectTypeDevice,self).__init__(parent)
            uic.loadUi('../res/GUI/selecttype.ui', self)
            self.type = 0
            self.parent = parent

        def accept(self):
            if(self.general_radio.isChecked()):
                self.type = 1
            elif(self.radioButton.isChecked()):
                self.type = 2
            elif(self.radioButton_2.isChecked()):
                self.type = 3
            elif (self.radioButton_3.isChecked()):
                self.type = 4
            else:
                self.type = 0
            self.dialog = selectDevices(self)
            self.dialog.show()


class selectDevices(QtWidgets.QDialog):
        def __init__(self, parent = None):
            super(selectDevices,self).__init__(parent)
            self.idArray = []
            uic.loadUi('../res/GUI/selectdevices.ui', self)
            stop = False
            stop0 = False
            stop2 = False
            stop3 = False
            self.parent = parent
            self.parser = ET.XMLParser(remove_blank_text=True)
            if(parent.type == 1):
                self.treeWidget.clear()
                with open("../xml/buildingNeighborhood.xml", 'r') as filename:
                            with open("../xml/buildingDevice.xml", 'w') as outf:
                                reader = filename.readlines()
                                for line in reader:
                                    if "<ecar>" in line:
                                        stop = True
                                    if "<battery>" in line:
                                        stop0 = True
                                    if "<heatercooler>" in line:
                                        stop2 = True
                                    if "<backgroundload>" in line:
                                        stop3 = True
                                    if (stop == False and stop0 == False and stop2 == False and stop3 == False):
                                        outf.write(line)
                                    if "</ecar>" in line:
                                        stop = False
                                    if "</battery>" in line:
                                        stop0 = False
                                    if "</heatercooler>" in line:
                                        stop2 = False
                                    if "</backgroundload>" in line:
                                        stop3 = False
                with open("../xml/buildingDevice.xml", 'r') as myfile:
                    self.xml = myfile.read()
                self.treeWidget.setHeaderLabels(['Title','id', 'Type'])
                self.source = QtXml.QXmlInputSource()
                self.source.setData(self.xml)
                handler = sC.XmlHandler(self.treeWidget)
                reader = QtXml.QXmlSimpleReader()
                reader.setContentHandler(handler)
                reader.setErrorHandler(handler)
                self.source.setData(self.xml)
                reader.parse(self.source)
                self.treeWidget.resizeColumnToContents(0)
                self.treeWidget.resizeColumnToContents(1)
                self.treeWidget.resizeColumnToContents(2)
                self.treeWidget.resizeColumnToContents(3)

            if(parent.type == 0):
                self.treeWidget.clear()
                with open("../xml/buildingNeighborhood.xml", 'r') as filename:
                            with open("../xml/buildingCars.xml", 'w') as outf:
                                reader = filename.readlines()
                                for line in reader:
                                    if "<device>" in line:
                                        stop = True
                                    if "<battery>" in line:
                                        stop0 = True
                                    if "<heatercooler>" in line:
                                        stop2 = True
                                    if "<backgroundload>" in line:
                                        stop3 = True
                                    if (stop == False and stop0 == False and stop2 == False and stop3 == False):
                                        outf.write(line)
                                    if "</device>" in line:
                                        stop = False
                                    if "</battery>" in line:
                                        stop0 = False
                                    if "</heatercooler>" in line:
                                        stop2 = False
                                    if "</backgroundload>" in line:
                                        stop3 = False
                with open("../xml/buildingCars.xml", 'r') as myfile:
                    self.xml = myfile.read()
                self.treeWidget.setHeaderLabels(['Title','id', 'Type'])
                self.source = QtXml.QXmlInputSource()
                self.source.setData(self.xml)
                handler = sC.XmlHandler(self.treeWidget)
                reader = QtXml.QXmlSimpleReader()
                reader.setContentHandler(handler)
                reader.setErrorHandler(handler)
                self.source.setData(self.xml)
                reader.parse(self.source)
                self.treeWidget.resizeColumnToContents(0)
                self.treeWidget.resizeColumnToContents(1)
                self.treeWidget.resizeColumnToContents(2)
                self.treeWidget.resizeColumnToContents(3)

            if(parent.type == 2):
                self.treeWidget.clear()
                with open("../xml/buildingNeighborhood.xml", 'r') as filename:
                    with open("../xml/buildingBattery.xml", 'w') as outf:
                        reader = filename.readlines()
                        for line in reader:
                            if "<ecar>" in line:
                                stop = True
                            if "<device>" in line:
                                stop0 = True
                            if "<heatercooler>" in line:
                                stop2 = True
                            if "<backgroundload>" in line:
                                stop3 = True
                            if (stop == False and stop0 == False and stop2 == False and stop3 == False):
                                outf.write(line)
                            if "</ecar>" in line:
                                stop = False
                            if "</device>" in line:
                                stop0 = False
                            if "</heatercooler>" in line:
                                stop2 = False
                            if "</backgroundload>" in line:
                                stop3 = False
                with open("../xml/buildingBattery.xml", 'r') as myfile:
                    self.xml = myfile.read()
                self.treeWidget.setHeaderLabels(['Title', 'id', 'Type'])
                self.source = QtXml.QXmlInputSource()
                self.source.setData(self.xml)
                handler = sC.XmlHandler(self.treeWidget)
                reader = QtXml.QXmlSimpleReader()
                reader.setContentHandler(handler)
                reader.setErrorHandler(handler)
                self.source.setData(self.xml)
                reader.parse(self.source)
                self.treeWidget.resizeColumnToContents(0)
                self.treeWidget.resizeColumnToContents(1)
                self.treeWidget.resizeColumnToContents(2)
                self.treeWidget.resizeColumnToContents(3)

            if (parent.type == 3):
                self.treeWidget.clear()
                with open("../xml/buildingNeighborhood.xml", 'r') as filename:
                    with open("../xml/buildingHC.xml", 'w') as outf:
                        reader = filename.readlines()
                        for line in reader:
                            if "<ecar>" in line:
                                stop = True
                            if "<battery>" in line:
                                stop0 = True
                            if "<device>" in line:
                                stop2 = True
                            if "<backgroundload>" in line:
                                stop3 = True
                            if (stop == False and stop0 == False and stop2 == False and stop3 == False):
                                outf.write(line)
                            if "</ecar>" in line:
                                stop = False
                            if "</battery>" in line:
                                stop0 = False
                            if "</device>" in line:
                                stop2 = False
                            if "</backgroundload>" in line:
                                stop3 = False
                with open("../xml/buildingHC.xml", 'r') as myfile:
                    self.xml = myfile.read()
                self.treeWidget.setHeaderLabels(['Title', 'id', 'Type'])
                self.source = QtXml.QXmlInputSource()
                self.source.setData(self.xml)
                handler = sC.XmlHandler(self.treeWidget)
                reader = QtXml.QXmlSimpleReader()
                reader.setContentHandler(handler)
                reader.setErrorHandler(handler)
                self.source.setData(self.xml)
                reader.parse(self.source)
                self.treeWidget.resizeColumnToContents(0)
                self.treeWidget.resizeColumnToContents(1)
                self.treeWidget.resizeColumnToContents(2)
                self.treeWidget.resizeColumnToContents(3)

            if (parent.type == 4):
                self.treeWidget.clear()
                with open("../xml/buildingNeighborhood.xml", 'r') as filename:
                    with open("../xml/buildingbackground.xml", 'w') as outf:
                        reader = filename.readlines()
                        for line in reader:
                            if "<ecar>" in line:
                                stop = True
                            if "<battery>" in line:
                                stop0 = True
                            if "<heatercooler>" in line:
                                stop2 = True
                            if "<device>" in line:
                                stop3 = True
                            if (stop == False and stop0 == False and stop2 == False and stop3 == False):
                                outf.write(line)
                            if "</ecar>" in line:
                                stop = False
                            if "</battery>" in line:
                                stop0 = False
                            if "</heatercooler>" in line:
                                stop2 = False
                            if "</device>" in line:
                                stop3 = False
                with open("../xml/buildingbackground.xml", 'r') as myfile:
                    self.xml = myfile.read()
                self.treeWidget.setHeaderLabels(['Title', 'id', 'Type'])
                self.source = QtXml.QXmlInputSource()
                self.source.setData(self.xml)
                handler = sC.XmlHandler(self.treeWidget)
                reader = QtXml.QXmlSimpleReader()
                reader.setContentHandler(handler)
                reader.setErrorHandler(handler)
                self.source.setData(self.xml)
                reader.parse(self.source)
                self.treeWidget.resizeColumnToContents(0)
                self.treeWidget.resizeColumnToContents(1)
                self.treeWidget.resizeColumnToContents(2)
                self.treeWidget.resizeColumnToContents(3)



        def itemch(self):
            for i in range(len(self.treeWidget.selectedItems())):
                if(len(self.treeWidget.selectedItems())!=0):
                    if(self.treeWidget.selectedItems()[i].parent() == None):
                        self.treeWidget.selectedItems()[i].setSelected(False)


        def accept(self):
            if(len(self.treeWidget.selectedItems()) == 0):
                QMessageBox.about(self, "Error", "Error, no devices selected")
            else:
                if(self.parent.type ==1):
                    basename= self.treeWidget.selectedItems()[0].text(0)
                    raiseException = False
                    for i in range(len(self.treeWidget.selectedItems())):
                        if(basename != self.treeWidget.selectedItems()[i].text(0)):
                            raiseException = True
                    if(raiseException == False):
                        for i in range(len(self.treeWidget.selectedItems())):
                            self.idArray.append(self.treeWidget.selectedItems()[i].text(1))
                        self.dialog = addEventUiMultiple(self)
                        self.dialog.show()
                    else:
                        QMessageBox.about(self, "Error", "Please, select Devices with same name and possible loads")
                elif(self.parent.type == 2):
                    #MODIFICARE QUI APPENA ESCE LA DEFINIZIONE DEGLI ATTRIBUTI DELLA BATTERIA
                    basename = self.treeWidget.selectedItems()[0].text(0)
                    raiseException = False
                    for i in range(len(self.treeWidget.selectedItems())):
                        if (basename != self.treeWidget.selectedItems()[i].text(0)):
                            raiseException = True
                    if (raiseException == False):
                        for i in range(len(self.treeWidget.selectedItems())):
                            self.idArray.append(self.treeWidget.selectedItems()[i].text(1))
                        self.dialog = addEventUiMultiple(self)
                        self.dialog.show()
                    else:
                        QMessageBox.about(self, "Error", "Please, select Devices with same name and possible loads")
                elif (self.parent.type == 3):
                    basename = self.treeWidget.selectedItems()[0].text(0)
                    raiseException = False
                    for i in range(len(self.treeWidget.selectedItems())):
                        if (basename != self.treeWidget.selectedItems()[i].text(0)):
                            raiseException = True
                    if (raiseException == False):
                        for i in range(len(self.treeWidget.selectedItems())):
                            self.idArray.append(self.treeWidget.selectedItems()[i].text(1))
                        self.dialog = heaterCooler(self)
                        self.dialog.show()
                    else:
                        QMessageBox.about(self, "Error", "Please, select Devices with same name and possible loads")
                elif (self.parent.type == 4):
                    basename = self.treeWidget.selectedItems()[0].text(0)
                    raiseException = False
                    for i in range(len(self.treeWidget.selectedItems())):
                        if (basename != self.treeWidget.selectedItems()[i].text(0)):
                            raiseException = True
                    if (raiseException == False):
                        for i in range(len(self.treeWidget.selectedItems())):
                            self.idArray.append(self.treeWidget.selectedItems()[i].text(1))
                        self.dialog = backgroundUi(self)
                        self.dialog.show()
                    else:
                        QMessageBox.about(self, "Error", "Please, select Devices with same name and possible loads")
                else:
                    for i in range(len(self.treeWidget.selectedItems())):
                        self.idArray.append(self.treeWidget.selectedItems()[i].text(1))
                    self.dialog = ecarloadUIMultiple(self)
                    self.dialog.show()



class addEventUiMultiple(QtWidgets.QMainWindow):


        def __init__(self, parent = None):
            super(addEventUiMultiple,self).__init__(parent)
            uic.loadUi('../res/GUI/addEvent.ui', self)
            self.parent = parent
            self.grandparent = self.parent.parent.parent
            with open('../res/csv_files/deviceRepositoryData.csv', "r") as fileInput:
                    reader = csv.reader(fileInput)
                    lines =[]
                    for line in reader:
                        if(self.parent.treeWidget.selectedItems()[0].text(0)==line[0]):
                            lines.append(line[2])
            splitted = lines[0].split(";")
            onlyname = []
            for i in range(len(splitted)-1):
                onlyname = splitted[i].split("/")
                self.comboBox_2.addItem(onlyname[len(onlyname)-1])
            self.horizontalSlider.setMinimum(1)
            self.horizontalSlider.setMaximum(72)
            self.horizontalSlider.setTickInterval(1)
            self.horizontalSlider_2.setMinimum(1)
            self.horizontalSlider_2.setMaximum(72)
            self.horizontalSlider_2.setTickInterval(1)



        def checkrandomize(self):
            if(self.checkBox_2.isChecked()==True):
                self.label.setText("EST StartPoint")
                self.label_2.setText("LST StartPoint")
                self.label_3.setText("Creation_Time StartPoint")
                self.timeEdit_4.setEnabled(True)
            else:
                self.label.setText("EST")
                self.label_2.setText("LST")
                self.label_3.setText("Creation_Time")
                self.timeEdit_4.setEnabled(False)


        def valuechange(self):
            ore = self.horizontalSlider.value()*10//60
            minuti = self.horizontalSlider.value()*10%60
            newtime = QtCore.QTime(ore,minuti,0)
            self.timeEdit_5.setTime(newtime)

        def valuechange2(self):
            ore = self.horizontalSlider_2.value()*10//60
            minuti = self.horizontalSlider_2.value()*10%60
            newtime = QtCore.QTime(ore,minuti,0)
            self.timeEdit_4.setTime(newtime)
            #self.lineEdit_4.setText(str(ore) + ":" + str(minuti))

        def submitEvent(self):

            def calculateTime(file):
                dirPath2 = "../Inputs/"+file
                f = open(dirPath2)
                csv_f = csv.reader(f)
                data = []
                count=0
                for row in csv_f:
                    data.append(row[0].split()[0])
                    count+=1
                f.close()
                delta = int(data[-1]) - int(data[0])
                return delta

            if(self.checkBox_2.isChecked()==True):
                interval = self.timeEdit_4.time().toString()
                hour = interval.split(":")[0]
                minutes = interval.split(":")[1]
                interval = int(hour)*60 + int(minutes)
                rand = random.randrange(0,interval,1)
                if(rand<0):
                    rand = rand*(-1)
                    hour = int(rand/60)
                    minutes = rand%60

                    hourEST = int(self.timeEdit_3.time().toString().split(":")[0])
                    minuteEST =  int(self.timeEdit_3.time().toString().split(":")[1])
                    minuteESTfinal = minuteEST - minutes
                    if(minuteESTfinal <0):
                        report = -1
                        minuteESTfinal = 60 + minuteESTfinal
                    else:
                        report = 0
                    hourESTfinal = hourEST - hour + report
                    if(hourESTfinal < 0):
                        newtime = QtCore.QTime(0,0,0)
                        self.timeEdit_3.setTime(newtime)
                    else:
                        newtime = QtCore.QTime(hourESTfinal, minuteESTfinal, 0)
                        self.timeEdit_3.setTime(newtime)


                    hourLST = int(self.timeEdit.time().toString().split(":")[0])
                    minuteLST =  int(self.timeEdit.time().toString().split(":")[1])
                    minuteLSTfinal = minuteLST - minutes

                    if(minuteLSTfinal <0):
                        report = -1
                        minuteLSTfinal = 60 + minuteLSTfinal
                    else:
                        report = 0
                    hourLSTfinal = hourLST - hour + report
                    if(hourLSTfinal < 0):
                        newtime = QtCore.QTime(0,0,0)
                        self.timeEdit.setTime(newtime)
                    else:
                        newtime = QtCore.QTime(hourLSTfinal, minuteLSTfinal, 0)
                        self.timeEdit.setTime(newtime)


                    hourCT = int(self.timeEdit_2.time().toString().split(":")[0])
                    minuteCT =  int(self.timeEdit_2.time().toString().split(":")[1])
                    minuteCTfinal = minuteCT - minutes

                    if(minuteCTfinal <0):
                        report = -1
                        minuteCTfinal = 60 + minuteCTfinal
                    else:
                        report = 0
                    hourCTfinal = hourCT - hour + report
                    if(hourCTfinal < 0):
                        newtime = QtCore.QTime(0,0,0)
                        self.timeEdit_2.setTime(newtime)
                    else:
                        newtime = QtCore.QTime(hourCTfinal, minuteCTfinal, 0)
                        self.timeEdit_2.setTime(newtime)

                else:
                    hour = int(rand/60)
                    minutes = rand%60
                    hourEST = int(self.timeEdit_3.time().toString().split(":")[0])
                    minuteEST =  int(self.timeEdit_3.time().toString().split(":")[1])
                    minuteESTfinal = minuteEST + minutes
                    if(minuteESTfinal > 60):
                        report = +1
                        minuteESTfinal =  minuteESTfinal - 60
                    else:
                        report = 0
                    hourESTfinal = hourEST + hour + report
                    if(hourESTfinal >= 24):
                        newtime = QtCore.QTime(23,59,0)
                        self.timeEdit_3.setTime(newtime)
                    else:
                        newtime = QtCore.QTime(hourESTfinal, minuteESTfinal, 0)
                        self.timeEdit_3.setTime(newtime)


                    hourLST = int(self.timeEdit.time().toString().split(":")[0])
                    minuteLST =  int(self.timeEdit.time().toString().split(":")[1])
                    minuteLSTfinal = minuteLST + minutes

                    if(minuteLSTfinal >60):
                        report = +1
                        minuteLSTfinal = minuteLSTfinal -60
                    else:
                        report = 0
                    hourLSTfinal = hourLST + hour + report
                    if(hourLSTfinal >=24 ):
                        newtime = QtCore.QTime(23,59,0)
                        self.timeEdit.setTime(newtime)
                    else:
                        newtime = QtCore.QTime(hourLSTfinal, minuteLSTfinal, 0)
                        self.timeEdit.setTime(newtime)


                    hourCT = int(self.timeEdit_2.time().toString().split(":")[0])
                    minuteCT =  int(self.timeEdit_2.time().toString().split(":")[1])
                    minuteCTfinal = minuteCT + minutes

                    if(minuteCTfinal >60):
                        report = +1
                        minuteCTfinal =  minuteCTfinal-60
                    else:
                        report = 0
                    hourCTfinal = hourCT + hour + report
                    if(hourCTfinal >=24):
                        newtime = QtCore.QTime(23,59,0)
                        self.timeEdit_2.setTime(newtime)
                    else:
                        newtime = QtCore.QTime(hourCTfinal, minuteCTfinal, 0)
                        self.timeEdit_2.setTime(newtime)

            else:
                None
            for i in self.parent.idArray:
                entry = []
                entry.append(i)
                entry.append(self.timeEdit_3.time().toString())
                entry.append(self.timeEdit.time().toString())
                entry.append(self.timeEdit_2.time().toString())
                entry.append(self.comboBox_2.currentText())

                with open('../res/csv_files/eventLoad.csv', mode='a') as device_data:
                        device_writer = csv.writer(device_data, delimiter=',')
                        device_writer.writerow(entry)
                        icon = QIcon("../res/GUI/images/icons8-checkmark-80")
                        item = self.grandparent.treeWidget_2.findItems(i, Qt.MatchExactly | Qt.MatchRecursive, 1)
                        item[0].setIcon(3,icon)
                        item[0].setText(3, "  ")


                if(self.checkBox.isChecked()):
                    start = (86400 - int(self.timeEdit_3.time().toString().split(":")[0])*60*60 - int(self.timeEdit_3.time().toString().split(":")[1])*60)
                    delta = (int(self.timeEdit_5.time().toString().split(":")[0])*60*60 + int(self.timeEdit_5.time().toString().split(":")[1])*60)
                    triptime = calculateTime(self.comboBox_2.currentText()[:-1])
                    numIter = 0
                    while(start >0):
                        start = start - delta - triptime
                        if(start>=0):
                            numIter +=1
                    for n in range(1,numIter):
                        entry = []
                        entry.append(self.parent.treeWidget_2.selectedItems()[0].text(1))
                        est = int (self.timeEdit_3.time().toString().split(":")[0])*60*60 + int(self.timeEdit_3.time().toString().split(":")[1])*60 + n*(delta+triptime)
                        entry.append(str(datetime.timedelta(seconds=est)))
                        lst = int(self.timeEdit.time().toString().split(":")[0])*60*60 + + int(self.timeEdit.time().toString().split(":")[1])*60 + n*(delta+triptime)
                        entry.append(str(datetime.timedelta(seconds=lst)))
                        entry.append(self.timeEdit_2.time().toString())
                        entry.append(self.comboBox_2.currentText())

                        with open('../res/csv_files/eventLoad.csv', mode='a') as device_data:
                                device_writer = csv.writer(device_data, delimiter=',')
                                device_writer.writerow(entry)

            self.grandparent.showLoads()
            self.parent.close()
            self.parent.parent.close()
            self.close()

        def checkDelta(self):
            if(self.checkBox.isChecked()==True):
                self.horizontalSlider.setEnabled(True)
                self.timeEdit_5.setEnabled(True)
            else:
                self.horizontalSlider.setEnabled(False)
                self.timeEdit_5.setEnabled(False)


class ecarloadUIMultiple(QtWidgets.QMainWindow):


        def __init__(self, parent = None):
            super(ecarloadUIMultiple,self).__init__(parent)
            uic.loadUi('../res/GUI/ecarload.ui', self)
            self.parent = parent
            self.grandparent = self.parent.parent.parent

        def submitEcarLoad(self):
                for i in self.parent.idArray:
                    entry = []
                    entry.append(i)
                    entry.append(self.timeEdit_7.time().toString())
                    entry.append(self.timeEdit_8.time().toString())
                    entry.append(self.timeEdit_2.time().toString())
                    entry.append(self.timeEdit_3.time().toString())
                    entry.append(self.timeEdit.time().toString())
                    entry.append(str(self.spinBox.value()))
                    entry.append(str(self.spinBox_2.value()))
                    entry.append(str(self.spinBox_3.value()))
                    if (self.checkBox_4.isChecked()):
                        entry.append("1")
                    else:
                        entry.append("0")
                    with open('../res/csv_files/eCarLoad.csv', mode='a') as device_data:
                        device_writer = csv.writer(device_data, delimiter=',')
                        device_writer.writerow(entry)
                        icon = QIcon("../res/GUI/images/icons8-checkmark-80")
                        self.parent.treeWidget_2.selectedItems()[0].setIcon(3, icon)
                        self.parent.treeWidget_2.selectedItems()[0].setText(3, "  ")
                    self.parent.showLoads()
                    self.close()

        def createAnEcar(self):
            self.dialog = createEcar(self)
            self.dialog.show()


        def changeModel(self):
            try:
                with open('../res/csv_files/eCarModels.csv', mode='r') as device_data:
                        for line in device_data:
                            name = line.split(',')[0]
                            V2G = line.split(',')[11]
                            if(name==self.comboBox_4.currentText()):
                                if(int(V2G)==1):
                                    self.checkBox_4.setEnabled(True)
                                else:
                                    self.checkBox_4.setEnabled(False)
            except:
                None


class ecarloadUI(QtWidgets.QMainWindow):


        def __init__(self, parent = None):
            super(ecarloadUI,self).__init__(parent)
            uic.loadUi('../res/GUI/ecarload.ui', self)
            root = parent.tree.getroot()
            self.parent = parent

        def submitEcarLoad(self):
                entry = []
                entry.append(self.parent.treeWidget_2.selectedItems()[0].text(1))
                entry.append(self.timeEdit_7.time().toString())
                entry.append(self.timeEdit_8.time().toString())
                entry.append(self.timeEdit_2.time().toString())
                entry.append(self.timeEdit_3.time().toString())
                entry.append(self.timeEdit.time().toString())
                entry.append(str(self.spinBox.value()))
                entry.append(str(self.spinBox_2.value()))
                entry.append(str(self.spinBox_3.value()))
                if(self.checkBox_4.isChecked()):
                    entry.append("1")
                else:
                    entry.append("0")
                with open('../res/csv_files/eCarLoad.csv', mode='a') as device_data:
                        device_writer = csv.writer(device_data, delimiter=',')
                        device_writer.writerow(entry)
                        icon = QIcon("../res/GUI/images/icons8-checkmark-80")
                        self.parent.treeWidget_2.selectedItems()[0].setIcon(3,icon)
                        self.parent.treeWidget_2.selectedItems()[0].setText(3, "  ")
                self.parent.showLoads()
                self.close()

        def createAnEcar(self):
            self.dialog = createEcar(self)
            self.dialog.show()


        def changeModel(self):
            try:
                with open('../res/csv_files/eCarModels.csv', mode='r') as device_data:
                        for line in device_data:
                            name = line.split(',')[0]
                            V2G = line.split(',')[11]
                            if(name==self.comboBox_4.currentText()):
                                if(int(V2G)==1):
                                    self.checkBox_4.setEnabled(True)
                                else:
                                    self.checkBox_4.setEnabled(False)
            except:
                None


class ModifyecarloadUI(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(ecarloadUI, self).__init__(parent)
        uic.loadUi('../res/GUI/ecarload.ui', self)
        root = parent.tree.getroot()
        self.parent = parent
        self.updateList()
        self.changeModel()

    def submitEcarLoad(self):
        entry = []
        entry.append(self.parent.treeWidget_2.selectedItems()[0].text(1))
        entry.append(self.timeEdit_7.time().toString())
        entry.append(self.timeEdit_8.time().toString())
        entry.append(self.timeEdit_2.time().toString())
        entry.append(self.timeEdit_3.time().toString())
        entry.append(self.timeEdit.time().toString())
        entry.append(self.comboBox_4.currentText())
        entry.append(str(self.spinBox.value()))
        entry.append(str(self.spinBox_2.value()))
        entry.append(str(self.spinBox_3.value()))
        with open('../res/csv_files/eCarModels.csv', mode='r') as device_data:
            for line in device_data:
                name = line.split(',')[0]
                if (name == self.comboBox_4.currentText()):
                    entry.append(line.split(',')[1])
                    entry.append(line.split(',')[2])
                    entry.append(line.split(',')[3])
                    entry.append(line.split(',')[4])
                    entry.append(line.split(',')[5])
                    entry.append(line.split(',')[6])
                    entry.append(line.split(',')[7])
                    entry.append(line.split(',')[8])
                    entry.append(line.split(',')[9])
                    entry.append(line.split(',')[10])

        if (self.checkBox_4.isChecked()):
            entry.append("1")
        else:
            entry.append("0")
        with open('../res/csv_files/eCarLoad.csv', mode='a') as device_data:
            device_writer = csv.writer(device_data, delimiter=',')
            device_writer.writerow(entry)
            icon = QIcon("../res/GUI/images/icons8-checkmark-80")
            self.parent.treeWidget_2.selectedItems()[0].setIcon(3, icon)
            self.parent.treeWidget_2.selectedItems()[0].setText(3, "  ")
        self.parent.showLoads()
        self.close()

    def createAnEcar(self):
        self.dialog = createEcar(self)
        self.dialog.show()

    def updateList(self):
        self.comboBox_4.clear()
        try:
            with open('../res/csv_files/eCarModels.csv', mode='r') as device_data:
                for line in device_data:
                    name = line.split(',')[0]
                    self.comboBox_4.addItem(name)
        except:
            None

    def changeModel(self):
        try:
            with open('../res/csv_files/eCarModels.csv', mode='r') as device_data:
                for line in device_data:
                    name = line.split(',')[0]
                    V2G = line.split(',')[11]
                    if (name == self.comboBox_4.currentText()):
                        if (int(V2G) == 1):
                            self.checkBox_4.setEnabled(True)
                        else:
                            self.checkBox_4.setEnabled(False)
        except:
            None





































class createEcar(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
            super(createEcar,self).__init__(parent)
            self.parent=parent
            uic.loadUi('../res/GUI/dialog.ui', self)
            #self.close()

    def accept(self):
            validator = True
            if(self.lineEdit.text() == ""):
                QMessageBox.about(self, "Error", "Please, give a name to E-Car Model")
                validator = False
            try:
                with open('../res/csv_files/eCarModels.csv', mode='r') as device_data:
                        for line in device_data:
                            name = line.split(',')[0]
                            if (name == self.lineEdit.text()):
                                QMessageBox.about(self, "Error", "Model already exist. Please Change Model Name")
                                validator = False
                                break
            except:
                None
            if(validator == True):
                entry = []
                entry.append(self.lineEdit.text())
                entry.append(str(self.spinBox.value()))
                entry.append(str(self.spinBox_2.value()))
                entry.append(str(self.spinBox_3.value()))
                entry.append(str(self.spinBox_4.value()))
                entry.append(str(self.spinBox_5.value()))
                entry.append(str(self.spinBox_6.value()))
                entry.append(str(self.doubleSpinBox.value()))
                entry.append(str(self.doubleSpinBox_2.value()))
                entry.append(str(self.doubleSpinBox_3.value()))
                entry.append(str(self.doubleSpinBox_4.value()))
                if(self.checkBox_2.isChecked()):
                    entry.append("1")
                else:
                    entry.append("0")

                with open('../res/csv_files/eCarModels.csv', mode='a') as device_data:
                        device_writer = csv.writer(device_data, delimiter=',')
                        device_writer.writerow(entry)
                self.parent.updateList()
                self.close()

    def reject(self):
        self.close()



class deviceUi(QtWidgets.QMainWindow):


        def __init__(self, parent = None):
            super(deviceUi,self).__init__(parent)
            self.parent=parent
            uic.loadUi('../res/GUI/deviceWindows.ui', self)
            self.updateTable()

        def updateTable(self):
            try:
                with open('../res/csv_files/deviceRepositoryData.csv', "r") as fileInput:
                    self.tableWidget.setRowCount(0)
                    for row_number, row_data in enumerate(csv.reader(fileInput)):
                        self.tableWidget.insertRow(row_number)
                        for column_number, column_data in enumerate(row_data):
                            self.tableWidget.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(column_data))
                self.tableWidget.resizeColumnsToContents()
                self.tableWidget.resizeRowsToContents()

            except IOError:
                None
        def addDeviceWindow(self):
            self.dialog = createDeviceUi(self)
            self.dialog.show()


        def selectedDevice(self):
            selected = self.tableWidget.currentRow()
            self.parent.selectedDevice = []
            for i in range(self.tableWidget.columnCount()):
                tring = self.tableWidget.item(selected,i).text()
                self.parent.selectedDevice.append(tring)
            self.parent.lineEdit.setText(self.parent.selectedDevice[0])
            self.close()


        def removeFromPreset(self):
            selected = self.tableWidget.currentRow()
            try:
                with open('../res/csv_files/deviceRepositoryData.csv', "r") as fileInput:
                    reader = csv.reader(fileInput)
                    lines =[]
                    for line in reader:
                        lines.append(line)

                    with open('../res/csv_files/deviceRepositoryData.csv', mode='w') as device_data:
                        for i,line in enumerate(lines):
                            if (i != selected):
                                device_writer = csv.writer(device_data, delimiter=',')
                                device_writer.writerow(line)
                self.updateTable()
            except IOError:
                None

class createDeviceUi(QtWidgets.QMainWindow):


        def __init__(self, parent = None):
            super(createDeviceUi,self).__init__(parent)
            uic.loadUi('../res/GUI/addDevice.ui', self)
            self.count = 0
            self.parent = parent
            self.comboBox.addItem("Producer")
            self.comboBox.addItem("Consumer")
            self.comboBox.addItem("Prosumer")
            self.comboBox_2.addItem("EV")
            self.comboBox_2.addItem("Panel")
            self.comboBox_2.addItem("General Device")
            self.comboBox_2.addItem("Battery")
            self.comboBox_2.addItem("Heater/Cooler")
            self.comboBox_2.addItem("Background Load")

        def createEcar(self):
            self.dialog = createEcar(self)
            self.dialog.show()

        def addDeviceAction(self):
                entry =  []
                entry.append(self.lineEdit.text())
                if self.comboBox_2.currentText() == "EV":
                    entry.append("Prosumer")
                else:
                    entry.append(self.comboBox.currentText())
                csvString = ""

                if self.comboBox_2.currentText() == "EV":
                    entry.append(self.comboBox.currentText())
                    entry.append("Ecar")
                elif self.comboBox_2.currentText() == "Heater/Cooler":
                    for index in range(self.listWidget.count()):
                        csvString = csvString + self.listWidget.item(index).text() + " ; "
                    entry.append(csvString)
                    entry.append("Heater/Cooler")
                elif self.comboBox_2.currentText() == "Background Load":
                    for index in range(self.listWidget.count()):
                        csvString = csvString + self.listWidget.item(index).text() + " ; "
                    entry.append(csvString)
                    entry.append("Background Load")
                elif self.comboBox_2.currentText() == "Battery":
                    for index in range(self.listWidget.count()):
                        csvString = csvString + self.listWidget.item(index).text() + " ; "
                    entry.append(csvString)
                    entry.append("Battery")
                else:
                    for index in range(self.listWidget.count()):
                        csvString = csvString + self.listWidget.item(index).text()+ " ; "
                    entry.append(csvString)
                    entry.append("General Device")
                with open('../res/csv_files/deviceRepositoryData.csv', mode='a') as device_data:
                    device_writer = csv.writer(device_data, delimiter=',')
                    device_writer.writerow(entry)
                self.parent.updateTable()
                self.close()

        def isEcar(self):
            if self.comboBox_2.currentText() == "EV":
                self.listWidget.setEnabled(False)
                self.pushButton.setEnabled(False)
                self.label_4.setText("eCar Model")
                self.updateList()

            elif self.comboBox_2.currentText() == "Panel":
                self.listWidget.setEnabled(True)
                self.pushButton.setEnabled(True)
                self.comboBox.clear()
                self.label_4.setText("Type")
                self.comboBox.addItem("Producer")
            elif self.comboBox_2.currentText() == "Heater/Cooler":
                self.listWidget.setEnabled(True)
                self.pushButton.setEnabled(True)
                self.label_4.setText("Type")
                self.comboBox.clear()
                self.comboBox.addItem("NS-Consumer")
            elif self.comboBox_2.currentText() == "Background Load":
                self.listWidget.setEnabled(True)
                self.pushButton.setEnabled(True)
                self.comboBox.clear()
                self.label_4.setText("Type")
                self.comboBox.addItem("NS-Consumer")
            elif self.comboBox_2.currentText() == "Battery":
                self.listWidget.setEnabled(True)
                self.pushButton.setEnabled(True)
                self.label_4.setText("Type")
                self.comboBox.clear()
                self.comboBox.addItem("Prosumer")
            else:
                self.listWidget.setEnabled(True)
                self.pushButton.setEnabled(True)
                self.label_4.setText("Type")
                self.comboBox.clear()
                self.comboBox.addItem("Consumer")

        def updateList(self):
            self.comboBox.clear()
            try:
                with open('../res/csv_files/eCarModels.csv', mode='r') as device_data:
                    for line in device_data:
                        name = line.split(',')[0]
                        self.comboBox.addItem(name)
            except:
                None

        def loadProfile(self):
            filter2 = "csv(*.csv)"
            filename = QFileDialog.getOpenFileName(self, 'Open profile.csv File', '../Inputs/',filter = filter2)
            if filename[0]:
                try:
                    copy2(filename[0],"../Inputs/")
                except:
                    None
                filename = "../Inputs/"+filename[0].split("/")[len(filename[0].split("/"))-1]
                item = QListWidgetItem(filename)
                self.listWidget.addItem(item)


class houseUi(QtWidgets.QMainWindow):


        def __init__(self, parent = None):
            super(houseUi,self).__init__(parent)
            uic.loadUi('../res/GUI/HouseAndStationSelectionScreen.ui', self)
            root = parent.tree.getroot()
            self.parent = parent
            for house in root:
                #item = QListWidgetItem(house.tag+" "+house.attrib['id'])
                self.houseListView.addItem(house.tag+" "+house.attrib['id'])

        def createHouseVector(self):
            self.parent.houseVector = []
            for item in self.houseListView.selectedItems():
                self.parent.houseVector.append(item.text())
            self.close()


class addEventUi(QtWidgets.QMainWindow):


        def __init__(self, parent = None):
            super(addEventUi,self).__init__(parent)
            uic.loadUi('../res/GUI/addEvent.ui', self)
            root = parent.tree.getroot()
            self.parent = parent
            with open('../res/csv_files/deviceRepositoryData.csv', "r") as fileInput:
                    reader = csv.reader(fileInput)
                    lines =[]
                    for line in reader:
                        if(self.parent.treeWidget_2.selectedItems()[0].text(0)==line[0]):
                            lines.append(line[2])
                            if(line[1]=="Producer"):
                                self.timeEdit_3.setEnabled(False)
                                self.timeEdit.setEnabled(False)
                                self.checkBox.setEnabled(False)
                                self.horizontalSlider.setEnabled(False)
                                self.timeEdit_5.setEnabled(False)
                                self.checkBox_2.setEnabled(False)
                                self.horizontalSlider_2.setEnabled(False)
                                self.timeEdit_4.setEnabled(False)


            splitted = lines[0].split(";")
            onlyname = []
            for i in range(len(splitted)-1):
                onlyname = splitted[i].split("/")
                self.comboBox_2.addItem(onlyname[len(onlyname)-1])
            self.horizontalSlider.setMinimum(1)
            self.horizontalSlider.setMaximum(72)
            self.horizontalSlider.setTickInterval(1)
            self.horizontalSlider_2.setMinimum(1)
            self.horizontalSlider_2.setMaximum(72)
            self.horizontalSlider_2.setTickInterval(1)



        def checkrandomize(self):
            if(self.checkBox_2.isChecked()==True):
                self.label.setText("EST StartPoint")
                self.label_2.setText("LST StartPoint")
                self.label_3.setText("Creation_Time StartPoint")
                self.timeEdit_4.setEnabled(True)
            else:
                self.label.setText("EST")
                self.label_2.setText("LST")
                self.label_3.setText("Creation_Time")
                self.timeEdit_4.setEnabled(False)


        def valuechange(self):
            ore = self.horizontalSlider.value()*10//60
            minuti = self.horizontalSlider.value()*10%60
            newtime = QtCore.QTime(ore,minuti,0)
            self.timeEdit_5.setTime(newtime)

        def valuechange2(self):
            ore = self.horizontalSlider_2.value()*10//60
            minuti = self.horizontalSlider_2.value()*10%60
            newtime = QtCore.QTime(ore,minuti,0)
            self.timeEdit_4.setTime(newtime)
            #self.lineEdit_4.setText(str(ore) + ":" + str(minuti))

        def submitEvent(self):

            def calculateTime(file):
                dirPath2 = "../Inputs/"+file
                f = open(dirPath2)
                csv_f = csv.reader(f)
                data = []
                count=0
                for row in csv_f:
                    data.append(row[0].split()[0])
                    count+=1
                f.close()
                delta = int(data[-1]) - int(data[0])
                return delta

            if(self.checkBox_2.isChecked()==True):
                interval = self.timeEdit_4.time().toString()
                hour = interval.split(":")[0]
                minutes = interval.split(":")[1]
                interval = int(hour)*60 + int(minutes)
                rand = random.randrange(0,interval,1)
                if(rand<0):
                    rand = rand*(-1)
                    hour = int(rand/60)
                    minutes = rand%60

                    hourEST = int(self.timeEdit_3.time().toString().split(":")[0])
                    minuteEST =  int(self.timeEdit_3.time().toString().split(":")[1])
                    minuteESTfinal = minuteEST - minutes
                    if(minuteESTfinal <0):
                        report = -1
                        minuteESTfinal = 60 + minuteESTfinal
                    else:
                        report = 0
                    hourESTfinal = hourEST - hour + report
                    if(hourESTfinal < 0):
                        newtime = QtCore.QTime(0,0,0)
                        self.timeEdit_3.setTime(newtime)
                    else:
                        newtime = QtCore.QTime(hourESTfinal, minuteESTfinal, 0)
                        self.timeEdit_3.setTime(newtime)


                    hourLST = int(self.timeEdit.time().toString().split(":")[0])
                    minuteLST =  int(self.timeEdit.time().toString().split(":")[1])
                    minuteLSTfinal = minuteLST - minutes

                    if(minuteLSTfinal <0):
                        report = -1
                        minuteLSTfinal = 60 + minuteLSTfinal
                    else:
                        report = 0
                    hourLSTfinal = hourLST - hour + report
                    if(hourLSTfinal < 0):
                        newtime = QtCore.QTime(0,0,0)
                        self.timeEdit.setTime(newtime)
                    else:
                        newtime = QtCore.QTime(hourLSTfinal, minuteLSTfinal, 0)
                        self.timeEdit.setTime(newtime)


                    hourCT = int(self.timeEdit_2.time().toString().split(":")[0])
                    minuteCT =  int(self.timeEdit_2.time().toString().split(":")[1])
                    minuteCTfinal = minuteCT - minutes

                    if(minuteCTfinal <0):
                        report = -1
                        minuteCTfinal = 60 + minuteCTfinal
                    else:
                        report = 0
                    hourCTfinal = hourCT - hour + report
                    if(hourCTfinal < 0):
                        newtime = QtCore.QTime(0,0,0)
                        self.timeEdit_2.setTime(newtime)
                    else:
                        newtime = QtCore.QTime(hourCTfinal, minuteCTfinal, 0)
                        self.timeEdit_2.setTime(newtime)

                else:
                    hour = int(rand/60)
                    minutes = rand%60
                    hourEST = int(self.timeEdit_3.time().toString().split(":")[0])
                    minuteEST =  int(self.timeEdit_3.time().toString().split(":")[1])
                    minuteESTfinal = minuteEST + minutes
                    if(minuteESTfinal > 60):
                        report = +1
                        minuteESTfinal =  minuteESTfinal - 60
                    else:
                        report = 0
                    hourESTfinal = hourEST + hour + report
                    if(hourESTfinal >= 24):
                        newtime = QtCore.QTime(23,59,0)
                        self.timeEdit_3.setTime(newtime)
                    else:
                        newtime = QtCore.QTime(hourESTfinal, minuteESTfinal, 0)
                        self.timeEdit_3.setTime(newtime)


                    hourLST = int(self.timeEdit.time().toString().split(":")[0])
                    minuteLST =  int(self.timeEdit.time().toString().split(":")[1])
                    minuteLSTfinal = minuteLST + minutes

                    if(minuteLSTfinal >60):
                        report = +1
                        minuteLSTfinal = minuteLSTfinal -60
                    else:
                        report = 0
                    hourLSTfinal = hourLST + hour + report
                    if(hourLSTfinal >=24 ):
                        newtime = QtCore.QTime(23,59,0)
                        self.timeEdit.setTime(newtime)
                    else:
                        newtime = QtCore.QTime(hourLSTfinal, minuteLSTfinal, 0)
                        self.timeEdit.setTime(newtime)


                    hourCT = int(self.timeEdit_2.time().toString().split(":")[0])
                    minuteCT =  int(self.timeEdit_2.time().toString().split(":")[1])
                    minuteCTfinal = minuteCT + minutes

                    if(minuteCTfinal >60):
                        report = +1
                        minuteCTfinal =  minuteCTfinal-60
                    else:
                        report = 0
                    hourCTfinal = hourCT + hour + report
                    if(hourCTfinal >=24):
                        newtime = QtCore.QTime(23,59,0)
                        self.timeEdit_2.setTime(newtime)
                    else:
                        newtime = QtCore.QTime(hourCTfinal, minuteCTfinal, 0)
                        self.timeEdit_2.setTime(newtime)

            else:
                None

            entry = []
            entry.append(self.parent.treeWidget_2.selectedItems()[0].text(1))
            entry.append(self.timeEdit_3.time().toString())
            entry.append(self.timeEdit.time().toString())
            entry.append(self.timeEdit_2.time().toString())
            entry.append(self.comboBox_2.currentText())

            with open('../res/csv_files/eventLoad.csv', mode='a') as device_data:
                    device_writer = csv.writer(device_data, delimiter=',')
                    device_writer.writerow(entry)
                    icon = QIcon("../res/GUI/images/icons8-checkmark-80")
                    self.parent.treeWidget_2.selectedItems()[0].setIcon(3,icon)
                    self.parent.treeWidget_2.selectedItems()[0].setText(3, "  ")


            if(self.checkBox.isChecked()):
                start = (86400 - int(self.timeEdit_3.time().toString().split(":")[0])*60*60 - int(self.timeEdit_3.time().toString().split(":")[1])*60)
                delta = (int(self.timeEdit_5.time().toString().split(":")[0])*60*60 + int(self.timeEdit_5.time().toString().split(":")[1])*60)
                triptime = calculateTime(self.comboBox_2.currentText()[:-1])
                numIter = 0
                while(start >0):
                    start = start - delta - triptime
                    if(start>=0):
                        numIter +=1
                for n in range(1,numIter):
                    entry = []
                    entry.append(self.parent.treeWidget_2.selectedItems()[0].text(1))
                    est = int (self.timeEdit_3.time().toString().split(":")[0])*60*60 + int(self.timeEdit_3.time().toString().split(":")[1])*60 + n*(delta+triptime)
                    entry.append(str(datetime.timedelta(seconds=est)))
                    lst = int(self.timeEdit.time().toString().split(":")[0])*60*60 + + int(self.timeEdit.time().toString().split(":")[1])*60 + n*(delta+triptime)
                    entry.append(str(datetime.timedelta(seconds=lst)))
                    entry.append(self.timeEdit_2.time().toString())
                    entry.append(self.comboBox_2.currentText())

                    with open('../res/csv_files/eventLoad.csv', mode='a') as device_data:
                            device_writer = csv.writer(device_data, delimiter=',')
                            device_writer.writerow(entry)



            self.parent.showLoads()
            self.close()

        def checkDelta(self):
            if(self.checkBox.isChecked()==True):
                self.horizontalSlider.setEnabled(True)
                self.timeEdit_5.setEnabled(True)
            else:
                self.horizontalSlider.setEnabled(False)
                self.timeEdit_5.setEnabled(False)






class Ui(QtWidgets.QMainWindow):


        def __init__(self):
            super(Ui,self).__init__()
            uic.loadUi('../res/GUI/mainwindow3.ui', self)
            self.treeWidget.setHeaderLabels(['Name','id', 'Type'])
            self.treeWidget_2.setHeaderLabels(['Name','id', 'Type'])
            self.parser = ET.XMLParser(remove_blank_text=True)
            self.tree = ET.parse('../xml/buildingNeighborhood.xml',self.parser)
            with open("../xml/buildingNeighborhood.xml", 'a') as f:
                self.tree.write('../xml/buildingNeighborhood.xml',encoding="utf-8", xml_declaration=True, pretty_print=True)
            with open('../xml/buildingLoad.xml', mode='w') as device_data:
                None
            def prettify(elem):
                """Return a pretty-printed XML string for the Element.
                """
                rough_string = ElementTree.tostring(elem, 'utf-8')
                reparsed = minidom.parseString(rough_string)
                return reparsed.toprettyxml(indent="  ")

            with open("../xml/buildingLoad.xml", 'a') as f:
                neigh = ET.Element('Neighborhood')
                f.write(prettify(neigh))

            self.tree2 = ET.parse('../xml/buildingLoad.xml',self.parser)
            self.tree2.write('../xml/buildingLoad.xml',encoding="utf-8", xml_declaration=True, pretty_print=True)
            with open('../res/csv_files/eventLoad.csv', mode='w') as device_data:
                    None
            with open('../res/csv_files/eCarLoad.csv', "w") as fileInput:
                    None
            with open('../res/csv_files/eventbackground.csv', "w") as fileInput:
                None
            with open('../res/csv_files/eventHC.csv', "w") as fileInput:
                    None
            self.count = 0
            self.xml=""
            self.all_list = []
            self.houseVector = []
            self.pathneigh = "../xml/buildingNeighborhood.xml"
            self.pathload = "../xml/buildingLoad.xml"
            self.updateTree()
            self.tableWidget.setRowCount(0)
            self.lineEdit.setReadOnly(True)
            self.selectedDevice = []
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(4)
            self.tableWidget.horizontalHeaderItem(0).setText("EST")
            self.tableWidget.horizontalHeaderItem(1).setText("LST")
            self.tableWidget.horizontalHeaderItem(2).setText("Creation_Time")
            self.tableWidget.horizontalHeaderItem(3).setText("Profile")
            self.full = True
            self.pids = []
            self.sm = 0
            self.abilit = 0
            self.semaphore = 1


        def start_disp(self,thread):
            self.dispatcher = di.dispatcher("taskmanager@localhost/taskmanager", "branco", self,thread)
            future = self.dispatcher.start()
            #future.result() # wait for receiver agent to be prepared.


        def pauseSimulation(self):
            self.mythread.stop()

        def start_Simulation(self):
            for x in range(1):
                    self.mythread = MyThread(self)
                    self.start_disp(self.mythread)
                    self.mythread.start()
                    time.sleep(.9)

        def display_GrigliaChange(self):
            self.grafico.griglia(self.cb_griglia.isChecked())

        def display_Grafico(self):
            self.grafico.tracciaGrafico()

        def openFileDialog(self):
            filter2 = "xml(*.xml)"
            filename = QFileDialog.getOpenFileName(self, 'Open neighborhood.xml File', '../xml/',filter=filter2)
            if filename[0]:
                self.pathNeighborhood.setText(filename[0])

        def selectLoadxml(self):
            filter2 = "xml(*.xml)"
            filename = QFileDialog.getOpenFileName(self, 'Open load.xml File', '../xml/',filter=filter2)
            if filename[0]:
                self.lineEdit_2.setText(filename[0])

        def submitLoadxml(self):
            self.pathload = self.lineEdit_2.text()
            self.tree2 = ET.parse(self.pathload)
            self.pathload = '../xml/buildingLoad.xml'
            self.tree2.write('../xml/buildingLoad.xml',encoding="utf-8", xml_declaration=True, pretty_print=True)
            self.updateTree()
            if(self.pathneigh != "" and self.pathload != ""):
                None #REPLACE WITH ACTION

        def editLoad(self):
            myid = self.treeWidget_2.selectedItems()[0].text(1)
            root = self.tree.getroot()
            entry= []
            for house in root:
                for user in house:
                    for device in user:
                        if (device.find('id').text == myid and device.tag == "device" ):
                            with open("../res/csv_files/eventLoad.csv", 'r') as filename:
                                with open("../res/csv_files/eventLoad_temp.csv", 'w') as outf:
                                    reader = csv.reader(filename)
                                    writer = csv.writer(outf)
                                    for line in reader:
                                        if line[0] == myid:
                                            try:
                                                entry.append(myid)
                                                col = self.tableWidget.column(self.tableWidget.selectedItems()[0])
                                                row = self.tableWidget.row(self.tableWidget.selectedItems()[0])
                                                for i in range (4):
                                                    entry.append(self.tableWidget.item(row,i).text())
                                                writer.writerow(entry)
                                                break
                                            except:
                                                writer.writerow(line)
                                        else:
                                            writer.writerow(line)
                                    writer.writerows(reader)
                            os.remove("../res/csv_files/eventLoad.csv")
                            os.rename("../res/csv_files/eventLoad_temp.csv", "../res/csv_files/eventLoad.csv")
                        elif (device.find('id').text == myid and device.tag == "ecar"):
                            with open("../res/csv_files/eCarLoad.csv", 'r') as ecarl:
                                with open("../res/csv_files/eCarLoad_temp.csv", 'w') as outf:
                                    reader = csv.reader(ecarl)
                                    writer = csv.writer(outf)
                                    for line in reader:
                                        if line[0] == myid:
                                            try:
                                                entry.append(myid)
                                                col = self.tableWidget.column(self.tableWidget.selectedItems()[0])
                                                row = self.tableWidget.row(self.tableWidget.selectedItems()[0])
                                                for i in range (7):
                                                    entry.append(self.tableWidget.item(row,i).text())
                                                writer.writerow(entry)
                                                break
                                            except:
                                                writer.writerow(line)
                                        else:
                                            writer.writerow(line)
                                    writer.writerows(reader)
                            os.remove("../res/csv_files/eCarLoad.csv")
                            os.rename("../res/csv_files/eCarLoad_temp.csv", "../res/csv_files/eCarLoad.csv")


        def saveConfig(self):
            def select_item(self, item):
                if(item.childCount() == 0 and item.parent() != None and  item.text(3) != "  "):
                        self.full = False
                for i in range(item.childCount()):
                    child = item.child(i)
                    select_item(self, child)

            item = self.treeWidget_2.invisibleRootItem()
            select_item(self, item)
            if(self.full):
                self.tableWidget.setRowCount(0)
                with open('../xml/buildingLoad.xml', mode='w') as device_data:
                    None
                root = self.tree.getroot()
                rootLoad = self.tree2.getroot()
                rootLoad.clear()
                allLoads = []
                alleCarLoads = []
                allHCLoads = []
                allBGLoads = []

                with open("../res/csv_files/eCarLoad.csv", "r") as f:
                    for i, line in enumerate(csv.reader(f)):
                        alleCarLoads.append(line)
                with open("../res/csv_files/eventLoad.csv", "r") as f:
                    for i, line in enumerate(csv.reader(f)):
                        allLoads.append(line)
                with open("../res/csv_files/eventHC.csv", "r") as f:
                    for i, line in enumerate(csv.reader(f)):
                        allHCLoads.append(line)
                with open("../res/csv_files/eventbackground.csv", "r") as f:
                    for i, line in enumerate(csv.reader(f)):
                        allBGLoads.append(line)
                for house in root:
                    if(house.tag == "house"):
                        attrib = {'id' : house.attrib['id']}
                        element = root.makeelement('house', attrib)
                        rootLoad.append(element)
                    else:
                        attrib = {'id' : house.attrib['id']}
                        element = root.makeelement('chargingStation', attrib)
                        rootLoad.append(element)
                    for user in house:
                        attrib = {'id' : user.attrib['id']}
                        user2 = element.makeelement('user',attrib)
                        element.append(user2)
                        for device in user:
                            if(device.tag == "device"):
                                first = 0
                                device2 = ET.SubElement(user2,"device")
                                id = ET.SubElement(device2,"id")
                                est = ET.SubElement(device2,"est")
                                lst = ET.SubElement(device2,"lst")
                                type2 = ET.SubElement(device2,"type")
                                type2.text = "load"

                                creat_time = ET.SubElement(device2,"creation_time")
                                profile = ET.SubElement(device2,"profile")
                                id.text = device.find('id').text
                                for data in allLoads:
                                    if(data[0] == id.text and first == 0):
                                        temp = data[1].split(':')
                                        timestamp = (int((temp[0])) * 60 * 60) + (int((temp[1])) * 60) + int((temp[2]))
                                        est.text= str(timestamp)
                                        temp = data[2].split(':')
                                        timestamp = (int((temp[0])) * 60 * 60) + (int((temp[1])) * 60) + int((temp[2]))
                                        lst.text = str(timestamp)
                                        temp = data[3].split(':')
                                        timestamp = (int((temp[0])) * 60 * 60) + (int((temp[1])) * 60) + int((temp[2]))
                                        creat_time.text = str(timestamp)
                                        profile.text = data[4]
                                        first = 1
                                    elif(data[0]== id.text and first == 1):
                                        device2 = ET.SubElement(user2,"device")
                                        id = ET.SubElement(device2,"id")
                                        est = ET.SubElement(device2,"est")
                                        lst = ET.SubElement(device2,"lst")
                                        type2 = ET.SubElement(device2,"type")
                                        type2.text = "load"
                                        creat_time = ET.SubElement(device2,"creation_time")
                                        profile = ET.SubElement(device2,"profile")
                                        id.text = device.find('id').text
                                        temp = data[1].split(':')
                                        timestamp = (int((temp[0])) * 60 * 60) + (int((temp[1])) * 60) + int((temp[2]))
                                        est.text= str(timestamp)
                                        temp = data[2].split(':')
                                        timestamp = (int((temp[0])) * 60 * 60) + (int((temp[1])) * 60) + int((temp[2]))
                                        lst.text = str(timestamp)
                                        temp = data[3].split(':')
                                        timestamp = (int((temp[0])) * 60 * 60) + (int((temp[1])) * 60) + int((temp[2]))
                                        creat_time.text = str(timestamp)
                                        profile.text = data[4]

                            elif(device.tag == "ecar"):
                                device2 = ET.SubElement(user2,"ecar")
                                id = ET.SubElement(device2,"id")
                                pat = ET.SubElement(device2,"pat")
                                pdt = ET.SubElement(device2,"pdt")
                                aat = ET.SubElement(device2,"aat")
                                adt = ET.SubElement(device2,"adt")
                                booking_time = ET.SubElement(device2,"creation_time")
                                soc = ET.SubElement(device2,"soc")
                                targetCharge = ET.SubElement(device2,"targetSoc")
                                v2g = ET.SubElement(device2,"V2G")
                                priority = ET.SubElement(device2,"priority")
                                id.text = device.find('id').text
                                for data in alleCarLoads:
                                    if(data[0] == id.text):
                                        temp = data[1].split(':')
                                        timestamp = (int((temp[0])) * 60 * 60) + (int((temp[1])) * 60) + int((temp[2]))
                                        pat.text= str(timestamp)
                                        temp = data[2].split(':')
                                        timestamp = (int((temp[0])) * 60 * 60) + (int((temp[1])) * 60) + int((temp[2]))
                                        pdt.text = str(timestamp)
                                        temp = data[3].split(':')
                                        timestamp = (int((temp[0])) * 60 * 60) + (int((temp[1])) * 60) + int((temp[2]))
                                        aat.text = str(timestamp)
                                        temp = data[4].split(':')
                                        timestamp = (int((temp[0])) * 60 * 60) + (int((temp[1])) * 60) + int((temp[2]))
                                        adt.text = str(timestamp)
                                        temp = data[5].split(':')
                                        timestamp = (int((temp[0])) * 60 * 60) + (int((temp[1])) * 60) + int((temp[2]))
                                        booking_time.text = str(timestamp)
                                        soc.text = data[6]
                                        targetCharge.text = data[7]
                                        v2g.text = data[9]
                                        priority.text = data[8]

                            elif(device.tag == "backgroundload"):
                                device2 = ET.SubElement(user2, "backgroundload")
                                id = ET.SubElement(device2,"id")
                                profile = ET.SubElement(device2,"profile")
                                id.text = device.find('id').text
                                for data in allBGLoads:
                                    if(data[0] == id.text):
                                        profile.text = data[1]
                            elif (device.tag == "heatercooler"):
                                device2 = ET.SubElement(user2, "heatercooler")
                                id = ET.SubElement(device2, "id")
                                profile = ET.SubElement(device2, "profile")
                                id.text = device.find('id').text
                                for data in allHCLoads:
                                    if(data[0] == id.text):
                                        print(data[1])
                                        profile.text = data[1]

                self.tree2.write("../xml/buildingLoad.xml",encoding="utf-8", xml_declaration=True,pretty_print=True)
                self.updateTree()
                def checkAll(self, item):
                    if(item.childCount() == 0 and item.parent() != None):
                        icon = QIcon("../res/GUI/images/icons8-checkmark-80")
                        item.setIcon(3,icon)
                        item.setText(3, "  ")
                    for i in range(item.childCount()):
                        child = item.child(i)
                        checkAll(self, child)

                item = self.treeWidget_2.invisibleRootItem()
                checkAll(self, item)
            else:
                QMessageBox.about(self, "Error", "Not enough Loads")

            self.full = True

        def saveXmlConfig(self):
            self.pathneigh = self.pathNeighborhood.text()
            self.tree = ET.parse(self.pathneigh)
            self.pathneigh = '../xml/buildingNeighborhood.xml'
            self.tree.write('../xml/buildingNeighborhood.xml',encoding="utf-8", xml_declaration=True, pretty_print=True)

            self.updateTree()
            if(self.pathneigh != "" and self.pathload != ""):
                None #REPLACE WITH ACTION

        def updateTree(self):
            self.treeWidget.clear()
            self.treeWidget_2.clear()
            with open(self.pathneigh, 'r') as myfile:
                self.xml = myfile.read()
            self.treeWidget.setHeaderLabels(['Title','id', 'Type'])
            self.treeWidget_2.setHeaderLabels(['Title','id', 'Type', 'has_Behaviour'])
            self.source = QtXml.QXmlInputSource()
            self.source.setData(self.xml)
            handler = sC.XmlHandler(self.treeWidget)
            handler2 = sC.XmlHandler(self.treeWidget_2)
            reader = QtXml.QXmlSimpleReader()
            reader.setContentHandler(handler)
            reader.setErrorHandler(handler)
            reader.parse(self.source)
            reader.setContentHandler(handler2)
            reader.setErrorHandler(handler2)
            self.source.setData(self.xml)
            reader.parse(self.source)
            self.tree = ET.parse('../xml/buildingNeighborhood.xml',self.parser)
            self.treeWidget_2.resizeColumnToContents(0)
            self.treeWidget_2.resizeColumnToContents(1)
            self.treeWidget_2.resizeColumnToContents(2)
            self.treeWidget_2.resizeColumnToContents(3)
            self.treeWidget.resizeColumnToContents(0)
            self.treeWidget.resizeColumnToContents(1)
            self.treeWidget.resizeColumnToContents(2)
            self.treeWidget.resizeColumnToContents(3)

        def deleteSelectedElementTree(self):
            root = self.tree.getroot()
            count = 1

            if self.treeWidget.selectedItems()[0].parent() is not None:
                while('0'<=self.treeWidget.selectedItems()[0].parent().text(0)[-count:] and self.treeWidget.selectedItems()[0].parent().text(0)[-count:]<='9'):
                    count +=1
                count -=1
                for house in root:
                   if(house.attrib['id'] ==  self.treeWidget.selectedItems()[0].parent().text(0)[-count:]):
                        for user in house:
                            for device in user:
                                device_name = device.find('name').text
                                device_id = device.find('id').text

                                if(device_name == self.treeWidget.selectedItems()[0].text(0) and device_id == self.treeWidget.selectedItems()[0].text(1)):
                                    user.remove(device)
                                    self.tree.write("../xml/buildingNeighborhood.xml",encoding="utf-8", xml_declaration=True,pretty_print=True)
            else:
                while('0'<=self.treeWidget.selectedItems()[0].text(0)[-count:] and self.treeWidget.selectedItems()[0].text(0)[-count:]<='9'):
                    count +=1
                count -=1
                for house in root:
                    if(house.attrib['id'] == self.treeWidget.selectedItems()[0].text(0)[-count:]):
                            root.remove(house)
                            self.tree.write("../xml/buildingNeighborhood.xml",encoding="utf-8", xml_declaration=True,pretty_print=True)

            self.updateTree()

        def openHouseSelection(self):
            self.dialog = houseUi(self)
            self.dialog.show()


        def openDeviceSelection(self):
            self.dialog = deviceUi(self)
            self.dialog.show()

        def addEvent(self):
            errorAlert = False
            root = self.tree.getroot()
            lines = '0'
            if(len(self.treeWidget_2.selectedItems())==0):
                QMessageBox.about(self, "Error", "No Device Selected")
            else:
                for item in self.treeWidget_2.selectedItems():
                    if(item.parent()==None):
                        errorAlert = True
                if(errorAlert == True):
                    QMessageBox.about(self, "Error", "House or charging station can not have Events associated")
                else:
                    for house in root:
                        #print(" now" + self.treeWidget_2.selectedItems()[0].parent().text(0))
                        #print("house " + house.attrib['id'])
                        if(self.treeWidget_2.selectedItems()[0].parent().text(0) == "House " + house.attrib['id'] or self.treeWidget_2.selectedItems()[0].parent().text(0) == "Charging Station " + house.attrib['id']):
                            for user in house:
                                for device in user:
                                    device_name = device.find('id').text
                                    if(self.treeWidget_2.selectedItems()[0].text(1)==device_name):
                                       if(device.tag =="device"):
                                           self.dialog = addEventUi(self)
                                           self.dialog.show()
                                       elif(device.tag == "heatercooler"):
                                           self.dialog = heaterCoolerSingle(self)
                                           self.dialog.show()
                                       elif(device.tag == "backgroundload"):
                                           self.dialog = backgroundUiSingle(self)
                                           self.dialog.show()
                                       else:
                                           self.dialog = ecarloadUI(self)
                                           self.dialog.show()


        def openSplashScreen(self):
            self.addDevice()

        def addHouse(self):
            min = 0
            root = self.tree.getroot()
            for house in root:
                if(int(house.attrib['id']) >min or int(house.attrib['id'])== min):
                    min=int(house.attrib['id'])+1

            attrib = {'id' : str(min)}
            element = root.makeelement('house', attrib)
            root.append(element)
            attrib2 = {'id' : '0'}
            user = element.makeelement('user',attrib2)
            element.append(user)
            self.tree.write("../xml/buildingNeighborhood.xml",encoding="utf-8", xml_declaration=True,pretty_print=True)
            self.updateTree()

        def addChargingStation(self):
            min = 0
            root = self.tree.getroot()
            for house in root:
                if(int(house.attrib['id'])>min or int(house.attrib['id'])== min):
                    min=int(house.attrib['id'])+1

            attrib = {'id' : str(min)}
            element = root.makeelement('chargingStation', attrib)
            root.append(element)
            attrib2 = {'id' : '0'}
            user = element.makeelement('user',attrib2)
            element.append(user)
            self.tree.write("../xml/buildingNeighborhood.xml",encoding="utf-8", xml_declaration=True,pretty_print=True)
            self.updateTree()

        def countDevice(self):
            self.count = 0
            root = self.tree.getroot()
            for house in root:
                for user in house:
                    for device in user:
                        self.count +=1

        def removeAll(self):
            root = self.tree.getroot()
            self.countDevice()
            for house in root:
                root.remove(house)
            self.tree.write("../xml/buildingNeighborhood.xml",encoding="utf-8", xml_declaration=True,pretty_print=True)
            self.updateTree()

        def selectType(self):
            self.dialog = selectTypeDevice(self)
            self.dialog.show()

        def addDevice(self):
            root = self.tree.getroot()
            if(len(self.houseVector)==0):
                QMessageBox.about(self, "Error", "No House/Charging Station Selected")
            elif(len(self.selectedDevice)==0):
                QMessageBox.about(self, "Error", "No Device Selected")
            else:
                self.countDevice()
                for element in self.houseVector:
                    temp = element.split()
                    for house in root:
                        for user in house:
                            if(int(house.attrib['id']==temp[1])):
                                for i in range(self.spinBox.value()):
                                    if(self.selectedDevice[3] == "General Device"):
                                            element2 = ET.SubElement(user,"device")
                                    elif(self.selectedDevice[3] == 'Ecar'):
                                            element2 = ET.SubElement(user,"ecar")
                                            model = ET.SubElement(element2, "model")
                                            capacity = ET.SubElement(element2, "capacity")
                                            max_ch_pow_ac = ET.SubElement(element2, "maxchpowac")
                                            max_ch_pow_cc = ET.SubElement(element2, "maxchpowcc")
                                            max_dis_pow = ET.SubElement(element2, "maxdispow")
                                            max_all_en = ET.SubElement(element2, "maxallen")
                                            min_all_en = ET.SubElement(element2, "minallen")
                                            sb_ch = ET.SubElement(element2, "sbch")
                                            sb_dis = ET.SubElement(element2, "sbdis")
                                            ch_eff = ET.SubElement(element2, "cheff")
                                            dis_eff = ET.SubElement(element2, "dis_eff")
                                            with open('../res/csv_files/eCarModels.csv', mode='r') as device_data:
                                                for line in device_data:
                                                    name = line.split(',')
                                                    if (name[0] == self.selectedDevice[2]):
                                                        model.text = name[0]
                                                        capacity.text = name[1]
                                                        max_ch_pow_ac.text = name[2]
                                                        max_ch_pow_cc.text = name[3]
                                                        max_dis_pow.text = name[4]
                                                        max_all_en.text = name[5]
                                                        min_all_en.text = name[6]
                                                        sb_ch.text = name[7]
                                                        sb_dis.text = name[8]
                                                        ch_eff.text = name[9]
                                                        dis_eff.text = name[10]
                                    elif (self.selectedDevice[3] == 'Ecar'):
                                        element2 = ET.SubElement(user, "ecar")
                                    elif (self.selectedDevice[3] == 'Heater/Cooler'):
                                        element2 = ET.SubElement(user, "heatercooler")
                                    elif (self.selectedDevice[3] == 'Background Load'):
                                        element2 = ET.SubElement(user, "backgroundload")
                                    elif (self.selectedDevice[3] == 'Battery'):
                                        element2 = ET.SubElement(user, "battery")
                                    type = ET.SubElement(element2,"type")
                                    type.text = self.selectedDevice[1]
                                    name = ET.SubElement(element2,"name")
                                    name.text = self.selectedDevice[0]
                                    deviceId = ET.SubElement(element2,"id")
                                    deviceId.text = str(self.count)
                                    self.count+=1
                self.houseVector = []
                self.tree.write("../xml/buildingNeighborhood.xml",encoding="utf-8", xml_declaration=True,pretty_print=True)
                self.updateTree()

        def modifyLoad(self):
            print("Ciao")


        def showLoads(self):
            isEcar = False
            isBackground = False
            isHeaterCooler = False
            isBattery = False
            if(len(self.treeWidget_2.selectedItems())!=0):
                if(self.treeWidget_2.selectedItems()[0].parent() == None):
                    self.treeWidget_2.selectedItems()[0].setSelected(False)
                else:
                    root = self.tree.getroot()
                    myid = self.treeWidget_2.selectedItems()[0].text(1)
                    for house in root:
                        for user in house:
                            for device in user:
                                if (device.find('id').text == myid and device.tag == "ecar" ):
                                        isEcar = True
                                elif(device.find('id').text == myid and device.tag == "backgroundload" ):
                                        isBackground = True
                                elif (device.find('id').text == myid and device.tag == "heatercooler"):
                                        isHeaterCooler = True
                                elif (device.find('id').text == myid and device.tag == "battery"):
                                        isBattery = True
                    self.tableWidget.setColumnCount(10)


                    if(isEcar):
                        try:
                            self.tableWidget.setRowCount(0)
                            self.tableWidget.setColumnCount(7)
                            self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Arrival Time"))
                            self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Departure Time"))
                            self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Creation Time"))
                            self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("E-Car Model"))
                            self.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem("Starting Charge"))
                            self.tableWidget.setHorizontalHeaderItem(5, QTableWidgetItem("Leaving Charge"))
                            self.tableWidget.setHorizontalHeaderItem(6, QTableWidgetItem("V2G"))
                            count = 0
                            with open('../res/csv_files/eCarLoad.csv', "r") as fileInput:
                                self.tableWidget.setRowCount(0)
                                for row_number,row_data in enumerate(csv.reader(fileInput)):
                                    if(str(row_data[0]) == self.treeWidget_2.selectedItems()[0].text(1)):
                                        self.tableWidget.insertRow(count)
                                        for column_number, column_data in enumerate(row_data):
                                            if(column_number != 0):
                                                self.tableWidget.setItem(count,column_number-1,QtWidgets.QTableWidgetItem(column_data))
                                        count +=1
                            self.tableWidget.resizeColumnsToContents()
                        except IOError:
                            None
                    elif(isBackground):
                        try:
                            self.tableWidget.setRowCount(0)
                            self.tableWidget.setColumnCount(1)
                            self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Profile"))
                            count = 0
                            with open('../res/csv_files/eventbackground.csv', "r") as fileInput:
                                self.tableWidget.setRowCount(0)
                                for row_number,row_data in enumerate(csv.reader(fileInput)):
                                    if(str(row_data[0]) == self.treeWidget_2.selectedItems()[0].text(1)):
                                        self.tableWidget.insertRow(count)
                                        for column_number, column_data in enumerate(row_data):
                                            if(column_number != 0):
                                                self.tableWidget.setItem(count,column_number-1,QtWidgets.QTableWidgetItem(column_data))
                                        count +=1
                            self.tableWidget.resizeColumnsToContents()
                        except IOError:
                            self.tableWidget.setRowCount(0)
                            None
                    elif (isHeaterCooler):
                        try:
                            self.tableWidget.setRowCount(0)
                            self.tableWidget.setColumnCount(1)
                            self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Profile"))
                            count = 0
                            with open('../res/csv_files/eventHC.csv', "r") as fileInput:
                                self.tableWidget.setRowCount(0)
                                for row_number, row_data in enumerate(csv.reader(fileInput)):
                                    if (str(row_data[0]) == self.treeWidget_2.selectedItems()[0].text(1)):
                                        self.tableWidget.insertRow(count)
                                        for column_number, column_data in enumerate(row_data):
                                            if (column_number != 0):
                                                self.tableWidget.setItem(count, column_number - 1,
                                                                         QtWidgets.QTableWidgetItem(column_data))
                                        count += 1
                            self.tableWidget.resizeColumnsToContents()
                        except IOError:
                            None
                    elif(isBattery):
                        self.tableWidget.setColumnCount(10)

                    else:
                        try:
                            count = 0
                            self.tableWidget.setRowCount(0)
                            self.tableWidget.setColumnCount(4)
                            self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("EST"))
                            self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("LST"))
                            self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Creation_Time"))
                            self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Profile"))
                            with open('../res/csv_files/eventLoad.csv', "r") as fileInput:
                                for row_number,row_data in enumerate(csv.reader(fileInput)):
                                    if(str(row_data[0]) == self.treeWidget_2.selectedItems()[0].text(1)):
                                        self.tableWidget.insertRow(count)
                                        for column_number, column_data in enumerate(row_data):
                                            if(column_number != 0):
                                                self.tableWidget.setItem(count,column_number-1,QtWidgets.QTableWidgetItem(column_data))
                                        count +=1
                            self.tableWidget.resizeColumnsToContents()
                        except IOError:
                            None





app = QtWidgets.QApplication([])

#progressb = QtWidgets.QProgressBar()
window = Ui()
#window.progressBar.setValue(0)
#window.lcdNumber.display(1)

class MyThread(threading.Thread):
    abilit = 1
    def __init__(self,window):
        super(MyThread,self).__init__()
        window = window


    def run(self):
        self.scheduler = sche.scheduler("adapter@localhost", "branco25")
        self.scheduler.web.add_get("/gettime", self.scheduler.get_time, "message.html")
        self.scheduler.web.add_post("/postanswer", self.scheduler.post_answer, "message2.html")
        self.scheduler.start()
        cors = aiohttp_cors.setup(self.scheduler.web.app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*",
            )
        })

        routes = [{
            'method': 'GET',
            'path': '/getmessage',
            'handler': self.scheduler.get_message,
            'name': 'test-good'
        },]
        for route in routes:
            cors.add(
                self.scheduler.web.app.router.add_route(
                    method=route['method'],
                    path=route['path'],
                    handler=route['handler'],
                    name=route['name']
                )
            )

        #self.scheduler.web.setup_routes()
        self.scheduler.web.start(hostname="192.168.1.207",port="10002")


        #sched.result()
        #self.editStartTime.text()



        for i in range(int(window.spinBox_2.text())):
            self.abilit = 0
            es.date = window.editStartTime.text()
            print(es.date)
            es.datetime_object = datetime.datetime.strptime(window.editStartTime.text(), '%m/%d/%y %H:%M:%S')
            print(window.pathload)
            print(window.pathneigh)
            external = es.ExternalSourceAgent("externalSource@localhost", "branco25",window.pathneigh, window.pathload)
            ex = external.start()
            ex.result()
            external.stop()
            self.setupmodule = sm.setupModule("setupmodule@localhost", "branco25")
            self.setupmodule.start()
            while(self.abilit == 0):
                None
            while(self.setupmodule.is_alive()):
                self.setupmodule.stop()
        while(self.scheduler.is_alive()):
            self.scheduler.stop()
        while(window.dispatcher.is_alive()):
            window.dispatcher.stop()

    def stop(self):
        b = self.setupmodule.stopService()
        self.setupmodule.add_behaviour(b)




if __name__ == "__main__":
    window.show()
    app.exec()
