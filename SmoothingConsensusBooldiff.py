
from itertools import combinations
import os

def factorize(minterm,literal_list_fact,var):

    factorized_list = []

    if var.isupper():
        index = literal_list_fact.index(var.lower())
        del literal_list_fact[index]
        for cube in minterm:
            if cube[index] == '0':
                factorized_list.append(cube[:index]+cube[index+1:])
    else:
        index = literal_list_fact.index(var)
        del literal_list_fact[index]
        for cube in minterm:
            if cube[index] == '1':
                factorized_list.append(cube[:index]+cube[index+1:])
    
    factorized_list = list(set(factorized_list))

    return factorized_list,literal_list_fact


def generate_combinations(s,expanded_list):
    # Base case: if there's no 'x' in the string, add it to expanded_list
    if 'x' not in s:
        expanded_list.append(s)
        return
    
    # Replace the first 'x' with '0' and '1', and recursively process both
    generate_combinations(s.replace('x', '0', 1),expanded_list)  # Replace 'x' with '0' in the first occurrence
    generate_combinations(s.replace('x', '1', 1),expanded_list)  # Replace 'x' with '1' in the first occurrence


def gen_minterm(cube,literal_list):
    minterm = []
    for literal in literal_list:
        if literal in cube:
            minterm.append("1")
        elif literal.capitalize() in cube:
            minterm.append("0")
        else:
            minterm.append("x")
    minterm =  "".join(minterm)

    expanded_list = []

    if 'x' in minterm:
        generate_combinations(minterm,expanded_list) 
        return expanded_list
    return minterm


def consensus_fun(fact_norm,fact_comp):
    consensus_list = []
    if len(fact_norm)>len(fact_comp):
        iteratable_list = fact_norm
        comparing_list = fact_comp
    else:
        iteratable_list = fact_comp
        comparing_list = fact_norm
        

    for item in iteratable_list:
        if item in comparing_list:
            consensus_list.append(item)

    
    if len(consensus_list) == 0 :
        return 0
    else :
        return consensus_list
    

def booldiff(smoothing,consensus):

    """
      Implement booldiff = smoothing * (consensus)' 
      Initially implement (consensus)' and then apply 
      consensus function with smoothing and (consensus)' 
      as arguments.
    """
    if  consensus == 0 :
        return smoothing
    else :
        bit_length = len(smoothing[0])
        possible_bool_list = [bin(i)[2:].zfill(bit_length) for i in range(2**bit_length)]

        # Computing Consensus'
        for minterm in consensus:
            if minterm in possible_bool_list:
               possible_bool_list.remove(minterm)
        
        # After the loop possible_bool_list becomes the complement of consensus
    return consensus_fun(smoothing,possible_bool_list)



# Function to check if two minterms differ by only one bit
def differ_by_one_bit(a, b):
    diff_count = 0
    diff_index = -1
    for i in range(len(a)):
        if a[i] != b[i]:
            diff_count += 1
            diff_index = i
    return diff_count == 1, diff_index

# Function to combine two minterms if they differ by one bit
def combine_minterms(a, b, index):
    combined = list(a)
    combined[index] = '-'
    return ''.join(combined)

# Function to find prime implicants
def find_prime_implicants(minterms):
    new_minterms = set()
    used = set()
    for a, b in combinations(minterms, 2):
        differ, index = differ_by_one_bit(a, b)
        if differ:
            new_minterms.add(combine_minterms(a, b, index))
            used.add(a)
            used.add(b)
    remaining_minterms = set(minterms) - used
    return new_minterms.union(remaining_minterms)

# Main function to minimize the boolean function
def minimize_function(minterms):
    # Keep simplifying until no more combinations can be made
    while True:
        new_minterms = find_prime_implicants(minterms)
        if new_minterms == set(minterms):
            break
        minterms = new_minterms
    return minterms

def min_to_cube(minfunc,fact_literal_list):
    minfunc = list(minfunc)
    length = len(minfunc[0])

    final_rep = []

    for item in minfunc:
        counter = 0
        cube_list = []

        for index,char in enumerate(item):
            if char == '-':
                counter = counter + 1
            elif char == '1':
                cube_list.append(fact_literal_list[index])
            else:
                cube_list.append(fact_literal_list[index].capitalize())

        if counter == length:
            return 1 
        else :
            final_rep.append("".join(cube_list))

    final_rep = "+".join(final_rep)
    return final_rep    


def main():
    
    os.system("clear")
    
    Welcome_text = """
    
    Python script to obtain Smoothing, Consensus and Boolean Difference for a Boolean Function 
    
    Smoothing           = f_a + f_A
    Consensus           = f_a & f_A
    Boolean Difference  = Smoothing & (Consensus)'
    
    The script is written using few assumptions : 
    1. Normal variables are represented using lower case variables (a,b,x,y)
    2. Complement variables are represented using Upper case variables (A,B,X,Y)
    
    Upon program start the user is expected to input the total number of distinct varibles being used i,e.
    if the variables use are x,y and z then the input must be xyz without any spaces
    
    Then the boolean expression must be entered in the SOP form(seperated by (+) and without spaces)
    
    At the last, the user is expected to input the variable for which Smoothing, Consensus and Boolean Difference 
    are expected( lower case literal is expected ).
    
    Upon entering all the inputs, the program will return minimized Smoothing, Consensus and Boolean Difference
    
    """
    print(Welcome_text)
    variables =  input("    Enter the variables: ")
    expression = input("    Enter the boolean expression: ")
    fact_var   = input("    Enter the variable for factorization: ")


    literal_list = []
    for literal in variables:
        literal_list.append(literal)

    exp_minterms = []

    for cube in expression.split("+"):
        exp_minterms.append(gen_minterm(cube,literal_list))


    exp_minterms = sum([item if isinstance(item, list) else [item] for item in exp_minterms], [])
    exp_minterms = list(set(exp_minterms))

    fact_norm,fact_literal_list = factorize(exp_minterms,literal_list[:],fact_var)

    fact_comp,fact_literal_list = factorize(exp_minterms,literal_list[:],fact_var.capitalize())

    smoothing = list(set(fact_norm+fact_comp)) 

    consensus = consensus_fun(fact_norm,fact_comp)

    if consensus == 0:
        final_consensus = 0
    else:
        final_consensus = min_to_cube(minimize_function(consensus),fact_literal_list)

    BooleanDiference = booldiff(smoothing,consensus)


    # These Print statements are for intermdiate steps : Minterms Identification in each step
    
    
    #print("smoothing function = ",smoothing)
    #print("Consensus function =",consensus)
    #print("Boolean Difference function = ",BooleanDiference)

    #print("Minimized Minterms of smoothing function =",minimize_function(smoothing))
    #print("Minimized Minterms of Consensus function =",minimize_function(consensus))
    #print("Minimized Minterms of Boolean Difference function =",minimize_function(BooleanDiference))
    
    
    print("\n")
    print("smoothing function =",min_to_cube(minimize_function(smoothing),fact_literal_list))
    print("\nConsensus function =",final_consensus)
    print("\nBoolean Difference function = ",min_to_cube(minimize_function(BooleanDiference),fact_literal_list))
    print("\n\n")



# Main function 

if __name__ == "__main__":
    main()