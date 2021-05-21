# tag_finder
Тестовое задание: поиск уникальных тегов в html странице на flask 

Heroku: https://link-parser-git.herokuapp.com/
Docker(windows): 
1. Собрать контейнер compile_container.bat или ``docker build -t tag_parser /путь/к/папке_содержащей_Dockerfile``
2. Запустить образ start_docker.bat или ``docker run -d -p 5000:5000 tag_parser``
<br>
<br>
<b>Реализовать RESTful-сервис который позволит реализовать следующий сценарий: 
1. Внешний пользователь вызывает endpoint в который передаёт произвольный URL адрес. Его запросу присваивается некоторый уникальный идентификатор. 
2. Пользователь может передавать этот идентификатор в endpoint получения результатов обработки. Если обработка завершена, пользователь должен получить количество уникальных тегов в документе, с количеством “вложенных” в него элементов. Например: {“html”: {“count”:1, “nested”:100}, “body”:{“count”:1, “nested”:99}, “H1”: {“count”:2,”nested”:0}. 
3. Входящие данные должны валидироваться, ошибки доступности URL, ответа внешних серверов и т.д. обрабатываться. </b>

api имеет два эндпоинта:
<b>/api/send</b> - принимает json в post-запросе вида {"link" : "https://url.link/"} 
<b>/api/<int:link_id></b> - принимает get-запрос без параметров(основным параметром является уникальный номер ссылки, который передается в endpoint) и возвращает данные из БД по виду 


Чтобы отправить запрос через тестовый клиент flask, необходимо сделать следующие шаги:
1. Открыть CMD и перейти в директорию расположения проекта: ``cd path/to/dir`` и вызвать интерпретатор: ``python``
<p align="center"><img width=700px src="https://user-images.githubusercontent.com/71926912/118775954-232ec080-b890-11eb-8380-069e78ca9a51.PNG" alt="start python"></p>

2. Импортировать клиент: ``from app import client``
<p align="center"><img width=700px src="https://user-images.githubusercontent.com/71926912/118776157-5a04d680-b890-11eb-9c8b-ad7558b78b37.PNG" alt="import client"></p>

<b>Отправка</b>
Чтобы получить уникальный идентификатор, необходимо сформировать запрос следующего вида: ``result = client.post("/api/send", json={"link": "https://github.com/"})``
Чтобы проверить статус запроса необходимо вызвать переменную ``result``, которая вернет http-статус запроса
Чтобы получить ответ сервера, необходимо воспользоваться методом ``result.get_json()``, который вернет ответ вида {'id': 21, 'link': 'https://github.com/'}
<p align="center"><img width=700px src="https://user-images.githubusercontent.com/71926912/118776375-99cbbe00-b890-11eb-83a4-f912dff6d3eb.PNG" alt="client post"></p>


<b>Получение списка тегов</b>
чтобы получить информацию об уникальных тегах на сайте, необходимо через клиент перейти на адрес ``/api/<int:link_id>``. Пример: /api/22, /api/3
``res = client.get("/api/21")``
Просмотр ответа сервера теми же вызовами: ``res`` и ``res.get_json()``
<p align="center"><img width=700px src="https://user-images.githubusercontent.com/71926912/118778269-96393680-b892-11eb-9f65-5f655d921fcc.PNG" alt="client get"></p>

Методы также работают и для heroku. Обращение к api heroku(сайт сначала необходимо "разбудить" - перейти на него):<br>
``curl --header "Content-Type: application/json" --request POST -d '{"link": "https://qna.habr.com/q/639456"}' https://link-parser-git.herokuapp.com/api/send``<br>
``curl -X GET https://link-parser-git.herokuapp.com/api/2``<br>
<p align="center"><img width=700px src="https://user-images.githubusercontent.com/71926912/118824587-a6690a00-b8c2-11eb-9d93-a117ea966962.PNG" alt="heroku"></p>

<b>Валидация данных</b>
Валидация входящих данных осуществляется через flask-apispec: схема данных передается через декораторы @use_kwargs и @marshal_with. 
При передаче невалидых данных возвращается http-статус "422 Unprocessable Entity". 
Все ответы, которые возвращают HTML, возвращают список тегов, в том числе 404, 500 и т.д., Внутренние ошибки возвращают json вида {"error": error_description}
<p align="center"><img width=700px src="https://user-images.githubusercontent.com/71926912/118781161-6b041680-b895-11eb-9081-fe53fa7735a0.PNG" alt="internal error"></p>

<b>Дополнительно</b><br>
<b>Реализация UI для сервиса</b><br>
<b>Генерация документации для созданных методов</b><br> 

Из дополнений я добавил Генерацию документации с помощью swagger и реализацию UI(браузерная)

Авматизированная документация реализована с помощью swagger и swagger-ui. Я описал только api-методы. Я мало работал со сваггером, поэтому, считаю, что это место можно и доработать.
<p align="center"><img width=700px src="https://user-images.githubusercontent.com/71926912/118781992-51170380-b896-11eb-831e-375cde315d20.PNG" alt="swagger"></p>


UI построенный на flask-wtforms, jinja2. я не стал добавлять оформление, поскольку ограничен во времени.

<b>Отправка ссылок: </b><br>
отправка доступна по адресу: ``/`` и ``/index``
Валидация данных осуществляется через wtforms и принимает только url.
<p align="center"><img width=500px src="https://user-images.githubusercontent.com/71926912/118808991-c09aec00-b8b2-11eb-9cbe-44839c9dcff7.PNG" alt="ui send"></p>
При вводе неправильного значения выдает всплывающие сообщения или возвращает ID, по которому можно получить теги
Неправильный ввод:
<p align="center"><img width=500px src="https://user-images.githubusercontent.com/71926912/118808903-a6610e00-b8b2-11eb-89b0-06287c7a198e.PNG" alt="incorrect send"></p>
Правильный ввод:
<p align="center"><img width=500px src="https://user-images.githubusercontent.com/71926912/118808489-3d799600-b8b2-11eb-82b4-9b9699059c97.PNG" alt="correct send"></p>

<b>получение тегов:</b><br>
Получение списка тегов доступно по адресу ``/tags``
Валидация также через wtforms. Внутренние ошибки возвращаются с кодом 422, остальные со своими реальными кодами.
<p align="center"><img width=500px src="https://user-images.githubusercontent.com/71926912/118809370-369f5300-b8b3-11eb-81cd-a7a401662e28.PNG" alt="ui tags"></p>
Корректный ответ:
<p align="center"><img width=500px src="https://user-images.githubusercontent.com/71926912/118809764-b62d2200-b8b3-11eb-97d4-1070db73021e.PNG" alt="validate tags"></p>
Один из видов валидации:
<p align="center"><img width=500px src="https://user-images.githubusercontent.com/71926912/118809481-5b93c600-b8b3-11eb-924c-3fca5e7c092b.PNG" alt="validate tags"></p>
Обработка ошибок:
<p align="center"><img width=500px src="https://user-images.githubusercontent.com/71926912/118809863-d78e0e00-b8b3-11eb-8c0b-6a6163d9c04f.PNG" alt="validate tags"></p>



<!-- <p align="center"><img width=700px src="" alt=""></p> -->
