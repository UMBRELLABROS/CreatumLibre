MAIN_DIALOG = """
            QDialog {
                background-color: #222831;  /* Dark background */
                color: white;
                border-radius: 10px;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
                color: #EEEEEE; /* Soft contrast */
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #393E46; /* Groove color */
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #00ADB5; /* Handle color */
                width: 14px;
                height: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }
        """

BTN_APPLY = """
            QPushButton {
                background-color: #00ADB5;
                color: white;
                border-radius: 5px;
                height: 30px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #007F8F;
            }
        """

BTN_CANCEL = """
            QPushButton {
                background-color: #F05454;
                color: white;
                border-radius: 5px;
                height: 30px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #D43C3C;
            }
        """
