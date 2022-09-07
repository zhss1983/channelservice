# channelservice

Установка Docker Compose

```/usr/bin/bash
VERSION=$(curl --silent https://api.github.com/repos/docker/compose/releases/latest | grep -Po '"tag_name": "\K.*\d')
echo $VERSION
```

В моём случае это v2.10.2

```/usr/bin/bash
DESTINATION=/usr/local/bin/docker-compose
sudo curl -L https://github.com/docker/compose/releases/download/${VERSION}/docker-compose-$(uname -s)-$(uname -m) -o $DESTINATION
sudo chmod 755 $DESTINATION
```

Теперь можно и docker-compose.yaml собрать и запустить:

```/usr/bin/bash
docker-compose up
```

Подключение к БД через pgadmin: [http://localhost:5050/browser/](http://localhost:5050/browser/)

хост **postgres**, порт **5432**.

имя пользователя и базы данных **postgres**, пароль: **lehrjgjg**
