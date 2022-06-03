import sys
from PyQt5.QtWidgets import QApplication

import main
import utils

if __name__ == '__main__':
    
    utils.check_create_projects_folder()
    app = QApplication(sys.argv)

    utils.load_fonts()
    utils.load_style(app)
    
    window = main.mainWindow()
    window.show()
    sys.exit(app.exec_())
    