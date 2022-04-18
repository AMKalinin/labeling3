import sys
from PyQt5.QtWidgets import QApplication

import main
import utils

if __name__ == '__main__':
    
    utils.check_create_projects_folder()
    app = QApplication(sys.argv)
    window = main.main_window()
    window.show()
    sys.exit(app.exec_())