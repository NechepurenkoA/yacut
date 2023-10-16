Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone 
```

```bash
cd yacut
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```bash
    source venv/bin/activate
    ```

* Если у вас windows

    ```bash
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

Запустите проект командой
```bash
flask run
```