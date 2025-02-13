from firebase_admin import db
from app.models.post_model import Post, Comment
import uuid
from datetime import datetime

def add_post(user_id, post_id, post_data):
    """Добавляет пост в базу данных для конкретного пользователя.
    :param post_data: Данные поста в формате словаря."""
    ref = db.reference(f'posts/{post_id}')
    ref.set(post_data)
    print(f'Пост {post_id} добавлен в базу данных.')

def get_user_nickname(user_id):
    """Получает никнейм пользователя по его user_id.
    :return: Никнейм пользователя или пустая строка, если пользователь не найден."""
    user_ref = db.reference(f'users/{user_id}/info')
    user_data = user_ref.get()
    if user_data:
        return user_data.get('nickname', '')
    return ''

def check_post_id_exists(post_id):
    """Проверяет, существует ли пост с указанным post_id.
    :return: True, если пост существует, иначе False."""
    ref = db.reference(f'posts/{post_id}')
    return ref.get() is not None

def create_post(user_id, text="", image_url=""):
    """Создает новый пост для пользователя.
    :return: Уникальный идентификатор поста (post_id) или None, если пользователь не найден."""
    nickname = get_user_nickname(user_id)
    if not nickname:
        print(f"Ошибка: Никнейм пользователя с ID {user_id} не найден.")
        return None

    post_id = str(uuid.uuid4())
    post_data = {
        "user_id": user_id,
        "nickname": nickname,
        "text": text,
        "image_url": image_url,
        "timestamp": datetime.utcnow().isoformat(),
        "likes": 0,
        "liked_by": [],  # Список пользователей, которые лайкнули пост
        "comments": {}
    }

    add_post(user_id, post_id, post_data)
    print(f'Пост {post_id} успешно создан для пользователя {user_id}.')
    return post_id

def like_post(user_id, post_id):
    """Увеличивает количество лайков у поста, если пользователь еще не лайкал его.
    :return: Количество лайков или None, если пост не найден."""
    post_ref = db.reference(f'posts/{post_id}')
    post_data = post_ref.get()

    if not post_data:
        print(f"Ошибка: Пост с ID {post_id} не найден.")
        return None

    # Проверяем, лайкал ли пользователь пост ранее
    liked_by = post_data.get('liked_by', [])
    if user_id in liked_by:
        print(f"Пользователь {user_id} уже лайкал пост {post_id}.")
        return post_data.get('likes', 0)  # Возвращаем текущее количество лайков

    # Добавляем пользователя в список лайкнувших
    liked_by.append(user_id)
    post_data['liked_by'] = liked_by

    # Увеличиваем количество лайков
    post_data['likes'] = post_data.get('likes', 0) + 1

    # Обновляем данные поста в Firebase
    post_ref.update(post_data)
    print(f'Пост {post_id} лайкнут пользователем {user_id}.')
    return post_data['likes']

def check_comment_id_exists(post_id, comment_id):
    """Проверяет, существует ли комментарий с указанным comment_id у поста.
    :return: True, если комментарий существует, иначе False."""
    ref = db.reference(f'posts/{post_id}/comments/{comment_id}')
    return ref.get() is not None

def add_comment(post_id, comment_id, comment_data):
    """Добавляет комментарий к посту.
    :param comment_data: Данные комментария в формате словаря."""
    ref = db.reference(f'posts/{post_id}/comments')
    ref.child(comment_id).set(comment_data)
    print(f'Комментарий {comment_id} добавлен к посту {post_id}.')

def create_comment(user_id, post_id, text):
    """Создает новый комментарий к посту.
    :return: Уникальный идентификатор комментария (comment_id) или None, если пользователь не найден."""
    nickname = get_user_nickname(user_id)
    if not nickname:
        print(f"Ошибка: Никнейм пользователя с ID {user_id} не найден.")
        return None

    while True:
        comment_id = str(uuid.uuid4())
        if not check_comment_id_exists(post_id, comment_id):
            break

    comment_data = {
        "user_id": user_id,
        "nickname": nickname,
        "text": text,
        "timestamp": datetime.utcnow().isoformat()
    }

    add_comment(post_id, comment_id, comment_data)
    print(f'Комментарий {comment_id} успешно создан к посту {post_id}.')
    return comment_id