'''
Created on Sep 9, 2014

@author: davy.moyon
'''
from __future__ import division
import sys
from PyQt4 import QtCore, QtGui



class MainWindow(QtGui.QMainWindow):

    def __init__(self,  parent = None, settingVersion=1):
        # initialization of the superclass
        super(MainWindow, self).__init__(parent)

        # ui setup
        self.setupUi()
        
        # the console we want to use
#         self.createConsole = self.createIpythonConsole
        self.createConsole = self.createSpyderConsole
        
        self.createConsole()
        
    def dummyForDebuggerTest(self):
        print 'test'
        
        
    def setupUi(self):
        
        self.consoleDock = QtGui.QDockWidget(self)
        self.consoleLayout = QtGui.QWidget()
        self.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.consoleDock)
          
    def createIpythonConsole(self):
        from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
        from IPython.qt.inprocess import QtInProcessKernelManager
        from IPython.lib import  backgroundjobs
#         from IPython.lib import guisupport
#         app = guisupport.get_app_qt4()
        # Create an in-process kernel
        # >>> print_process_id()
        # will print the same process ID as the main process
        kernel_manager = QtInProcessKernelManager()
        kernel_manager.start_kernel()
        self.kernel = kernel_manager.kernel
        self.kernel.gui = 'qt4'
        
        # create a background job manager
        self.bg = backgroundjobs.BackgroundJobManager()
        self.ns = {'main':self}
        self.kernel.shell.push(self.ns)
        kernel_client = kernel_manager.client()
        kernel_client.start_channels()
        
        def stop():
            kernel_client.stop_channels()
            kernel_manager.shutdown_kernel()
            app.exit()
    
        control = RichIPythonWidget()
        control.kernel_manager = kernel_manager
        control.kernel_client = kernel_client
        control.exit_requested.connect(stop)

        self.consoleDock.setWidget(control)
#         self.control.setParent(self.consoleDock)
        control.show()
#         guisupport.start_event_loop_qt4(app)         
            
  
    def createSpyderConsole(self):
        from spyderlib.widgets.internalshell import InternalShell
        from spyderlib.plugins.variableexplorer import VariableExplorer
        from spyderlib.qt.QtGui import (QFont)
        # from spyderlib.qt.QtGui import (QApplication, QMainWindow, QWidget, QLabel,
        #                                 QLineEdit, QHBoxLayout, QDockWidget, QFont)
        # from spyderlib.qt.QtCore import Qt
        # Create the console widget
        font = QFont("Courier new")
        font.setPointSize(10)
        self.ns = {'main':self}
#         ns =None
        msg = "Main window can be accessed with main"
        # Note: by default, the internal shell is multithreaded which is safer
        # but not compatible with graphical user interface creation.
        # For example, if you need to plot data with Matplotlib, you will need
        # to pass the option: multithreaded=False
#         self.console = InternalShell(self, namespace=ns, message=msg, 
#                                     max_line_count= 2000, multithreaded=False)
        self.console = InternalShell(self, namespace=self.ns, message=msg, 
                                     max_line_count= 2000, multithreaded=True)
        self.consoleDock.setWidget(self.console)
        self.console.setParent(self.consoleDock)
        # Setup the self.consoleole widget    
        self.console.set_font(font)
        self.console.set_codecompletion_auto(True)
        self.console.set_calltips(True)
#         self.console.setup_calltips(size=600, font=font)
        self.console.setup_completion(size=(300, 200), font=font)
#         self.console.setMaximumBlockCount(2000)    # change the max number of line we can scroll (same as max_line_count in constructor)

        
        
        
if __name__ == "__main__":
 
    app = QtGui.QApplication(sys.argv)
 
    window = MainWindow()
    window.show()
 
    sys.exit(app.exec_())
