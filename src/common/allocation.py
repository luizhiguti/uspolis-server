from pulp import *
import numpy as np

def _can_alocate(s_obj, a_obj): # Wheter or not classroom s has the required resources for class a

    a_prefs = a_obj['preferences']
    is_same_building = s_obj['building'] and a_prefs['building']

    if a_obj['subscribers'] <= s_obj['capacity']:
        has_enough_room = True
    else: 
        has_enough_room = False
    
    if a_prefs['air_conditioning'] == True:
        satisfies_air_conditioning = s_obj['air_conditioning'] 
    else:
        satisfies_air_conditioning = True

    if a_prefs['projector'] == True:
        satisfies_projector = s_obj['projector']
    else:
        satisfies_projector = True

    if a_prefs['accessibility'] == True:
        satisfies_accessibility = s_obj['accessibility']
    else:
        satisfies_accessibility = True

    return is_same_building and has_enough_room and satisfies_air_conditioning and satisfies_projector and satisfies_accessibility


def _has_conflicts(a_obj, a_p_obj):
    same_weekday = (a_obj['week_days'] == a_p_obj['week_days'])
    if (a_obj['start_time'] <= a_p_obj['end_time']) and \
        (a_obj['end_time'] <= a_p_obj['start_time']) :
        hour_conflict = True
    else:
        hour_conflict = False

    return same_weekday and hour_conflict


def allocate_classrooms(classroom_list, class_list):

    # Creating set S of classrooms
    S = [s['classroom_name'] for s in classroom_list]

    # Creating set A of classes
    A = [a['class_id'] for a in class_list]

    # Creating USO (cost of allocation) and eta (possibility of allocation) matrices
    USO = {}
    eta = {}
    for s_obj in classroom_list:
        s = s_obj['classroom_name']
        USO[s] = {}
        eta[s] = {}
        for a_obj in class_list:
            a = a_obj['class_id']
            USO[s][a] = 1 - a_obj['subscribers']/s_obj['capacity']
            if _can_alocate(s_obj, a_obj):
                eta[s][a] = 1
            else:
                eta[s][a] = 0

    # Creating theta (time conflict of classes) matrix
    theta = {}
    for a_obj in class_list:
        a = a_obj['class_id']
        theta[a] = {}
        for a_p_obj in class_list:
            a_p = a_p_obj['class_id']
            if a == a_p:
                continue
            
            if _has_conflicts(a_obj, a_p_obj):
                theta[a][a_p] = 1
            else:
                theta[a][a_p] = 0

    a_s_tuples = [(s,a) for s in S for a in A]

    x = LpVariable.dicts("alloc_", (S,A), 0, 1, cat='Integer')

    ############################ Problem formulation ############################

    prob = LpProblem("Classroom allocation problem", LpMinimize)

    # Objective function
    prob += (
        lpSum([USO[s][a] * x[s][a] for (s,a) in a_s_tuples]),
        "Sum_of_allocation_cost"
    )

    # One classroom per class constraint
    for a in A:
        prob += (
            lpSum([x[s][a] for s in S]) == 1,
            f"Number_of_allocated_classrooms_for_class_{a}"
        )

    # Resources/Preferences constraint
    for s in S:
        for a in A:
            prob += (
                x[s][a] <= eta[s][a],
                f'Classroom_{s}_can_contain_class{a}'
            )
    
    # Time conflict constraint
    for s in S:
        for a in A:
            for a_p in A:
                if a == a_p:
                    continue
                if theta[a][a_p] == 1:
                    prob += (
                        x[s][a] + x[s][a_p] <= 1
                    )

    ############################## Problem solution ##############################

    # The problem data is written to an .lp file
    prob.writeLP("ClassroomAllocationProblem.lp")

    # The problem is solved using PuLP's choice of Solver
    prob.solve()

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])

    # Each of the variables is printed with it's resolved optimum value
    for x in prob.variables():
        print(x.name, "=", x.varValue)

    # The optimised objective function value is printed to the screen
    print("Total Cost of Allocation = ", value(prob.objective))

    return prob






