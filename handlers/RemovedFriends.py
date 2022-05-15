import time
from vk_api import VkApi
from functions import Functions


class RemovedFriends:
    """
        Класс, который вызывается при включенном обработчике removed_friends.
        Проверяет каждые n-секунд список подписок и при наличии подписок, отписывается и отправляет уведомление самому себе об этом в ЛС.

        Параметры, которые можно менять: n (количество секунд, между которыми происходит проверка, не советую менять на число ниже 1200)
    """

    vk_session: VkApi = None
    f: Functions = None
    n: int = 1800

    def __init__(self, vk_session: VkApi, f: Functions):
        self.vk_session = vk_session
        self.f = f

        self.handler()

    def handler(self):
        while True:
            time.sleep(self.n)  # Специально в начале, чтобы бот сразу же не удалил все заявки в друзья, подождем n секунд и потом удалим

            my_requests = self.vk_session.method("friends.getRequests", {"out": 1, "extended": 1})  # Получаем исходящие заявки в друзья
            if my_requests['count'] <= 0:  # Если количество заявок <= 0 (от VK Api все что угодно можно ожидать), то ничего не делаем
                continue

            count = 0
            text = "🔔 Список клоунов удаливших из друзей:\n"

            for user in my_requests['items']:
                response = self.vk_session.method("friends.delete", {"user_id": user['user_id']})
                if response.get('success') == 1:
                    count += 1
                    text += f"🚷 [id{user['user_id']}|{user['first_name']} {user['last_name']}] удалил(-а) Вас из друзей.\n"

                    print(f"⚙️ {user['first_name']} {user['last_name']} (vk.com/id{user['user_id']} удалил(-а) Вас из друзей.")

            text += f"\nℹ️ Общее количество клоунов, от которых отписался бот: {count}"
            self.f.send_message(self.f.owner_id, text)

