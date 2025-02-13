from flask import request, jsonify
from app.services.post_service import create_post, like_post, create_comment
import logging

logging.basicConfig(level=logging.INFO)

def create_post_controller():
    """
    Контроллер для создания поста.
    Ожидает user_id, text и image_url в теле запроса.
    Возвращает post_id в случае успеха.
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        text = data.get('text', '')
        image_url = data.get('image_url', '')

        if not user_id:
            logging.error("Недостаточно данных для создания поста.")
            return jsonify({"error": "Недостаточно данных для создания поста"}), 400

        post_id = create_post(user_id, text, image_url)
        if not post_id:
            return jsonify({"error": "Ошибка при создании поста"}), 500

        return jsonify({"message": "Пост успешно создан", "post_id": post_id}), 201
    except Exception as e:
        logging.error(f"Ошибка при создании поста: {str(e)}")
        return jsonify({"error": "Внутренняя ошибка сервера"}), 500

def like_post_controller(user_id, post_id):
    """
    Контроллер для лайка поста.
    Ожидает user_id и post_id в URL.
    Возвращает количество лайков в случае успеха.
    """
    try:
        likes = like_post(user_id, post_id)
        if likes is None:
            return jsonify({"error": "Пост не найден"}), 404

        return jsonify({"message": "Пост успешно лайкнут", "likes": likes}), 200
    except Exception as e:
        logging.error(f"Ошибка при лайке поста: {str(e)}")
        return jsonify({"error": "Внутренняя ошибка сервера"}), 500

def create_comment_controller(user_id, post_id):
    """
    Контроллер для создания комментария.
    Ожидает user_id, post_id и text в теле запроса.
    Возвращает comment_id в случае успеха.
    """
    try:
        data = request.json
        text = data.get('text')

        if not text:
            logging.error("Недостаточно данных для создания комментария.")
            return jsonify({"error": "Недостаточно данных для создания комментария"}), 400

        comment_id = create_comment(user_id, post_id, text)
        if not comment_id:
            return jsonify({"error": "Ошибка при создании комментария"}), 500

        return jsonify({"message": "Комментарий успешно создан", "comment_id": comment_id}), 201
    except Exception as e:
        logging.error(f"Ошибка при создании комментария: {str(e)}")
        return jsonify({"error": "Внутренняя ошибка сервера"}), 500