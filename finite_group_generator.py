# finite_group_generator.py
# Max Liang
# created 12/18/22
# Description:
# Generate multiplication table
# Using nodal network to model the branching of multiplication table
# Using recursion to generate the full branches

    
class node:
    def __init__(self, n):
        self.item = [[[[-1 for i in range(n)] for j in range(n)]]]
        self.n = n
        self.branches = 1
        self.gen = 0
        self.i = 0
        self.j = 0
        self.state = True


    def get_stat(self):
        """Print the state of the object node"""
        print(f"the current generation is {self.gen + 1} \nwith total {self.branches} branches \nthe indexes are ({self.i}, {self.j})")


    def update(self):
        """Update i, j index"""
        if self.j < (self.n - 1):
            self.j += 1
        elif self.i < (self.n - 1):
            self.j = 0
            self.i += 1
        else:
            self.state = False


    def cond(self, mult_list, branch):
        """Produce restricted list of possible transformation between group member by enforcing the once_and_only_once rule"""
        table = self.item[self.gen][branch-1]  
        x_row = table[self.i]
        y_row = [ele[self.j] for ele in table]
        del_list = []
        for i in mult_list:
            if (i in x_row) or (i in y_row):
                del_list.append(i)
        for i in del_list:
            mult_list.remove(i) 
        return mult_list


    def mult(self):
        """Generate branches for index i, j and update stats to next generation"""
        next_gen = []
        mult_list = []
        if self.i == 0:
            mult_list.append(self.j)
            for b in range(self.branches):
                clone = self.item[self.gen][b].copy()
                clone[self.i][self.j] = mult_list[0]
                next_gen.append(clone)
            self.branches = self.branches
            
        elif self.j == 0:
            mult_list.append(self.i)
            for b in range(self.branches):
                clone = self.item[self.gen][b].copy()
                clone[self.i][self.j] = mult_list[0]
                next_gen.append(clone)
            self.branches = self.branches
            
        else:
            new_branch = 0
            for b in range(self.branches):
                full_list = [i for i in range(self.n)]
                mult_list = self.cond(full_list, b)
                for p in mult_list:
                    clone = [ele[:] for ele in self.item[self.gen][b-1]]
                    clone[self.i][self.j] = p
                    next_gen.append(clone)
                    new_branch += 1
            self.branches = new_branch
            
        self.update()
        self.gen += 1
        return next_gen


    def edge(self):
        """Runs self.edge() recursively until i, j indexes are out of bound"""
        self.get_stat()
        self.item.append(self.mult())
        if self.state == False:
            return self
        else:
            return self.edge()


dim = int(input("Enter an positive integer: "))
g = node(dim)
g.edge()

