import shutil
import json
import os
import sys
from os import mkdir

import nltk
from nltk.corpus import stopwords
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QPlainTextEdit, QComboBox, QCheckBox, \
    QMessageBox, QFileDialog, QLineEdit
from nltk.parse import stanford as SParse
from nltk.tag import stanford as STag
from nltk.tokenize import StanfordSegmenter
from polyglot.text import Text
from qtpy import QtCore, QtGui
from Shakkala import Shakkala
arb_stopwords = set(nltk.corpus.stopwords.words("arabic"))
stp=str(arb_stopwords)

#You can add your own stop words here
#stp_list_added=[]

#You can add your own NER here
NER_list_added=["لندليام","بئرتوتة","مغربي","بجكرتا"]
Money=["دولار","الدرهم","الدينار","يورو","روبل","فرنك","دينار","درهم"]



#Fonction of Json
def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w',encoding="utf-8") as fp:
        json.dump(data,fp)
#Creating interface
a=QApplication(sys.argv)
root=QWidget()
lb1=QLabel(root)
pm1=QPixmap("2.png")
lb1.setPixmap(pm1)
root.setWindowTitle("AAAL Platform")
root.setFixedSize(pm1.width(),pm1.height())
le1=QPlainTextEdit(root)
le1.setGeometry(100,210,1070,180)
lb2=QLabel("Please enter your text:",root)
lb2.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
lb2.move(100,180)
lb3=QLabel("يرجى إدخال النص المراد معالجته :",root)
lb3.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
lb5=QLabel("NB: Enter at most 315 character on vocalisation fonctions",root)
lb5.move(400,520)
lb5.setVisible(False)
lb5.setFont(QtGui.QFont("Times", 12))
lb3.move(915,180)
bt1=QPushButton("Process Text معالجة النص ",root)
bt1.move(100,470)
bt1.resize(280,70)
bt1.setFont(QtGui.QFont("Times", 13, QtGui.QFont.Bold))
icon1 =QtGui.QIcon('3.png')
bt2=QPushButton("Details المزايا",root)
bt2.move(965,490)
bt2.resize(100,50)
bt2.setIcon(icon1)
bt2.setFont(QtGui.QFont("Times", 9))
icon3 =QtGui.QIcon('9.png')
bt5=QPushButton("SIMPLE",root)
bt5.move(1180,700)
bt5.resize(100,50)
bt5.setIcon(icon3)
bt5.setFont(QtGui.QFont("Times", 9, QtGui.QFont.Bold))
bt5.setVisible(False)
icon2 =QtGui.QIcon('8.png')
bt3=QPushButton("ADVANCED",root)
bt3.move(1180,700)
bt3.resize(100,50)
bt3.setIcon(icon2)
bt3.setFont(QtGui.QFont("Times", 9, QtGui.QFont.Bold))
icon4 =QtGui.QIcon('5.png')
bt4=QPushButton("Get File",root)
bt4.resize(200,50)
bt4.move(980,220)
bt4.setIcon(icon4)
bt4.setFont(QtGui.QFont("Times", 13, QtGui.QFont.Bold))
bt4.setVisible(False)
icon5 =QtGui.QIcon('10.png')
printbox=QCheckBox("Print",root)
printbox.move(1080,500)
printbox.setIcon(icon5)
printbox.setFont(QtGui.QFont("Times", 15))
le2=QLineEdit(root)
le2.setGeometry(100,220,850,50)
le2.setVisible(False)
le2.setFont(QtGui.QFont("Times", 15))
le1.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
root.resize(pm1.width(),pm1.height())
lb4=QLabel("",root)
lb4.move(100,350)
pte1=QPlainTextEdit(root)
pte1.setGeometry(100,550,1070,200)
pte1.setFont(QtGui.QFont("Times", 10))
pte1.setLayoutDirection(QtCore.Qt.RightToLeft)
cb1=QComboBox(root)
cb1.move(100,410)
cb1.resize(270,35)
#combobox
cb1.addItem("pre-processing التجهيزات الاوليّة")
cb1.addItem("Stemming Words تجذير الكلمات")
cb1.addItem("تقسيم الكلام Segmentation")
cb1.addItem("Vocalisation Functions وضائف التشكيل")
cb1.addItem("Numbers Functions وضائف الارقام")
cb1.addItem("تصنيف أقسام الكلام  Part-of-Speech (POS) tagging")
cb1.addItem("تحديد الأعلام Named Entity Recognition NER")
cb1.addItem("الإعراب Parsing")
cb1.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
cb1.setLayoutDirection(QtCore.Qt.RightToLeft)

#Checkbox
cbx1=QCheckBox("word token \n إستخلاص الكلمات",root)
cbx1.move(400,410)
cbx1.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

cbx23=QCheckBox("word token \n إستخلاص الكلمات",root)
cbx23.move(550,410)
cbx23.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
cbx23.setVisible(False)
cbx23.setEnabled(False)

cbx24=QCheckBox("morphology \n أقسام الكلمة",root)
cbx24.move(695,410)
cbx24.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
cbx24.setVisible(False)
cbx24.setEnabled(False)

cbx2=QCheckBox("sentence token \n إستخلاص الجمل",root)
cbx2.move(550,410)
cbx2.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

cbx3=QCheckBox("morphemes \n أقسام الكلمة",root)
cbx3.move(695,410)
cbx3.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
#CheckBox for first combobox
cbx4=QCheckBox("Removing Stop-Words \n نزع الكلمات الزائدة",root)
cbx4.move(820,410)
cbx4.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
cbx5=QCheckBox("Strip-Vocalisation \n نزع التشكيل",root)
cbx5.move(400,460)
cbx5.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
cbx6=QCheckBox("Except NER \n استثناء اسماء العلم",root)
cbx6.move(550,460)
cbx6.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
cbx11=QCheckBox("Except Stop-Words \n استثناء الكلمات الزائدة",root)
cbx11.move(700,460)
cbx11.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

#ChechBox for seconde combobox
cbx7=QCheckBox("Extract root \n استخلاص الجذر",root)
cbx7.move(380,410)
cbx7.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
cbx8=QCheckBox("Extract Stem \n استخلاص الجذع",root)
cbx8.move(515,410)
cbx8.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
cbx9=QCheckBox("Get Star Word \n استرجاع الكلمة المنجمة",root)
cbx9.move(645,410)
cbx9.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
cbx10=QCheckBox("Get Affixes \n استرجاع الكلمات الزائدة",root)
cbx10.move(820,410)
cbx10.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

#ChechBox for fourth combobox
cbx15=QCheckBox("Text Vocalisation \n تشكيل النص",root)
cbx15.move(400,410)
cbx15.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
cbx12=QCheckBox("Text Mid-Vocalisation  \n تشكيل جزئي للنص",root)
cbx12.move(700,410)
cbx12.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
cbx13=QCheckBox("Strip Vocalisation \n نزع التشكيل ",root)
cbx13.move(400,460)
cbx13.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
cbx14=QCheckBox("Normalize_Hamza \n توحيد الهمزة",root)
cbx14.move(700,460)
cbx14.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

#ChechBox for fifth combobox
cbx16=QCheckBox("Convert Number to Words \n تحويل عدد الى كلمة",root)
cbx16.move(400,410)
cbx16.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
cbx17=QCheckBox("Convert text to number \n تحويل الكلمات إلى أعداد",root)
cbx17.move(700,410)
cbx17.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
cbx18=QCheckBox("Extract number words with context \n استخلاص العبارات العددية مع سياقها",root)
cbx18.move(400,460)
cbx18.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
cbx19=QCheckBox("Extract number words \n استخلاص العبارات العددية",root)
cbx19.move(700,460)
cbx19.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

#ChechBox for sixth combobox
cbx20=QCheckBox("Strip-Vocalisation \n نزع التشكيل",root)
cbx20.move(400,410)
cbx20.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
cbx21=QCheckBox("Except NER \n استثناء اسماء العلم",root)
cbx21.move(550,410)
cbx21.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
cbx22=QCheckBox("Except Stop-Words \n استثناء الكلمات الزائدة",root)
cbx22.move(695,410)
cbx22.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

#hidden combobox
hiden1=QCheckBox("",root)
hiden1.move(1,1)
hiden1.setVisible(False)
hiden1.setChecked(False)

hiden2=QCheckBox("",root)
hiden2.move(1,1)
hiden2.setVisible(False)
hiden2.setChecked(False)

hiden3=QCheckBox("",root)
hiden3.move(1,1)
hiden3.setVisible(False)
hiden3.setChecked(False)

hiden3=QCheckBox("",root)
hiden3.move(1,1)
hiden3.setVisible(False)
hiden3.setChecked(False)

hiden4=QCheckBox("",root)
hiden4.move(1,1)
hiden4.setVisible(False)
hiden4.setChecked(False)

#combobox organisation
cbx1.setVisible(False)
cbx2.setVisible(False)
cbx3.setVisible(False)
cbx4.setVisible(False)
cbx5.setVisible(False)
cbx6.setVisible(False)
cbx11.setVisible(False)
cbx12.setVisible(False)
cbx13.setVisible(False)
cbx14.setVisible(False)
cbx15.setVisible(False)
cbx7.setVisible(False)
cbx8.setVisible(False)
cbx9.setVisible(False)
cbx10.setVisible(False)
cbx17.setVisible(False)
cbx18.setVisible(False)
cbx19.setVisible(False)
cbx16.setVisible(False)
cbx20.setVisible(False)
cbx21.setVisible(False)
cbx22.setVisible(False)
cbx5.setChecked(True)
cbx5.setEnabled(False)
cbx20.setChecked(True)
cbx21.setChecked(True)
cbx22.setChecked(True)
cbx20.setEnabled(False)
cbx21.setEnabled(False)
cbx22.setEnabled(False)
cbx6.setEnabled(False)
cbx11.setEnabled(False)

##importing stanford
os.environ['STANFORD_MODELS'] = 'stanford-segmenter-2018-10-16/data/;stanford-postagger-full-2018-10-16/models/'
os.environ['STANFORD_PARSER'] = 'stanford-parser-full-2018-10-17'
os.environ['CLASSPATH'] = 'stanford-parser-full-2018-10-17'
os.environ['JAVAHOME'] = 'D:/Program Files/Java/jdk1.8.0_171'

#declaration of variables
globvar = " "
lolo = " "

#Hide first interface
def ev3():
    le1.setVisible(False)
    le2.setVisible(True)
    lb2.setVisible(False)
    lb3.setVisible(False)
    bt4.setVisible(True)
    bt5.setVisible(True)
    bt3.setVisible(False)

#Hide Seconde interface
def ev5():
    le1.setVisible(True)
    le2.setVisible(False)
    lb2.setVisible(True)
    lb3.setVisible(True)
    bt4.setVisible(False)
    bt5.setVisible(False)
    bt3.setVisible(True)

#First Getting file Fontion
def ev4():
    global lolo
    op = QFileDialog.getOpenFileName(root, "choose file","C:/Users/Public/Documents")
    lolo = op[0]
    le2.setText(lolo)

#seconde Getting file Fontion
def ev6():
    global globvar
    globvar=lolo

#Fonction of "show détails"
def ev1():
    lb5.setVisible(False)
    hiden1.setChecked(False)
    hiden2.setChecked(False)
    hiden3.setChecked(False)
    hiden4.setChecked(False)
    cbx7.setChecked(False)
    cbx8.setChecked(False)
    cbx9.setChecked(False)
    cbx10.setChecked(False)
    cbx16.setChecked(False)
    cbx17.setChecked(False)
    cbx18.setChecked(False)
    cbx19.setChecked(False)
    cbx12.setChecked(False)
    cbx13.setChecked(False)
    cbx14.setChecked(False)
    cbx15.setChecked(False)
    cbx1.setChecked(False)
    cbx2.setChecked(False)
    cbx3.setChecked(False)
    cbx4.setChecked(False)
    cbx23.setChecked(True)
    cbx24.setChecked(True)
    cbx23.setVisible(False)
    cbx24.setVisible(False)
    cbx1.setVisible(False)
    cbx2.setVisible(False)
    cbx3.setVisible(False)
    cbx4.setVisible(False)
    cbx5.setVisible(False)
    cbx6.setVisible(False)
    cbx11.setVisible(False)
    cbx12.setVisible(False)
    cbx13.setVisible(False)
    cbx14.setVisible(False)
    cbx15.setVisible(False)
    cbx16.setVisible(False)
    cbx17.setVisible(False)
    cbx18.setVisible(False)
    cbx19.setVisible(False)
    cbx20.setVisible(False)
    cbx21.setVisible(False)
    cbx22.setVisible(False)
    cbx7.setVisible(False)
    cbx8.setVisible(False)
    cbx9.setVisible(False)
    cbx10.setVisible(False)
    c = cb1.currentIndex()
    if c==0:
        cbx1.setVisible(True)
        cbx2.setVisible(True)
        cbx3.setVisible(True)
        cbx4.setVisible(True)
    if c==1:
        cbx7.setVisible(True)
        cbx8.setVisible(True)
        cbx9.setVisible(True)
        cbx10.setVisible(True)

    if c==4:
        cbx16.setVisible(True)
        cbx17.setVisible(True)
        cbx18.setVisible(True)
        cbx19.setVisible(True)
    if c==3:
        cbx12.setVisible(True)
        cbx13.setVisible(True)
        cbx14.setVisible(True)
        cbx15.setVisible(True)
        lb5.setVisible(True)
    if c==2:
        cbx20.setVisible(True)
        cbx21.setVisible(True)
        cbx22.setVisible(True)
        hiden1.setChecked(True)
    if c==5:
        cbx20.setVisible(True)
        cbx23.setVisible(True)
        cbx24.setVisible(True)
        hiden2.setChecked(True)
    if c==6:
        cbx20.setVisible(True)
        cbx23.setVisible(True)
        cbx24.setVisible(True)
        hiden3.setChecked(True)
    if c==7:
        cbx20.setVisible(True)
        cbx23.setVisible(True)
        cbx24.setVisible(True)
        hiden4.setChecked(True)
def ev2():
    try:
        from pyarabic import araby
        ev6()
        ee = le1.toPlainText()
        cbx6.setVisible(False)
        cbx11.setVisible(False)
        #if the text is a txt file
        if (bt3.isVisible()== False):
            ev6()
            print(globvar)
            gg=globvar
            print(gg)
            F = open(gg, "r",encoding="utf-8")
            ee=F.read()
            F.close()
        # if the text is an input
        else:
            F = open("sample.txt", "w", encoding="utf-8")
            F.write(ee)
            F.close()
        tt = araby.strip_tashkeel(ee)
        se = Text(tt)
        segmenter = StanfordSegmenter('stanford-segmenter-2018-10-16/stanford-segmenter-3.9.2.jar')
        segmenter.default_config('ar')
        pte1.setPlainText(" ")
        if cbx1.isChecked():
            cbx5.setVisible(False)
            pte1.appendPlainText("     ---------------------------------- Extracting Word Tokens ----------------------------------    \n")
            se = Text(tt)
            l1 = se.words
            pte1.appendPlainText(str(l1))
            pte1.appendPlainText("")
            pte1.appendPlainText("---------------------------------------------------------------------------------------------------- \n")
            if printbox.isChecked():
                F = open("output/Word Tokens.txt", "w", encoding="utf-8")
                F.write("Extracting Word Tokens : \n")
                F.write("------------- \n")
                F.write(str(l1))
                F.close()
                #convert to JSON
                F = open("output/Word Tokens.txt", "r", encoding="utf-8")
                ee = F.read()
                F.close()
                path = './output/'
                filename = 'Word Tokens'
                data = ee
                writeToJSONFile(path, filename, data)


        if cbx2.isChecked():
            cbx5.setVisible(False)
            pte1.appendPlainText(
                "     ---------------------------------- Extracting Sentence Tokens ----------------------------------    \n")
            se = Text(tt)
            l2 = se.sentences
            pte1.appendPlainText(str(l2))
            pte1.appendPlainText("")
            pte1.appendPlainText("---------------------------------------------------------------------------------------------------- \n")
            if printbox.isChecked():
                F = open("output/Word Sentences.txt", "w", encoding="utf-8")
                F.write("Extracting Sentences Tokens : \n")
                F.write("------------- \n")
                F.write(str(l2))
                F.close()
                # convert to JSON
                F = open("output/Word Sentences.txt", "r", encoding="utf-8")
                ee = F.read()
                F.close()
                path = './output/'
                filename = 'Word Sentences'
                data = ee
                writeToJSONFile(path, filename, data)
                """"
                #re-convert to txt
                from pprint import pprint
                with open('Word Sentences.json') as f:
                    data = json.load(f)
                pprint(data)
                """
        if cbx3.isChecked():
            # morphology
            cbx5.setVisible(True)
            pte1.appendPlainText(
                "     ---------------------------------- Extracting Morphemes ----------------------------------    \n")
            se = Text(tt)
            p = se.words
            for i in p:
                pte1.appendPlainText(str(i.morphemes))
            pte1.appendPlainText("")
            pte1.appendPlainText(
                "---------------------------------------------------------------------------------------------------- \n")
            if printbox.isChecked():
                F = open("output/Extracting Morphemes.txt", "w", encoding="utf-8")
                F.write("Extracting Morphemes : \n")
                F.write("------------- \n")
                for y in p:
                    F.write(str(y.morphemes))
                F.close()
                # convert to JSON
                F = open("output/Extracting Morphemes.txt", "r", encoding="utf-8")
                ee = F.read()
                F.close()
                path = './output/'
                filename = 'Extracting Morphemes'
                data = ee
                writeToJSONFile(path, filename, data)
                """"
                #re-convert to txt
                from pprint import pprint
                with open('Extracting Morphemes.json') as f:
                    data = json.load(f)
                pprint(data)
                """
        if cbx4.isChecked():
            cbx5.setVisible(False)
            pte1.appendPlainText(
                "     ---------------------------------- Removing Stop Words ----------------------------------    \n")
            se = Text(tt)
            p = se.words
            ls1=[]
            for i in p:
                if i not in stp:
                  #if i not in stp_list_added:
                    ls1.append(i)
            pte1.appendPlainText(str(ls1))
            pte1.appendPlainText("")
            pte1.appendPlainText(
                "---------------------------------------------------------------------------------------------------- \n")
            if printbox.isChecked():
                F = open("output/Removing Stop Words.txt", "w", encoding="utf-8")
                F.write("Removing Stop Words : \n")
                F.write("------------- \n")
                F.write(str(ls1))
                F.close()
                # convert to JSON
                F = open("output/Removing Stop Words.txt", "r", encoding="utf-8")
                ee = F.read()
                F.close()
                path = './output/'
                filename = 'Removing Stop Words'
                data = ee
                writeToJSONFile(path, filename, data)
                """"
                #re-convert to txt
                from pprint import pprint
                with open('Removing Stop Words.json') as f:
                    data = json.load(f)
                pprint(data)
                """

        #extract stems
        if cbx8.isChecked():
            pte1.appendPlainText("")
            cbx5.setVisible(True)
            cbx6.setChecked(True)
            cbx6.setVisible(True)
            cbx11.setChecked(True)
            cbx11.setVisible(True)
            if printbox.isChecked():
                F = open("output/Word Stems.txt", "w", encoding="utf-8")
                F.write("Extracting Words Stems" + "\n")
                F.write("----------------------" + "\n")
                F.close()
            import pyarabic.arabrepr
            arepr = pyarabic.arabrepr.ArabicRepr()
            repr = arepr.repr
            from tashaphyne.stemming import ArabicLightStemmer
            ArListem = ArabicLightStemmer()
            se = Text(tt)
            p = se.words
            pte1.appendPlainText(
                "     ---------------------------------- Extracting Words Stems ----------------------------------    \n")
            ls = ["كيلانيمي", "شركة"]
            for entity in se.entities:
                for i in entity:
                    ls.append(i)
            for i in p:
                if i not in ls:
                    if i not in stp:
                        stem = ArListem.light_stem(i)
                        pte1.appendPlainText(ArListem.get_stem())
                        if printbox.isChecked():
                            F = open("output/Word Stems.txt", "a", encoding="utf-8")
                            F.write(ArListem.get_stem()+"\n")
                            F.close()
                    else:
                        pte1.appendPlainText(str(i))
                        if printbox.isChecked():
                            F = open("output/Word Stems.txt", "a", encoding="utf-8")
                            F.write(str(i)+"\n")
                            F.close()
                else:
                    pte1.appendPlainText(str(i))
                    if printbox.isChecked():
                        F = open("output/Word Stems.txt", "a", encoding="utf-8")
                        F.write(str(i)+"\n")
                        F.close()
            if printbox.isChecked():
                # convert to JSON
                F = open("output/Word Stems.txt", "r", encoding="utf-8")
                ee = F.read()
                F.close()
                path = './output/'
                filename = 'Word Stems'
                data = ee
                writeToJSONFile(path, filename, data)
                """"
                #re-convert to txt
                from pprint import pprint
                with open('Word Stems.json') as f:
                    data = json.load(f)
                pprint(data)
                """
            pte1.appendPlainText("")
            pte1.appendPlainText(
                "---------------------------------------------------------------------------------------------------- \n")
        #extract roots
        if cbx7.isChecked():
            pte1.appendPlainText("")
            cbx5.setVisible(True)
            cbx6.setChecked(True)
            cbx6.setVisible(True)
            cbx11.setChecked(True)
            cbx11.setVisible(True)
            if printbox.isChecked():
                F = open("output/Word roots.txt", "w", encoding="utf-8")
                F.write("Extracting Words roots" + "\n")
                F.write("----------------------" + "\n")
                F.close()
            import pyarabic.arabrepr
            arepr = pyarabic.arabrepr.ArabicRepr()
            repr = arepr.repr
            from tashaphyne.stemming import ArabicLightStemmer
            ArListem = ArabicLightStemmer()
            se = Text(tt)
            p = se.words
            pte1.appendPlainText(
                "     ---------------------------------- Extracting Words roots ----------------------------------    \n")
            ls = ["كيلانيمي","شركة"]
            for entity in se.entities:
                for i in entity:
                    ls.append(i)
            for i in p:
                if i not in ls:
                    if i not in stp:
                        stem = ArListem.light_stem(i)
                        # extract stem
                        pte1.appendPlainText(ArListem.get_root())
                        if printbox.isChecked():
                            F = open("output/Word roots.txt", "a", encoding="utf-8")
                            F.write(str(ArListem.get_root()) + "\n")
                            F.close()
                    else:
                        pte1.appendPlainText(str(i))
                        if printbox.isChecked():
                            F = open("output/Word roots.txt", "a", encoding="utf-8")
                            F.write(str(i) + "\n")
                            F.close()
                else:
                    pte1.appendPlainText(str(i))
                    if printbox.isChecked():
                        F = open("output/Word roots.txt", "a", encoding="utf-8")
                        F.write(str(i) + "\n")
                        F.close()
            if printbox.isChecked():
                # convert to JSON
                F = open("output/Word roots.txt", "r", encoding="utf-8")
                ee = F.read()
                F.close()
                path = './output/'
                filename = 'Word roots'
                data = ee
                writeToJSONFile(path, filename, data)
                """"
                #re-convert to txt
                from pprint import pprint
                with open('Word roots.json') as f:
                    data = json.load(f)
                pprint(data)
                """
            pte1.appendPlainText("")
            pte1.appendPlainText(
                "---------------------------------------------------------------------------------------------------- \n")

        #Extract Star Word
        if cbx9.isChecked():
            pte1.appendPlainText("")
            cbx5.setVisible(True)
            cbx6.setChecked(True)
            cbx6.setVisible(True)
            cbx11.setChecked(True)
            cbx11.setVisible(True)
            if printbox.isChecked():
                F = open("output/Star Words.txt", "w", encoding="utf-8")
                F.write("Extracting Star Word" + "\n")
                F.write("----------------------" + "\n")
                F.close()
            import pyarabic.arabrepr
            arepr = pyarabic.arabrepr.ArabicRepr()
            repr = arepr.repr
            from tashaphyne.stemming import ArabicLightStemmer
            ArListem = ArabicLightStemmer()
            se = Text(tt)
            p = se.words
            pte1.appendPlainText(
                "     ---------------------------------- Extracting Star Word ----------------------------------    \n")
            ls = []
            for entity in se.entities:
                for i in entity:
                    ls.append(i)
            for i in p:
                if i not in ls:
                    if i not in stp:
                        stem = ArListem.light_stem(i)
                        pte1.appendPlainText(ArListem.get_starword())
                        if printbox.isChecked():
                            F = open("output/Star Words.txt", "a", encoding="utf-8")
                            F.write(str(ArListem.get_starword()) + "\n")
                            F.close()
                    else:
                        pte1.appendPlainText(str(i))
                        if printbox.isChecked():
                            F = open("output/Star Words.txt", "a", encoding="utf-8")
                            F.write(str(i) + "\n")
                            F.close()
                else:
                    pte1.appendPlainText(str(i))
                    if printbox.isChecked():
                        F = open("output/Star Words.txt", "a", encoding="utf-8")
                        F.write(str(i) + "\n")
                        F.close()
            if printbox.isChecked():
                # convert to JSON
                F = open("output/Star Words.txt", "r", encoding="utf-8")
                ee = F.read()
                F.close()
                path = './output/'
                filename = 'Star Words'
                data = ee
                writeToJSONFile(path, filename, data)
                """"
                #re-convert to txt
                from pprint import pprint
                with open('Star Words.json') as f:
                    data = json.load(f)
                pprint(data)
                """
            pte1.appendPlainText("")
            pte1.appendPlainText(
                "---------------------------------------------------------------------------------------------------- \n")
            # Extract Affixes
        if cbx10.isChecked():
                pte1.appendPlainText("")
                cbx5.setVisible(True)
                cbx6.setChecked(True)
                cbx6.setVisible(True)
                cbx11.setChecked(True)
                cbx11.setVisible(True)
                if printbox.isChecked():
                    F = open("output/Words affixes.txt", "w", encoding="utf-8")
                    F.write("Extracting Affixes" + "\n")
                    F.write("----------------------" + "\n")
                    F.close()
                import pyarabic.arabrepr
                arepr = pyarabic.arabrepr.ArabicRepr()
                repr = arepr.repr
                from tashaphyne.stemming import ArabicLightStemmer
                ArListem = ArabicLightStemmer()
                se = Text(tt)
                p = se.words
                pte1.appendPlainText(
                    "     ---------------------------------- Extracting Affixes ----------------------------------    \n")
                ls = []
                for entity in se.entities:
                    for i in entity:
                        ls.append(i)
                for i in p:
                    if i not in ls:
                        if i not in stp:
                            stem = ArListem.light_stem(i)
                            aff=str(ArListem.get_affix())
                            pte1.appendPlainText(aff)
                            if printbox.isChecked():
                                F = open("output/Words affixes.txt", "a", encoding="utf-8")
                                F.write(str(aff) + "\n")
                                F.close()
                        else:
                            pte1.appendPlainText(str(i))
                            if printbox.isChecked():
                                F = open("output/Words affixes.txt", "a", encoding="utf-8")
                                F.write(str(i) + "\n")
                                F.close()
                    else:
                        pte1.appendPlainText(str(i))
                        if printbox.isChecked():
                            F = open("output/Words affixes.txt", "a", encoding="utf-8")
                            F.write(str(i) + "\n")
                            F.close()
                if printbox.isChecked():
                    # convert to JSON
                    F = open("output/Words affixes.txt", "r", encoding="utf-8")
                    ee = F.read()
                    F.close()
                    path = './output/'
                    filename = 'Words affixes'
                    data = ee
                    writeToJSONFile(path, filename, data)
                    """"
                    #re-convert to txt
                    from pprint import pprint
                    with open('Words affixes.json') as f:
                        data = json.load(f)
                    pprint(data)
                    """
                pte1.appendPlainText("")
                pte1.appendPlainText(
                    "---------------------------------------------------------------------------------------------------- \n")
        if cbx15.isChecked():
          try:
            # shakkala
            pte1.appendPlainText("")
            input_text = tt

            folder_location = './'

            # create Shakkala object
            sh = Shakkala(folder_location, version=3)

            # prepare input
            input_int = sh.prepare_input(input_text)

            print("finished preparing input")

            print("start with model")
            if printbox.isChecked():
                F = open("output/Vocalized text.txt", "w", encoding="utf-8")
                F.write("Text Vocalsisation" + "\n")
                F.write("----------------------" + "\n")
                F.close()

            model, graph = sh.get_model()

            with graph.as_default():
                logits = model.predict(input_int)[0]

                print("prepare and print output")
                predicted_harakat = sh.logits_to_text(logits)

                final_output = sh.get_final_text(input_text, predicted_harakat)
                pte1.appendPlainText(
                    "     ----------------------------------  Text Vocalsisation ----------------------------------    \n")
                pte1.appendPlainText(final_output)
                if printbox.isChecked():
                    F = open("output/Vocalized text.txt", "a", encoding="utf-8")
                    F.write(str(final_output) + "\n")
                    F.close()
                if printbox.isChecked():
                    # convert to JSON
                    F = open("output/Vocalized text.txt", "r", encoding="utf-8")
                    ee = F.read()
                    F.close()
                    path = './output/'
                    filename = 'Vocalized text'
                    data = ee
                    writeToJSONFile(path, filename, data)
                    """"
                    #re-convert to txt
                    from pprint import pprint
                    with open('Vocalized text.json') as f:
                        data = json.load(f)
                    pprint(data)
                    """
                pte1.appendPlainText("")
                pte1.appendPlainText(
                    "---------------------------------------------------------------------------------------------------- \n")
                print("finished successfully")
          except:
              mb1 = QMessageBox.warning(root, "Oversize", "Please Enter at most 315 character  !")
        if cbx12.isChecked():
          try:
                # shakkala
                pte1.appendPlainText("")
                input_text = tt

                folder_location = './'

                # create Shakkala object
                sh = Shakkala(folder_location, version=3)

                # prepare input
                input_int = sh.prepare_input(input_text)

                print("finished preparing input")

                print("start with model")

                model, graph = sh.get_model()
                if printbox.isChecked():
                    F = open("output/Semi-vocalized text.txt", "w", encoding="utf-8")
                    F.write("Text Semi-Vocalisation" + "\n")
                    F.write("----------------------" + "\n")
                    F.close()

                with graph.as_default():
                    logits = model.predict(input_int)[0]

                    print("prepare and print output")
                    predicted_harakat = sh.logits_to_text(logits)

                    final_output = sh.get_final_text(input_text, predicted_harakat)
                    pte1.appendPlainText(
                        "     ---------------------------------- Text Semi-Vocalisation ----------------------------------    \n")
                    reduced = araby.reduce_tashkeel(final_output)
                    pte1.appendPlainText(reduced)
                    if printbox.isChecked():
                        F = open("output/Semi-vocalized text.txt", "a", encoding="utf-8")
                        F.write(str(reduced) + "\n")
                        F.close()
                    if printbox.isChecked():
                        # convert to JSON
                        F = open("output/Semi-vocalized text.txt", "r", encoding="utf-8")
                        ee = F.read()
                        F.close()
                        path = './output/'
                        filename = 'Semi-vocalized text'
                        data = ee
                        writeToJSONFile(path, filename, data)
                        """"
                        #re-convert to txt
                        from pprint import pprint
                        with open('Semi-vocalized text.json') as f:
                            data = json.load(f)
                        pprint(data)
                        """
                    pte1.appendPlainText("")
                    pte1.appendPlainText(
                        "---------------------------------------------------------------------------------------------------- \n")
                    print("finished successfully")
          except:
              mb1 = QMessageBox.warning(root, "Oversize", "Please Enter at most 315 character  !")
        if cbx13.isChecked():
                    pte1.appendPlainText("")
                    if printbox.isChecked():
                        F = open("output/Text with Strip Vocalisation.txt", "w", encoding="utf-8")
                        F.write("Strip Vocalisation" + "\n")
                        F.write("----------------------" + "\n")
                        F.close()
                    pte1.appendPlainText(
                        "     ---------------------------------- Strip Vocalisation ----------------------------------    \n")
                    from pyarabic.araby import strip_tashkeel
                    reduced = araby.strip_tashkeel(tt)
                    pte1.appendPlainText(reduced)
                    if printbox.isChecked():
                        F = open("output/Text with Strip Vocalisation.txt", "a", encoding="utf-8")
                        F.write(str(reduced) + "\n")
                        F.close()
                    if printbox.isChecked():
                        # convert to JSON
                        F = open("output/Text with Strip Vocalisation.txt", "r", encoding="utf-8")
                        ee = F.read()
                        F.close()
                        path = './output/'
                        filename = 'Text with Strip Vocalisation'
                        data = ee
                        writeToJSONFile(path, filename, data)
                        """"
                        #re-convert to txt
                        from pprint import pprint
                        with open('Text with Strip Vocalisation.json') as f:
                            data = json.load(f)
                        pprint(data)
                        """
                    pte1.appendPlainText(
                        "---------------------------------------------------------------------------------------------------- \n")
        if cbx14.isChecked():
                    pte1.appendPlainText("")
                    if printbox.isChecked():
                        F = open("output/Text with normalized hamza.txt", "w", encoding="utf-8")
                        F.write("Normalize_Hamza" + "\n")
                        F.write("----------------------" + "\n")
                        F.close()
                    pte1.appendPlainText(
                        "     ---------------------------------- Normalize_Hamza ----------------------------------    \n")
                    from pyarabic.araby import normalize_hamza
                    pp = normalize_hamza(tt)
                    pte1.appendPlainText(pp)
                    if printbox.isChecked():
                        F = open("output/Text with normalized hamza.txt", "a", encoding="utf-8")
                        F.write(str(pp) + "\n")
                        F.close()
                    if printbox.isChecked():
                        # convert to JSON
                        F = open("output/Text with normalized hamza.txt", "r", encoding="utf-8")
                        ee = F.read()
                        F.close()
                        path = './output/'
                        filename = 'Text with normalized hamza'
                        data = ee
                        writeToJSONFile(path, filename, data)
                        """"
                        #re-convert to txt
                        from pprint import pprint
                        with open('Text with normalized hamza.json') as f:
                            data = json.load(f)
                        pprint(data)
                        """
                    pte1.appendPlainText(
                        "---------------------------------------------------------------------------------------------------- \n")
        if cbx16.isChecked():

            import pyarabic.number
            pte1.appendPlainText("")
            if printbox.isChecked():
                F = open("output/Number written in letters.txt", "w", encoding="utf-8")
                F.write("Writing in letters" + "\n")
                F.write("----------------------" + "\n")
                F.close()
            pte1.appendPlainText(
                "     ---------------------------------- Writing in letters ----------------------------------    \n")
            an = pyarabic.number.ArNumbers()
            num1=an.int2str(ee)
            if printbox.isChecked():
                F = open("output/Number written in letters.txt", "a", encoding="utf-8")
                F.write(str(num1) + "\n")
                F.close()
            if printbox.isChecked():
                # convert to JSON
                F = open("output/Number written in letters.txt", "r", encoding="utf-8")
                ee = F.read()
                F.close()
                path = './output/'
                filename = 'Number written in letters'
                data = ee
                writeToJSONFile(path, filename, data)
                """"
                #re-convert to txt
                from pprint import pprint
                with open('Number written in letters.json') as f:
                    data = json.load(f)
                pprint(data)
                """
            pte1.appendPlainText(str(num1))
            pte1.appendPlainText(
                "---------------------------------------------------------------------------------------------------- \n")
        if cbx17.isChecked():
            from pyarabic.number import text2number
            pte1.appendPlainText("")
            if printbox.isChecked():
                F = open("output/Text written in numbers.txt", "w", encoding="utf-8")
                F.write("Writing in Numbers" + "\n")
                F.write("----------------------" + "\n")
                F.close()
            pte1.appendPlainText(
                "     ---------------------------------- Writing in Numbers ----------------------------------    \n")
            num2=text2number(ee)
            pte1.appendPlainText(str(num2))
            if printbox.isChecked():
                F = open("output/Text written in numbers.txt", "a", encoding="utf-8")
                F.write(str(num2) + "\n")
                F.close()
            if printbox.isChecked():
                # convert to JSON
                F = open("output/Text written in numbers.txt", "r", encoding="utf-8")
                ee = F.read()
                F.close()
                path = './output/'
                filename = 'Text written in numbers'
                data = ee
                writeToJSONFile(path, filename, data)
                """"
                #re-convert to txt
                from pprint import pprint
                with open('Text written in numbers.json') as f:
                    data = json.load(f)
                pprint(data)
                """
            pte1.appendPlainText(
                "---------------------------------------------------------------------------------------------------- \n")
        if cbx18.isChecked():
            from pyarabic.number import extract_number_context
            pte1.appendPlainText("")
            if printbox.isChecked():
                F = open("output/Extract Numbers with Context.txt", "w", encoding="utf-8")
                F.write("Extract Numbers with Context" + "\n")
                F.write("----------------------" + "\n")
                F.close()
            pte1.appendPlainText(
                "     ---------------------------------- Extract Numbers with Context ----------------------------------    \n")
            num3=extract_number_context(ee)
            pte1.appendPlainText(str(num3))
            if printbox.isChecked():
                F = open("output/Extract Numbers with Context.txt", "a", encoding="utf-8")
                F.write(str(num3) + "\n")
                F.close()
            if printbox.isChecked():
                # convert to JSON
                F = open("output/Extract Numbers with Context.txt", "r", encoding="utf-8")
                ee = F.read()
                F.close()
                path = './output/'
                filename = 'Extract Numbers with Context'
                data = ee
                writeToJSONFile(path, filename, data)
                """"
                #re-convert to txt
                from pprint import pprint
                with open('Extract Numbers with Context.json') as f:
                    data = json.load(f)
                pprint(data)
                """
            pte1.appendPlainText(
                "---------------------------------------------------------------------------------------------------- \n")
        if cbx19.isChecked():
            from pyarabic.number import extract_number_phrases
            pte1.appendPlainText("")
            pte1.appendPlainText(
                "     ---------------------------------- Extract Numbers Text  ----------------------------------    \n")
            num4 = extract_number_phrases(ee)
            pte1.appendPlainText(str(num4))
            if printbox.isChecked():
                F = open("output/Extract Numbers text.txt", "w", encoding="utf-8")
                F.write("Extract Numbers Text" + "\n")
                F.close()
            if printbox.isChecked():
                F = open("output/Extract Numbers text.txt", "a", encoding="utf-8")
                F.write(str(num4) + "\n")
                F.close()
            if printbox.isChecked():
                # convert to JSON
                F = open("output/Extract Numbers text.txt", "r", encoding="utf-8")
                ee = F.read()
                F.close()
                path = './output/'
                filename = 'Extract Numbers text'
                data = ee
                writeToJSONFile(path, filename, data)
                """"
                #re-convert to txt
                from pprint import pprint
                with open('Extract Numbers text.json') as f:
                    data = json.load(f)
                pprint(data)
                """
            pte1.appendPlainText(
                "---------------------------------------------------------------------------------------------------- \n")

        if hiden1.isChecked():
            pte1.setPlainText("")
            if printbox.isChecked():
                F = open("output/Segmentation.txt", "w", encoding="utf-8")
                F.write("Segmentation" + "\n")
                F.write("----------------------" + "\n")
                F.close()
            pte1.appendPlainText(
                "------------------------------------- Segmentation --------------------------------------------------------------- \n")
            if (bt3.isVisible() == False):
                x = open(gg, "r", encoding="utf-8")
                text = ""

                for line in x:
                    text = text + line
                t = text.split()

                temp1 = open("temp1.txt", "w", encoding="utf-8")
                temp2 = open("temp2.txt", "w", encoding="utf-8")

                outstr = """"""
                ner = """"""

                for word in t:
                    # print("word : ",word)
                    if word not in NER_list_added:
                        temp1 = open("temp1.txt", "w", encoding="utf-8")
                        temp1.write(word)

                    else:
                        temp2 = open("temp2.txt", "w", encoding="utf-8")
                        temp2.write(word + " ")
                        ner = word

                    temp1.close()
                    temp2.close()

                    s = segmenter.segment_file('temp1.txt')
                    temp1 = open("temp1.txt", "w", encoding="utf-8")
                    temp1.truncate()
                    temp1.close()

                    outstr += ner + " " + s.strip() + " "
                    ner = ""
                    s = ""

                outfile = open("outfile.txt", "w", encoding="utf-8")
                outfile.write(outstr.strip(''))
                outfile.close()
                pte1.appendPlainText(str(outstr))
            else:
                x = open("sample.txt", "r", encoding="utf-8")

                text = ""

                for line in x:
                    text = text + line
                t = text.split()

                temp1 = open("temp1.txt", "w", encoding="utf-8")
                temp2 = open("temp2.txt", "w", encoding="utf-8")

                outstr = """"""
                ner = """"""

                for word in t:
                    # print("word : ",word)
                    if word not in NER_list_added:
                        temp1 = open("temp1.txt", "w", encoding="utf-8")
                        temp1.write(word)

                    else:
                        temp2 = open("temp2.txt", "w", encoding="utf-8")
                        temp2.write(word + " ")
                        ner = word

                    temp1.close()
                    temp2.close()

                    s = segmenter.segment_file('temp1.txt')
                    temp1 = open("temp1.txt", "w", encoding="utf-8")
                    temp1.truncate()
                    temp1.close()

                    outstr += ner + " " + s.strip() + " "
                    ner = ""
                    s = ""

                outfile = open("outfile.txt", "w", encoding="utf-8")
                outfile.write(outstr.strip(''))
                outfile.close()
                pte1.appendPlainText(str(outstr))
            if printbox.isChecked():
                F = open("output/Segmentation.txt", "a", encoding="utf-8")
                F.write(outstr + "\n")
                F.close()
            if printbox.isChecked():
                # convert to JSON
                F = open("output/Segmentation.txt", "r", encoding="utf-8")
                ee = F.read()
                F.close()
                path = './output/'
                filename = 'Segmentation'
                data = ee
                writeToJSONFile(path, filename, data)
                """"
                #re-convert to txt
                from pprint import pprint
                with open('Segmentation.json') as f:
                    data = json.load(f)
                pprint(data)
                """
            pte1.appendPlainText(
                "---------------------------------------------------------------------------------------------------- \n")
        if hiden2.isChecked():

            pte1.setPlainText("")
            if printbox.isChecked():
                F = open("output/POS tagging.txt", "w", encoding="utf-8")
                F.write("POS Tagging" + "\n")
                F.write("----------------------" + "\n")
                F.close()
            pte1.appendPlainText(
                "------------------------------------- POS Tagging --------------------------------------------------------------- \n")
            tagger = STag.StanfordPOSTagger('arabic.tagger',
                                            'stanford-postagger-full-2018-10-16/stanford-postagger.jar')
            aa = segmenter.segment_file('sample.txt')
            for tag in tagger.tag(aa.split()):
                list = ""
                list = list + " " + tag[1]
                list = list.replace('/',': ')
                list = list.replace('CD', ' عدد أصلي.')
                list = list.replace('IN', ' ضمير متصل.')
                list = list.replace('NN', ' اسم مفرد.')
                list = list.replace('VBP', ' فعل ماضي يعود لضمير مفرد.')
                list = list.replace('CC', ' ضمير منفصل.')
                list = list.replace('PRP', ' ضمير للمخاطب أو للغائب.')
                list = list.replace('P', ' اسم علم.')
                list = list.replace('DT', ' اسم حر.')
                list = list.replace('VBD', ' فعل ماض منصوب.')
                pte1.appendPlainText(list)

                if printbox.isChecked():
                    F = open("output/POS tagging.txt", "a", encoding="utf-8")
                    F.write(str(tag[1]) + "\n")
                    F.close()
            if printbox.isChecked():
                # convert to JSON
                F = open("output/POS tagging.txt", "r", encoding="utf-8")
                ee = F.read()
                F.close()
                path = './output/'
                filename = 'POS tagging'
                data = ee
                writeToJSONFile(path, filename, data)
                """"
                #re-convert to txt
                from pprint import pprint
                with open('POS tagging.json') as f:
                    data = json.load(f)
                pprint(data)
                """
            pte1.appendPlainText(
                "---------------------------------------------------------------------------------------------------- \n")
        if hiden3.isChecked():
            pte1.setPlainText("")
            if printbox.isChecked():
                F = open("output/NER.txt", "w", encoding="utf-8")
                F.write("Named Entity Recognition" + "\n")
                F.write("----------------------" + "\n")
                F.close()
            pte1.appendPlainText(
                "------------------------------------ Named Entity Recognition---------------------------------------------------------------- \n")
            ner = Text(tt)
            for sent in ner.sentences:
                pte1.appendPlainText(str(sent))
                if printbox.isChecked():
                    F = open("output/NER.txt", "a", encoding="utf-8")
                    F.write(str(sent) + "\n")
                    F.close()
                for entity in sent.entities:
                    pte1.appendPlainText(str(entity.tag) + " " + str(entity))
                    if printbox.isChecked():
                        F = open("output/NER.txt", "a", encoding="utf-8")
                        F.write(str(entity.tag) + " " + str(entity) + "\n")
                        F.close()
                for word in ner.words:
                    if (word in NER_list_added):
                        pte1.appendPlainText("I-LOC ['" + word + "']")
                    if printbox.isChecked():
                        if (word in NER_list_added):
                            F = open("output/NER.txt", "a", encoding="utf-8")
                            F.write("I-LOC ['" + word + "']""\n")
                            F.close()
                for word in ner.words:
                    if (word in Money):
                        pte1.appendPlainText("I-MONEY ['" + word + "']")
                    if printbox.isChecked():
                        if (word in Money):
                            F = open("output/NER.txt", "a", encoding="utf-8")
                            F.write("I-MONEY ['" + word + "']""\n")
                            F.close()
                if printbox.isChecked():
                    # convert to JSON
                    F = open("output/NER.txt", "r", encoding="utf-8")
                    ee = F.read()
                    F.close()
                    path = './output/'
                    filename = 'NER'
                    data = ee
                    writeToJSONFile(path, filename, data)
                    """"
                    #re-convert to txt
                    from pprint import pprint
                    with open('NER.json') as f:
                        data = json.load(f)
                    pprint(data)
                    """
                pte1.appendPlainText("")
            pte1.appendPlainText(
                "---------------------------------------------------------------------------------------------------- \n")

        if hiden4.isChecked():
            pte1.setPlainText("")
            if printbox.isChecked():
                F = open("output/Sentence Parsing.txt", "w", encoding="utf-8")
                F.write("Sentence Parsing" + "\n")
                F.write("----------------------" + "\n")
                F.close()
            pte1.appendPlainText(
                "----------------------------------- Sentence Parsing ----------------------------------------------------------------- \n")
            parser = SParse.StanfordParser(model_path='edu/stanford/nlp/models/lexparser/arabicFactored.ser.gz')
            aa = segmenter.segment_file('sample.txt')
            sentences = parser.raw_parse_sents(aa.split('.'))
            for line in sentences:
                for sentence in line:
                    pte1.appendPlainText(str(sentence))
                    sentence.draw()
                    if printbox.isChecked():
                        F = open("output/Sentence Parsing.txt", "a", encoding="utf-8")
                        F.write(str(sentence) + "\n")
                        F.close()
            if printbox.isChecked():
                # convert to JSON
                F = open("output/Sentence Parsing.txt", "r", encoding="utf-8")
                ee = F.read()
                F.close()
                path = './output/'
                filename = 'Sentence Parsing'
                data = ee
                writeToJSONFile(path, filename, data)
                """"
                #re-convert to txt
                from pprint import pprint
                with open('Sentence Parsing.json') as f:
                    data = json.load(f)
                pprint(data)
                """
            pte1.appendPlainText(
                "---------------------------------------------------------------------------------------------------- \n")
        if (cbx1.isChecked()==False) & (cbx2.isChecked()==False) & (cbx3.isChecked()==False) & (cbx4.isChecked()==False) & (cbx8.isChecked()==False) & (cbx7.isChecked()==False) & (cbx9.isChecked()==False) & (cbx10.isChecked()==False) & (cbx15.isChecked()==False) &(cbx12.isChecked()==False) & (cbx13.isChecked()==False) & (cbx14.isChecked()==False) & (cbx16.isChecked()==False) & (cbx17.isChecked()==False) & (cbx18.isChecked()==False) & (cbx19.isChecked()==False) & (hiden4.isChecked()==False) & (hiden3.isChecked()==False) & (hiden2.isChecked()==False) & (hiden1.isChecked()==False):
            mb2=QMessageBox.warning(root,"Select fonction","Please Select a Fonction !!")
    except Exception as eee:
        mb1=QMessageBox.warning(root,"Empty Text","Please Enter an Arabic Text !")
        print(eee)

bt2.clicked.connect(ev1)
bt1.clicked.connect(ev2)
bt3.clicked.connect(ev3)
bt4.clicked.connect(ev4)
bt5.clicked.connect(ev5)
root.show()
sys.exit(a.exec_())
