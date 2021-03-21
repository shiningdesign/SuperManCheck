'''
file_input v1.0
FileLineEdit:
  * a LineEdit with built-in Import/Export/Browse

'''

# python 2,3 support unicode function
try:
    UNICODE_EXISTS = bool(type(unicode))
except NameError:
    unicode = lambda s: str(s)

try:
    from PySide import QtGui, QtCore
    import PySide.QtGui as QtWidgets
    print("PySide Try")
    qtMode = 0
except ImportError:
    try:
        from PySide2 import QtCore, QtGui, QtWidgets
        print("PySide2 Try")
        qtMode = 2
    except ImportError:
        try:
            from PyQt4 import QtGui,QtCore
            import PyQt4.QtGui as QtWidgets
            import sip
            qtMode = 1
            print("PyQt4 Try")
        except ImportError:
            from PyQt5 import QtGui,QtCore,QtWidgets
            import sip
            qtMode = 3
            print("PyQt5 Try")

import os,sys
import subprocess

class FileLineEdit(QtWidgets.QWidget):
    def __init__(self, parent=None,btn_list=[],type='',pathType='',ext='',label='',import_func='',export_func=''):
        QtWidgets.QWidget.__init__(self,parent)
        # memo
        self.parent=parent
        self.pathType = pathType
        self.ext = ext
        self.import_func=import_func
        self.export_func=export_func
        
        self.memoData={}
        self.memoData['last_import']=''
        self.memoData['last_export']=''
        self.memoData['last_browse']=''
        # UI
        self.uiList={}
        self.uiList['main_layout']=QtWidgets.QHBoxLayout();
        self.uiList['main_layout'].setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.uiList['main_layout'])
        
        self.uiList['main_label'] = QtWidgets.QLabel(label)
        self.uiList['main_layout'].addWidget(self.uiList['main_label'])
        self.uiList['main_input'] = QtWidgets.QLineEdit()
        
        self.uiList['main_layout'].addWidget(self.uiList['main_input'])
        if len(btn_list)==0:
            btn_list = ['browse','show','clear','import','export']
        
        for t in btn_list:
            self.uiList['{0}_btn'.format(t)] = QtWidgets.QPushButton(t.title())
            self.uiList['{0}_btn'.format(t)].setMaximumWidth(50)
            self.uiList['main_layout'].addWidget(self.uiList['{0}_btn'.format(t)])
            if type=='':
                if t in ['import','export']:
                    self.uiList['{0}_btn'.format(t)].setVisible(1)
            else:
                if t=='browse':
                    self.uiList['{0}_btn'.format(t)].setVisible(1)
        self.qui_policy('main_input',5,3)
        # hide ui
        
        # connect UI
        self.Establish_Connections()
    def Establish_Connections(self):
        for ui_name in self.uiList.keys():
            prefix = ui_name.rsplit('_', 1)[0]
            if ui_name.endswith('_btn'):
                if hasattr(self, prefix+"_action"):
                    self.uiList[ui_name].clicked.connect(getattr(self, prefix+"_action"))
        # drop support
        self.uiList['main_input'].installEventFilter(self)
    # the main window event filter function
    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.DragEnter:
            data = event.mimeData()
            urls = data.urls()
            if object is self.uiList['main_input'] and (urls and urls[0].scheme() == 'file'):
                event.acceptProposedAction()
            return 1
        elif event.type() == QtCore.QEvent.Drop:
            data = event.mimeData()
            urls = data.urls()
            if object is self.uiList['main_input'] and (urls and urls[0].scheme() == 'file'):
                filePath = unicode(urls[0].path())[1:]
                if self.pathType=='folder':
                    if os.path.isdir(filePath):
                        self.uiList['main_input'].setText(os.path.normpath(filePath))
                    else:
                        self.quickMsg('Require Folder as Input')
                else:
                    self.uiList['main_input'].setText(os.path.normpath(filePath))
                    
            return 1
        return 0
        
    def setText(self,txt):
        self.uiList['main_input'].setText(txt)
    def text(self):
        return unicode(self.uiList['main_input'].text())
    def setLabel(self,txt):
        self.uiList['main_label'].setText(txt)
    def label(self):
        return unicode(self.uiList['main_label'].text())
    def setReadOnly(self,state):
        self.uiList['main_input'].setReadOnly(state)
    def setImportFunc(self, import_func):
        self.import_func = import_func
    def setExportFunc(self, export_func):
        self.export_func = export_func
        
    def browse_action(self):
        if self.pathType == 'folder':
            tmp_path= self.quickFolderAsk()
            if tmp_path == '':
                return
            self.setText(tmp_path)
        else:
            file= self.quickFileAsk('import',ext=self.ext)
            if file == "":
                return
            self.setText(file)
    def show_action(self):
        file_path = self.text()
        if file_path is not None and os.path.exists(file_path):
            self.openFolder(file_path)
            
    def clear_action(self):
        self.uiList['main_input'].setText('')
        
    def export_action(self):
        filePath_input = self.uiList['main_input']
        file = unicode(filePath_input.text())
        if file == "":
            file= self.quickFileAsk('export',self.ext)
        if file == "":
            return
        # update ui
        filePath_input.setText(file)
        # export process
        if self.parent is not None:
            if self.export_func !='' and hasattr(self.parent, self.export_func):
                getattr(self.parent,self.export_func)(file)
                self.quickInfo("File: '"+file+"' creation finished.")
    
    def import_action(self):
        filePath_input = self.uiList['main_input']
        file=unicode(filePath_input.text())
        if file == "":
            file= self.quickFileAsk('import',self.ext)
        if file == "":
            return
        # check exists
        if not os.path.exists(file):
            self.quickMsg('File not exists.')
            return
        # update ui
        filePath_input.setText(file)
        # import process
        if self.parent is not None:
            if self.import_func !='' and hasattr(self.parent, self.import_func):
                getattr(self.parent,self.import_func)(file)
                self.quickInfo("File: '"+file+"' loading finished.")
        
    # support functions
    def openFolder(self, folderPath):
        if os.path.isfile(folderPath):
            folderPath = os.path.dirname(folderPath)
        if os.path.isdir(folderPath):
            cmd_list = None
            if sys.platform == 'darwin':
                cmd_list = ['open', '--', folderPath]
            elif sys.platform == 'linux2':
                cmd_list = ['xdg-open', '--', folderPath]
            elif sys.platform in ['win32','win64']:
                cmd_list = ['explorer', folderPath.replace('/','\\')]
            if cmd_list != None:
                try:
                    subprocess.check_call(cmd_list)
                except subprocess.CalledProcessError:
                    pass # handle errors in the called executable
                except OSError:
                    pass # executable not found
    def quickMsg(self,msg):
        tmpMsg = QtWidgets.QMessageBox() # for simple msg that no need for translation
        tmpMsg.setWindowTitle("Info")
        tmpMsg.setText(msg)
        tmpMsg.addButton("OK",QtWidgets.QMessageBox.YesRole)
        tmpMsg.exec_()
    def quickInfo(self, info, force=0):
        if hasattr( self.window(), "quickInfo") and force == 0:
            self.window().statusBar().showMessage(info)
    def quickFolderAsk(self,dir=None):
        if dir == None:
            dir = self.memoData['last_browse']
            if self.parent is not None and hasattr(self.parent, 'memoData'):
                dir = self.parent.memoData['last_browse']
        return unicode(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory",dir))
    def quickFileAsk(self, type, ext=None, dir=None):
        # standalone version parent access option
        if ext == None:
            ext = "RAW data (*.json);;RAW binary data (*.dat);;Format Txt (*{0});;AllFiles (*.*)".format(self.fileType)
        elif isinstance(ext, (str,unicode)):
            if ';;' not in ext:
                if ext == '':
                    ext = 'AllFiles (*.*)'
                else:
                    ext = self.extFormat(ext) + ';;AllFiles (*.*)'
        elif isinstance(ext, (tuple,list)):
            if len(ext) > 0 and isinstance(ext[0], (tuple,list)):
                tmp_list = [self.extFormat(x) for x in ext]
                tmp_list.append('AllFiles (*.*)')
                ext = ';;'.join(tmp_list)
            else:
                ext = ';;'.join([self.extFormat(x) for x in ext].append('AllFiles(*.*)')) 
        elif isinstance(ext, dict):
            tmp_list = [self.extFormat(x) for x in ext.items()]
            tmp_list.append('AllFiles (*.*)')
            ext = ';;'.join(tmp_list)
        else:
            ext = "AllFiles (*.*)"
        file = ''
        if type == 'export':
            if dir == None:
                dir = self.memoData['last_export']
                if self.parent is not None and hasattr(self.parent, 'memoData'):
                    dir = self.parent.memoData['last_export']
            file = QtWidgets.QFileDialog.getSaveFileName(self, "Save File",dir,ext)
        elif type == 'import':
            if dir == None:
                dir = self.memoData['last_import']
                if self.parent is not None and hasattr(self.parent, 'memoData'):
                    dir = self.parent.memoData['last_import']
            file = QtWidgets.QFileDialog.getOpenFileName(self, "Open File",dir,ext)
        if isinstance(file, (list, tuple)):
            file = file[0] # for deal with pyside case
        else:
            file = unicode(file) # for deal with pyqt case
        # save last dir in memoData
        if file != '':
            if type == 'export':
                self.memoData['last_export'] = os.path.dirname(file) #QFileInfo().path()
                if self.parent is not None and hasattr(self.parent, 'memoData'):
                    self.parent.memoData['last_export'] = os.path.dirname(file)
            elif type == 'import':
                self.memoData['last_import'] = os.path.dirname(file)
                if self.parent is not None and hasattr(self.parent, 'memoData'):
                    self.parent.memoData['last_import'] = os.path.dirname(file)
        return file
    def extFormat(self, ext):
        if isinstance(ext, (tuple,list)):
            ext = '{0} (*.{1})'.format(ext[1],ext[0])
        else:
            if ext.startswith('.'):
                ext = ext[1:]
            ext = '{0} (*.{0})'.format(ext)
        return ext
    def qui_policy(self, ui_list, w, h):
        # reference value
        policyList = ( 
            QtWidgets.QSizePolicy.Fixed, 
            QtWidgets.QSizePolicy.Minimum, 
            QtWidgets.QSizePolicy.Maximum, 
            QtWidgets.QSizePolicy.Preferred, 
            QtWidgets.QSizePolicy.Expanding, 
            QtWidgets.QSizePolicy.MinimumExpanding, 
            QtWidgets.QSizePolicy.Ignored,
        )
        # 0 = fixed; 1 > min; 2 < max; 3 = prefered; 4 = <expanding>; 5 = expanding> Aggresive; 6=4 ignored size input
        if not isinstance(ui_list, (list, tuple)):
            ui_list = [ui_list]
        for each_ui in ui_list:
            if isinstance(each_ui, str):
                each_ui = self.uiList[each_ui]
            each_ui.setSizePolicy(policyList[w],policyList[h])