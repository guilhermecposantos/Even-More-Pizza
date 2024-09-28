import utils  
import copy  
import matplotlib.pyplot as plt  

def get_candidate_solution(neighbourhood):
    """
    Returns the best candidate solution and its score from a given neighbourhood.
    
    Parameters:
        neighbourhood (list): List of neighbouring solutions
        
    Returns:
        new_solution (object): Best candidate solution
        new_solution_score (float): Score of the best candidate solution
    """
    new_solution = None
    new_solution_score = 0

    for neighbour in neighbourhood:
        neighbour_score = utils.evaluation_function(neighbour)

        if neighbour_score > new_solution_score:
            new_solution = neighbour
            new_solution_score = neighbour_score

    return new_solution, new_solution_score

def penalty_function(solution, best_solution_so_far):
    """
    Calculates the penalty for a given solution compared to the best solution so far.
    
    Parameters:
        solution (object): Current solution
        best_solution_so_far (object): Best solution found so far
        
    Returns:
        penalty (int): Penalty for the current solution
    """
    penalty = 0

    for i in range(min(len(solution.solution), len(best_solution_so_far.solution))):
        current_delivery = solution.solution[i]
        best_delivery = best_solution_so_far.solution[i]

        penalty += abs(current_delivery.team_size - best_delivery.team_size)

        current_ingredients = set()
        best_ingredients = set()

        for pizza in current_delivery.pizzas:
            current_ingredients.update(pizza.ingredients)

        for pizza in best_delivery.pizzas:
            best_ingredients.update(pizza.ingredients)

        penalty += len(current_ingredients.intersection(best_ingredients))

    return penalty

def guided_local_search(pizzas, team_sizes, iterations):
    """
    Performs Guided Local Search algorithm for optimizing pizza delivery routes.
    
    Parameters:
        pizzas (list): List of pizzas
        team_sizes (list): List of team sizes
        iterations (int): Number of iterations
        
    Returns:
        best_solution (object): Best solution found
        best_score (float): Score of the best solution
    """
    curr_solution = utils.randomize_deliveries(pizzas, team_sizes)  # Initialize current solution
    curr_score = utils.evaluation_function(curr_solution)  # Evaluate current solution

    best_solution = copy.deepcopy(curr_solution)  # Initialize best solution
    best_score = curr_score  # Initialize best score

    explored_nodes = []  # List to store scores of explored solutions
    best_nodes = []  # List to store scores of the best solutions found

    curr_iteration = 0

    while curr_iteration < iterations:
        neighbourhood = utils.generate_neighbourhood(curr_solution)  # Generate neighbourhood solutions

        new_solution, new_solution_score = get_candidate_solution(neighbourhood)  # Get best candidate solution

        # Calculate scores with penalty function
        new_solution_score_with_penalty = new_solution_score - penalty_function(new_solution, best_solution)
        curr_score_with_penalty = curr_score - penalty_function(curr_solution, best_solution)

        # Update current solution if a better candidate is found
        if new_solution is not None and new_solution_score_with_penalty > curr_score_with_penalty:
            curr_solution = new_solution
            curr_score = new_solution_score

            # Update best solution if current solution is better
            if curr_score > best_score:
                best_solution = copy.deepcopy(curr_solution)
                best_score = curr_score

        # Append scores to lists
        explored_nodes.append(curr_score)
        best_nodes.append(best_score)

        curr_iteration += 1

    # Plot the evolution of the algorithm
    plt.plot(range(1, len(explored_nodes) + 1), explored_nodes, label='Explored Nodes')
    plt.plot(range(1, len(best_nodes) + 1), best_nodes, label='Best Nodes')

    plt.xlabel('Iteration')
    plt.ylabel('Solution Score')
    plt.title('Evolution of the Guided Local Search Algorithm')
    plt.legend()
    plt.grid(True)
    plt.show()

    return best_solution, best_score
