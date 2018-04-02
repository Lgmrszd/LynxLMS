from gui.App import App
import db_config
import managers.user_manager

if __name__ == "__main__":
    db_config.init_db()
    managers.user_manager.Queue.update_queue()
    app = App()#starts application cycle