from flask import request, jsonify
from app.services.user_service import register_step1, register_step2, login_user, update_profile
import logging

logging.basicConfig(level=logging.INFO)

def register_step1_controller():
    """
    Контроллер для первого этапа регистрации пользователя.
    Ожидает email и password в теле запроса.
    Возвращает user_id в случае успеха.
    """
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            logging.error("Недостаточно данных для первого этапа регистрации.")
            return jsonify({"error": "Недостаточно данных для регистрации"}), 400

        user_id = register_step1(email, password)
        if not user_id:
            return jsonify({"error": "Ошибка при регистрации пользователя"}), 500

        return jsonify({"message": "Пользователь успешно зарегистрирован на первом этапе", "user_id": user_id}), 201
    except Exception as e:
        logging.error(f"Ошибка при регистрации пользователя на первом этапе: {str(e)}")
        return jsonify({"error": "Внутренняя ошибка сервера"}), 500

def register_step2_controller(user_id):
    """
    Контроллер для второго этапа регистрации пользователя.
    Ожидает nickname, description и avatar в теле запроса.
    Возвращает обновленные данные пользователя.
    """
    try:
        data = request.json
        nickname = data.get('nickname')
        description = data.get('description', '')
        avatar = data.get('avatar', '')

        if not nickname:
            logging.error("Никнейм обязателен для заполнения.")
            return jsonify({"error": "Никнейм обязателен для заполнения"}), 400

        user_data = register_step2(user_id, nickname, description, avatar)
        if not user_data:
            return jsonify({"error": "Пользователь не найден"}), 404

        return jsonify({
            "message": "Профиль успешно обновлен на втором этапе",
            "user_data": {
                "nickname": nickname,
                "description": description,
                "avatar": avatar
            }
        }), 200
    except Exception as e:
        logging.error(f"Ошибка при обновлении профиля пользователя на втором этапе: {str(e)}")
        return jsonify({"error": "Внутренняя ошибка сервера"}), 500

def login_user_controller():
    """
    Контроллер для входа пользователя.
    Ожидает email и password в теле запроса.
    Возвращает user_id в случае успеха.
    """
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            logging.error("Недостаточно данных для входа.")
            return jsonify({"error": "Недостаточно данных для входа"}), 400

        user_id = login_user(email, password)
        if not user_id:
            return jsonify({"error": "Неверный email или пароль"}), 401

        return jsonify({"message": "Успешный вход", "user_id": user_id}), 200
    except Exception as e:
        logging.error(f"Ошибка при входе пользователя: {str(e)}")
        return jsonify({"error": "Внутренняя ошибка сервера"}), 500

def update_profile_controller(user_id):
    """
    Контроллер для обновления профиля пользователя.
    Ожидает nickname, description и avatar в теле запроса.
    Возвращает обновленные данные пользователя.
    """
    try:
        data = request.json
        nickname = data.get('nickname')
        description = data.get('description', '')
        avatar = data.get('avatar', '')

        if not nickname:
            logging.error("Никнейм обязателен для заполнения.")
            return jsonify({"error": "Никнейм обязателен для заполнения"}), 400

        user_data = update_profile(user_id, nickname, description, avatar)
        if not user_data:
            return jsonify({"error": "Пользователь не найден"}), 404

        return jsonify({
            "message": "Профиль успешно обновлен",
            "user_data": {
                "nickname": nickname,
                "description": description,
                "avatar": avatar
            }
        }), 200
    except Exception as e:
        logging.error(f"Ошибка при обновлении профиля пользователя: {str(e)}")
        return jsonify({"error": "Внутренняя ошибка сервера"}), 500