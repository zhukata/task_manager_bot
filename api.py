import os, httpx

from database.orm_query import orm_add_user, orm_get_user, orm_update_user


API_URL = os.getenv('API_URL')


async def auth_user(session, message, data):
    user_id = message.from_user.id
    print(f"User ID: {user_id}")

    try:
        # Получаем пользователя из базы данных
        user = await orm_get_user(session, user_id)
        print(f"User from DB: {user}")

        # Проверяем валидность токена, если пользователь найден
        if user and await is_token_valid(user):
            await message.answer("Вы успешно авторизованы!")
            return

        # Если пользователь не найден или токен недействителен
        print("START")
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_URL}token/", data=data)

        print(f"Response status: {response.status_code}")

        if response.status_code == 200:
            # Получаем токены из ответа
            tokens = response.json()
            access_token = tokens.get('access')
            refresh_token = tokens.get('refresh')

            if not access_token or not refresh_token:
                raise ValueError("Ответ API не содержит токенов")

            # Создаём пользователя
            new_user = await make_data(user_id, access_token, refresh_token)
            print(f"New user: {new_user}")

            # Сохраняем пользователя в базу данных
            await add_user(session, message, new_user)
            await message.answer("Вы успешно авторизованы!")

        elif response.status_code == 401:
            await message.answer("Ошибка авторизации. Проверьте логин и пароль.")

        else:
            await message.answer("Что-то пошло не так при авторизации.")

    except Exception as e:
        # Логируем ошибку и уведомляем пользователя
        print(f"Ошибка в auth_user: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")
            
            
async def add_user(session, message, new_user):
    try:
        print('Start adding user...')
        await orm_add_user(session, new_user)  # Добавляем пользователя
        print('End adding.')
        await message.answer("Вы успешно авторизовались! Теперь вы можете получать данные.")
    except Exception as e:
        # Логируем ошибку и уведомляем пользователя
        print(f"Ошибка при добавлении пользователя: {e}")
        await message.answer("Ошибка базы данных. Попробуйте позже.")


async def refresh_access_token(session, user):
    """Обновление access-токена с помощью refresh-токена."""
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}token/refresh/",
            data={"refresh": user.refresh_token}
            )
    if response.status_code == 200:
        new_access_token = response.json().get("access")
        updated_user = make_data(user.id, new_access_token, user.refresh_token)
        orm_update_user(session, user.id, updated_user)
        return new_access_token
    return None


async def get_access_token(session, user_id):
    """Возвращает действующий access-токен."""
    user = await orm_get_user(session, user_id)
    if not user:
        return None

    if not await is_token_valid(user):  # Проверка срока действия токена
        token = await refresh_access_token(user)
    return token


async def make_data(user_id, access_token, refresh_token):
    return {
        'telegram_id': user_id,
        'access_token': access_token,
        'refresh_token': refresh_token,
        }


async def is_token_valid(user):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}token/verify/",
            data={"token": user.access_token},
        )
    if response.status_code == 200:
        return True
    return False
    
    
        
async def get_tasks(session, message):
    token = get_access_token(session, message.from_user.id)
    if not token:
        await message.answer("Вы не авторизованы.")
        return None

    headers = {"Authorization": f"Token {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}tasks/", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception("Ошибка при получении данных. Проверьте ваши права доступа.")