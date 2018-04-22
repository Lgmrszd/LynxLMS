from gui.App import App
import db_config
import managers.user_manager
import logging

if __name__ == "__main__":
    logging.basicConfig(filename='main.log', level=logging.DEBUG, format='%(asctime)s \
                        | %(levelname)s: %(message)s ') #logging confgi description
    db_config.init_db()
    managers.user_manager.Queue.update_queue()
    app = App()#starts application cycle