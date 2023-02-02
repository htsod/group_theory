# finite_group_generator.py
# Max Liang
# created 12/18/22
# Description:
# Generate multiplication table
# Using nodal network to model the branching of multiplication table
# Using recursion to generate the full branches

import numpy as np


class finite_group:
    def __init__(self, n):
        """
        Description:
            "self.item" stores all dynamic information, it gets modified as the mult table get generated
            "self.n" tells the order of the group
            "self.branch" is being used when there is more than one way to update the mult table
            "self.gen" step forward when the modification to the current indices, "self.i" and "self.j" finished
            "self.i" tells the i indices of the mult table
            "self.j" tells the j indices of the mult table
            "self.state" stops the recursion when "self.i" and "self.j" reaches the limit

        :param n: the dimensions of the group
        """
        # self.item is being used to hold the multiplication table
        self.item = [[[[-1 for i in range(n)] for j in range(n)]]]
        self.n = n
        self.branches = 1
        self.gen = 0
        # indices i, j is being used to track and modify the element in the mult table
        self.i = 0
        self.j = 0
        self.state = True


    def get_stat(self):
        """
        Description:
            Print the state of the object node, is being used for debug purposes
        """
        print(f"the current generation is {self.gen + 1} \nwith total {self.branches} branches \nthe indexes are ({self.i}, {self.j})")


    def _update(self):
        """
        Description:
            Update i, j index if the state of the system is false.
            The state will turn false if certain conditions are met
        """
        if self.j < (self.n - 1):
            self.j += 1
        elif self.i < (self.n - 1):
            self.j = 0
            self.i += 1
        else:
            self.state = False


    def _cond(self, mult_list, branch):
        """
        Description:
            Produce restricted list of possible transformation between group member
            Enforcing the once_and_only_once rule

        :param mult_list: Possible ways to assign the element in the mult table
        :param branch: The current branch
        :return: Mult table without any duplicate
        """
        # create a link to self.item with the current generation and branch
        table = self.item[self.gen][branch-1]
        # create x and y row to iterate through
        x_row = table[self.i]
        y_row = [ele[self.j] for ele in table]
        del_list = []
        # Remove any duplicate element in mult_list
        for i in mult_list:
            if (i in x_row) or (i in y_row):
                del_list.append(i)
        for i in del_list:
            mult_list.remove(i)
        return mult_list


    def _mult(self):
        """
        Description:
            Generate branches for index i, j and update stats to next generation
        """
        next_gen = []

        # if element either i or j is the identity, then fill the current spot with j or i.
        if self.i == 0:
            for b in range(self.branches):
                clone = self.item[self.gen][b].copy()
                clone[self.i][self.j] = self.j
                next_gen.append(clone)
            
        elif self.j == 0:
            for b in range(self.branches):
                clone = self.item[self.gen][b].copy()
                clone[self.i][self.j] = self.i
                next_gen.append(clone)

        # if not an identity, carry out the multiplication rule
        else:
            new_branch = 0
            for b in range(self.branches):
                # full_list gives all the possibilities while mult_list gives the refined list
                full_list = [i for i in range(self.n)]
                mult_list = self._cond(full_list, b)
                # for each possible possibilities, generate add a new branch
                for p in mult_list:
                    clone = [ele[:] for ele in self.item[self.gen][b-1]]
                    clone[self.i][self.j] = p
                    next_gen.append(clone)
                    new_branch += 1
            self.branches = new_branch
            
        self._update()
        self.gen += 1
        return next_gen


    def edge(self):
        """Runs self.edge() recursively until i, j indexes are out of bound"""
        self.item.append(self._mult())
        # The following command is for debugging purposes
        # get the statistic for each generation
        # self.get_stat()
        # print the current generation
        # print(self.item[self.gen])
        if self.state == False:
            pass
        else:
            return self.edge()


    def associative_check(self):
        """Check the associativity of each group generated and remove table that fail the conditions"""
        need_remove = [0 for i in range(len(self.item[self.gen]))]
        current_item = self.item[self.gen].copy()
        index = 0
        for t in current_item:
            for i in range(self.n):
                for j in range(self.n):
                    for k in range(self.n):
                        break_out_flag_1, break_out_flag_2, break_out_flag_3 = False, False, False
                        if (i != j) and (j != k) and (i != k):
                            j_k = t[j][k]
                            ii = t[i][j_k]
                            i_j = t[i][j]
                            kk = t[i_j][k]
                            # if the associativity test fails
                            if ii != kk:
                                break_out_flag_1 = True
                                break
                    if break_out_flag_1:
                        break_out_flag_2 = True
                        break
                if break_out_flag_2:
                    need_remove[index] = 1
                    break
            index += 1

        if (np.array(need_remove).sum()) != 0:
            for i, j in enumerate(need_remove):
                if j:
                    current_item.remove(self.item[self.gen][i])
        self.item[self.gen] = current_item





dim = int(input("Enter an positive integer: "))
g = finite_group(dim)
g.edge()
g.associative_check()
print(f"The groups generated are: \n{g.item[g.gen]} \n With {len(g.item[g.gen])} generated groups")

