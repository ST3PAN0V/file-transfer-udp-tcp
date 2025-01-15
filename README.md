# About
Это мое решение тестового задания.

В ветке main ничего нет, только поясняющий README. 
- В ветке tcp реализовал сервер и клиент на tcp-сокетах.
- В ветке udp соответственно клиент и сервер на udp-сокетах.

## Задание
Написать программы, которые используют сокеты для передачи файлов любого разме-
ра и наполнения. Должна получиться программа-клиент, которая может запросить файл, и
программа-сервер, которая должна по запросу его отправить. Нужно написать две реализации
этих программ, одну с использованием tcp, а другую – с использованием udp.
Кроме этого, нужно написать тест на bash, который создаст файл размером более 1 мегабай-
та со случайным содержимым, запустит эти две программы, чтобы клиент получил созданный
файл от сервера, а затем проверит, что отправленный и полученный файлы совпадают.
## Оформление решения
Мы ожидаем получить архив с git-репозиторием, сообщения коммитов должны быть содер-
жательными (в идеале по conventional commit). В репозитории должно быть две ветки: tcp с
реализацией на tcp сокетах, и udp с реализацией на udp сокетах.
## Структура репозитория:
src/
test/
В src/ должны быть исходники сервера и клиента, в test/ – исходники теста. У каждой
функции в .py файлах должно быть описание, и код должен быть оформлен по PEP8.
## Пример вывода программ
```bash
> python src/server.py filetoserve
serving /path/to/filetoserve
request from 127.0.0.1:8081
sending...
finished sending to 127.0.0.1:8081
----------------------------------
> python src/client.py newfile
requesting from 127.0.0.1:8080
downloading...
downloaded as /path/to/newfile
```

# Примечания

## Реализация tcp и udp
Некоторые вещи я не стал реализовывать намеренно, т.к есть некоторые нюансы которые стоило бы уточнить.
С tcp все гладко. Но с udp возможно несколько вариантов релизации, передачи огромных файлов(как я вижу):
1. По фрагментам размером 4096 байт(необязательно 4096), пока не придёт пустой файл, потом соединение закроется.
2. Можно было бы сначала отправлять пакет, который сообщает размер передаваемого файла, а далее клиент бы уже знал сколько байт ему надо принять.
3. Отправка специального сообщения, сообщающее, что все пакеты получены.
Можно было сделать так, что бы udp работал корректно и получал бы весь поток байт без потерь, добавить подтверждающие пакеты со стороны сервера, трехкратное рукопожатие, но тогда бы udp превратился в tcp и потерял юы скорость. Не знаю насколько нужно было это делать, я решил обойтись без этого.

### Сервер
Как я понял не было необходимости застявлять сервер работать постоянно, и сервер должен быть настроен на 1 соединение. В противном случае реализацию нужно менять, чтобы сервер асинхронно обрабатывал подключения >1 числа клиентов.

## Реализация теста
Я сделал генерацию файла разного размера каждый раз, т.к посчитал, что это улучшит тестирование.
Нужно было как-то синхронизировать сервер и клиент, был вариант сделать это через `sleep`, но это не гибко. поэтому я отслеживал логи, так синхронизация была более гибкой.
