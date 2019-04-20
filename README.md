# Markov Decision Process

> CSCI 360 Project 3 - Value Iteration Approach

<br>

### Background

Mars Rover planning is part of a larger set of problems that involve planning with uncertainty ,
in this case with a fixed, known world. Given knowledge of this world (in the form of a
2-dimensional grid), a movement cost (-1), a reward for reaching the destination (+100), and a
penalty for hitting obstacles (-100), you are asked to compute policies given that each
movement has uncertainty. You must compute a policy, i.e., a mapping that tells you where
your Rover should try to go in each grid location, based on expected utility 

<br>

### Input

The input file will be formatted as follows (all arguments are 32-bit integers):
< grid_size > // strictly positive
< num_obstacles > // non-negative
Next num_obstacles  lines: <x>, <y> // strictly positive, denoting locations of obstacles
< x> , <y> // destination point

<br>

### Output
For each input, you will compute a policy with value-iteration and write a file containing the
policy in the following format:

- Obstacles are represented by the letter ‘o’
- EAST is represented by the right-caret character ‘>’
- WEST is represented by the left-caret character ‘<’
- NORTH is represented by the hat symbol ‘^’
- SOUTH is represented by the letter ‘v’
- The destination is represented by a period symbol ‘.’ 

<br>

