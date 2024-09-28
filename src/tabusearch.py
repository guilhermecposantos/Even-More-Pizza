import utils
import copy
import matplotlib.pyplot as plt

def update_tabu_list(tabu_list, curr_solution, tabu_tenure):
    """
    Updates the tabu list with the current solution.
    
    Parameters:
        tabu_list (dict): Tabu list containing solutions and their tabu tenure
        curr_solution (object): Current solution to be added to the tabu list
        tabu_tenure (int): Number of iterations a solution stays in the tabu list
        
    Returns:
        tabu_list (dict): Updated tabu list
    """
    tabu_list[curr_solution] = tabu_tenure

    for sol in list(tabu_list.keys()):
        tabu_list[sol] -= 1
        if tabu_list[sol] <= 0:
            del tabu_list[sol]
    return tabu_list

def get_candidate_solution(neighbourhood, tabu_list):
    """
    Returns the best candidate solution from the neighbourhood that is not in the tabu list.
    
    Parameters:
        neighbourhood (list): List of neighbouring solutions
        tabu_list (dict): Tabu list containing solutions and their tabu tenure
        
    Returns:
        new_solution (object): Best candidate solution found
        new_solution_score (float): Score of the best candidate solution
    """
    new_solution = None
    new_solution_score = 0 
    
    for neighbour in neighbourhood:
        neighbour_score = utils.evaluation_function(neighbour)

        if (neighbour_score > new_solution_score) and (neighbour not in tabu_list):
            new_solution = neighbour
            new_solution_score = neighbour_score

    return new_solution, new_solution_score

def tabu_search(pizzas, team_sizes, iterations, tabu_tenure):
    """
    Performs Tabu Search algorithm for optimizing pizza delivery routes.
    
    Parameters:
        pizzas (list): List of pizzas
        team_sizes (list): List of team sizes
        iterations (int): Number of iterations
        tabu_tenure (int): Number of iterations a solution stays in tabu list
        
    Returns:
        final_solution (object): Best solution found
        final_score (float): Score of the best solution
    """
    curr_solution = utils.randomize_deliveries(pizzas, team_sizes)
    curr_score = utils.evaluation_function(curr_solution)
  
    best_solution = copy.deepcopy(curr_solution)
    best_score = curr_score
    
    tabu_list = {}
    explored_nodes = []  
    best_nodes = []     

    curr_iteration = 0

    while curr_iteration < iterations:

        tabu_list = update_tabu_list(tabu_list, curr_solution, tabu_tenure)
        
        neighbourhood = utils.generate_neighbourhood(curr_solution)

        new_solution, new_solution_score = get_candidate_solution(neighbourhood, tabu_list)
  
        if new_solution is not None:
            curr_solution = new_solution
            curr_score = new_solution_score
   
            if curr_score > best_score:
                best_solution = copy.deepcopy(curr_solution)
                best_score = curr_score

        else:
            curr_solution = utils.randomize_deliveries(pizzas, team_sizes)
            curr_score =  utils.evaluation_function(curr_solution)
  
        explored_nodes.append(curr_score) 
        best_nodes.append(best_score)

        curr_iteration += 1
    
    # Print final solution and score
    print(curr_solution)
    print(curr_score)

    # Plot the performance graph
    plt.plot(range(1, len(explored_nodes) + 1), explored_nodes, label='Explored Nodes')
    plt.plot(range(1, len(best_nodes) + 1), best_nodes, label='Best Nodes')
    plt.xlabel('Iteration')
    plt.ylabel('Solution Score')
    plt.title('Evolution of the Tabu Search Algorithm')
    plt.legend()
    plt.grid(True)
    plt.show()

    return best_solution, best_score
