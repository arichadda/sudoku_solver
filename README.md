# README for PA5

### Ari Chadda - CS76 - F20 - 10/25/20
--

To run the SAT solver, go to `solve_sodoku.py` and uncomment the puzzle you would like to run as well as the algorithm either `gsat()` or `walksat()`. The solution will be written to a `.sol` file with the same base name as the puzzle. 

*GSAT:* The GSAT algorithm was implemented as per the recommenced pseudocode. A random assignment of True or False was chosen for each variable and then assigned. At each iteration, the number of unsatisfied constraints was checked. Then based on the random number between 0 and 1 that was generated (if it was greater than the threshold value), a random variable was flipped or the variable that satisfied the most constraints if flipped was flipped. For the flip check, I used the same unsatisfied constraint function as the terminal test and then re-updated back to the original value while recording the number of unsatisfied constraints where fewer was better. 
  
*WalkSAT:* The WalkSAT algorithm was implement based on the pseudocode from class. This also began with a random assignment of True or False for each variable and then assigned. With each iteration the number of unsatisfied constraints was checked and from this a random clause was selected. If the random number between 0 and 1 that was generated was less than the probability p value, then a random variable was selected from the clause and flipped making sure to get rid of all negative signs during assignment, while if it was greater then, then the variable was chosen greedily from variables in the rule to see which one if flipped would decrease the number of unsatisfied clauses the most. I interpreted this in implementation again as flipping one of the rule variables, using the terminal function to get the new number of unsatisfied clauses and then flipping it back. Then, sorting this number ascending and taking the first number without randomization and flipping it. 

*Terminal Checking:* Using the CNF principles, I implemented the constraint checking as suggested in the assignment documentation. If at least one value was in a true or statement, then it was considered satisfied, and vise versa if it was a false or statement. 