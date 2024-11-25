import os, requests

API_URL = os.getenv('API_URL')
user_tokens = {}


async def get_token(data, message):
    response = requests.post(f"{API_URL}token/", data)
    if response.status_code == 200:
        token = response.json().get('token')
        user_tokens[message.from_user.id] = token
        await message.answer("Вы успешно авторизовались! Теперь вы можете получать данные.")
    else:
        raise Exception("Ошибка авторизации. Проверьте логин и пароль.")
            # await message.answer("Ошибка авторизации. Проверьте логин и пароль.")


async def get_tasks(message):
    token = user_tokens.get(message.from_user.id)
    if not token:
        await message.answer("Вы не авторизованы.")
        return

    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{API_URL}tasks/", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception("Ошибка при получении данных. Проверьте ваши права доступа.")
