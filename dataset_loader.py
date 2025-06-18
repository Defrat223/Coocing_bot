import pandas as pd
import ast


class DatasetLoader:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = None

    def load_data(self):
        self.data = pd.read_csv(self.csv_file)
        self.data = self.data.dropna(subset=['ingredients'])

    def get_recipes(self):
        recipes = []
        for i in range(len(self.data)):
            ingredients_str = self.data['ingredients'][i]
            ingredients = ast.literal_eval(ingredients_str)
            ingredients_lower = {k.lower(): v for k, v in ingredients.items()}
            recipes.append((self.data['url'][i], self.data['name'][i], list(ingredients_lower.keys())))
        return recipes
