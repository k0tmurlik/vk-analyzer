import vk_api
import config
from handlers import *
from threading import Thread

try:
    import config_local as config
except ImportError:
    pass

class Main:
    workers: list = []

    def __init__(self):
        vk_session = vk_api.VkApi(token=config.access_token)
        f = Functions(vk_session)

        print("ℹ️ Бот запущен.\n⚙️ Запуск обработчиков указанных в конфиге...\n")
        for handler in config.handlers:
            status = config.handlers[handler]
            if not status:
                print(f"⛔️ Обработчик `{handler}` отключен.")
                continue

            multiprocess_worker = None
            if handler == "removed_friends":
                multiprocess_worker = Thread(target=RemovedFriends, args=(vk_session, f,))
            elif handler == "relation_partner_removed":
                multiprocess_worker = Thread(target=RelationPartnerRemoved, args=(vk_session, f,))

            if multiprocess_worker is not None:
                self.workers.append(multiprocess_worker)

                multiprocess_worker.daemon = True
                multiprocess_worker.start()

                print(f"✅ Обработчик `{handler}` запущен!")

        try:
            for worker in self.workers:
                worker.join()
        except KeyboardInterrupt:
            pass

        print("\n\n👋🏻 Пока, пока!")


Main()
