# Тестовое задание SDIU54

Поместить в папку proj файлы проекта Flask
```bash
   mkdir myproject
   mkdir proj
   ```

1. Создать виртуальное окружение:
    ```bash
   python3.9 -m venv ../venv
   source ../venv/bin/activate
   ```

2. Установить необходимые пакеты:
    ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Указать интерфейс и порт для привязки:
    ```bash
   gunicorn --bind 0.0.0.0:5000 wsgi:app
   ```

4. Создать файл элементов с расширением .service и записат конфигурацию для Gunicorn:
    ```bash
   sudo nano /etc/systemd/system/myproject.service
   ```

    [Unit]
    Description=Gunicorn instance to serve proj
    After=network.target

    [Service]
    User=anton
    Group=www-data
    WorkingDirectory=/home/anton/myproject/proj
    Environment="PATH=/home/anton/myproject/venv/bin"
    ExecStart=/home/anton/myproject/venv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi:app

    [Install]
    WantedBy=multi-user.target

5. Запустить службу Gunicorn и активируем:
    ```bash
   sudo systemctl start proj
   sudo systemctl enable proj
   ```

6. Создать файл конфигурации серверных блоков в каталоге Nginx:
    ```bash
   sudo nano /etc/nginx/sites-available/myproject
   ```

    server {
        listen 80;
        server_name 143.198.134.106 www.143.198.134.106;

        location / {
            include proxy_params;
            proxy_pass http://unix:/home/anton/myproject/proj/myproject.sock;
        }
    }

7. Активировать созданную конфигурацию Nginx:
    ```bash
   sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
   sudo ufw delete allow 5000
   sudo ufw allow 'Nginx Full'
   ```

