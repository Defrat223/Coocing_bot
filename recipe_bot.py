import os.path
import pickle
import telebot
from bk_tree import *
from dataset_loader import DatasetLoader

class RecipeBot:
    def __init__(self, token, data):
        self.bot = telebot.TeleBot('7845414262:AAEA69LU7fRlBVvzJ9Hy3ISe-bmN6nazKXI')
        self.dataset_loader = data
        self.RT = Node([], [])

    def start(self):
        if os.path.exists('bk_tree.pkl'):
            f = open('bk_tree.pkl', 'rb')
            self.RT, _ = pickle.load(f)
            f.close()
        else:
            self.dataset_loader.load_data()
            recipes = self.dataset_loader.get_recipes()
            for recipe in recipes:
                tmp = Node(recipe[2], (recipe[0], recipe[1]))
                add(self.RT, tmp)
            f = open('bk_tree.pkl', 'wb')
            pickle.dump((self.RT, tree), f)
            f.close()

    def handle_message(self, message):
        ingredients = sorted([x.strip().lower() for x in message.text.lower().split(', ')])
        match = get_similar_recipies(self.RT, ingredients)
        if not match:
            self.bot.send_message(message.chat.id, 'Рецепт не найден(')
        else:
            match2 = []
            for i in range(len(match)):
                if len(match2) < 4:
                    match2.append(match[i])
            for ingredient, recipe in match2:
                self.bot.send_message(message.chat.id, f"Название блюда: {recipe[1]},\nИнгридиенты: {ingredient},\nСсылка, по "
                                                      f"которой вы можете ознакомиться с порядком приготовления: {recipe[0]}\n")

    def run(self):
        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            self.bot.send_message(message.chat.id, 'Привет! Я помощник в нахождении рецептов. Какие продукты у вас '
                                                   'есть? Введите их через запятую (формат: "Картошка, мясо")')

        @self.bot.message_handler(content_types=['text'])
        def handle_text(message):
            self.handle_message(message)

        self.bot.polling()


if __name__ == "__main__":
    dataset_loader = DatasetLoader('recipes - recipes.csv')
    bot = RecipeBot('7143887902:AAF95642pcw34y2Gffv3oDfMHDgf-SRt7Mo', dataset_loader)
    bot.start()
    bot.run()
