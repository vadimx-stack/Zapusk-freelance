# 🔥 Flask Хаос 

![GitHub stars](https://img.shields.io/github/stars/vadimx-stack/flask-project?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/vadimx-stack/flask-project?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/vadimx-stack/flask-project?style=for-the-badge)
![GitHub license](https://img.shields.io/github/license/vadimx-stack/flask-project?style=for-the-badge)

<div align="center">
  <img src="https://i.pinimg.com/originals/8e/0e/d1/8e0ed18a7a87e844dee43a25097118a6.gif" alt="animated" />
</div>

## 🚀 О проекте

Flask Хаос — это высокопроизводительное веб-приложение, созданное с использованием микрофреймворка Flask. Проект разработан с душой художника, страстью к хаосу и работает как швейцарские часы.

> "Код — это искусство, а я — его разрушитель и творец" — CodeDestroyer

## ✨ Функциональность

- ⚡️ Молниеносная скорость работы
- 🔒 Высокий уровень безопасности
- 🎨 Стильный и интуитивно понятный интерфейс
- 📱 Адаптивный дизайн для всех устройств
- 🌍 Мультиязычная поддержка
- 🔄 REST API для интеграции с другими сервисами

## 🛠️ Технологии

<div align="center">
  
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

</div>

## 📋 Требования

- Python 3.8+
- Flask 2.3.3
- Прочие зависимости указаны в `requirements.txt`

## 🔧 Установка

```bash
# Переходим в директорию проекта
cd zapusk

# Создаем виртуальное окружение
python -m venv venv

# Активируем виртуальное окружение
# Для Windows:
venv\Scripts\activate
# Для Linux/Mac:
source venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Запускаем приложение
python app.py
```

## 🚀 Использование

После запуска приложения, оно будет доступно по адресу `http://localhost:5000/`.

```python
# Пример использования API
import requests

response = requests.get('http://localhost:5000/api/data')
data = response.json()
print(data)
```

## 🏗️ Структура проекта

```
📦 zapusk/
 ┣ 📂 instance/               # Директория для экземпляра приложения Flask
 ┣ 📂 static/                 # Статические файлы
 ┃ ┣ 📂 css/                  # CSS стили
 ┃ ┣ 📂 js/                   # JavaScript файлы
 ┃ ┗ 📂 img/                  # Изображения
 ┣ 📂 templates/              # HTML шаблоны
 ┃ ┣ 📜 404.html              # Страница ошибки 404
 ┃ ┣ 📜 base.html             # Базовый шаблон
 ┃ ┣ 📜 client_dashboard.html # Панель клиента
 ┃ ┣ 📜 client_profile.html   # Профиль клиента
 ┃ ┣ 📜 edit_project.html     # Редактирование проекта
 ┃ ┣ 📜 freelancer_dashboard.html # Панель фрилансера
 ┃ ┣ 📜 freelancer_profile.html # Профиль фрилансера
 ┃ ┣ 📜 index.html            # Главная страница
 ┃ ┣ 📜 loading.html          # Страница загрузки
 ┃ ┣ 📜 login.html            # Страница входа
 ┃ ┣ 📜 project_details.html  # Детали проекта
 ┃ ┣ 📜 projects.html         # Страница проектов
 ┃ ┣ 📜 register.html         # Страница регистрации
 ┃ ┣ 📜 submit_proposal.html  # Отправка предложения
 ┃ ┗ 📜 view_proposals.html   # Просмотр предложений
 ┣ 📜 app.py                  # Основной файл приложения
 ┣ 📜 requirements.txt        # Зависимости проекта
 ┗ 📜 README.md               # Документация проекта
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функциональности (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Добавлена новая функция'`)
4. Отправьте изменения в ваш форк (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📝 Лицензия

Распространяется под лицензией MIT. См. файл `LICENSE` для получения дополнительной информации.

## 📬 Контакты

CodeDestroyer - [@vadimx-stack](https://github.com/vadimx-stack) - [@CodeX_developer](https://t.me/CodeX_developer)

<div align="center">
  <img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%">
  
  <p>Сделано с ❤️, кофе и пикселями. Пиши, если хочешь творить вместе!</p>
  
  <img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%">
</div> 