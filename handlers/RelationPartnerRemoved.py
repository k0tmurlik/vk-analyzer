import time
from vk_api import VkApi
from functions import Functions


class RelationPartnerRemoved:
    """
            Класс, который вызывается при включенном обработчике relation_partner_removed.
            Проверяет каждые n-секунд семейное положение, если из него пропал партнер, то убирает СП и сообщает об этом в ЛС.

            Параметры, которые можно менять: n (количество секунд, между которыми происходит проверка, не советую менять на число ниже 1200),
            default_relation_id (СП, на которое поменяет бот, если партнер уберет СП)
        """

    vk_session: VkApi = None
    f: Functions = None
    n: int = 1800
    default_relation_id = 0  # https://vk.com/dev/account.saveProfileInfo

    def __init__(self, vk_session: VkApi, f: Functions):
        self.vk_session = vk_session
        self.f = f

        self.handler()

    def handler(self):
        status = 0  # Статусы, для того чтобы не было однотипных проверок
        n = self.n  # запоминаем изначальное self.n
        relation_partner_id = 0

        while True:
            time.sleep(self.n)  # Засыпаем на n-секунд, после просыпания сделаем повторную проверку

            profile = self.vk_session.method("account.getProfileInfo")
            if profile.get('relation') in [0, 1, 5] and status != 1:
                status = 1
                self.n = 3600
                relation_partner_id = 0

                print("\n⚙️ RelationPartnerRemoved: У Вас не установлено семейное положение, в связи с этим время проверок увеличено до 1 часа.\n")
                continue  # Если СП у пользователя всё сложно/не женат/не стоит, то изменяем время проверки на один час (чтобы бессмысленно не ддосить VK Api)

            if relation_partner_id == 0:
                if profile.get('relation_partner') is None and status != 1:
                    status = 1
                    self.n = 3600
                    relation_partner_id = 0

                    print("\n⚙️ RelationPartnerRemoved: У семейного положения отсутствует партнёр, в связи с этим время проверок увеличено до 1 часа.\n")
                    continue  # Если у пользователя изначально СП без партнера, то изменяем время проверки на один час (чтобы бессмысленно не ддосить VK Api)

                if profile.get('relation_partner') is None:
                    continue
                else:
                    relation_partner_id = profile.get('relation_partner').get('id')

            if profile.get('relation_partner') is None:
                # Не понятно из-за чего, но почему-то с первого раза ВК не меняет СП, поэтому отправляем сразу же два запроса.
                self.vk_session.method("account.saveProfileInfo", {"relation": self.default_relation_id, "relation_partner_id": 0})
                self.vk_session.method("account.saveProfileInfo", {"relation": self.default_relation_id, "relation_partner_id": 0})

                partner = self.f.get_user(str(relation_partner_id))
                self.f.send_message(self.f.owner_id, f"🔔️ [id{partner['id']}|{partner['first_name']} {partner['last_name']}] убрал(-а) семейное положение.")
                print(f"🔔 {partner['first_name']} {partner['last_name']} убрал(-а) семейное положение.")

            self.n = n
