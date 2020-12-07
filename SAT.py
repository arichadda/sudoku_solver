### Ari Chadda
### 10/25/20 CS76 F20
### PA5

import random


class SAT:
    def __init__(self, puzzle_name):
        self.puzzle_name = puzzle_name  # passed file
        self.cnf_file = puzzle_name[:-4] + ".cnf"  # get cnf file

        self.constraints = []  # all of the clauses
        self.variables = set()  # set of variables
        self.solution = {}  # to store answer with T/F
        self.unsatisfied = []  # list of unsatisfied clauses

        self.gsat_threshold = 0.7  # threshold for GSAT
        self.p = 0.2  # probability for WalkSAT

        # max number allowed b/c the SAT solvers will run till the find a solution eventually
        self.max_iterations = 100000
        self.iteration_count = 0

        f = open(self.cnf_file, 'r')  # open cnf file to read
        for line in f:
            line = line.strip()

            if len(line) == 0:  # if the line is empty skip
                pass
            else:
                temp_list = line.split(" ")  # otherwise add the or clause to a list

                for literal in temp_list:
                    if literal[0] != '-':
                        self.variables.add(literal)  # add the variables without the - sign to the set w/ no repeats

                self.constraints.append(temp_list)  # add all the constraints to a list
        f.close()  # close file


    def gsat(self):

        for variable in self.variables:  # random assignment of T/F for all variables
            self.solution[variable] = random.choice([True, False])

        while not self.check_sat():  # checking for terminal, while not, keep going

            self.iteration_count += 1  # counter for max number

            if self.iteration_count <= self.max_iterations:  # if not max number keep going

                rand_num = random.random()  # get random number between 0 and 1

                if rand_num > self.gsat_threshold:  # if random number is greater than threshold, execute random flip
                    to_get = random.randint(1, len(self.variables) - 1)
                    to_flip = list(self.variables)[to_get]  # pick random literal from clause
                    self.flipper(to_flip)  # flip it

                else:
                    score_dict = {}

                    for element in self.variables:
                        # find which variable results in fewest unsatisfied clauses
                        self.min_conflict_heuristic(element, score_dict)

                    temp_list = list(score_dict.items())  # convert to list for shuffle
                    random.shuffle(temp_list)  # shuffled so variables with same score are randomized
                    score_dict = dict(temp_list)
                    score_list = sorted(score_dict, key=score_dict.get)  # sort in ascending order
                    to_flip = score_list[0]  # take the first one
                    self.flipper(to_flip)  # flip it

            else:
                print("FAIL: Reached max iterations with no solution")
                return False  # failed to find solution within max
        return True  # success - should print ascii solution


    def walksat(self):
        for variable in self.variables:   # random assignment of T/F for all variables
            self.solution[variable] = random.choice([True, False])

        while not self.check_sat():  # checking for terminal, while not, keep going

            self.iteration_count += 1  # counter for max number

            if self.iteration_count <= self.max_iterations:  # if not max number keep going

                index = random.randint(0, len(self.unsatisfied) - 1)  # pick a random clause from unsatisfied
                rule = self.unsatisfied[index]
                rand_num = random.random()  # get random number between 0 and 1

                if rand_num < self.p:  # if the random number is less than p, execute random flip
                    to_get = random.randint(0, len(rule) - 1)
                    to_flip = rule[to_get]  # pick random literal from clause
                    if to_flip[0] == '-':
                        self.flipper(to_flip[1:])
                    else:
                        self.flipper(to_flip)  # flip it
                else:

                    score_dict = {}

                    for element in rule:
                        # find which variable results in fewest unsatisfied clauses
                        self.min_conflict_heuristic(element, score_dict)

                    score_list = sorted(score_dict, key=score_dict.get)  # sort in ascending order
                    to_flip = score_list[0]  # take the lowest one
                    self.flipper(to_flip)  # flip it
            else:
                print("FAIL: Reached max iterations with no solution")
                return False  # failed to find solution within max
        return True  # success - should print ascii solution

    def check_sat(self):
        self.unsatisfied = []  # re-initialize the unsatisfied list
        true_count = 0  # counter for clause satisfaction

        for sentence in self.constraints:
            for literal in range(len(sentence)):

                if sentence[literal][0] == "-":  # if negative, then if there is at least one false, clause satisfied
                    if not self.solution.get(sentence[literal][1:]):
                        true_count += 1
                else:  # if positive, then if there is at least one true, clause satisfied
                    if self.solution.get(sentence[literal]):
                        true_count += 1

            if true_count == 0:  # if unsatisfied add to list
                self.unsatisfied.append(sentence)
            true_count = 0
        if len(self.unsatisfied) == 0:  # if no unsatisfied terminate
            return True
        return False

    def flipper(self, to_flip):
        current_val = self.solution.get(to_flip)  # get the current value
        if current_val:  # if the current value is true then make it false
            self.solution[to_flip] = False
        else:  # vise versa
            self.solution[to_flip] = True

    def write_solution(self, solution_file):
        f = open(solution_file, 'w')  # open file for writing

        for key in self.solution.keys():  # for all the literals in the solution
            if self.solution.get(key):
                f.write(key + '\n')  # write to teh solution file with one literal per line
            else:
                f.write('-' + key + '\n')
        f.close()

    def min_conflict_heuristic(self, element, score_dict):  # minimize the number of unsatisfied clauses
        if element[0] == '-':
            element = element[1:]
        self.flipper(element)  # flip it
        self.check_sat()  # get new unsatisfied
        score_dict[element] = len(self.unsatisfied)  # add to score - fewer is better
        self.flipper(element)  # flip it back
