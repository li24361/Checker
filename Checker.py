# -*- coding: utf-8 -*-

"""
Module implementing CheckTool.
"""
import sys,threading
from PyQt4 import QtGui
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature
import os
reload(sys)
sys.setdefaultencoding("utf-8")
from PIL import Image

from Ui_Checker import Ui_Dialog

class CheckTool(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
    
    @pyqtSignature("")
    def on_check_clicked(self):
        rootDir = self.lineEdit.text()
        dir = unicode(rootDir, 'utf-8')
        if os.path.exists(dir):
            self.printLog(u"--------------检测开始！----------------")
            #self.checkDir(dir)
            thread = threading.Thread(target = self.checkDir(dir))
            thread.setDaemon(True)
            thread.start()
            self.printLog(u"--------------检测结束！----------------")


        else :
           self.printLog(u"--------------请选择有效文件夹！！----------------")


    @pyqtSignature("")
    def on_file_clicked(self):
        s = QtGui.QFileDialog.getExistingDirectory(self,u"选择文件夹","/")
        self.lineEdit.setText(unicode(s , "utf8"))

    def checkDir(self,rootDir):
        list_dirs = os.walk(rootDir)
        for root, dirs, files in list_dirs:
            # for d in dirs:
            #     print os.path.join(root, d)
            for f in files:
                if f.endswith('.jpg') or f.endswith('.png'):
                    self.checkPic( os.path.join(root, f))
                if f.endswith('.txt'):
                    self.checkTxt(os.path.join(root, f))


    def checkPic(self,PicPath):
        file = os.path.basename(PicPath)
        size = os.path.getsize(PicPath)
        #返回图形对象
        im = Image.open(PicPath)
        #获取图片宽高
        iw, ih = im.size

        ##1-2-3-4-像素1100*1390（≤300KB）
        if file.startswith("1") or file.startswith("2") or file.startswith("3") or file.startswith("4") or file.startswith("15"):
            if size > 300*1024:
                msg  = u"%s 文件大小为%d，超出规定大小300KB " % (PicPath,size)
                self.printLog(msg)
            if iw > 1100 or ih >1390:
                msg = u"%s 文件像素为%d*%d，不符合规定大小1100*1390！"% (PicPath,iw,ih)
                self.printLog(msg)

        ##5-7-像素235*297 （≤30KB）
        if file.startswith("5") or file.startswith("7"):
            if size > 30*1024:
                msg  =  u"%s文件大小为%d，超出规定大小300KB " % (PicPath,size)
                self.printLog(msg)
            if iw > 235 or ih >297:
                msg = u"%s 文件像素为%d*%d，不符合规定大小235*297！"% (PicPath,iw,ih)
                self.printLog(msg)

        ##6-像素750*10000px，≤2MB
        if file.startswith("6"):
            if size > 2*1024*1024:
                msg  = u"%s 文件大小为%d，超出规定大小2MB " % (PicPath,size)
                self.printLog(msg)
            if iw > 750 or ih >10000:
                msg = u" %s 文件像素为%d*%d，不符合规定大小750*10000！"% (PicPath,iw,ih)
                self.printLog(msg)




    def checkTxt(self,TxtPath):
        file = open(TxtPath,'r')
        for (num,line) in enumerate(file):
            if line.find("taobao.com")!=-1 or line.find("tmall.com")!=-1:
                msg = u"%s 文件中第%d行包含字符串 taobao.com或者tmall.com，请检查！"% (TxtPath,num)
                self.printLog(msg)
        file.close()
 
    def printLog(self,msg):
        self.textBrowser.append(msg)
        self.textBrowser.moveCursor(QtGui.QTextCursor.End)

        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ck = CheckTool()
    ck.show()
    sys.exit(app.exec_())
