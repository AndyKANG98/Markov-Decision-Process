def read_input(filename):
    """
    grid_size - strictly positive
    num_obstacles - non-negative
    Next num_obstacles lines: <x>,<y> - strictly positive, denoting locations of obstacles
    < x>,<y> - destination point
    """
    lines = open(filename + ".txt").read().splitlines()
    grid_size = int(lines[0])
    num_obstacles = int(lines[1])
    obstacles = []
    for i in range(num_obstacles):
        obstacles.append(tuple(eval(lines[i+2])))
    destination = tuple(eval(lines[num_obstacles+2]))
    
    return grid_size, obstacles, destination

def write_output(mdp, policy):
    output_file = open("output.txt","w")
    for j in range(mdp.grid_size):
        for i in range(mdp.grid_size):
            output_file.write(policy[(i,j)][0])
        output_file.write('\n')
    output_file.close()

class MDP():
    def __init__(self, grid_size, obstacles, destination, gamma):
        self.grid_size = grid_size
        self.obstacles = obstacles
        self.destination = destination
        # Set up reward map for each state
        self.reward = {}
        for i in range(grid_size):
            for j in range(grid_size):
                self.reward[(i,j)] = -1
        for o in obstacles:
            self.reward[o] = -101
        self.reward[destination] = 99
        
        # set up gamma
        self.gamma = gamma

    def action(self, state, action):
        """
        param: 
            state - (i,j) current state
            action - 'up', 'left', 'down', 'right'
        return:
            next_state - new (i,j)
        """
        if action == 'up':
            if state[1] == 0:
                return state
            return (state[0], state[1]-1)
        elif action == 'left':
            if state[0] == 0:
                return state
            return (state[0]-1, state[1])
        elif action == 'down':
            if state[1] + 1 == self.grid_size:
                return state
            return (state[0], state[1]+1)
        elif action == 'right':
            if state[0] + 1 == self.grid_size:
                return state
            return (state[0]+1, state[1])
        else:
            print ('Invalid action: ' + action)
            return
        
    def expect_utility(self, state, policy, utility):
        actions = ['up', 'left', 'down', 'right']
        expect_u = 0
        for a in actions:
            new_state = self.action(state, a)
            if a == policy:
                expect_u += 0.7 * utility[new_state]
            else:
                expect_u += 0.1 * utility[new_state]
        return expect_u

def value_interation(mdp, e):
    """
    param:
        mdp - an MDP with states S, actions A(s), transition model P(s'|s,a), Reward R(s), discount gamma
        e - epsilon tolerence
    return:
        utility
    """
    # Set up utility map for each state
    utility = {}
    for i in range(grid_size):
        for j in range(grid_size):
            utility[(i,j)] = 0
    new_utility = utility.copy()
    
    # initial delta - the maximum change in the utility of any state in an iteration
    delta = 0
    # value iteration
    while (True):
        utility = new_utility.copy()
        delta = 0
        for i in range(mdp.grid_size):
            for j in range(mdp.grid_size):
                s = (i,j)
                if s == mdp.destination:
                    new_utility[s] = mdp.reward[s]
                else:
                    new_utility[s] = mdp.reward[s] + mdp.gamma * max(mdp.expect_utility(s, 'up', utility), 
                                                                  mdp.expect_utility(s, 'left', utility),
                                                                  mdp.expect_utility(s, 'right', utility),
                                                                  mdp.expect_utility(s, 'down', utility))
                if abs(new_utility[s] - utility[s]) > delta:
                    delta = abs(new_utility[s] - utility[s])
        
        if (delta < e*(1-mdp.gamma)/mdp.gamma):
            break
    
    return utility

def find_policy(mdp, utility):
    policy = {}
    # compute policies
    for i in range(mdp.grid_size):
        for j in range(mdp.grid_size):
            state = (i,j)
            policy[state] = ['up']
            max_expect_utility = mdp.expect_utility(state, 'up', utility)
            for p in ['down', 'right', 'left']:
                if mdp.expect_utility(state, p, utility) > max_expect_utility:
                    max_expect_utility = mdp.expect_utility(state, p, utility)
                    policy[state] = [p]
    # write obscatles and destination
    for o in mdp.obstacles:
        policy[o] = ['o']
    policy[mdp.destination] = ['.']
    return policy

def translate_policy(policy):
    translate_map = {'up':['^'], 'left':['<'], 'down':['v'], 'right':['>']}
    for key in policy:
        if policy[key][0] in translate_map:
            policy[key] = translate_map[policy[key][0]]
    return policy

if __name__ == "__main__":
    filename = 'input'
    grid_size, obstacles, destination = read_input(filename)
    gamma = 0.9
    e = 0.1

    mdp = MDP(grid_size, obstacles, destination, gamma)

    utility = value_interation(mdp, e)
    policy = find_policy(mdp, utility)
    translate_policy(policy)

    write_output(mdp,policy)