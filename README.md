# Photo Editor (PyQt5 + PIL)

## Описание
**Photo Editor** — это простое приложение для редактирования изображений, созданное с использованием библиотеки **PyQt5** для графического интерфейса и **PIL (Pillow)** для обработки изображений.

Приложение позволяет:
- Загружать изображения из выбранной папки
- Применять базовые фильтры и преобразования
- Сохранять измененные изображения в отдельной папке

## Функции
- **Ч/Б (Чёрно-белый фильтр)** — преобразует изображение в оттенки серого
- **Лево** — поворачивает изображение на 90° влево
- **Право** — поворачивает изображение на 90° вправо
- **Зеркало** — отражает изображение по горизонтали
- **Резкость** — применяет фильтр резкости
- **Сбросить** — возвращает изображение в исходное состояние

## Установка и запуск
### Требования
Перед установкой убедитесь, что у вас установлен **Python 3.7+**.

### Установка зависимостей
```sh
pip install pyqt5 pillow
```

### Запуск приложения
```sh
python main.py
```

## Использование
1. **Нажмите кнопку "Папка"**, чтобы выбрать директорию с изображениями.
2. Выберите изображение из списка слева.
3. Используйте кнопки для применения эффектов.
4. Измененные изображения сохраняются в папке `Modified` внутри выбранной директории.

## Структура проекта
```
PhotoEditor/
│── main.py         # Основной код приложения
│── Modified/       # Директория для сохранения измененных изображений
```

## Лицензия
Этот проект распространяется под лицензией **MIT**. Вы можете свободно использовать и модифицировать код.

