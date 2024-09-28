import random
import copy
from models import Pizza, Delivery, Solution

def parse_file(file_path):
    """
    Parse input file and extract pizzas and team sizes.

    Parameters:
        file_path (str): Path to the input file.

    Returns:
        pizzas (set): Set of Pizza objects.
        team_sizes (list): List of team sizes.
    """
    with open(file_path, 'r') as file:
        i = 0
        team_sizes = list(map(int, file.readline().split()))[1:]
        pizzas = set()

        for line in file:
            i += 1
            pizza_data = line.split()
            num_ingredients = int(pizza_data[0])
            ingredients = pizza_data[1:]
            pizzas.add(Pizza(i, num_ingredients, ingredients))

    return pizzas, team_sizes

def randomize_deliveries(pizzas, team_sizes):
    """
    Randomly allocate pizzas to delivery teams.

    Parameters:
        pizzas (set): Set of Pizza objects.
        team_sizes (list): List of team sizes.

    Returns:
        solution (Solution): Initial solution containing deliveries.
    """
    deliveries = []
    shuffled_pizzas = list(pizzas)
    random.shuffle(shuffled_pizzas)

    while True:
        random_index = random.randint(0, 2)
        team_size = random_index + 2

        if team_sizes[0] == 0 and team_sizes[1] == 0 and team_sizes[2] == 0:
            break

        if team_sizes[random_index] == 0:
            continue

        if len(shuffled_pizzas) < team_size:
            if len(shuffled_pizzas) == 3 and team_sizes[1] > 0:
                deliveries.append(Delivery(3, shuffled_pizzas))
                team_sizes[1] -= 1
                shuffled_pizzas = shuffled_pizzas[3:]
            if len(shuffled_pizzas) == 2 and team_sizes[0] > 0:
                deliveries.append(Delivery(2, shuffled_pizzas))
                team_sizes[0] -= 1
                shuffled_pizzas = shuffled_pizzas[2:]
            break

        team_sizes[random_index] -= 1
        pizzas_for_delivery = shuffled_pizzas[:team_size]
        shuffled_pizzas = shuffled_pizzas[team_size:]
        deliveries.append(Delivery(team_size, pizzas_for_delivery))

    return Solution(deliveries, shuffled_pizzas, team_sizes[0], team_sizes[1], team_sizes[2])

def swap_pizza_between_teams_random(solution, curr_score):
    """
    Switches a pizza between two random teams.

    Parameters:
        solution (Solution): Current solution.
        curr_score (float): Current score of the solution.

    Returns:
        solution (Solution): Updated solution after the swap.
        curr_score (float): Updated score of the solution.
    """
    if len(solution.solution) == 0:
        return Solution(solution.solution, solution.unused_pizzas, solution.free[0], solution.free[1], solution.free[2]), curr_score

    first_team = random.choice(solution.solution)
    second_team = random.choice(solution.solution)
    if first_team == second_team:
        second_team = random.choice(solution.solution)

    first_team_oldscore = len(set(ingredient for pizza in first_team.pizzas for ingredient in pizza.ingredients)) ** 2
    second_team_oldscore = len(set(ingredient for pizza in second_team.pizzas for ingredient in pizza.ingredients)) ** 2

    curr_score = curr_score - first_team_oldscore - second_team_oldscore

    n1 = random.randint(1, first_team.team_size)
    n2 = random.randint(1, second_team.team_size)
    old_value = first_team.pizzas[n1 - 1] 
    first_team.pizzas[n1 - 1] = second_team.pizzas[n2 - 1]
    second_team.pizzas[n2 - 1] = old_value

    first_team_newscore = len(set(ingredient for pizza in first_team.pizzas for ingredient in pizza.ingredients)) ** 2
    second_team_newscore = len(set(ingredient for pizza in second_team.pizzas for ingredient in pizza.ingredients)) ** 2

    curr_score = curr_score + first_team_newscore + second_team_newscore

    return Solution(solution.solution, solution.unused_pizzas, solution.free[0], solution.free[1], solution.free[2]), curr_score

def swap_1_unused(solution, curr_score):
    """
    Switches one pizza in a team with an unused one.

    Parameters:
        solution (Solution): Current solution.
        curr_score (float): Current score of the solution.

    Returns:
        solution (Solution): Updated solution after the swap.
        curr_score (float): Updated score of the solution.
    """
    if len(solution.solution) == 0 or len(solution.unused_pizzas) == 0:
        return Solution(solution.solution, solution.unused_pizzas, solution.free[0], solution.free[1], solution.free[2]), curr_score

    team = random.choice(solution.solution)
    n1 = random.randint(1, team.team_size)
    n2 = random.randint(1, len(solution.unused_pizzas))

    team_oldscore = len(set(ingredient for pizza in team.pizzas for ingredient in pizza.ingredients)) ** 2
    curr_score = curr_score - team_oldscore

    old_value = team.pizzas[n1 - 1]
    team.pizzas[n1 - 1] = solution.unused_pizzas[n2 - 1]
    solution.unused_pizzas.append(old_value)
    solution.unused_pizzas.remove(team.pizzas[n1 - 1])

    team_newscore = len(set(ingredient for pizza in team.pizzas for ingredient in pizza.ingredients)) ** 2
    curr_score = curr_score + team_newscore

    return Solution(solution.solution, solution.unused_pizzas, solution.free[0], solution.free[1], solution.free[2]), curr_score

def new_pizzas(solution, curr_score):
    """
    Adds a new set of pizzas to a team.

    Parameters:
        solution (Solution): Current solution.
        curr_score (float): Current score of the solution.

    Returns:
        solution (Solution): Updated solution with new pizzas.
        curr_score (float): Updated score of the solution.
    """
    free_sizes = []
    if solution.free[0] > 0 and len(solution.unused_pizzas) > 1:
        free_sizes.append(0)
    if solution.free[1] > 0 and len(solution.unused_pizzas) > 2:
        free_sizes.append(1) 
    if solution.free[2] > 0 and len(solution.unused_pizzas) > 3:
        free_sizes.append(2)
        
    if len(free_sizes) == 0:
        return Solution(solution.solution, solution.unused_pizzas, solution.free[0], solution.free[1], solution.free[2]), curr_score

    size_team = random.choice(free_sizes)
    solution.free[size_team] -= 1
    new_pizzas = solution.unused_pizzas
    random.shuffle(new_pizzas)
    team = Delivery(size_team + 2, new_pizzas[:size_team + 2])

    team_score = len(set(ingredient for pizza in team.pizzas for ingredient in pizza.ingredients)) ** 2
    curr_score = curr_score + team_score

    solution.solution.append(team)
    solution.unused_pizzas = new_pizzas[size_team + 2:]

    return Solution(solution.solution, solution.unused_pizzas, solution.free[0], solution.free[1], solution.free[2]), curr_score

def remove_team(solution, curr_score):
    """
    Removes a team.

    Parameters:
        solution (Solution): Current solution.
        curr_score (float): Current score of the solution.

    Returns:
        solution (Solution): Updated solution with the team removed.
        curr_score (float): Updated score of the solution.
    """
    if len(solution.solution) == 0:
        return Solution(solution.solution, solution.unused_pizzas, solution.free[0], solution.free[1], solution.free[2]), curr_score

    team = random.choice(solution.solution)
    solution.free[team.team_size - 2] += 1
    solution.solution.remove(team)
    solution.unused_pizzas.extend(team.pizzas)

    team_score = len(set(ingredient for pizza in team.pizzas for ingredient in pizza.ingredients)) ** 2
    curr_score = curr_score - team_score

    return Solution(solution.solution, solution.unused_pizzas, solution.free[0], solution.free[1], solution.free[2]), curr_score

def evaluation_function(solution):
    """
    Calculates the evaluation score of a solution.

    Parameters:
        solution (Solution): Solution to be evaluated.

    Returns:
        score (float): Evaluation score of the solution.
    """
    if len(solution.solution) == 0:
        return 0
    return sum(len(set(ingredient for pizza in delivery.pizzas for ingredient in pizza.ingredients)) ** 2 for delivery in solution.solution)

def generate_neighbour_random(solution, prev_score=0):
    """
    Generates a random neighbour of the current solution.

    Parameters:
        solution (Solution): Current solution.
        prev_score (float): Previous score of the solution.

    Returns:
        solution (Solution): Random neighbour solution.
        score (float): Score of the random neighbour solution.
    """
    random_index = random.randint(0, 3)
    random_neighbour_function = [swap_pizza_between_teams_random, new_pizzas, remove_team, swap_1_unused][random_index]
    solution, score = random_neighbour_function(solution, prev_score)
    return solution, score

def generate_neighbour(solution, prev_score=0):
    """
    Generates the best neighbour of the current solution.

    Parameters:
        solution (Solution): Current solution.
        prev_score (float): Previous score of the solution.

    Returns:
        best_solution (Solution): Best neighbour solution.
        best_score (float): Score of the best neighbour solution.
    """
    random_neighbour_function = [swap_pizza_between_teams_random, new_pizzas, remove_team, swap_1_unused]
    best_score = prev_score
    best_solution = copy.deepcopy(solution)
    for function in random_neighbour_function:
        new_neighbour = function(copy.deepcopy(solution))
        new_score = evaluation_function(new_neighbour)
        if new_score > best_score:
            best_solution = new_neighbour
            best_score = new_score
    return best_solution, best_score

def generate_neighbourhood(solution):
    """
    Generates the neighbourhood of the current solution.

    Parameters:
        solution (Solution): Current solution.

    Returns:
        neighbourhood (list): List of neighbour solutions.
    """
    neighbourhood = []
    random_neighbour_function = [swap_pizza_between_teams_random, new_pizzas, remove_team, swap_1_unused]
    score = evaluation_function(solution)
    for function in random_neighbour_function:
        new_neighbour, new_score = function(copy.deepcopy(solution), score)
        if str(new_neighbour) != str(solution):
            neighbourhood.append(new_neighbour)
    return neighbourhood

def is_feasible(solution, team_sizes, debug=False):
    """
    Checks if a solution is feasible.

    Parameters:
        solution (Solution): Solution to be checked.
        team_sizes (list): List of team sizes.
        debug (bool): Debug mode flag.

    Returns:
        feasible (bool): True if the solution is feasible, False otherwise.
    """
    pizzas = []
    for delivery in solution.solution:
        for pizza in delivery.pizzas:
            if pizza.index in pizzas:
                return False
            pizzas.append(pizza.index)

    for delivery in solution.solution:
        delivery_size = delivery.team_size
        if team_sizes[delivery_size - 2] == 0:
            return False
        team_sizes[delivery_size - 2] -= 1

    return True
