import sys
from PyQt5.QtWidgets import QApplication

import main

if __name__ == '__main__':
    

    app = QApplication(sys.argv)
    window = main.main_window()
    window.show()
    sys.exit(app.exec_())