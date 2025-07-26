import os
import shutil
import zipfile
import exifread
import time
import tempfile
from pathlib import Path
# Сделал SirRigterion 
# Предопределённые списки расширений
PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif'}
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv'}
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.flac', '.aac', '.ogg'}
TEXT_EXTENSIONS = {'.txt', '.md', '.rtf', '.doc', '.docx'}
LOG_EXTENSIONS = {'.log'}
SCRIPT_EXTENSIONS = {'.py', '.bat', '.sh', '.js', '.ps1'}
EXE_EXTENSIONS = {'.exe'}
ZIP_EXTENSIONS = {'.zip'}

def get_photo_year(file_path):
    # Извлекает год из EXIF-данных фото или времени изменения файла.
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
            date_tag = tags.get('EXIF DateTimeOriginal')
            if date_tag:
                return str(date_tag).split(':')[0]
    except Exception:
        pass
    mod_time = os.path.getmtime(file_path)
    return str(time.localtime(mod_time).tm_year)

def get_file_year(file_path):
    # Извлекает год из времени изменения файла.
    mod_time = os.path.getmtime(file_path)
    return str(time.localtime(mod_time).tm_year)

def ensure_dir(directory):
    # Создаёт директорию, если её нет.
    if not os.path.exists(directory):
        os.makedirs(directory)

def move_file(file_path, target_dir, file_name):
    # Перемещает файл в указанную папку с обработкой дубликатов.
    ensure_dir(target_dir)
    target_path = os.path.join(target_dir, file_name)

    counter = 1
    base_name, ext = os.path.splitext(file_name)
    while os.path.exists(target_path):
        target_path = os.path.join(target_dir, f"{base_name}_{counter}{ext}")
        counter += 1

    try:
        shutil.move(file_path, target_path)
        print(f"Перемещён: {file_path} -> {target_path}")
    except Exception as e:
        print(f"Ошибка при перемещении {file_path}: {e}")

def process_zip(file_path, base_output_dir, sort_method, custom_filters=None):
    # Распаковывает zip-файл и обрабатывает его содержимое.
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
                print(f"Распакован: {file_path} -> {temp_dir}")
            process_directory(temp_dir, base_output_dir, sort_method, custom_filters)
        os.remove(file_path)
        print(f"Удалён: {file_path}")
    except zipfile.BadZipFile:
        print(f"Ошибка: {file_path} не является валидным zip-файлом")
    except Exception as e:
        print(f"Ошибка при обработке {file_path}: {e}")

def process_file_by_year(file_path, base_output_dir):
    # Сортировка по годам.
    ext = os.path.splitext(file_path)[1].lower()
    file_name = os.path.basename(file_path)

    if ext in PHOTO_EXTENSIONS:
        year = get_photo_year(file_path)
        target_dir = os.path.join(base_output_dir, 'Photos', year)
    elif ext in VIDEO_EXTENSIONS:
        year = get_file_year(file_path)
        target_dir = os.path.join(base_output_dir, 'Videos', year)
    elif ext in AUDIO_EXTENSIONS:
        year = get_file_year(file_path)
        target_dir = os.path.join(base_output_dir, 'Audio', year)
    elif ext in TEXT_EXTENSIONS:
        year = get_file_year(file_path)
        target_dir = os.path.join(base_output_dir, 'Text', year)
    elif ext in LOG_EXTENSIONS:
        year = get_file_year(file_path)
        target_dir = os.path.join(base_output_dir, 'Logs', year)
    elif ext in SCRIPT_EXTENSIONS:
        year = get_file_year(file_path)
        target_dir = os.path.join(base_output_dir, 'Scripts', year)
    elif ext in EXE_EXTENSIONS:
        year = get_file_year(file_path)
        target_dir = os.path.join(base_output_dir, 'Executables', year)
    else:
        year = get_file_year(file_path)
        target_dir = os.path.join(base_output_dir, 'Other', year)

    move_file(file_path, target_dir, file_name)

def process_file_by_type(file_path, base_output_dir):
    # Сортировка по типу файла.
    ext = os.path.splitext(file_path)[1].lower()
    file_name = os.path.basename(file_path)

    if ext in PHOTO_EXTENSIONS:
        target_dir = os.path.join(base_output_dir, 'Photos')
    elif ext in VIDEO_EXTENSIONS:
        target_dir = os.path.join(base_output_dir, 'Videos')
    elif ext in AUDIO_EXTENSIONS:
        target_dir = os.path.join(base_output_dir, 'Audio')
    elif ext in TEXT_EXTENSIONS:
        target_dir = os.path.join(base_output_dir, 'Text')
    elif ext in LOG_EXTENSIONS:
        target_dir = os.path.join(base_output_dir, 'Logs')
    elif ext in SCRIPT_EXTENSIONS:
        target_dir = os.path.join(base_output_dir, 'Scripts')
    elif ext in EXE_EXTENSIONS:
        target_dir = os.path.join(base_output_dir, 'Executables')
    else:
        target_dir = os.path.join(base_output_dir, 'Other')

    move_file(file_path, target_dir, file_name)

def process_file_by_custom(file_path, base_output_dir, custom_filters):
    # Сортировка по пользовательским фильтрам с учётом предопределённых категорий.
    ext = os.path.splitext(file_path)[1].lower()
    file_name = os.path.basename(file_path)
    year = get_file_year(file_path)

    # Сначала проверяем предопределённые категории
    if ext in PHOTO_EXTENSIONS:
        target_dir = os.path.join(base_output_dir, 'Photos', year)
    elif ext in VIDEO_EXTENSIONS:
        target_dir = os.path.join(base_output_dir, 'Videos', year)
    elif ext in AUDIO_EXTENSIONS:
        target_dir = os.path.join(base_output_dir, 'Audio', year)
    elif ext in TEXT_EXTENSIONS:
        target_dir = os.path.join(base_output_dir, 'Text', year)
    elif ext in LOG_EXTENSIONS:
        target_dir = os.path.join(base_output_dir, 'Logs', year)
    elif ext in SCRIPT_EXTENSIONS:
        target_dir = os.path.join(base_output_dir, 'Scripts', year)
    elif ext in EXE_EXTENSIONS:
        target_dir = os.path.join(base_output_dir, 'Executables', year)
    else:
        # Проверяем пользовательские фильтры
        for category, extensions in custom_filters.items():
            if ext in extensions:
                target_dir = os.path.join(base_output_dir, category, year)
                move_file(file_path, target_dir, file_name)
                return
        # Если не попадает никуда, отправляем в Other
        target_dir = os.path.join(base_output_dir, 'Other', year)

    move_file(file_path, target_dir, file_name)

def process_directory(root_dir, base_output_dir, sort_method, custom_filters=None):
    # Рекурсивно обрабатывает директорию с учётом метода сортировки.
    for dirpath, _, filenames in os.walk(root_dir):
        if Path(base_output_dir).resolve() in Path(dirpath).resolve().parents:
            continue

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            ext = os.path.splitext(filename)[1].lower()

            if ext in ZIP_EXTENSIONS:
                process_zip(file_path, base_output_dir, sort_method, custom_filters)
            elif sort_method == '1':
                process_file_by_year(file_path, base_output_dir)
            elif sort_method == '2':
                process_file_by_type(file_path, base_output_dir)
            elif sort_method == '3' and custom_filters:
                process_file_by_custom(file_path, base_output_dir, custom_filters)

def get_custom_filters():
    # Запрашивает пользовательские фильтры.
    custom_filters = {}
    print("Введите категории и их расширения (например, 'Documents:.doc,.pdf'). Оставьте пустым для завершения.")
    while True:
        category_input = input("Категория: ").strip()
        if not category_input:
            break
        extensions = input(f"Расширения для {category_input} (через запятую, с точкой, например .txt,.doc): ").strip()
        custom_filters[category_input] = set(ext.lower() for ext in extensions.split(',') if ext)
    return custom_filters

def main():
    # Запрашиваем путь к корневой директории
    root_dir = input("Введите путь к папке с файлами: ").strip()
    if not os.path.isdir(root_dir):
        print("Ошибка: Указанный путь не является директорией или не существует.")
        return

    # Выбор метода сортировки
    print("\nВыберите метод сортировки:")
    print("1. По годам (Photos/Год, Videos/Год, Audio/Год, Text/Год, Logs/Год, Scripts/Год, Executables/Год, Other/Год)")
    print("2. По типу файла (Photos, Videos, Audio, Text, Logs, Scripts, Executables, Other)")
    print("3. По пользовательским фильтрам (с годом) + предопределённые категории")
    sort_method = input("Введите номер метода (1-3): ").strip()

    if sort_method not in ['1', '2', '3']:
        print("Ошибка: Неверный выбор метода.")
        return

    # Создаём базовую директорию
    base_output_dir = os.path.join(root_dir, 'Organized')
    ensure_dir(base_output_dir)

    # Инициализация категорий
    categories = ['Photos', 'Videos', 'Audio', 'Text', 'Logs', 'Scripts', 'Executables', 'Other']
    custom_filters = None

    if sort_method == '1' or sort_method == '2':
        for category in categories:
            ensure_dir(os.path.join(base_output_dir, category))
    elif sort_method == '3':
        custom_filters = get_custom_filters()
        for category in categories + list(custom_filters.keys()):
            ensure_dir(os.path.join(base_output_dir, category))

    # Обрабатываем директорию (сделано Rigterion) 
    process_directory(root_dir, base_output_dir, sort_method, custom_filters)
    print("Обработка завершена!")

if __name__ == "__main__":
    main()