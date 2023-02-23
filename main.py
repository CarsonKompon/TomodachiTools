import os

from PyQt6 import QtCore, QtGui, QtWidgets

cssStyleButton = """
color: #333;
border: 2px solid #555;
border-radius: 20px;
"""

cssStyleMenubar = """
color: black;
border-color: rgb(148, 148, 148);
"""

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Initialize the Window and it's properties
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(382, 475)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("")

        # Initialize the central widget
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Initialize the Header Text "TomodachiTools"
        self.lblHeader = QtWidgets.QLabel(parent=self.centralwidget)
        self.lblHeader.setGeometry(QtCore.QRect(60, 30, 261, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lblHeader.setFont(font)
        self.lblHeader.setObjectName("lblHeader")

        # Initialize the Subheader Text
        self.lblSubheader = QtWidgets.QLabel(parent=self.centralwidget)
        self.lblSubheader.setGeometry(QtCore.QRect(80, 70, 341, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(11)
        self.lblSubheader.setFont(font)
        self.lblSubheader.setObjectName("lblSubheader")

        # Initialize the Github and Discord buttons
        self.logoGithub = QtWidgets.QLabel(parent=self.centralwidget)
        self.logoGithub.setGeometry(QtCore.QRect(306, 416, 30, 30))
        self.logoGithub.setText("")
        self.logoGithub.setPixmap(QtGui.QPixmap(":/logos/discord_black.png"))
        self.logoGithub.setScaledContents(True)
        self.logoGithub.setObjectName("logoGithub")
        self.logoDiscord = QtWidgets.QLabel(parent=self.centralwidget)
        self.logoDiscord.setGeometry(QtCore.QRect(346, 416, 30, 30))
        self.logoDiscord.setText("")
        self.logoDiscord.setPixmap(QtGui.QPixmap(":/logos/github_black.png"))
        self.logoDiscord.setScaledContents(True)
        self.logoDiscord.setObjectName("logoDiscord")

        # Initialize the line that separates the file menu from the rest of the window
        self.line = QtWidgets.QFrame(parent=self.centralwidget)
        self.line.setGeometry(QtCore.QRect(-10, -10, 401, 31))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")

        buttonPos = 100

        # Initialize the "Project Editor" button
        self.btnProjectEditor = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnProjectEditor.setGeometry(QtCore.QRect(60, buttonPos, 261, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(16)
        self.btnProjectEditor.setFont(font)
        self.btnProjectEditor.setStyleSheet(cssStyleButton)
        self.btnProjectEditor.setObjectName("btnProjectEditor")
        buttonPos += 60

        # Initialize the "Layout Editor" button
        self.btnLayoutEditor = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnLayoutEditor.setGeometry(QtCore.QRect(60, buttonPos, 261, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(16)
        self.btnLayoutEditor.setFont(font)
        self.btnLayoutEditor.setStyleSheet(cssStyleButton)
        self.btnLayoutEditor.setObjectName("btnLayoutEditor")
        buttonPos += 60

        # Initialize the "Message Editor" button
        self.btnMessageEditor = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnMessageEditor.setGeometry(QtCore.QRect(60, buttonPos, 261, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(16)
        self.btnMessageEditor.setFont(font)
        self.btnMessageEditor.setStyleSheet(cssStyleButton)
        self.btnMessageEditor.setObjectName("btnMessageEditor")
        buttonPos += 60

        # Initialize the "Flowchart Editor" button
        self.btnFlowchartEditor = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnFlowchartEditor.setGeometry(QtCore.QRect(60, buttonPos, 261, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(16)
        self.btnFlowchartEditor.setFont(font)
        self.btnFlowchartEditor.setStyleSheet(cssStyleButton)
        self.btnFlowchartEditor.setObjectName("btnFlowchartEditor")
        buttonPos += 60

        # Initialize the "Texture Editor" button
        self.btnTextureEditor = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnTextureEditor.setGeometry(QtCore.QRect(60, buttonPos, 261, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(16)
        self.btnTextureEditor.setFont(font)
        self.btnTextureEditor.setStyleSheet(cssStyleButton)
        self.btnTextureEditor.setObjectName("btnTextureEditor")
        buttonPos += 60





        # Initialize the Menu Bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 382, 23))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.menubar.setFont(font)
        self.menubar.setStyleSheet(cssStyleMenubar)
        self.menubar.setObjectName("menubar")

        # Initialize the File Menu
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.menuFile.setFont(font)
        self.menuFile.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.menuFile.setAutoFillBackground(False)
        self.menuFile.setStyleSheet("")
        self.menuFile.setObjectName("menuFile")
        self.menubar.addAction(self.menuFile.menuAction())

        # Initialize the Edit Menu
        self.menuEdit = QtWidgets.QMenu(parent=self.menubar)
        self.menuEdit.setStyleSheet("")
        self.menuEdit.setObjectName("menuEdit")
        self.menubar.addAction(self.menuEdit.menuAction())

        # Initialize the Scripts Menu
        self.menuScripts = QtWidgets.QMenu(parent=self.menubar)
        self.menuScripts.setObjectName("menuScripts")
        self.menubar.addAction(self.menuScripts.menuAction())

        # Initialize the Scripts Sub-Menus by checking folders withing the "scripts" folder
        scriptSubmenuFolders = os.listdir("scripts")
        self.menuScriptsSubmenus = []
        self.menuScriptsFolderNames = []
        for folder in scriptSubmenuFolders:
            if os.path.isdir("scripts/" + folder):
                submenu = QtWidgets.QMenu(parent=self.menuScripts)
                submenu.setObjectName("menuScripts" + folder)
                self.menuScriptsSubmenus.append(submenu)
                self.menuScriptsFolderNames.append(folder)

        MainWindow.setMenuBar(self.menubar)

        # Create the actions for the File Menu
        self.actionFileNew = QtGui.QAction(parent=MainWindow)
        self.actionFileNew.setObjectName("actionNew")
        self.menuFile.addAction(self.actionFileNew)

        self.actionFileOpen = QtGui.QAction(parent=MainWindow)
        self.actionFileOpen.setObjectName("actionFileOpen")
        self.menuFile.addAction(self.actionFileOpen)

        self.actionFileSaveAs = QtGui.QAction(parent=MainWindow)
        self.actionFileSaveAs.setObjectName("actionFileSaveAs")
        self.menuFile.addAction(self.actionFileSaveAs)

        # Create the actions for the Edit Menu
        self.actionEditWorkspaceSettings = QtGui.QAction(parent=MainWindow)
        self.actionEditWorkspaceSettings.setObjectName("actionEditWorkspaceSettings")
        self.menuEdit.addAction(self.actionEditWorkspaceSettings)

        # Create the actions for the Scripts Sub-Menus by checking the files within each folder
        self.menuScriptsActions = []
        self.menuScriptsActionNames = []
        self.menuScriptsActionFunctions = []
        for folder in self.menuScriptsFolderNames:
            scriptFiles = os.listdir("scripts/" + folder)
            for file in scriptFiles:
                if file.endswith(".py"):
                    action = QtGui.QAction(parent=MainWindow)
                    action.setObjectName("action" + file[:-3])
                    
                    def scriptFunc(scriptFile):
                        # Prompt for the input file
                        inputFilePath = QtWidgets.QFileDialog.getOpenFileName(parent=MainWindow, caption="Select the input file", filter="All Files (*.*)")[0]
                        if inputFilePath == "":
                            return

                        # Prompt for the output file
                        outputFilePath = QtWidgets.QFileDialog.getSaveFileName(parent=MainWindow, caption="Select the output file", filter="All Files (*.*)")[0]
                        if outputFilePath == "":
                            return
                        
                        print(scriptFile)
                        print(inputFilePath)
                        print(outputFilePath)

                        # Run the script with the input and output files as arguments
                        os.system("python3 " + scriptFile + " \"" + inputFilePath + "\" \"" + outputFilePath + "\"")

                    action.triggered.connect(lambda checked, scriptFile="scripts/" + folder + "/" + file: scriptFunc(scriptFile))

                    self.menuScriptsSubmenus[self.menuScriptsFolderNames.index(folder)].addAction(action)
                    self.menuScriptsActions.append(action)
                    self.menuScriptsActionNames.append(file[:-3])

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TomodachiTools"))
        
        self.lblHeader.setText(_translate("MainWindow", "TomodachiTool"))
        self.lblSubheader.setText(_translate("MainWindow", "An editor for different file formats"))
        
        self.btnProjectEditor.setText(_translate("MainWindow", "Project Editor"))
        self.btnLayoutEditor.setText(_translate("MainWindow", "Layout Editor"))
        self.btnMessageEditor.setText(_translate("MainWindow", "Message Editor"))
        self.btnFlowchartEditor.setText(_translate("MainWindow", "Flowchart Editor"))
        self.btnTextureEditor.setText(_translate("MainWindow", "Texture Editor"))
        
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuScripts.setTitle(_translate("MainWindow", "Scripts"))

        # File Menu
        self.actionFileNew.setText(_translate("MainWindow", "Create new workspace"))
        self.actionFileOpen.setText(_translate("MainWindow", "Open workspace"))
        self.actionFileSaveAs.setText(_translate("MainWindow", "Save workspace as..."))
        
        # Edit Menu
        self.actionEditWorkspaceSettings.setText(_translate("MainWindow", "Edit workspace settings"))

        # Scripts Menu
        for folder in self.menuScriptsFolderNames:
            self.menuScripts.addMenu(self.menuScriptsSubmenus[self.menuScriptsFolderNames.index(folder)])
            self.menuScriptsSubmenus[self.menuScriptsFolderNames.index(folder)].setTitle(_translate("MainWindow", folder))
            for action in self.menuScriptsActions:
                if action.objectName() == "action" + self.menuScriptsActionNames[self.menuScriptsActions.index(action)]:
                    action.setText(_translate("MainWindow", self.menuScriptsActionNames[self.menuScriptsActions.index(action)].replace("_", " ").replace("-", " ")))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())