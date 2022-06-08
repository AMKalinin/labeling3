import sys
from PyQt5.QtWidgets import QApplication
from qssimport import stylesheet

import main
import utils

if __name__ == '__main__':
    
    utils.check_create_projects_folder()
    app = QApplication(sys.argv)
    screen_rect = app.desktop().screenGeometry()

    utils.load_fonts()
    utils.load_style(app)
    #app.setStyle('Windows')
    
    window = main.mainWindow(screen_rect)
    window.show()
    sys.exit(app.exec_())
    