import re
from vk_api import VkApi


class Functions:
    vk_session: VkApi = None
    owner_id: int = None

    def __init__(self, vk_session: VkApi):
        self.vk_session = vk_session

        try:  # Пробуем записать ID владельца бота
            self.owner_id = vk_session.method("users.get")[0]['id']
        except Exception:
            exit("📛  Некорректный токен, нужно ввести новый.")

    def send_message(self, peer_id: int, text: str, params: object = {}):
        if params.get('random_id') is None:
            params['random_id'] = 0
        params['peer_id'] = peer_id
        params['message'] = text

        try:
            if len(text) > 4096:  # Если сообщение больше 4096 символов, то делим на несколько сообщений.
                n = 4000
                chunks = [text[i - n:i] for i in range(n, len(text) + 1, n)]

                response = []
                for chunk in chunks:
                    response.append(self.send_message(peer_id, chunk, params))
                return response

            return self.vk_session.method("messages.send", params)
        except Exception:
            return None

    def edit_message(self, peer_id: int, message_id: int, text: str, params: object = {}):
        if params.get('keep_forward_messages') is None:
            params['keep_forward_messages'] = 1
        params['peer_id'] = peer_id
        params['message_id'] = message_id
        params['message'] = text

        try:
            return self.vk_session.method("messages.edit", params)
        except Exception:
            return None

    def get_user(self, scheme: str):

        url = re.findall(r'vk\.com/([a-zA-Z0-9_\.]+)', scheme)
        if len(url) > 0:
            scheme = url[0]

        reg = re.findall(r'\[id(\d*)\|.*]', scheme)
        if len(reg) > 0:
            scheme = reg[0]

        reg = re.findall(r'\[([a-zA-Z0-9_\.]+)\|.*]', scheme)
        if len(reg) > 0:
            scheme = reg[0]

        try:
            return self.vk_session.method("users.get", {"user_ids": scheme})[0]
        except Exception:
            return None
