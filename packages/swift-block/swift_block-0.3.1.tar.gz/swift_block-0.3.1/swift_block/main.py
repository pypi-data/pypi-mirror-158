'''
Copyright (C) 2021 xploreinfinity

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
'''

from PyQt6 import QtWidgets,QtCore,QtGui,uic
import sys,os,inspect
from swift_block import Parser
#from swift_block import elevate
from swift_block import RuleManager
class Ui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        #*load the ui file
        self.scriptPath=os.path.abspath(os.path.dirname(inspect.getsourcefile(lambda:0))).replace('\\','/')
        uic.loadUi(self.scriptPath+"/ui/adblock.ui",self)
        #*init the library for interacting with host sources,etc...
        #!WARNING:This changes the current directory
        self.parser=Parser.Parser()

        #*GLOBAL VARIABLES DECLARATION:
        self.status=False  #*Flag which indicates whether swiftblock is enabled or disabled
        self.editMode=True #*controls whether the source editing form is set to edit source mode or add source mode
        self.selectedSource=''#*Will store QListWidgetItem that is currently selected by the user
        self.sourceDct={}#*Stores source names and corresponding source URLs for display in the source edit form when user clicks on a source

        self.SignalSlotConfig()
        self.show()
        self.reconf_ui()

    def reconf_ui(self):
        self.setWindowIcon(QtGui.QIcon(self.scriptPath+"/assets/app_icon.svg"))
        #*Reconfig for the status tab:
        self.loadStatus()
        self.manageRules_btn.setIcon(QtGui.QIcon(self.scriptPath+"/assets/ruleMan.svg"))
        self.manageRules_btn.setIconSize(QtCore.QSize(30,30))
        self.updateSources_btn.setIcon(QtGui.QIcon(self.scriptPath+"/assets/sources_update.png"))
        self.updateSources_btn.setIconSize(QtCore.QSize(35,35))
        #*Reconfig for the sources tab:
        self.loadSrcData()
        self.sourcesForm_widget.setDisabled(True)
        self.sourceDelete_btn.setDisabled(True)
        self.editMode_lbl.hide()
        self.formStatus_lbl.hide()
        self.sourceName_tf.setPlaceholderText("Unqiue nickname for the source")
        self.sourceURL_tf.setPlaceholderText("Unique URL of the source")
        #*Reconfig for the about tab:
        self.gitRepo_btn.setIcon(QtGui.QIcon(self.scriptPath+'/assets/github.svg'))
        self.gitRepo_btn.setIconSize(QtCore.QSize(35,50))
        self.license_btn.setIcon(QtGui.QIcon(self.scriptPath+'/assets/license.png'))
        self.license_btn.setIconSize(QtCore.QSize(30,30))
        self.uninstall_btn.setIcon(QtGui.QIcon(self.scriptPath+'/assets/uninstall.png'))
        self.uninstall_btn.setIconSize(QtCore.QSize(30,30))
        self.appIcon_lbl.setStyleSheet("border-image:url("+self.scriptPath+"/assets/app_icon.svg);")

    #*Several utility functions that prevent code repetition:
    #*Shows an error MessageBox which informs the user of the error(and provides additional info):
    def err_msg(self,err):
        msg=QtWidgets.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.setText("Oops! An error occurred. Additional info is provided below")
        msg.setDetailedText(str(err))
        msg.exec()

    #*Displays a success/error message on the label passed as an argument:
    def showStatus_lbl(self,message,lbl,success=False):
        if success:
            lbl.setStyleSheet("color:black;background-color:limegreen;font-weight:bold")
        else:
            lbl.setStyleSheet("color:white;background-color:crimson;font-weight:bold")
        lbl.setText(message)
        lbl.show()

    #*load the status of the adblocker(whether active,no. of hosts blocked/redirected/allowed):
    def loadStatus(self):
        blocked,redirected,allowed,self.status=self.parser.getStatus()
        if blocked !=None and redirected!=None and allowed !=None:
            self.blockedCount_lbl.setText(str(blocked))
            self.redirectedCount_lbl.setText(str(redirected))
            self.allowedCount_lbl.setText(str(allowed))
        #*Based on swiftblock's status,change the gui accordingly:
        if self.status:
            self.status_lbl.setText("SwiftBlock is enabled")
            self.toggleStatus_btn.setText("Disable")
            self.background_lbl.setStyleSheet("background-image:url('"+self.scriptPath+"/assets/martini.png');")
            self.statusShield_lbl.setStyleSheet("border-image:url('"+self.scriptPath+"/assets/active_shield.svg');")
        else:
            self.status_lbl.setText("SwiftBlock is disabled")
            self.toggleStatus_btn.setText("Enable")
            self.background_lbl.setStyleSheet("background-image:url('"+self.scriptPath+"/assets/autumn.png');")
            self.statusShield_lbl.setStyleSheet("border-image:url('"+self.scriptPath+"/assets/inactive_shield.svg');")


    #*fetches and shows user's host sources on the sourcesList:
    def loadSrcData(self):
        self.sourcesList.clear()
        self.selectedSource=None
        sources=self.parser.fetch_sources()
        self.sourceDct={}
        for source in sources:
            self.sourcesList.addItem(source[0])
            self.sourceDct[source[0]]=source[1]
        #*Reset the form and disable said form and the delete btn:
        self.sourceName_tf.setText('')
        self.sourceURL_tf.setText('')
        self.sourcesForm_widget.setDisabled(True)
        self.sourceDelete_btn.setDisabled(True)

    #*A vital function that assigns all widgets handlers(slots) for specific events(signals):
    def SignalSlotConfig(self):
        #*for events occurring in status tab:
        self.toggleStatus_btn.clicked.connect(self.toggleStatusClicked)
        self.manageRules_btn.clicked.connect(self.openRuleManager)
        self.updateSources_btn.clicked.connect(self.updateSourcesClicked)
        #*for events occurring in sources tab:
        self.sourcesList.selectionModel().currentChanged.connect(self.sourceSelected)
        self.sourceAdd_btn.clicked.connect(self.addBtnClicked)
        self.sourceDelete_btn.clicked.connect(self.deleteBtnClicked)
        self.sourceSave_btn.clicked.connect(self.sourceSaveBtnClicked)
        #*for events occurring in the about tab:
        self.gitRepo_btn.clicked.connect(self.gitRepo_btnClicked)
        self.license_btn.clicked.connect(self.license_btnClicked)
        self.uninstall_btn.clicked.connect(self.uninstall_btnClicked)

    #*SLOTS FOR EACH SIGNAL BELOW:
    #*slots for status tab:
    #*Enables or disables swiftblock:
    def toggleStatusClicked(self):
        #*If swiftblock is enabled, disable it:
        if self.status:
            self.status=False
            self.parser.write_changes(purge=True)
            #*Reload the status to reflect the change in the GUI:
            self.loadStatus()
        #*If swiftblock is disabled, enable it:
        else:
            self.status=False
            self.parser.write_changes()
            #*Reload the status to reflect the change in the GUI:
            self.loadStatus()

    #*Opens the rule manager window:
    def openRuleManager(self):
        self.rm=RuleManager.RuleManager(self.scriptPath)
        self.close()


    #*Updates the sources(fetches them fro their origin) and then regenerates hosts file:
    def updateSourcesClicked(self):
        try:
            self.parser.generateSourceRules(updateSources=True)
            self.parser.regen_hosts()
            self.loadStatus()#*Refresh the blocked/redirected/allowed counts after the update
            #*Inform the user that the update succeeded:
            msg=QtWidgets.QMessageBox()
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msg.setWindowTitle("Success")
            msg.setText("Sources updated successfully and changes applied!")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.exec()
        except Exception as err:
            self.err_msg(err)

    #*slots for the sources tab:
    def sourceSelected(self,current):
        #*Make sure the list isnt empty(which makes selected item None type)
        if self.sourcesList.currentItem():
            item=self.sourcesList.currentItem().text()
            #*update the value of the selectedSource global var:
            self.selectedSource=item
            self.sourceName_tf.setText(item)
            self.sourceURL_tf.setText(self.sourceDct[item])
            #*Activate the form and show the user that they're now editing a source:
            self.sourcesForm_widget.setDisabled(False)
            self.editMode=True
            self.editMode_lbl.setText("Editing an existing source:")
            self.editMode_lbl.show()
            #*also hide previous status messages and enable the delete btn:
            self.formStatus_lbl.hide()
            self.sourceDelete_btn.setDisabled(False)

    def addBtnClicked(self):
        #*Clear(and enable if disabled) the form and change the editMode to add mode:
        self.sourcesForm_widget.setDisabled(False)
        self.editMode_lbl.show()
        self.sourceName_tf.setText('')
        self.sourceURL_tf.setText('')
        self.editMode=False
        self.editMode_lbl.setText("Adding a new source:")
        #*Also hide any previous messages:
        self.formStatus_lbl.hide()

    def deleteBtnClicked(self):
        #*ensure that a source from the list is selected,warn the user otherwise:
        if not self.selectedSource:
            self.showStatus_lbl("Select a source from the list first!",self.formStatus_lbl)
        else:
            #*Ask the user if they really want to delete the source
            question=QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,"Please Confirm","Are you sure you want to delete this source?",(QtWidgets.QMessageBox.StandardButton.Yes|QtWidgets.QMessageBox.StandardButton.No))
            confirm=question.exec()
            if confirm==QtWidgets.QMessageBox.StandardButton.Yes:
                self.sourceDelete_btn.setDisabled(True)
                try:
                    self.parser.del_source(self.selectedSource)
                    self.loadSrcData()
                    self.showStatus_lbl("Deleted source successfully!",self.formStatus_lbl,True)
                except Exception as err:
                    self.err_msg(err)
                    self.showStatus_lbl("Oops! An error occurred",self.formStatus_lbl)
                self.sourceDelete_btn.setDisabled(True)

    def sourceSaveBtnClicked(self):
        srcName=self.sourceName_tf.text()
        srcURL=self.sourceURL_tf.text()
        if(srcName=="" or srcURL==""):
            self.formStatus_lbl.setStyleSheet("color:white;background-color:crimson;font-weight:bold")
            self.formStatus_lbl.setText("Fields can't be empty!")
            self.formStatus_lbl.show()
        #*ensure that a source from the list is selected,warn the user otherwise:
        elif not self.selectedSource and self.editMode:
            self.showStatus_lbl("Select a source from the list first!",self.formStatus_lbl)
        else:
            #*Save button disabled to prevent multiple save attempts at once
            self.sourceSave_btn.setDisabled(True)
            #*Check the mode[editMode when True is to edit an existing source and to add a new source when False]
            if self.editMode:
                try:
                    self.parser.edit_source(self.selectedSource,srcName,self.sourceDct[self.selectedSource],srcURL)
                    self.loadSrcData()
                    self.showStatus_lbl("Edited source successfully!",self.formStatus_lbl,True)
                except Exception as err:
                    self.err_msg(err)
                    self.showStatus_lbl("Oops! An error occurred",self.formStatus_lbl)
                    #*calling this here incase the editing of the source succeeded but something else failed:(which would effectively make existing sourceList entries old and obsolete)
                    self.loadSrcData()


            else:
                try:
                    self.parser.add_source(srcName,srcURL)
                    self.loadSrcData()
                    self.showStatus_lbl("Added source successfully!",self.formStatus_lbl,True)
                except Exception as err:
                    self.err_msg(err)
                    self.showStatus_lbl("Oops! An error occurred",self.formStatus_lbl)
                    #*calling this here incase the adding of the source succeeded but something else failed:(which would effectively make existing sourceList entries old and obsolete)
                    self.loadSrcData()

            #*re-enable the save btn
            self.sourceSave_btn.setDisabled(False)

    #*Slots for the about tab:
    def gitRepo_btnClicked(self):
        import webbrowser
        if sys.platform.startswith('win32'):
            webbrowser.open("https://github.com/XploreInfinity/swift-block")
        else:
            self.err_msg("To see the Git Repo,visit 'https://github.com/XploreInfinity/swift-block' in your web-browser.\n\nSince swiftblock runs as root/administrator user,we can't(safely)open it for you")

    def license_btnClicked(self):
        import webbrowser
        if sys.platform.startswith('win32'):
            webbrowser.open("https://github.com/XploreInfinity/swift-block/blob/main/LICENSE")
        else:
            self.err_msg("To see the license,visit 'https://github.com/XploreInfinity/swift-block/blob/main/LICENSE' in your web-browser.\n\nSince swiftblock runs as root/administrator user,we can't(safely)open it for you")

    def uninstall_btnClicked(self):
        #*Ask the user if they really want to uninstall swift-block:
        question=QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,"Please Confirm","Swift Block will be removed along with its menu launcher. Are you sure you want to continue?",(QtWidgets.QMessageBox.StandardButton.Yes|QtWidgets.QMessageBox.StandardButton.No))
        confirm=question.exec()
        if confirm==QtWidgets.QMessageBox.StandardButton.Yes:
                try:
                    #*Call the uninstaller:
                    self.parser.uninstall()
                except Exception as err:
                    #*Unfortunately, windows doesnt allow running programs to be deleted. So uninstalling swiftblock from within swiftblock will certainly fail
                    #*Pip will uninstall the package,but some .exe files will persist in the %TEMP% directory. This is a trivial faliure and not worth asking
                    #*the user to manually uninstall swiftblock from cmd. Exit swiftblock and call it a day:
                    if sys.platform.startswith('win32'):
                        print(err)
                        exit()
                    self.err_msg(str(err)+'\nTry uninstalling swift-block using pip from your terminal/cmd')
