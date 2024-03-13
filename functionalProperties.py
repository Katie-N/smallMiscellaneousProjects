'''
Program Name: EECS 210 Assignment 4
Description: This program uses functions to evaluate relations similarly to assignment 3. We will again examine if the relations are reflexive, symmetric, or transitive. However on top of that we will find the closures for relations that do not meet these properties. We will also examine the more advanced properties of relations: whether the relations are an equivalence relation and whether a relation and set form a poset.
Inputs: none
Output:
    - Print out the part of each problem being evaluated
    - Print out the relation being tested
    - All problems print out the whether the relation (and domain if applicable) have a given property.
        - 2 tests for reflexive
        - 2 tests for symmetric
        - 2 tests for transitive
        - 2 tests for equivalence
        - 2 tests for partial ordering
    - For the first 3 problems (testing if the relation has the following properties: reflexive, symmetric, and transitive), if a test is failed the respective closure will be found and printed out.
    - For problems 4 and 5, if the property is not found, it will print out which test(s) failed.
Collaborators: none
Other sources: My own code for the reflexive, symmetric, antisymmetric and transitive functions from Assignment 3.
Author: Katie N github.com/Katie-N
Creation Date: 2/20/2024
'''

# Initalize variable values in the relations:
a = "a"
b = "b"
c = "c"
d = "d"
e = "e"

# 1. Determine if a relation (R) of ordered pairs is reflexive

# This reflexive function is taken directly from my code in assignment 3
# Make a function that takes a relation in the form of a set of ordered pairs
# returns true if the the relation is reflexive on the defined range
# returns false if it is not reflexive on the defined range
def reflexive(set, domain):
    # loop through the range
    for x in domain:
        # If any occurrence of (x,x) is not in the given set then it is not in the set
        if (x,x) not in set:
            # Let the user know the set is not reflexive and which value proved this
            print(f"Not reflexive because there exists ({x}, {x}) which is not in the set")
            # Return false because the set is not reflexive
            return False
    # Every (x,x) was tested and passed so the set must be reflexive by exhaustion
    # Let the user know it is reflexive
    print("Reflexive because every (a,a) is in the set")
    # Return true because the set is reflexive
    return True

# This function finds the reflexive closure of a relation given the relation as a set of ordered pairs and the domain as a list
def reflexiveClosure(set, domain):
    # Create a shallow copy of the original set so we can modify it by adding the missing ordered pairs which would make the set reflexive.
    # We need a shallow copy instead of a simple assignment because we want to modify a copy of the original values of the set.
    # With simple assignment, we create a reference to the same memory address as the original set so modifying the copy would actually modify the original.
    closure = set.copy()
    # loop through the range
    for x in domain:
        # If any occurrence of (x,x) is not in the given set then we must add it
        if (x,x) not in set:
            closure.add((x,x))
    # Any (x,x) that was not in the set before, is in there now.
    # Return the closure
    return closure

# This function takes a relation in the form of a set and the domain of the relation. It uses the helper functions "reflexive" and "reflexiveClosure" to tell the user if the set is reflexive and if it is not, tell the user what the reflexive closure is.
def reflexivity(set, domain):
    # Part a says to print the relation out.
    # Note that end="" allows us to not print a new line after print() which is the default behavior
    print("R = ", end="")
    # This prints out the actual relation. sep="" allows python to separate each ordered pair with a comma.
    print(set, sep=",")

    # Call the reflexive function and store the boolean result
    isReflexive = reflexive(set, domain)
    # If the given relation is not reflexive then we want to find the closure
    if (not isReflexive):
        # Tell the user what the closure is
        print("The closure is R* = ", end="")
        print(reflexiveClosure(set, domain))
    # Print a new line to make our output clean
    print("")

# Tell the user what problem is being executed
print("1d)")
# Initialize the relation and the domain of the relation
R = {(1,1), (4,4), (2,2), (3,3)}
domain = [1,2,3,4]
# Call the main function that handles the reflexivity of the relation
reflexivity(R, domain)

# Tell the user what problem is being executed
print("1e)")
# Initialize the relation and the domain of the relation
R = {(a,a), (c,c)}
domain = [a,b,c,d]
# Call the main function that handles the reflexivity of the relation
reflexivity(R, domain)

# 2. Determine if a relation (R) of ordered pairs is symmetric

# This symmetric function is taken directly from my code in assignment 3
# Make a function that takes a relation in the form of a set of ordered pairs
# Returns true if the relation is symmetric
# Returns false if the relation is not symmetric
def symmetric(set):
    # Loop through each (a,b) in the given set
    for pair in set:
        # Pull out the a and b from the ordered pair
        a = pair[0]
        b = pair[1]
        # Check if (b,a) isn't in the set. If it is not then the set cannot be symmetric
        if (b,a) not in set:
            # Let the user know the set is not symmetric
            print(f"Not symmetric because there exists {pair} for which ({b},{a}) is not in the set")
            # Return False because the set is not symmetric
            return False
    # Every (b,a) was tested and passed so the set must be symmetric by exhaustion
    # Let the user know it is symmetric
    print("Symmetric because for every (a,b) in the set, (b,a) is also in the set")
    # Return true because the set is symmetric
    return True

# This function finds the symmetric closure of a relation given the relation as a set of ordered pairs
def symmetricClosure(set):
    # Create a shallow copy of the original set so we can modify it by adding the missing ordered pairs which would make the set reflexive.
    # We need a shallow copy instead of a simple assignment because we want to modify a copy of the original values of the set.
    # With simple assignment, we create a reference to the same memory address as the original set so modifying the copy would actually modify the original.
    closure = set.copy()
    # Loop through each (a,b) in the given set
    for pair in set:
        # Pull out the a and b from the ordered pair
        a = pair[0]
        b = pair[1]
        # Check if (b,a) isn't in the set. If it is not then the set then we must add it to the closure
        if (b,a) not in set:
            closure.add((b,a))
    # Return the closure
    return closure

# This function takes a relation in the form of a set of ordered pairs. It uses the helper functions "symmetric" and "symmetricClosure" to tell the user if the set is symmetric and if it is not, tell the user what the symmetric closure is.
def symmetricity(set):
    # Part a says to print the relation out.
    # Note that end="" allows us to not print a new line after print() which is the default behavior
    print("R = ", end="")
    # This prints out the actual relation. sep="" allows python to separate each ordered pair with a comma.
    print(set, sep=",")

    # Call the symmetric function and store the boolean result
    isSymmetric = symmetric(set)
    # If the given relation is not symmetric then we want to find the closure
    if (not isSymmetric):
        # Tell the user what the closure is
        print("The closure is R* = ", end="")
        print(symmetricClosure(set))
    # Print a new line to make our output clean
    print("")

# Tell the user what problem is being executed
print("2d)")
# Initialize the relation
R = {(1,2), (4,4), (2,1), (3,3)}
# Call the main function that handles the symmetry of the relation
symmetricity(R)

# Tell the user what problem is being executed
print("2e)")
# Initialize the relation
R = {(1,2), (3,3)}
# Call the main function that handles the symmetry of the relation
symmetricity(R)

# 3. Write code that determines if a relation (R) of ordered pairs is transitive or not

# R is transitive if it contains (a,b) and (b,c), then it also must contain (a,c) for a ∈ A, b ∈ A, and c ∈ A
# This transitive function is taken directly from my code in assignment 3
# Make a function that takes a relation in the form of a set of ordered pairs
# Returns true if the relation is transitive
# Returns false if the relation is not transitive
def transitive(set):
    for pair in set:
        # Pull out the a and b from the ordered pair
        a = pair[0]
        b = pair[1]
        # Loop through the set a second time
        for pair2 in set:
            # If the first value of pair2 is the same as the second value of pair,
            # then in order to be transitive, the pair (a,c) must also be in the set
            if pair2[0] == b:
                # Pull out c
                c = pair2[1]
                # Check if (a,c) isn't in the set so we can prove the set is not transitive
                if (a, c) not in set:
                    # Let the user know what values made the set fail the transitive test
                    print(f"Not transitive because ({a},{b}) and ({b},{c}) are in the set but ({a},{c}) is not")
                    # Return false because the set is not transitive
                    return False
    # At this point we've looped through every pair in the set and haven't found
    # any that makes the set not transitive. Therefore the set is transitive by exhaustion
    print("Transitive because for every (a,b) and (b,c) in the set, (a,c) is also in the set")
    return True

# If it is not, find the transitive closure of R (R*) using Warshall’s Algorithm.

# This transitiveClosure function takes in a matrix arranged as:
# [[row 1], [row 2], ... [row n]] where each element within a row is in a new column.
# It uses Warshall's algorithm to find the transitive closure matrix which is what gets returned at the end.
# This assumes a well-formed square matrix will be given
def transitiveClosure (matrix):
    # Get the length of the matrix which is really the number of rows (which is the same as the number of columns since it must be a square matrix).
    length = len(matrix)
    # Loop through the matrix n times (in an nxn matrix)
    # We will be finding the matrix when k is held constant for each loop. This comes from the Warshall Algorithm.
    # So for the first loop, k = 0, for the second loop, k = 1...
    for k in range(0, length):
        # Loop through each row of the matrix
        for row in range(0, length):
            # Loop through each column of the matrix
            for col in range(0, length):
                # Warshall's algorithm tells us that the new value in the matrix should equal m_ij ∪ (m_ik ∩ m_kj)
                # Use the python keyword "or" for ∪ and "and" for ∩
                matrix[row][col] = matrix[row][col] or (matrix[row][k] and matrix[k][col])
        # Print the matrix found during this iteration of k
        # Note we use "k + 1" because we want the English count to start at 1 even though technically the index starts at 0
        print("\nk = " + str(k + 1))
        # We want the matrix to be printed with each row on a new line.
        # So we have to insert a new line between all the closing brackets.
        # One way to do this is to replace all "]" instances with "]\n"
        print(str(matrix).replace("]," , "]\n"))
    # At this point we have finished all of the loops and found all k matrices.
    # The matrix is now in its final form as a trasitive closure so we can print it out
    # (again we have to insert some new lines when we print it so the matrix is formatted correctly)
    print("\nTransitive Closure: \n" + str(matrix).replace("]," , "]\n"))
    # Return the transitive closure matrix
    return matrix

# I made this function to take in a relation in the form of a set of ordered pairs, along with the domain the relation is on.
# It then returns a matrix representing the relation.
# The order of the elements in the domain is the order of the elements as the header of the columns and sidebar of the rows.
# Meaning if domain = [a,b,c] then the matrix is formed with (a,a) in the top left.
# But if domain = [c,b,a] then the matrix is formed with (c,c) in the top left.
def relationToMatrix(set, domain):
    # declare an empty list for the matrix
    mtx = []
    # Loop through the rows
    for x in range(0, len(domain)):
        # create a new empty row for the matrix
        mtx.append([])

        # Loop through columns
        for y in range(0, len(domain)):
            # If the pair is in the set
            if (domain[x],domain[y]) in set:
                # then we want to put a 1 in the matrix at this row and column
                mtx[x].append(1)
            else:
                # If it is not in the set then we want to put a 0 in this row and column
                mtx[x].append(0)
    # If we wanted t o print the new matrix out, we could use the same line we used in the transpose function
    # print(str(mtx).replace("]," , "]\n"))
    return mtx

# This function takes a relation in the form of a set of ordered pairs and the domain of the relation on the set. It uses the helper functions "transitive" and "transitiveClosure" to tell the user if the set is transitive and if it is not, tell the user what the transitive closure is.
def transitivity(set, domain):
    # Part a says to print the relation out.
    # Note that end="" allows us to not print a new line after print() which is the default behavior
    print("R = ", end="")
    # This prints out the actual relation. sep="" allows python to separate each ordered pair with a comma.
    print(set, sep=",")

    # Call the transitive function and store the boolean result
    isTransitive = transitive(set)
    # If the given relation is not transitive then we want to find the closure
    if (not isTransitive):
        # Tell the user what the closure is
        print("The closure is", end="")
        # Get the relation into matrix form
        matrixOfR = relationToMatrix(set, domain)
        # Find the transitive closure
        transitiveClosure(matrixOfR)
        # Label the transitive closure as R*
        print("= R*")
    # Print a new line to make our output clean
    print("")

# Tell the user what problem is being executed
print("3d)")
# Initialize the relation and domain of the relation
R = {(a,b), (d,d), (b,c), (a,c)}
domain = [a,b,c,d]
# Call the main function that handles the transitivity of the relation
transitivity(R, domain)

# Tell the user what problem is being executed
print("3e)")
# Initialize the relation and domain of the relation
R = {(1,1), (1,3), (2,2), (3,1), (3,2)}
domain = [1,2,3]
# Call the main function that handles the transitivity of the relation
transitivity(R, domain)

# 4. Write code that determines if a relation (R) of ordered pairs is an equivalence relation or not and the reason why.

# This function takes a relation in the form of a set of ordered pairs.
# It also takes the domain of the set.
# It then performs the reflexve, symmetric, and transitive tests to determine if the relation is an equivalence.
# It will output its results
def equivalence(set, domain):
    # Run reflexive, symmetric, and transitive tests and store their respective results
    isRef = reflexive(set, domain)
    isSym = symmetric(set)
    isTrans = transitive(set)
    # If any of the tests fail, the relation is not an equivalence relation
    if((not isRef) or (not isSym) or (not isTrans)):
        # Print a nice message for the user giving a breakdown of where exactly the relation failed the equivalence test.
        print("Not an equivalence relation because at least one of the following is false:")
        print("Reflexive: " + str(isRef))
        print("Symmetric: " + str(isSym))
        print("Transitive: " + str(isTrans))
        # The relation is not an equivalence so we return False
        return False
    else:
        # Otherwise the relation is an equivalence relation
        # Let the user know the relation passed
        print("It is an equivalence relation because it is reflexive, symmetric, and transitive.")
        # Return True because the relation is an equivalence
        return True

# This function takes a relation in the form of a set of ordered pairs and the domain of the relation on the set. It uses the helper functions "equivalence" to tell the user if the relation is an equivalence.
# This function does not do the heavy lifting of determining if a relation is an equivalence. Rather, it handles printing out the relation and calling equivalence() which DOES do the actual calculations.
def equivalency(set, domain):
    # Part a says to print the relation out.
    # Note that end="" allows us to not print a new line after print() which is the default behavior
    print("R = ", end="")
    # This prints out the actual relation. sep="" allows python to separate each ordered pair with a comma.
    print(set, sep=",")

    # Call the equivalence function and store the boolean result
    equivalence(set, domain)

    # Print a new line to make our output clean
    print("")

# Tell the user what problem is being executed
print("4d)")
# Initialize the relation and domain of the relation
R = {(1,1),(2,2),(2,3)}
domain = [1,2,3]
# Call the main function that handles the equivalency of the relation
equivalency(R, domain)

# Tell the user what problem is being executed
print("4e)")
# Initialize the relation and domain of the relation
R = {(a,a), (b,b), (c,c), (b,c), (c,b)}
domain = [a,b,c]
# Call the main function that handles the equivalency of the relation
equivalency(R, domain)

# This antisymmetric function comes directly from my assignment 3
# Make a function that takes a relation in the form of a set of ordered pairs
# Returns true if the relation is antisymmetric
# Returns false if the relation is not antisymmetric
def antisymmetric(set):
    # Loop through each (a,b) in the given set
    for pair in set:
        # Pull out the a and b from the ordered pair
        a = pair[0]
        b = pair[1]
        # Check if (b,a) is in the set. If it is then the set cannot be antisymmetric
        if (b,a) in set and a != b:
            # Let the user know the set is not antisymmetric
            print(f"Not antisymmetric because there exists {pair} for which ({b},{a}) is also in the set")
            # Return False because the set is not antisymmetric
            return False
    # Every (b,a) was tested and passed so the set must be antisymmetric by exhaustion
    # Let the user know it is antisymmetric
    print("Antisymmetric because for every (a,b) in the set, (b,a) is not in the set")
    # Return true because the set is antisymmetric
    return True

# 5. Write code that determines if a relation (R) of ordered pairs is a poset of the set (S) or not and the reason why.

# R and S form a partial ordering, or partial order, or poset iff R is reflexive, antisymmetric, and transitive
# This function takes a relation in the form of a set of ordered pairs, and a domain which is the set of value the relation is over.
# It then runs three tests to determine if the given relation and domain form a poset.
def poset(relation, domain):
    # Run reflexive, antisymmetric, and transitive tests and store their respective results
    isRef = reflexive(relation, domain)
    isAntiSym = antisymmetric(relation)
    isTrans = transitive(relation)
    # If any of the tests fail, the relation is not a Poset
    if((not isRef) or (not isAntiSym) or (not isTrans)):
        # Print a nice message for the user giving a breakdown of where exactly the relation and set failed the poset test.
        print("Not a Poset relation because at least one of the following is false:")
        print("Reflexive: " + str(isRef))
        print("Antisymmetric: " + str(isAntiSym))
        print("Transitive: " + str(isTrans))
        # The relation and set are not a poset so we return False
        return False
    else:
        # Otherwise the relation and set are a poset
        # Let the user know the relation and set passed
        print("It is a poset relation because it is reflexive, antisymmetric, and transitive on the set.")
        # Return True because the relation and set form a poset
        return True

# This function takes a relation in the form of a set of ordered pairs and the domain of the relation on the set. It uses the helper function "poset" to tell the user if the relation and domaain form a poset.
# This function does not do the heavy lifting of determining if a relation and set form a poset. Rather, it handles printing out the relation and calling poset() which DOES do the actual calculations.
def posetivity(R, S):
    # Part a says to print the relation out.
    # Note that end="" allows us to not print a new line after print() which is the default behavior
    print("R = ", end="")
    # This prints out the actual relation. sep="" allows python to separate each ordered pair with a comma.
    print(R, sep=",")

    # Call the poset function and store the boolean result
    poset(R, S)

    # Print a new line to make our output clean
    print("")

# Tell the user what problem is being executed
print("5e)")
# Initialize the relation and domain of the relation
R = {(1,1), (1,2), (2,2), (3,3), (4,1), (4,2), (4,4)}
domain = [1, 2, 3, 4]
# Call the main function that handles the transitivity of the relation
posetivity(R, domain)

# Tell the user what problem is being executed
print("5f)")
# Initialize the relation and domain of the relation
R = {(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 2), (3, 3)}
domain = [0, 1, 2, 3]
# Call the main function that handles the transitivity of the relation
posetivity(R, domain)
