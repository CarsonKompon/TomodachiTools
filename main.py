import os
import sys

from PyQt6 import QtCore, QtGui, QtWidgets, uic


VERSION = 1.0

class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()

        # Load the mainWindow ui file
        uic.loadUi("ui/mainWindow.ui", self)

        self.setWindowTitle(f"TomodachiTool: Version {VERSION}")

        # All QPushButtons
        self.scriptBtn: QtWidgets.QPushButton
        self.flwBtn: QtWidgets.QPushButton
        self.msgBtn: QtWidgets.QPushButton
        self.prjBtn: QtWidgets.QPushButton
        self.lytBtn: QtWidgets.QPushButton 
        self.texBtn: QtWidgets.QPushButton
        self.createWorkspaceBtn: QtWidgets.QPushButton
        self.manegeWorkspaceBtn: QtWidgets.QPushButton

        # Events for opening windows
        self.scriptBtn.clicked.connect(self.showScriptMenu)

    def showScriptMenu(self):
        self.scriptMenu = scriptMenu()
        self.scriptMenu.show()


class scriptMenu(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/scriptMenu.ui", self)
        self.setWindowTitle("Script Menu")

        self.selectBtn: QtWidgets.QPushButton
        self.inputBtn: QtWidgets.QPushButton
        self.outputBtn: QtWidgets.QPushButton
        self.runBtn: QtWidgets.QPushButton

        self.scriptEdit: QtWidgets.QLineEdit
        self.inputEdit: QtWidgets.QLineEdit
        self.outputEdit: QtWidgets.QLineEdit

        self.selectBtn.clicked.connect(self.selectScript)
        self.inputBtn.clicked.connect(self.getInputFile)
        self.outputBtn.clicked.connect(self.getOutputFile)

        self.runBtn.clicked.connect(self.runScript)

    def selectScript(self) -> None:
        file = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Select a script",
            directory=f"{os.getcwd()}/scripts",
            filter="Python Script (*.py)"
        )
        self.scriptEdit.setText(file[0])

    def getInputFile(self) -> None:
        file = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            directory=os.getcwd(),
            caption="Select an input file.",
        )
        self.inputEdit.setText(file[0])

    def getOutputFile(self) -> None:
        file = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            directory=os.getcwd(),
            caption="Create an output file.",
        )
        self.outputEdit.setText(file[0])

    def runScript(self) -> None:
        # Get the paths of everything that was set earlier
        scriptPath = self.scriptEdit.text()
        inputPath = self.inputEdit.text()
        outputPath = self.outputEdit.text()
        # Check if all paths have been set
        if scriptPath != "" and inputPath != "" and outputPath != "":
            # Run the script with python3, this might not work on all systems
            commandReturnValue = os.system(
                f'python3 "{scriptPath}" "{inputPath}" "{outputPath}"')

            # Error code 9009 occurs when a malfunction occurs in software
            # This happens when the user does not have Microsoft Store version of python
            # installed, thus this check is to ensure it runs on installations via the website
            if commandReturnValue == 9009:
                commandReturnValue = os.system(
                    f'python "{scriptPath}" "{inputPath}" "{outputPath}"')

            message = QtWidgets.QMessageBox()
            # Check the script ran succesfully, but account for every other error code
            if commandReturnValue != 0:
                message.setWindowTitle("Script Error")
                message.setText(
                    f"""The selected script has not executed properly! The script exited with exit code {commandReturnValue}.""")
                message.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                message.exec()
            else:
                message.setWindowTitle("Script Success")
                message.setText(
                    f"The selected script has executed properly!")
                message.setIcon(QtWidgets.QMessageBox.Icon.Information)
                message.exec()
        else:
            # if not all the paths were not inputted an error will occur
            pathsNotSetMessage = QtWidgets.QMessageBox()
            pathsNotSetMessage.setWindowTitle("Script Error")
            pathsNotSetMessage.setText(
                "Please select all the paths before running a script."
            )
            pathsNotSetMessage.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            pathsNotSetMessage.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec())
