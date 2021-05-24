import os, sys

from SuperManCheck_template_2010 import *
import SuperManCheck_FileLineEdit as FileLineEdit
import SuperManCheck_LNTextEdit as LNTextEdit

#=======================================
#  scandir module check
#=======================================
'''
try:
    from os import scandir, walk
    print('try local py3.x: scandir')
except ImportError:
'''
try:
    from scandir import scandir, walk
    print('try local: scandir')
except ImportError:
    print('missing scandir')
#############################################
# User Class creation
#############################################
version = '2.0'
date = '2021.05.24'
log = '''
#------------------------------
by shining ying
https://github.com/shiningdesign/
v2.0: (2021.05.24)
  * fix error on empty script string
v1.9: (2021.03.16)
  * better local config check
v1.6: (2021.03.09)
  * add method option
  * add preview method
v1.5: (2021.03.08)
  * add fix method choice
v1.0: (2021.03.08)
  * add virus fixer fix
v0.2: (2020.06.29)
  * add scriptNode, fopen,fclose,fprint keyword detection 
  * code standalonization
v0.1: (2020.06.27)
  * notes here
#------------------------------
'''
help = '''
wip
'''
# --------------------
#  user module list
# --------------------

class SuperManCheck(UniversalToolUI):
    def __init__(self, parent=None, mode=0):
        UniversalToolUI.__init__(self, parent)
        
        # class variables
        self.version= version
        self.date = date
        self.log = log
        self.help = help
        
        # mode: example for receive extra user input as parameter
        self.mode = 0
        if mode in [0,1]:
            self.mode = mode # mode validator
        # Custom user variable
        #------------------------------
        # initial data
        #------------------------------
        self.memoData['data']=[]
        self.memoData['settingUI']=[]
        self.qui_user_dict = {} # e.g: 'edit': 'LNTextEdit',
        
        if isinstance(self, QtWidgets.QMainWindow):
            self.setupMenu()
        self.setupWin()
        self.setupUI()
        self.Establish_Connections()
        self.loadLang()
        self.loadData()
        
    #------------------------------
    # overwrite functions
    #------------------------------
    def setupMenu(self):
        self.qui_menubar('file_menu;&File | setting_menu;&Setting | help_menu;&Help')
        
        info_list = ['export', 'import','user']
        info_item_list = ['{0}Config_atn;{1} Config (&{2}),Ctrl+{2}'.format(info,info.title(),info.title()[0]) for info in info_list]+['_']
        self.qui_menu('|'.join(info_item_list), 'setting_menu')
        # toggle on top
        self.qui_menu('toggleTop_atn;Toggle Always-On-Top', 'setting_menu')
        # default help menu
        super(self.__class__,self).setupMenu()
    
    def setupWin(self):
        super(self.__class__,self).setupWin()
        # self.setGeometry(500, 300, 250, 110) # self.resize(250,250)
        if hostMode == "desktop":
            QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Cleanlooks'))
        self.setStyleSheet("QLineEdit:disabled{background-color: gray;}")
        
    def setupUI(self):
        super(self.__class__,self).setupUI('vbox')
        #------------------------------
        # user ui creation part
        #------------------------------
        self.uiList['maya_browse'] = FileLineEdit.FileLineEdit(self,btn_list=['browse','show','clear'],label='Open Maya File Safely:')
        # self.qui('super_localCheck_btn;Local Machine Config Check and Rename Issue file | super_vaccination_btn;Inject Local vaccination (no affection by virus but you still need to clean it) | super_check_space', 'super_check_grp;hbox;Local Config Check')
        self.qui('super_localCheck_btn;Local Machine Config Check and Rename Issue file | super_check_space', 'super_check_grp;hbox;Local Config Check')
        self.qui('maya_browse | super_openMayaSafe_btn;Open Maya with Safe Mask', 'super_open_layout;hbox')
        self.uiList['maya_input'] = self.uiList['maya_browse'].uiList['main_input']
        self.qui('super_checkCurrentMayaFile_btn;Check and Fix Current Maya File | super_fix_space', 'super_fix_layout;hbox')
        self.qui('super_open_layout | super_fix_layout', 'super_maya_grp;vbox;Current Maya Scene Check (Inside Maya)')
        
        # batch
        self.uiList['root_browse'] = FileLineEdit.FileLineEdit(self,btn_list=['browse','show','clear'],label='Root Path for all Maya file:',pathType='folder')
        self.uiList['root_input'] = self.uiList['root_browse'].uiList['main_input']
        self.qui('root_browse | super_batchFileCheck_btn;Batch Scan | super_batchFileCheck_count_check;Count File Only', 'super_batch_1_layout;hbox')
        self.qui('super_batchMethod_label;Fix Method: | super_batchMethod_choice;(Fix File and backup old as _issueTmp,Scan Only and Do Nothing) | super_batchMethod_space','super_batch_2_layout;hbox')
        #Dont touch file and fix as _tmpFix.ma_mb,
        self.qui('super_batch_1_layout | super_batch_2_layout','super_batch_grp;vbox;Batch Maya Scan with deep reference check (Run in Maya)')
        
        
        self.uiList['super_lockCheck_edit']=LNTextEdit.LNTextEdit()
        self.qui('super_check_grp | super_maya_grp | super_batch_grp | super_lockCheck_edit ', 'main_layout')
        
        self.uiList['super_batchFileCheck_count_check'].setChecked(1)
        # hide
        # if hostMode!='maya':
        #    self.uiList['super_maya_grp'].setHidden(1)
        
        self.memoData['settingUI']=[]
        #------------- end ui creation --------------------
        keep_margin_layout = ['main_layout']
        keep_margin_layout_obj = []
        # add tab layouts
        for each in self.uiList.values():
            if isinstance(each, QtWidgets.QTabWidget):
                for i in range(each.count()):
                    keep_margin_layout_obj.append( each.widget(i).layout() )
        for name, each in self.uiList.items():
            if isinstance(each, QtWidgets.QLayout) and name not in keep_margin_layout and not name.endswith('_grp_layout') and each not in keep_margin_layout_obj:
                each.setContentsMargins(0, 0, 0, 0)
        self.quickInfo('Ready')
        # self.statusBar().hide()
        
    def Establish_Connections(self):
        super(self.__class__,self).Establish_Connections()
        # custom ui response
        # shortcut connection
        self.hotkey = {}
        # self.hotkey['my_key'] = QtWidgets.QShortcut(QtGui.QKeySequence( "Ctrl+1" ), self)
        # self.hotkey['my_key'].activated.connect(self.my_key_func)
        
    def loadData(self):
        print("Load data")
        # load config
        config = {}
        config['root_name'] = 'root_default_name'
        # ban word for keyword
        config['keyword']=['PuTianTongQing','fopen','fprint','fclose','with open','.write','makedirs','shutil','copyfile']
        config['appPath']={}
        t_user_dir = os.path.expanduser('~')
        
        # - userSetup.mel
        config['appPath']['local_userSetup'] = os.path.join(t_user_dir, 'Documents', 'maya', 'scripts', 'userSetup.mel')
        if 'Documents' in t_user_dir:
            config['appPath']['local_userSetup'] = os.path.join(t_user_dir, 'maya', 'scripts', 'userSetup.mel')
        
        local_config_root = os.path.join(t_user_dir, 'Documents', 'maya')
        if 'Documents' in t_user_dir:
            local_config_root = os.path.join(t_user_dir, 'maya')
        # - userSetup.py + mel for all version and global script
        config['appPath']['local_setup'] =[ os.path.join(local_config_root, 'scripts', 'userSetup.*'), os.path.join(local_config_root, '*', 'scripts', 'userSetup.*')]
        
        # - plugin
        config['appPath']['local_plugin'] = r'C:\Program Files\Autodesk\Maya*\resources\l10n\*\plug-ins\animImportExport.pres.mel'
        
        # overload config file if exists next to it
        # then, save merged config into self.memoData['config']
        prefix, ext = os.path.splitext(self.location)
        config_file = prefix+'_config.json'
        if os.path.isfile(config_file):
            external_config = self.readDataFile(config_file)
            print('info: External config file found.')
            if isinstance( external_config, dict ):
                self.memoData['config'] = self.dict_merge(config, external_config, addKey=1)
                print('info: External config merged.')
            else:
                self.memoData['config'] = config
                print('info: External config is not a dict and ignored.')
        else:
            self.memoData['config'] = config
        
        # load user setting
        user_setting = {}
        if self.mode == 0:
            # for standalone mode only
            user_dirPath = os.path.join(os.path.expanduser('~'), 'Tool_Config', self.__class__.__name__)
            user_setting_filePath = os.path.join(user_dirPath, 'setting.json')
            if os.path.isfile(user_setting_filePath):
                user_setting = self.readDataFile(user_setting_filePath)
                if 'sizeInfo' in user_setting:
                    self.setGeometry(*user_setting['sizeInfo'])
        # custome setting loading here
        preset = {}
        for ui in self.memoData['settingUI']:
            if ui in user_setting:
                preset[ui]=user_setting[ui]
        #self.updateUI(preset)
        
    def closeEvent(self, event):
        if self.mode == 0:
            # for standalone mode only
            user_dirPath = os.path.join(os.path.expanduser('~'), 'Tool_Config', self.__class__.__name__)
            if not os.path.isdir(user_dirPath):
                try: 
                    os.makedirs(user_dirPath)
                except OSError:
                    print('Error on creation user data folder')
            if not os.path.isdir(user_dirPath):
                print('Fail to create user dir.')
                return
            # save setting
            user_setting = {}
            geoInfo = self.geometry()
            user_setting['sizeInfo'] = [geoInfo.x(), geoInfo.y(), geoInfo.width(), geoInfo.height()]
            # custome setting saving here
            for ui in self.memoData['settingUI']:
                if ui.endswith('_choice'):
                    user_setting[ui] = unicode(self.uiList[ui].currentText())
                elif ui.endswith('_check'):
                    user_setting[ui] = self.uiList[ui].isChecked()
                elif ui.endswith('_input'):
                    user_setting[ui] = unicode(self.uiList[ui].text())
                elif ui.endswith('_tab'):
                    user_setting[ui] = self.uiList[ui].currentIndex()
            user_setting_filePath = os.path.join(user_dirPath, 'setting.json')
            self.writeDataFile(user_setting, user_setting_filePath)
        
    # - example button functions
    def updateUI(self, preset):
        for ui_name in preset:
            if ui_name.endswith('_choice'):
                if preset[ui_name] != '':
                    the_idx = self.uiList[ui_name].findText(preset[ui_name])
                    if the_idx != -1:
                        self.uiList[ui_name].setCurrentIndex(the_idx)
            elif ui_name.endswith('_check'):
                self.uiList[ui_name].setChecked(preset[ui_name])
            elif ui_name.endswith('_input'):
                if preset[ui_name] != '':
                    self.uiList[ui_name].setText(preset[ui_name])
            elif ui_name.endswith('_tab'):
                self.uiList[ui_name].setCurrentIndex(preset[ui_name])
    def super_vaccination_action(self):
        # only for the putiantongqing, better just kill it.
        cur_edit = self.uiList['super_lockCheck_edit']
        cur_edit.clear()
        config = self.memoData['config']
        vaccination_text = 'global int $autoUpdateAttrEd_aoto_int;$autoUpdateAttrEd_aoto_int = -1;'
        local_mel = os.path.normpath(config['appPath']['local_userSetup'])
        print(local_mel)
        if not os.path.isfile(local_mel):
            self.writeTextFile(vaccination_text, local_mel)
        if os.path.isfile(local_mel):
            mel_text =  self.readTextFile(local_mel)
            if vaccination_text not in mel_text:
                self.writeTextFile(mel_text+'\n\n'+vaccination_text, local_mel)
        if os.path.isfile(local_mel):
            mel_text =  self.readTextFile(local_mel)
            if vaccination_text in mel_text:
                cur_edit.setText('vaccination is done')
            else:
                cur_edit.setText('vaccination failed')
        else:
            cur_edit.setText('vaccination failed')
    def super_localCheck_action(self):
        config = self.memoData['config']
        error_file_list = []
        
        
        
        '''
        local_mel = self.getOptionPath(config['appPath'], 'local_userSetup')
        if local_mel and os.path.isfile(local_mel):
            # print(local_mel)
            has_issue = self.check_file_with_keyword(local_mel, config['keyword'])
            if has_issue:
                error_file_list.append(local_mel)
        '''
        local_config_file_list = self.getOptionPath(config['appPath'], 'local_setup',all=1)
        for each_file in local_config_file_list:
            has_issue = self.check_file_with_keyword(each_file, config['keyword'])
            if has_issue:
                error_file_list.append(each_file)
        
        mel_plugin_list = self.getOptionPath(config['appPath'], 'local_plugin', all=1)
        if len(mel_plugin_list)>0:
            #print(mel_plugin_list)
            for each_file in mel_plugin_list:
                has_issue = self.check_file_with_keyword(each_file, config['keyword'])
                if has_issue:
                    error_file_list.append(each_file)
        
        # update text
        cur_edit = self.uiList['super_lockCheck_edit']
        cur_edit.clear()
        if len(error_file_list)>0:
            # fix it
            for each_file in error_file_list:
                os.rename(each_file, each_file+'_issueFile')
            cur_edit.setText('Issue file list: \n\n'+'\n'.join(error_file_list)+'\n\nAnd tool has renamed them, run check again to double check')
        else:
            cur_edit.setText('Local File is Fine')
        
    def check_file_with_keyword(self, file_path, word_list):
        has_issue = 0
        if os.path.isfile(file_path):
            text = self.readTextFile(file_path)
            for check_work in word_list:
                if check_work in text:
                    has_issue = 1
                    break
        return has_issue
    
    def super_openMayaSafe_action(self):
        if hostMode == 'maya':
            maya_file_path = unicode(self.uiList['maya_input'].text().strip())
            if os.path.isfile(maya_file_path):
                if maya_file_path.lower().endswith(('.ma','.mb')):
                    cmds.file(f=1, new=1)
                    cmds.file(maya_file_path, open=1, executeScriptNodes=0)
                else:
                    self.quickMsg('Only ma mb file supported')
            else:
                self.quickMsg('File not exists')
        else:
            self.quickMsg('Run this tool in Maya to use')
    def super_checkCurrentMayaFile_action(self):
        if hostMode == 'maya':
            cur_edit = self.uiList['super_lockCheck_edit']
            cur_edit.clear()
            
            issue_scriptNode_list = self.getIssueNode()
            if len(issue_scriptNode_list)>0:
                # update ui
                # do fixing
                cmds.delete(issue_scriptNode_list)
                re_check_after_delete_list = self.getIssueNode()
                # update result
                result_text = 'Issue Node list: \n\n'+'\n'.join(issue_scriptNode_list)
                if len(re_check_after_delete_list)>0:
                    result_text += '\n\nAfter Deletion, still left over these nodes to fix: \n\n'+'\n'.join(re_check_after_delete_list)
                else:
                    result_text += '\n\n\nAll deleted, you can do check again if not sure'
                cur_edit.setText(result_text)
                    
            else:
                cur_edit.setText('This Maya File is Fine')
        else:
            self.quickMsg('Run this tool in Maya to use')
    def getIssueNode(self):
        config = self.memoData['config']
        all_scriptNode_list = cmds.ls(type='script')
        issue_scriptNode_list = []
        for each_scriptNode in all_scriptNode_list:
            script_check_text = cmds.scriptNode(each_scriptNode,q=1,bs=1)
            if script_check_text:
                for each_keyword in config['keyword']:
                    if each_keyword in script_check_text:
                        issue_scriptNode_list.append(each_scriptNode )
                        break
        return issue_scriptNode_list
    def getIssueNode_old(self):
        local_ui_scriptNode_list = cmds.ls('MayaMelUIConfigurationFile')
        ns_ui_scriptNode_list = cmds.ls('*:MayaMelUIConfigurationFile')
        all_ui_scriptNode_list = list(set(local_ui_scriptNode_list + ns_ui_scriptNode_list)) 
        #cmds.scriptNode(ui_scriptNode_list[0],scriptType=1,q=1) #1 	Execute on file load or on node deletion.
        issue_scriptNode_list = []
        for each_scriptNode in all_ui_scriptNode_list:
            script_check_text = cmds.scriptNode(each_scriptNode ,q=1,bs=1)
            if 'PuTianTongQing' in script_check_text:
                issue_scriptNode_list.append(each_scriptNode )
        return issue_scriptNode_list
    def getDirDetail(self, top):
        # path, parent_path, name
        top = os.path.normpath(top)
        res_dir = []
        res_file = []
        for root,dirs,files in walk(top, topdown=True):
            res_dir += [ [os.path.join(root, d), root, d] for d in dirs]
            res_file += [ [os.path.join(root, f), root, f] for f in files]
        return [res_dir, res_file]
    def super_batchFileCheck_action(self):
        
        # BEFORE: check root valid
        root_path = unicode(self.uiList['root_input'].text().strip())
        if not os.path.isdir(root_path):
            print('Path not exists: {0}'.format(root_path))
            return
        # ACTION: scan file list
        res_dir, res_file = self.getDirDetail(root_path)
        ma_file_list = []
        mb_file_list = []
        all_file_list = []
        for each in res_file:
            if each[0].endswith('.ma'):
                ma_file_list.append(each[0])
                all_file_list.append(each[0])
            elif each[0].endswith('.mb'):
                mb_file_list.append(each[0])
                all_file_list.append(each[0])
        # INFO: output
        cur_edit = self.uiList['super_lockCheck_edit']
        cur_edit.clear()
        # INFO: status
        info_list= []
        info_list.append('ma file count : {0}'.format(len(ma_file_list)))
        info_list.append('mb file count : {0}'.format(len(mb_file_list)))
        info_list.append('')
        info_list.append('===================')
        info_list.append('Maya Ascii files')
        info_list.append('===================')
        info_list.append('\n'.join(ma_file_list))
        info_list.append('')
        info_list.append('===================')
        info_list.append('Maya Binary files')
        info_list.append('===================')
        info_list.append('\n'.join(mb_file_list))
        info_list.append('')
        info_list.append('===================')
        info_list.append('')
        
        info_list.append('===================')
        info_list.append('Open file and scanning')
        info_list.append('===================')
        info_list.append('')
        info_pre = '\n'.join(info_list)
        print(info_pre)
        cur_edit.setText(info_pre)
        info_list= []
        # BATCH
        method = self.uiList['super_batchMethod_choice'].currentIndex()
        if method == 0:
            self.super_batchFileCheck_method_issueTmp_action(all_file_list, info_pre)
        elif method == 1:
            self.super_batchFileCheck_method_nothing_action(all_file_list, info_pre)
        elif method == 2:
            self.super_batchFileCheck_method_fixTmp_action()
    def super_batchFileCheck_method_issueTmp_action(self, all_file_list, info_pre=''):
        # method 1: fix file and backup issue file
        user_dirPath = os.path.join(os.path.expanduser('~'), 'Tool_Config', self.__class__.__name__)
        if not os.path.isdir(user_dirPath):
            try: 
                os.makedirs(user_dirPath)
            except OSError:
                print('Error on creation user data folder')
        if not os.path.isdir(user_dirPath):
            print('Fail to create user dir.')
            return
        # INFO: output
        cur_edit = self.uiList['super_lockCheck_edit']
        # BEFORE: check last scan OK list
        last_ok_filePath = os.path.join(user_dirPath, 'last_scan_ok_list.json')
        last_ok_file_list = []
        if os.path.isfile(last_ok_filePath):
            last_ok_file_list = self.readDataFile(last_ok_filePath)
        
        # BEFORE: IF user only want to do a preview without reading file
        count_only = self.uiList['super_batchFileCheck_count_check'].isChecked()
        # INFO: result info store
        skip_file_list = []
        do_file_list = []
        # ACTION: process file
        bad_txt_list= []
        ok_txt_list = []
        ok_file_list = []
        fail_file_list = []
        if hostMode != 'maya':
            count_only = 1
            self.quickInfo('Processing only works inside Maya, now only do processing files counting.')
        # INFO: cnt
        total_cnt = len(all_file_list)
        cur_cnt = 0
        for each in all_file_list:
            # store file info
            info_cur = ''
            info_cur+=each+'\n'
            cur_cnt+=1
            print(each)
            if os.path.isfile(each):
                # reference file to process
                refer_file_list = []
                
                skip = 0
                # SKIP: not maya file
                if not each.lower().endswith(('.ma','.mb')):
                    skip=1
                # SKIP: skip already fixed
                if each[:-3].endswith('_fixTmp'):
                    skip = 1
                # SKIP: existing fix
                if os.path.isfile( each[:-3]+'_fixTmp'+each[-3:]):
                    skip = 1
                # SKIP: existing fix
                if os.path.isfile( each+'_issueTmp'):
                    ok_file_list.append(each)
                    skip = 1
                # SKIP: if in last ok list
                if each in last_ok_file_list:
                    ok_file_list.append(each)
                    skip = 1
                # REST:
                if skip == 1:
                    print('>>>skip')
                    info_cur+='>>>skip\n'
                    skip_file_list.append(each)
                if skip == 0:
                    print('do: '+each)
                    info_cur+='>>>cleaning\n'
                    do_file_list.append(each)
                    # PROCESSING:
                    if count_only == 0:
                        cmds.file(f=1, new=1)
                        cmds.file(each, open=1, executeScriptNodes=0)
                        # scan
                        issue_scriptNode_list = self.getIssueNode()
                        if len(issue_scriptNode_list)>0:
                            # update info
                            info_cur += '\nIssue Node list: \n\n'+'\n'.join(issue_scriptNode_list)
                            # do fixing
                            self.deleteIfNotReferenced(issue_scriptNode_list)
                            re_check_after_delete_list = self.getIssueNode()
                            
                            # maybe reference node
                            fail_node_list = []
                            ref_node_list = []
                            test_fail = 0
                            for cur_node in re_check_after_delete_list:
                                is_ref = cmds.reference(cur_node , q=1, isNodeReferenced=1)
                                if is_ref:
                                    # get reference used file - C:/user/myfile.ma
                                    cur_ref_path = cmds.referenceQuery(cur_node, f=1)
                                    ref_node_list.append(cur_node)
                                    if cur_ref_path not in refer_file_list:
                                        refer_file_list.append(cur_ref_path)
                                else:
                                    # not refer but cant delete
                                    fail_node_list.append(cur_node)
                                    test_fail = 1
                            if test_fail == 1:
                                fail_file_list.append(each)
                                cmds.file(f=1, new=1, executeScriptNodes=0)
                                if len(fail_node_list)>0:
                                    info_cur += '\n\nAfter Deletion, still left over these nodes to fix: \n\n'+'\n'.join(fail_node_list)
                                info_cur+='\n>>>fail with script deletion'
                                bad_txt_list.append('\n----------\n'+info_cur)
                            if test_fail == 0:
                                # saving fix
                                cur_new_name = ''
                                #cmds.file(save=1, executeScriptNodes=0)
                                if each.lower().endswith('.ma'):
                                    cmds.file(rename = each[:-3]+'_fixTmp.ma')
                                    cur_new_name = cmds.file(f=1, save=1, type="mayaAscii", executeScriptNodes=0)
                                elif each.lower().endswith('.mb'):
                                    cmds.file(rename = each[:-3]+'_fixTmp.mb',  executeScriptNodes=0)
                                    cur_new_name = cmds.file(f=1, save=1, type="mayaBinary")
                                cmds.file(f=1, new=1, executeScriptNodes=0)
                                # rename
                                if os.path.isfile(cur_new_name):
                                    os.rename(each, each+'_issueTmp')
                                    os.rename(cur_new_name, each)
                                # update result
                                if len(refer_file_list)>0:
                                    info_cur += '\n\nAfter Deletion, this tool will process following reference files with issue: \n\n'+'\n'.join(refer_file_list)
                                else:
                                    info_cur += '\n\n\nAll deleted'
                                bad_txt_list.append('\n----------\n'+info_cur)
                        else:
                            info_cur += '\nFile is OK'
                            ok_txt_list.append(each+'\n'+'This Maya File is Fine')
                            ok_file_list.append(each)
                            # write to log
                            self.writeDataFile(ok_file_list, last_ok_filePath)
                # update UI
                cur_edit.setText(info_pre+'\n{0}/{1}\n'.format(cur_cnt,total_cnt)+info_cur)
                # process reference file
                if len(refer_file_list)>0:
                    ref_bad_result_text_list = self.super_batchFileCheck_method_issueTmp_action(refer_file_list, info_pre+'\n{0}/{1}\n'.format(cur_cnt,total_cnt)+info_cur)
                    bad_txt_list.append( '\n---reference result---\n'+'\n'.join(ref_bad_result_text_list)+'\n' )
        # done
        cmds.file(f=1, new=1, executeScriptNodes=0)
        final_text = info_pre
        final_text += 'process file count : {0}\n'.format(len(do_file_list))
        final_text += 'skip fixed file count : {0}\n'.format(len(skip_file_list))
        final_text += 'last ok file count : {0}\n'.format(len(last_ok_file_list))
        final_text += 'current ok file count : {0}\n'.format(len(ok_file_list))
        cur_edit.setText(final_text+'\n\n=======bad======\n\n'+'\n'.join(bad_txt_list)+'\n\n=======ok======\n\n'+'\n'.join(ok_txt_list))
        return bad_txt_list
    def deleteIfNotReferenced(self, nodeList ):
        if not isinstance(nodeList, (list, tuple)):
            nodeList = [nodeList]
        result_list = []
        for nodeToDelete in nodeList:
            if cmds.objExists(nodeToDelete) and not cmds.reference(nodeToDelete, q=1, isNodeReferenced=1):
                isLocked = cmds.lockNode(nodeToDelete, q=1, lock=1)[0]
                if not isLocked:
                    cmds.delete( nodeToDelete )
                    result_list.append(nodeToDelete)
    def super_batchFileCheck_method_nothing_action(self, all_file_list, info_pre=''):
        # method 1: fix file and backup issue file
        user_dirPath = os.path.join(os.path.expanduser('~'), 'Tool_Config', self.__class__.__name__)
        if not os.path.isdir(user_dirPath):
            try: 
                os.makedirs(user_dirPath)
            except OSError:
                print('Error on creation user data folder')
        if not os.path.isdir(user_dirPath):
            print('Fail to create user dir.')
            return
        # INFO: output
        cur_edit = self.uiList['super_lockCheck_edit']
        # BEFORE: check last scan OK list
        last_ok_filePath = os.path.join(user_dirPath, 'last_scan_ok_list.json')
        last_ok_file_list = []
        if os.path.isfile(last_ok_filePath):
            last_ok_file_list = self.readDataFile(last_ok_filePath)
        
        # BEFORE: IF user only want to do a preview without reading file
        count_only = self.uiList['super_batchFileCheck_count_check'].isChecked()
        # INFO: result info store
        skip_file_list = []
        do_file_list = []
        # ACTION: process file
        bad_txt_list= []
        ok_txt_list = []
        ok_file_list = []
        fail_file_list = []
        if hostMode != 'maya':
            count_only = 1
            self.quickInfo('Processing only works inside Maya, now only do processing files counting.')
        # INFO: cnt
        total_cnt = len(all_file_list)
        cur_cnt = 0
        for each in all_file_list:
            # store file info
            info_cur = ''
            info_cur+=each+'\n'
            cur_cnt+=1
            print(each)
            if os.path.isfile(each):
                # reference file to process
                refer_file_list = []
                
                skip = 0
                # SKIP: not maya file
                if not each.lower().endswith(('.ma','.mb')):
                    skip=1
                # SKIP: skip already fixed
                if each[:-3].endswith('_fixTmp'):
                    skip = 1
                # SKIP: existing fix
                if os.path.isfile( each[:-3]+'_fixTmp'+each[-3:]):
                    skip = 1
                # SKIP: existing fix
                if os.path.isfile( each+'_issueTmp'):
                    ok_file_list.append(each)
                    skip = 1
                # SKIP: if in last ok list
                if each in last_ok_file_list:
                    ok_file_list.append(each)
                    skip = 1
                # REST:
                if skip == 1:
                    print('>>>skip')
                    info_cur+='>>>skip\n'
                    skip_file_list.append(each)
                if skip == 0:
                    print('do: '+each)
                    info_cur+='>>>cleaning\n'
                    do_file_list.append(each)
                    # PROCESSING:
                    if count_only == 0:
                        cmds.file(f=1, new=1)
                        cmds.file(each, open=1, executeScriptNodes=0)
                        # scan
                        issue_scriptNode_list = self.getIssueNode()
                        if len(issue_scriptNode_list)>0:
                            # update info
                            info_cur += '\nIssue Node list: \n\n'+'\n'.join(issue_scriptNode_list)
                            # do fixing
                            self.deleteIfNotReferenced(issue_scriptNode_list)
                            re_check_after_delete_list = self.getIssueNode()
                            
                            # maybe reference node
                            fail_node_list = []
                            ref_node_list = []
                            test_fail = 0
                            for cur_node in re_check_after_delete_list:
                                is_ref = cmds.reference(cur_node , q=1, isNodeReferenced=1)
                                if is_ref:
                                    # get reference used file - C:/user/myfile.ma
                                    cur_ref_path = cmds.referenceQuery(cur_node, f=1)
                                    ref_node_list.append(cur_node)
                                    if cur_ref_path not in refer_file_list:
                                        refer_file_list.append(cur_ref_path)
                                else:
                                    # not refer but cant delete
                                    fail_node_list.append(cur_node)
                                    test_fail = 1
                            if test_fail == 1:
                                fail_file_list.append(each)
                                cmds.file(f=1, new=1, executeScriptNodes=0)
                                if len(fail_node_list)>0:
                                    info_cur += '\n\nAfter Deletion, still left over these nodes to fix: \n\n'+'\n'.join(fail_node_list)
                                info_cur+='\n>>>fail with script deletion'
                                bad_txt_list.append('\n----------\n'+info_cur)
                            if test_fail == 0:
                                # saving fix
                                '''
                                cur_new_name = ''
                                #cmds.file(save=1, executeScriptNodes=0)
                                if each.lower().endswith('.ma'):
                                    cmds.file(rename = each[:-3]+'_fixTmp.ma')
                                    cur_new_name = cmds.file(f=1, save=1, type="mayaAscii", executeScriptNodes=0)
                                elif each.lower().endswith('.mb'):
                                    cmds.file(rename = each[:-3]+'_fixTmp.mb',  executeScriptNodes=0)
                                    cur_new_name = cmds.file(f=1, save=1, type="mayaBinary")
                                cmds.file(f=1, new=1, executeScriptNodes=0)
                                # rename
                                if os.path.isfile(cur_new_name):
                                    os.rename(each, each+'_issueTmp')
                                    os.rename(cur_new_name, each)
                                '''
                                # update result
                                if len(refer_file_list)>0:
                                    info_cur += '\n\nAfter Deletion, this tool will process following reference files with issue: \n\n'+'\n'.join(refer_file_list)
                                else:
                                    info_cur += '\n\n\nAll deleted'
                                bad_txt_list.append('\n----------\n'+info_cur)
                        else:
                            info_cur += '\nFile is OK'
                            ok_txt_list.append(each+'\n'+'This Maya File is Fine')
                            ok_file_list.append(each)
                            # write to log
                            self.writeDataFile(ok_file_list, last_ok_filePath)
                # update UI
                cur_edit.setText(info_pre+'\n{0}/{1}\n'.format(cur_cnt,total_cnt)+info_cur)
                # process reference file
                if len(refer_file_list)>0:
                    ref_bad_result_text_list = self.super_batchFileCheck_method_nothing_action(refer_file_list, info_pre+'\n{0}/{1}\n'.format(cur_cnt,total_cnt)+info_cur)
                    bad_txt_list.append( '\n---reference result---\n'+'\n'.join(ref_bad_result_text_list)+'\n' )
        # done
        cmds.file(f=1, new=1, executeScriptNodes=0)
        final_text = info_pre
        final_text += 'process file count : {0}\n'.format(len(do_file_list))
        final_text += 'skip fixed file count : {0}\n'.format(len(skip_file_list))
        final_text += 'last ok file count : {0}\n'.format(len(last_ok_file_list))
        final_text += 'current ok file count : {0}\n'.format(len(ok_file_list))
        cur_edit.setText(final_text+'\n\n=======bad======\n\n'+'\n'.join(bad_txt_list)+'\n\n=======ok======\n\n'+'\n'.join(ok_txt_list))
        return bad_txt_list
    def super_batchFileCheck_method_fixTmp_action(self):
        # no long used as method 1 support reference file scan
        # method 2: dont touch file and save as fix file
        user_dirPath = os.path.join(os.path.expanduser('~'), 'Tool_Config', self.__class__.__name__)
        if not os.path.isdir(user_dirPath):
            try: 
                os.makedirs(user_dirPath)
            except OSError:
                print('Error on creation user data folder')
        if not os.path.isdir(user_dirPath):
            print('Fail to create user dir.')
            return
                
        last_ok_filePath = os.path.join(user_dirPath, 'last_scan_ok_list.json')
        last_ok_file_list = []
        skip_file_list = []
        do_file_list= []
        count_only = self.uiList['super_batchFileCheck_count_check'].isChecked()
        if os.path.isfile(last_ok_filePath):
            last_ok_file_list = self.readDataFile(last_ok_filePath)
        root_path = unicode(self.uiList['root_input'].text().strip())
        if not os.path.isdir(root_path):
            print('Path not exists: {0}'.format(root_path))
            return
        res_dir, res_file = self.getDirDetail(root_path)
        ma_file_list = []
        mb_file_list = []
        for each in res_file:
            if each[0].endswith('.ma'):
                ma_file_list.append(each[0])
            elif each[0].endswith('.mb'):
                mb_file_list.append(each[0])
        print('ma file count : {0}'.format(len(ma_file_list)))
        print('mb file count : {0}'.format(len(mb_file_list)))
        print('\n===================\n')
        print('Maya Ascii files')
        print('\n===================\n')
        print('\n'.join(ma_file_list))
        print('\n===================\n')
        print('Maya Binary files')
        print('\n===================\n')
        print('\n'.join(mb_file_list))
        print('\n===================\n')
        
        
        print('\n===================\n')
        print('Open file and scanning')
        print('\n===================\n')
        bad_txt_list= []
        ok_txt_list = []
        ok_file_list = []
        cur_edit = self.uiList['super_lockCheck_edit']
        cur_edit.clear()
        if hostMode != 'maya':
            return
        for each in ma_file_list+mb_file_list:
            print('\ncurrent:----------------\n')
            print(each)
            print('\n:::\n')
            if os.path.isfile(each):
                if each.lower().endswith(('.ma','.mb')):
                    # skip already fixed
                    skip=0
                    if each[:-3].endswith('_fixTmp'):
                        skip = 1
                    # skip existing fix
                    if os.path.isfile( each[:-3]+'_fixTmp'+each[-3:]):
                        skip = 1
                    # if in last ok list
                    if each in last_ok_file_list:
                        ok_file_list.append(each)
                        skip = 1
                    # rest
                    if skip == 1:
                        print('skip')
                        skip_file_list.append(each)
                    
                    if skip == 0:
                        print('do: '+each)
                        do_file_list.append(each)
                        if count_only == 0:
                            cmds.file(f=1, new=1)
                            cmds.file(each, open=1, executeScriptNodes=0)
                            # scan
                            issue_scriptNode_list = self.getIssueNode()
                            if len(issue_scriptNode_list)>0:
                                # update ui
                                # do fixing
                                cmds.delete(issue_scriptNode_list)
                                re_check_after_delete_list = self.getIssueNode()
                                # saving fix
                                if each.lower().endswith('.ma'):
                                    cmds.file(rename = each[:-3]+'_fixTmp.ma')
                                    cmds.file(f=1, save=1, type="mayaAscii")
                                elif each.lower().endswith('.mb'):
                                    cmds.file(rename = each[:-3]+'_fixTmp.mb')
                                    cmds.file(f=1, save=1, type="mayaBinary")
                                # update result
                                result_text = 'Issue Node list: \n\n'+'\n'.join(issue_scriptNode_list)
                                if len(re_check_after_delete_list)>0:
                                    result_text += '\n\nAfter Deletion, still left over these nodes to fix: \n\n'+'\n'.join(re_check_after_delete_list)
                                else:
                                    result_text += '\n\n\nAll deleted, you can do check again if not sure'
                                #cur_edit.setText(result_text)
                                
                                bad_txt_list.append('\n----------\n'+each+'\n'+result_text)
                                    
                            else:
                                ok_txt_list.append(each+'\n'+'This Maya File is Fine')
                                ok_file_list.append(each)
                                # write to log
                                
                                self.writeDataFile(ok_file_list, last_ok_filePath)
        # done
        cmds.file(f=1, new=1)
        final_text = 'ma file count : {0}\n'.format(len(ma_file_list))
        final_text += 'mb file count : {0}\n'.format(len(mb_file_list))
        final_text += 'process file count : {0}\n'.format(len(do_file_list))
        final_text += 'skip fixed file count : {0}\n'.format(len(skip_file_list))
        final_text += 'last ok file count : {0}\n'.format(len(last_ok_file_list))
        final_text += 'current ok file count : {0}\n'.format(len(ok_file_list))
        cur_edit.setText(final_text+'\n\n=======bad======\n\n'+'\n'.join(bad_txt_list)+'\n\n=======ok======\n\n'+'\n'.join(ok_txt_list))
    # ======= path functions =======
    def ____path_functions____():
        pass
        '''
        config['appPath']['djv'] = [r'C:\Program Files\djv-*-Windows-64\bin\djv_view.exe', r'R:\Pipeline\App\djv_win64\bin\djv_view.exe']
        # ('subFolder1', 'subFolder2', 'appName.ext')
        config['appPath']['ffmpeg'] = [ ('bin','ffmpeg.exe'), r'D:\z_sys\App\ffmpeg\ffmpeg.exe', r'R:\Pipeline\App_VHQ\ffmpeg\bin\ffmpeg.exe']
        config['appPath']['ffprobe'] = [  ('bin','ffprobe.exe'), r'D:\z_sys\App\ffmpeg\ffprobe.exe', r'R:\Pipeline\App_VHQ\ffmpeg\bin\ffprobe.exe']
        
        app = self.getOptionPath(config['appPath'], 'djv')
        nuke_app_list = self.getOptionPath(config['appPath'], 'nuke', all=1)
        if os.path.isfile(app):
           subprocess.Popen([app, os.path.normpath(pyPath)])
        if os.path.isfile(batch_appPath) and mod == 2:
           subprocess.Popen(batch_appPath,creationflags=subprocess.CREATE_NEW_CONSOLE)
        info=subprocess.Popen('tasklist.exe /FO CSV /FI "IMAGENAME eq {0}"'.format(appName),stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = info.communicate()
        result = [ x for x in out.replace('"','').splitlines() if x !='' ]
        '''

        
    def getOptionPath(self, dict, name, all=0):
        # updated: 2020.05.05 get self location sub path option
        # updated: 2019.01.09
        if name not in dict.keys():
            print('Dict has no key: {0}'.format(name))
            return
        option_list = []
        if not isinstance(dict[name], (list,tuple)):
            option_list = [ dict[name] ]
        else:
            option_list = dict[name]
        if all == 0:
            found = None
            for option in option_list:
                if isinstance(option,(tuple, list)):
                    # self path
                    self_option_info = [os.path.dirname(self.location)]+[x for x in option]
                    self_option = os.path.normpath( os.path.join(*self_option_info) )
                    if os.path.exists(self_option):
                        found = self_option
                        break
                else:
                    if '*' in option:
                        # wildchar search
                        import glob
                        sub_option_list = glob.glob(option)
                        if len(sub_option_list) > 0:
                            found = sorted(sub_option_list)[-1]
                            break
                    else:
                        if os.path.exists(option):
                            found = option
                            break
            if found is not None:
                found = found.replace('\\','/')
            print('found: {0}'.format(found))
            return found
        else:
            all_option = []
            for option in option_list:
                if '*' in option:
                    # wildchar search
                    import glob
                    sub_option_list = glob.glob(option)
                    all_option.extend(sorted(sub_option_list, reverse=1))
                else:
                    if os.path.exists(option):
                        all_option.append(option)
            standard_path_option = []
            for each_path in all_option:
                standard_path = each_path.replace('\\','/')
                if standard_path not in standard_path_option:
                    standard_path_option.append(standard_path)
            print(standard_path_option)
            return standard_path_option
    # getPathChild for non utt widget
    def getPathChild(self, scanPath, pattern='', isfile=0):
        resultList =[]
        scanPath = unicode(scanPath)
        if not os.path.isdir(scanPath):
            return resultList
        if isfile == 0:
            resultList = [x for x in os.listdir(scanPath) if os.path.isdir(os.path.join(scanPath,x))]
        elif isfile == 1:
            resultList = [x for x in os.listdir(scanPath) if os.path.isfile(os.path.join(scanPath,x))]
        else:
            resultList = os.listdir(scanPath)
        if pattern != '':
            cur_pattern = re.compile(pattern)
            resultList = [x for x in resultList if cur_pattern.match(x)]
        resultList.sort()
        return resultList
    # - example file io function
    def exportConfig_action(self):
        file= self.quickFileAsk('export', {'json':'JSON data file', 'xdat':'Pickle binary file'})
        if file == "":
            return
        # export process
        ui_data = self.memoData['config']
        # file process
        if file.endswith('.xdat'):
            self.writeDataFile(ui_data, file, binary=1)
        else:
            self.writeDataFile(ui_data, file)
        self.quickInfo("File: '"+file+"' creation finished.")
    def importConfig_action(self):
        file= self.quickFileAsk('import',{'json':'JSON data file', 'xdat':'Pickle binary file'})
        if file == "":
            return
        # import process
        ui_data = ""
        if file.endswith('.xdat'):
            ui_data = self.readDataFile(file, binary=1)
        else:
            ui_data = self.readDataFile(file)
        self.memoData['config'] = ui_data
        self.quickInfo("File: '"+file+"' loading finished.")
    def userConfig_action(self):
        user_dirPath = os.path.join(os.path.expanduser('~'), 'Tool_Config', self.__class__.__name__)
        self.openFolder(user_dirPath)
        
        
    # ======= file structure functions =======
    def ___file_structure_functions___():
        '''
        path_data = self.getDirData(folderPath, config['file_tree']['task'], config['file_tree']['pattern'])
        file_tree = self.uiList['file_tree']
        file_tree.clear()
        self.setTreeData(file_tree,file_tree.invisibleRootItem(),path_data)
        if 'cache' not in self.memoData:
            self.memoData['cache'] = {}
        self.memoData['cache']['file_tree'] = path_data
        
        version update:
          * FolderDesigner: improve on infinit depth dig and flat tree data features
        '''
        pass
    def update_tree_by_path(self, tree_name, rootPath):
        config = self.memoData['config']
        path_data = self.getDirData(rootPath, config[tree_name]['task'], config[tree_name]['pattern'])
        file_tree = self.uiList[tree_name]
        file_tree.clear()
        self.setTreeData(file_tree,file_tree.invisibleRootItem(),path_data)
        if 'cache' not in self.memoData:
            self.memoData['cache'] = {}
        self.memoData['cache'][tree_name] = path_data
        self.tree_resize(tree_name)
    def tree_resize(self, tree_name, extra=10):
        cur_tree = self.uiList[tree_name]
        for i in range(cur_tree.columnCount()):
            cur_tree.resizeColumnToContents(i)
            w = cur_tree.columnWidth(i)
            cur_tree.setColumnWidth(i,w+extra)
    def flatTreeData(self, treeData, flat_list=[]):
        node_info, node_info_child = treeData
        flat_list.append(node_info[2])
        for sub_node in node_info_child:
            flat_list = self.flatTreeData(sub_node, flat_list)
        return flat_list
    def getDirData(self, scanPath, task_list, patternDict, currentTag=''):
        #config['folder_tree']['task']=[ ('','category'), ('','app') ]
        #config['folder_tree']['task']=[ (2,'sub') ]
        #config['folder_tree']['task']=[ (-1,'sub') ]
        #config['folder_tree']['pattern']= {'app':'(?!(^Keyboard$)|(^icons$))'}
        if not isinstance(task_list, (tuple, list)):
            return ( [], [] )
        else:
            if len(task_list)== 0:
                return ( [], [] )
        scanPath = scanPath.replace('\\','/')
        # current task
        cur_task = task_list[0]
        if not isinstance( cur_task[0], int ):
            # normal str path seg
            cur_step_list = [x for x in cur_task[0].split('/') if x!='']
            if len(cur_step_list)>0:
                cur_step_list = [scanPath]+cur_step_list
                scanPath = os.path.join(*cur_step_list).replace('\\','/')
            if not os.path.isdir(scanPath):
                print('Error: path not exists: {}'.format(scanPath))
                return ( [], [] )
            # current filter
            cur_pattern = '' if cur_task[1] not in patternDict.keys() else patternDict[cur_task[1]]
            isfile = 0 # folder only
            if cur_task[1].endswith('_file'):
                isfile = 1 # file only
            if cur_task[1].endswith('_all'):
                isfile = 2 # folder and file
            node_name = os.path.basename(scanPath)
            node_info = ['', '', scanPath ] if currentTag == '' else [node_name, currentTag, scanPath ]
            node_info_child = []
            parentTag = currentTag
            # current child
            rest_task = [] if len(task_list)==1 else task_list[1:]
            for each_name in self.getPathChild(scanPath, cur_pattern, isfile):
                cur_path = os.path.join(scanPath, each_name).replace('\\','/')
                cur_tag = each_name if parentTag == '' else parentTag+':'+each_name
                if os.path.isdir(cur_path):
                    if len(rest_task) > 0:
                        # go next level task
                        node_info_child.append( self.getDirData(cur_path, rest_task, patternDict, cur_tag) )
                    else:
                        node_info_child.append( ( [os.path.basename(cur_path), cur_tag, cur_path ], [] ) )
                else:
                    node_info_child.append( ( [os.path.basename(cur_path), '', cur_path ], [] ) )
            return (node_info, node_info_child)
        else:
            # normal str path seg
            cur_step_depth = cur_task[0]
            if not os.path.isdir(scanPath):
                print('Error: path not exists: {}'.format(scanPath))
                return ( [], [] )
            # current filter
            cur_pattern = '' if cur_task[1] not in patternDict.keys() else patternDict[cur_task[1]]
            isfile = 0 # folder only
            if cur_task[1].endswith('_file'):
                isfile = 1 # file only
            if cur_task[1].endswith('_all'):
                isfile = 2 # folder and file
            node_name = os.path.basename(scanPath)
            node_info = ['', '', scanPath ] if currentTag == '' else [node_name, currentTag, scanPath ]
            node_info_child = []
            parentTag = currentTag
            # current child
            rest_task = []
            if cur_step_depth == -1:
                rest_task = [ cur_task ]
            else:
                if cur_step_depth > 1:
                    rest_task.append( (cur_step_depth-1, cur_task[1]) )
                if len(task_list) >1:
                    rest_task.extend( task_list[1:] )
            for each_name in self.getPathChild(scanPath, cur_pattern, isfile):
                cur_path = os.path.join(scanPath, each_name).replace('\\','/')
                cur_tag = each_name if parentTag == '' else parentTag+':'+each_name
                if os.path.isdir(cur_path):
                    if len(rest_task) > 0:
                        # go next level task
                        node_info_child.append( self.getDirData(cur_path, rest_task, patternDict, cur_tag) )
                    else:
                        node_info_child.append( ( [os.path.basename(cur_path), cur_tag, cur_path ], [] ) )
                else:
                    node_info_child.append( ( [os.path.basename(cur_path), '', cur_path ], [] ) )
            return (node_info, node_info_child)
    def cacheTreeData(self, tree, force=1):
        cur_tree = self.uiList[tree]
        if 'cache' not in self.memoData:
            self.memoData['cache'] = {}
        if force == 1:
            self.memoData['cache'][tree] = self.getTreeData(cur_tree, cur_tree.invisibleRootItem())
        else:
            if tree not in self.memoData['cache']:
                self.memoData['cache'][tree] = self.getTreeData(cur_tree, cur_tree.invisibleRootItem())
    def getTreeData(self, tree, cur_node):
        child_count = cur_node.childCount()
        node_info = [ unicode( cur_node.text(i) ) for i in range(cur_node.columnCount()) ]
        node_info_child = []
        for i in range(child_count):
            node_info_child.append( self.getTreeData(tree, cur_node.child(i) ) )
        return (node_info, node_info_child)
    def setTreeData(self, tree, cur_node, data, filter='', col=0):
        # correct node format [ [info list], [ child list] ]
        node_info = []
        node_info_child = []
        
        # format [ [info list], [child list] ]
        # possible input
        # 1. data [ a, b, c, d, e]; ==> set cur_node row info
        # 2. data a; ==> set cur_node row info
        # 3. data [a, [child list]]; ==> set cur_node and add child list
        # 4. data [ [a], [child list]]; ==> set cur_node and add child list
        # 5. child list only [ a, [], b, [c]]
        # ------------ 
        # situation 2: a
        # print('---------------------')
        # print(data)
        # print('---------------------')
        if isinstance(data, (str,unicode)):
            node_info = [data]
        elif isinstance(data,(tuple,list)):
            is_info_only = True
            for x in data:
                if not isinstance(x, (str,unicode)):
                    is_info_only = False
            if is_info_only:
                # situation 1: [ a,b,c ]
                node_info = data
            else:
                # situation 3: 
                if len(data) == 2:
                    # check info
                    if isinstance(data[0], (str,unicode)):
                        data_info = [ data[0] ]
                    elif isinstance(data[0],(tuple,list)):
                        node_info = data[0]
                    else:
                        print('bad format node: {0}'.format(unicode(data)))
                        return
                    # check child
                    if isinstance(data[1],(tuple,list)):
                        node_info_child = data[1]
                    else:
                        print('bad format node: {0}'.format(unicode(data)))
                        return
                else:
                    node_info_child = data
        # ------------ 
        
        [cur_node.setText(i, unicode(node_info[i])) for i in range(len(node_info))]
        # re filter
        if filter != '' and isinstance(filter, (str, unicode)):
            filter = re.compile(filter, re.IGNORECASE)
        for sub_data in node_info_child:
            if filter == '':
                new_node = QtWidgets.QTreeWidgetItem()
                cur_node.addChild(new_node)
                self.setTreeData(tree, new_node, sub_data)
            else:
                if not filter.search(sub_data[0][col]) and not self.checkChildData(sub_data[1], filter, col):
                    pass
                else:
                    new_node = QtWidgets.QTreeWidgetItem()
                    cur_node.addChild(new_node)
                    new_node.setExpanded(1)
                    self.setTreeData(tree, new_node, sub_data, filter, col)
    def checkChildData(self, DataChild, filter, col):
        ok_cnt = 0
        if isinstance(filter, (str, unicode)):
            filter = re.compile(filter, re.IGNORECASE)
        for sub_data in DataChild:
            if filter.search(sub_data[0][col]) or self.checkChildData(sub_data[1], filter, col):
                ok_cnt +=1
        return ok_cnt
        
#=======================================
#  window instance creation
#=======================================

import ctypes # for windows instance detection
single_SuperManCheck = None
app_SuperManCheck = None
def main(mode=0):
    # get parent window in Maya
    parentWin = None
    if hostMode == "maya":
        if qtMode in (0,2): # pyside
            parentWin = shiboken.wrapInstance(long(mui.MQtUtil.mainWindow()), QtWidgets.QWidget)
        elif qtMode in (1,3): # PyQt
            parentWin = sip.wrapinstance(long(mui.MQtUtil.mainWindow()), QtCore.QObject)
    # create app object for certain host
    global app_SuperManCheck
    if hostMode in ('desktop', 'blender', 'npp', 'fusion'):
        # single instance app mode on windows
        if osMode == 'win':
            # check if already open for single desktop instance
            from ctypes import wintypes
            order_list = []
            result_list = []
            top = ctypes.windll.user32.GetTopWindow(None)
            if top: 
                length = ctypes.windll.user32.GetWindowTextLengthW(top)
                buff = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(top, buff, length + 1)
                class_name = ctypes.create_string_buffer(200)
                ctypes.windll.user32.GetClassNameA(top, ctypes.byref(class_name), 200)
                result_list.append( [buff.value, class_name.value, top ])
                order_list.append(top)
                while True:
                    next = ctypes.windll.user32.GetWindow(order_list[-1], 2) # win32con.GW_HWNDNEXT
                    if not next:
                        break
                    length = ctypes.windll.user32.GetWindowTextLengthW(next)
                    buff = ctypes.create_unicode_buffer(length + 1)
                    ctypes.windll.user32.GetWindowTextW(next, buff, length + 1)
                    class_name = ctypes.create_string_buffer(200)
                    ctypes.windll.user32.GetClassNameA(next, ctypes.byref(class_name), 200)
                    result_list.append( [buff.value, class_name.value, next] )
                    order_list.append(next)
            # result_list: [(title, class, hwnd int)]
            winTitle = 'SuperManCheck' # os.path.basename(os.path.dirname(__file__))
            is_opened = 0
            for each in result_list:
                if re.match(winTitle+' - v[0-9.]* - host: desktop',each[0]) and each[1] == 'QWidget':
                    is_opened += 1
                    if is_opened == 1:
                        ctypes.windll.user32.SetForegroundWindow(each[2])
                        sys.exit(0) # 0: success, 1-127: bad error
                        return
        if hostMode in ('npp','fusion'):
            app_SuperManCheck = QtWidgets.QApplication([])
        elif hostMode in ('houdini'):
            pass
        else:
            app_SuperManCheck = QtWidgets.QApplication(sys.argv)
    
    #--------------------------
    # ui instance
    #--------------------------
    # Keep only one copy of windows ui in Maya
    global single_SuperManCheck
    if single_SuperManCheck is None:
        if hostMode == 'maya':
            single_SuperManCheck = SuperManCheck(parentWin, mode)
        elif hostMode == 'nuke':
            single_SuperManCheck = SuperManCheck(QtWidgets.QApplication.activeWindow(), mode)
        elif hostMode == 'houdini':
            hou.session.mainWindow = hou.qt.mainWindow()
            single_SuperManCheck = SuperManCheck(hou.session.mainWindow, mode)
        else:
            single_SuperManCheck = SuperManCheck()
    single_SuperManCheck.show()
    ui = single_SuperManCheck
    if hostMode != 'desktop':
        ui.activateWindow()
    
    # loop app object for certain host
    if hostMode in ('desktop'):
        sys.exit(app_SuperManCheck.exec_())
    elif hostMode in ('npp','fusion'):
        app_SuperManCheck.exec_()
    return ui

if __name__ == "__main__":
    main()