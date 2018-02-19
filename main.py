from gui.App import App
import db_config

if __name__ == "__main__":
    db_config.initialize_db()
    app = App()#starts application cycle