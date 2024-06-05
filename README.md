# Классификатор токсичных комментариев

## Описание

Этот проект состоит из двух компонентов: FastAPI приложения для предсказания токсичности комментариев и веб-интерфейса на Go для взаимодействия с пользователем. Модель машинного обучения написана с помощью `catboost` и была обучена на следующих датасетах:
- [Kaggle](https://www.kaggle.com/datasets/blackmoon/russian-language-toxic-comments)
- [Kaggle](https://www.kaggle.com/datasets/alexandersemiletov/toxic-russian-comments)

## Как запустить

Проект собирается с помощью docker compose, так что убедитесь, что `Docker` и `Docker Compose` установлены на вашей машине.

1. **Склонировать репозиторий**

    ```sh
    git clone https://github.com/Cesoneemz/toxic_comments_analyzator
    ```

2. **Сборка и запуск контейнеров**

    ```sh
    docker compose up --build
    ```

3. **Использование**

    Перейдите на адрес `localhost:8080`

## Техническая информация

- `API Image Size`: 1.01GB
- `Web UI Image Size`: 314.08MB
- `Model Accuracy`: 0.943254890764985
- `Model F1`: 0.8328795643818065