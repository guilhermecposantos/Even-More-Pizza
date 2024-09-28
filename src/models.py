class Pizza:
    def __init__(self , index, num_ingredient, ingredients):
        self.index = index
        self.num_ingredient = num_ingredient
        self.ingredients = ingredients
        
    
    def __str__(self):
        return f"Index: {self.index}, Number of ingrediente: {self.num_ingredient}, Ingredients: {', '.join(self.ingredients)}"

class Delivery:
    def __init__(self, team_size, pizzas):
        self.team_size = team_size
        self.pizzas = pizzas

    def __str__(self):
        pizzas_info = "\n".join(str(pizza) for pizza in self.pizzas)
        return f"Delivery: Team size - {self.team_size}, Pizzas:\n{pizzas_info}"
    


class Solution:    
    def __init__(self, solution, unused_pizzas, free_of_2, free_of_3, free_of_4):
        self.solution = solution
        self.unused_pizzas = unused_pizzas
        self.free = [free_of_2, free_of_3, free_of_4]
    
    def __str__(self):
        delivery_info = "\n".join(str(delivery) for delivery in self.solution)
        pizza_info = "\n".join(str(pizza) for pizza in self.unused_pizzas)
        return f"Deliveries: \n{delivery_info} \nUnused pizzas: \n{pizza_info} \nFree teams: \n{self.free}"
    
    def save_to_file(self, filename):
        output_path = f"output/{filename}"
        with open(output_path, "w") as file:
            file.write(str(len(self.solution)))
            for delivery in self.solution:
                file.write("\n" + str(delivery.team_size))
                for pizza in delivery.pizzas:
                    file.write(" " + str(pizza.index))

          
