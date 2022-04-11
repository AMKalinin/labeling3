import sys
from PyQt5.QtWidgets import QApplication

import segflex_main

if __name__ == '__main__':
    

    app = QApplication(sys.argv)
    window = segflex_main.main_window()
    window.show()
    sys.exit(app.exec_())