import utils  
import copy  
import matplotlib.pyplot as plt  

def hill_climbing(pizzas, team_sizes, iterations, improving_iterations=False):
    """
    Performs Hill Climbing algorithm for optimizing pizza delivery routes.
    
    Parameters:
        pizzas (list): List of pizzas
        team_sizes (list): List of team sizes
        iterations (int): Number of iterations
        improving_iterations (bool): If True, resets iteration count when a better solution is found
        
    Returns:
        final_solution (object): Best solution found
        final_score (float): Score of the best solution
    """
    total_iterations = 1
    scores = []
    curr_solution = utils.randomize_deliveries(pizzas, team_sizes)  # Initialize current solution
    curr_score = utils.evaluation_function(curr_solution)  # Evaluate current solution

    curr_iteration = 0
    
    while curr_iteration < iterations:
        total_iterations += 1
        curr_iteration += 1
        neighbour, neighbour_score  = utils.generate_neighbour_random(copy.deepcopy(curr_solution), curr_score)
        if neighbour_score > curr_score: 
            scores.append(neighbour_score)
            curr_solution = neighbour
            curr_score = neighbour_score
            if improving_iterations == True:
                curr_iteration = 0
        else:
            scores.append(curr_score)
                
    # Plot the performance
    plt.plot(range(1, total_iterations), scores)
    plt.xlabel('Iteration')
    plt.ylabel('Score')
    plt.title('Algorithm Performance')
    plt.show()
    print(curr_score)
    return curr_solution, curr_score
