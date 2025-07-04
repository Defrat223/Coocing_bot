# Телеграмм-бот для поиска рецептов

Телеграмм-бот для поиска рецепта по названиям ингридиента на python. 


## Используемые библиотеки
- telebot
- pandas
- ast

## Используемый датасет
[147к кулинарных рецептов](https://www.kaggle.com/datasets/rogozinushka/povarenok-recipes) - содержит более 147 тыс рецептов, где указаны название блюда, его ингридиенты и ссылка для поэтапного приготовления.
  
## Что входит в основу?
Основой послужило BK-дерево. Вообще BK-Tree — это структура данных, используемая для эффективного определения слов, близких к целевому слову с точки зрения расстояния Левенштейна. Расстояние Левенштейна - минимальное количество односимвольных операций (а именно вставки, удаления, замены), необходимых для превращения одной последовательности символов в другую. В данном случае модифицированное BK-дерево - это структура данных, которая позволяет осуществлять эффективный поиск ближайших соседей путем организации узлов таким образом, чтобы свести к минимуму количество узлов, подлежащих поиску.

## Как это всё работает

Используется 3 класса: 
- bk_tree
- recipe_bot
- dataset_loader

### Рассмотрим класс bk_tree

Константы и глобальные переменные:

- MAXN: максимальное количество узлов в дереве (в данном случае 144742)
- TOL: допустимый порог для рассмотрения двух списков ингредиентов как похожих (в данном случае 1)
- ptr: глобальный указатель для отслеживания следующего доступного индекса узла в дереве
  
Класс узла

- Узел: класс, представляющий узел в BK-дереве с атрибутами:
  - keys: список ключей ингредиентов (например, ["яблоко", "банан"])
  - recipe: соответствующая информация о рецепте
  - next: массив индексов дочерних узлов (изначально заданный равным 0)
 
Инициализация дерева

  - Идёт проверка, существует ли файл с именем bk_tree.pkl (уже построенного BK-дерева), и если это так, загружает содержимое файла в переменную tree. Если файл не существует, он инициализирует пустой список деревьев.

Далее идут функции добавления ингридиентов в дерево, рассчёта расстояния на основании схожести ингридиентов и нахождения рецепта по введенным данным.

Функция "add": 
- add(root, curr): добавляет новый узел curr в дерево, начиная с корневого узла
  - Если корневой узел пуст, установите для его ключей и атрибутов рецепта значения, соответствующие атрибутам curr
  - Вычислите расстояние редактирования между ключами корневого узла и ключами curr, используя функцию edit_distance
  - Если расстояние редактирования находится в пределах допустимого порога, добавьте curr в качестве дочернего узла root
  - В противном случае рекурсивно вызовите add для дочернего узла с вычисленным индексом расстояния редактирования

Функция "get_similar_recipies":
- get_similar_recipies(root, s, threshold=TOL): выполняет поиск рецептов, аналогичных входным данным (список ингредиентов), начиная с корневого узла
Если корневой узел пуст, возвращает пустой список
  - Рассчитайте расстояние редактирования между ключами корневого узла и s с помощью функции edit_distance
  - Если расстояние редактирования находится в пределах допустимого порога, добавьте рецепт корневого узла в список результатов
  - Рекурсивно вызывайте get_similar_recipies для дочерних узлов в пределах диапазона изменения расстояния и добавляйте их результаты в список

Функция "edit_distance":
- edit_distance(a, b): вычисляет расстояние редактирования между двумя списками ингредиентов a и b с помощью динамического программирования
  - Инициализирует двумерный массив dp для хранения расстояний редактирования между префиксами a и b
  - Заполняет массив dp, используя рекуррентное соотношение:
dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1), если a[i-1]!= b[j-1]
dp[i][j] = dp[i-1][j-1] в противном случае
  - Возвращает расстояние редактирования между целыми списками a и b

### Рассмотрим класс dataset_loader

Этот класс используется для загрузки и предварительной обработки набора данных рецептов из CSV-файла. У этого класса есть следующие методы:
  - __init__: Метод конструктора, который принимает аргумент csv_file, который является именем CSV-файла, содержащего набор данных. Он также инициализирует атрибут data значением None
  - load_data: Этот метод считывает CSV-файл с помощью библиотеки pandas и сохраняет результирующий фрейм данных в атрибуте data. Он также удаляет все строки, в которых отсутствуют значения в столбце ingredients
  - get_recipes: Этот метод извлекает рецепты из атрибута data и возвращает список кортежей. Каждый кортеж содержит URL-адрес рецепта, название рецепта и список названий ингредиентов в нижнем регистре.

Основная цель этого класса - отделить логику загрузки и предварительной обработки данных от остального кода, что упрощает его обслуживание и тестирование.

Метод load_data используется для загрузки набора данных из CSV-файла, а метод get_recipes - для извлечения рецептов из загруженных данных. Столбец ingredients в CSV-файле содержит строковое представление словаря, где ключами являются названия ингредиентов, а значениями - их количество. Функция ast.literal_eval используется для преобразования этого строкового представления в словарь. Затем ключи словаря преобразуются в нижний регистр и сохраняются в списке рецептов.

### Рассмотрим класс recipe_bot

Этот класс использует API Telegram Bot для создания бота, помогающего пользователям находить рецепты на основе имеющихся у них ингредиентов. Вот краткое описание того, что происходит в данном классе:
- Класс RecipeBot инициализируется токеном Telegram-бота и объектом DatasetLoader, который используется для загрузки и предварительной обработки набора данных рецептов из CSV-файла
- Метод start:
  - Это метод запуска класса, и он отвечает за инициализацию BK-дерева и загрузку или создание набора данных рецептов.

Вызывается для загрузки набора данных и создания BK-дерева или загрузки его из файла. Каждый узел в дереве представляет рецепт, а ингредиенты используются в качестве ключей поиска

- Метод handle_message предназначен для обработки входящих сообщений от пользователей. Когда пользователь отправляет сообщение со списком ингредиентов, метод:
  - Извлекает ингредиенты из сообщения и преобразует их в нижний регистр
  - Выполняет поиск в BK-дереве рецептов, соответствующих ингредиентам, с помощью функции get_similar_recipies
  - Если подходящие рецепты не найдены, отправляет пользователю сообщение о том, что рецепт не найден
  - Если найдены подходящие рецепты, отправляет пользователю сообщение с подробной информацией о рецепте, включая название, ингредиенты и URL-адрес
- Метод run предназначен для запуска Telegram-бота и начала прослушивания входящих сообщений. Он использует библиотеку telebot для определения двух обработчиков сообщений
  - По команде /start отправляется приветственное сообщение пользователю
  - Одно для текстовых сообщений, который вызывает метод handle_message для обработки пользовательского ввода
- В блоке if __name__ == "__main__": создается экземпляр класса RecipeBot и вызываются методы start и run для запуска бота
  
В целом, этот код создает Telegram-бота, который позволяет пользователям искать рецепты на основе имеющихся у них ингредиентов и предоставляет список подходящих рецептов с указанием их деталей
