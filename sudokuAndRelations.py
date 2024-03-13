'''
Program Name: EECS 210 Assignment 5
Description: This program has two parts. Part 1 concerns functions/relations and some of their properties. Part 2 concerns solving sudoku puzzles using brute force recursive methods.
Inputs:
    - A main menu offers users the selection between part 1 and part 2.
    - In part 1, the user is able to choose between a and j.
        - Options a-i represent test cases given in the program instructions.
        - Option j allows the user to enter their own A, B, and f representing 2 sets and a relation.
    - In part 2, the user is able to choose between 1 to 5 sudoku puzzles to be solved.
    - If invalid input is entered, the program will back out into the previous menu. If invalid input is entered on the main menu, the program will quit.
Output:
    - The main menu and its options are displayed for the user when the program is first run.
    - When Part 1 is selected, the available relations are displayed for the user to select from.
        - When an option is selected, A and B will be printed in Set notation. And f will be printed in Set notation as a set of ordered pairs.
        - Certain properties will be displayed regarding the option chosen. It will always be shown if the relation is a function or not.
            - If the relation is a function, then it will be shown if the function is injective, surjective, or bijective.
                - If the relation is bijective, then the inverse function will be displayed.
    - When Part 2 is selected, the menu showing the available sudoku puzzles is printed out.
        - When a user selects a puzzle, the name of the puzzle will be printed to the screen
        - If the puzzle has a solution, it will be printed to the screen.
        - The puzzle and its solution is formatted to look as close to how it would look on paper as possible. In other words, there are lines between each column and row. However there are not darker/thicker lines between each 3x3 box.
        - If there is no solution to the puzzle, the user will be informed with a message.
Collaborators: none
Other sources: The isSafe and solveSudoku functions come from https://www.geeksforgeeks.org/sudoku-backtracking-7/
Author: Katie N github.com/Katie-N/
Creation Date: 3/11/2024
'''

# --------------------Part 1-----------------------#
# All of this code is my own.

# Initialize variables with their corresponding values for use in ordered pairs in part 1.
a = "a"
b = "b"
c = "c"
d = "d"
v = "v"
w = "w"
x = "x"
y = "y"
z = "z"

# A relation is one to one iff for every element c in f(a) = c, there is a unique a that produces c
def isOneToOne(f):
    # Create a list to keep track of all of the a's we have seen in f.
    listOfa = []
    # Loop through every ordered pair in the relation
    for pair in f:
        # Pull out the first value in the ordered pair
        a = pair[0]
        # Check if the value is already in our list of a's in f
        if a in listOfa:
            # If the value is already in the list then we have found a duplicate entry
            # Meaning, there is more than one a that produces c in f which fails the definition of a one-to-one relation
            return False
        # Otherwise, the value is not yet in the list and we should add it
        else:
            listOfa.append(a)
    # At this point we have looped through every pair in f and have not found any different a's maping to the same c.
    # This means every different a must map to a different c which is the definition of a one-to-one relation so we return True.
    return True

# A relation is onto iff for every element b in B, there is an element a in A s.t. f(a) = b
# isOnto Takes in 1 sets, B, and a set of ordered pairs representing a relation, f.
# It returns True if the relation is onto according to the definition above. Returns False otherwise.
def isOnto(B, f):
    # Loop through every value in B
    for b in B:
        # Initialize a temporary variable that stores if the current value of b is in f
        # Initialize bInF with False and then toggle it if we do find b in f
        bInF = False
        # Loop through each pair in the relation f
        for pair in f:
            # Compare the second element in the pair with the current value of b.
            if pair[1] == b:
                # If the second element matches then we need to set the bInF variable accordingly.
                bInF = True
                # We only need one instance of (?,b) in f so we can break the loop now that we've found one.
                break;
        # At this point, we have looped through every pair in f
        # If bInF still is False then we know we did not find an occurrence of (?,b) for at least one b in f
        if (not bInF):
            # Return False because it is not onto as there exists a b for which there are no (?, b) in f
            return False
    # If we made it to this point then the if (not bInF) never got executed
    # and for every b in B, there exists and f(a) = b where a is in A
    return True

# This function takes in the codomain and the relation in the form of a set or ordered pairs and returns true if it is bijective and false otherwise.
# A relation is bijective if it is both injective and surjective
# Note that injective = one-to-one and surjective = onto
def isBijective(B, f):
    # Check if both injective and surjective
    if (isOneToOne(f) and isOnto(B,f)):
        # The function is bijective
        return True
    else:
        # The function is not bijective
        return False

# This function takes in 1 set, A, and a set of ordered pairs representing a relation, f
# It returns True if the relation forms a function. Returns False otherwise.
# To be a function every a in A must map to exactly 1 valid b in B and (a,b) must be present in f
def isFunction(A, f):
    for a in A:
        aInF = False
        for pair in f:
            if pair[0] == a:
                if (aInF):
                    # We have already found a pair in f with (a, b1)
                    # Since we just found a second pair in f with (a, b2), it cannot be a function
                    # as every a in A must map to exactly one b value.
                    return False
                # Since we did not return in the check above, we know this is the first pair found with a so we set it true
                aInF = True
                # Note we do not break the loop because we want to check every value of a
        # After looping through each pair in f, if there is no pair with (a, ?) then it cannot be a function as every a in A must be present in f
        if (not aInF):
            return False
        # Otherwise, continue looping with the next value in A
    # If we make it all the way to this point then we have a valid function because every a in A is present in f exactly once
    return True

# This function is the main handler for part 1 of assignment 5
# It takes in 2 sets, A and B, and a set of ordered pairs representing a relation, f
# Output: Prints out A, B, and f in set notation.
def part1(A, B, f):
    print("\n\tA = " + str(A))
    print("\tB = " + str(B))
    print("\tf = " + str(f))
    isFunc = isFunction(A, f)
    print("\tIs Function: " + str(isFunc))

    if (isFunc):
        # Note that injective and one-to-one are synonymous
        print("\tIs injective: " + str(isOneToOne(f)))
        # Note that surjective and onto are synonymous
        print("\tIs surjective: " + str(isOnto(B, f)))
        print("\tIs bijective: " + str(isBijective(B, f)))

        if (isBijective(B, f)):
            # The inverse of f = {(a,b)} is f' = {(b,a)}
            # We will reverse every ordered pair using a simple list comprehension
            inverseList = [(b, a) for a, b in f]
            # Then convert the list to a set
            invf = set(inverseList)

            # Let the user know what the inverse function is
            print("\t\tInverse of f: ")
            print("\t\tA' = " + str(B))
            print("\t\tB' = " + str(A))
            print("\t\tf' = " + str(invf))

# Here are all of the options available to the user in part 1.
# I preconfigured test cases (a) through (i) so they are easy to test without reentering the functions and relations each time.
part1Options = [
"\ta. A = {a,b,c,d},\tB = {v,w,x,y,z},\tf = {(a,z),(b,y),(c,x),(d,w)}",
"\tb. A = {a,b,c,d},\tB = {x,y,z},    \tf = {(a,z),(b,y),(c,x),(d,z)}",
"\tc. A = {a,b,c,d},\tB = {w,x,y,z},  \tf = {(a,z),(b,y),(c,x),(d,w)}",
"\td. A = {a,b,c,d},\tB = {1,2,3,4,5},\tf = {(a,4),(b,5),(c,1),(d,3)}",
"\te. A = {a,b,c},  \tB = {1,2,3,4},  \tf = {(a,3),(b,4),(c,1)}",
"\tf. A = {a,b,c,d},\tB = {1,2,3},    \tf = {(a,2),(b,1),(c,3),(d,2)}",
"\tg. A = {a,b,c,d},\tB = {1,2,3,4},  \tf = {(a,4),(b,1),(c,3),(d,2)}",
"\th. A = {a,b,c,d},\tB = {1,2,3,4},  \tf = {(a,2),(b,1),(c,2),(d,3)}",
"\ti. A = {a,b,c},  \tB = {1,2,3,4},  \tf = {(a,2),(b,1),(a,4),(c,3)}",
# If the user wants to enter their own A, B, and f, they can choose option j
"\tj. Custom",
# If the user wants to quit then they can enter anything other than the above options
"\tEnter anything else to return to main menu"]
# This is a list of all of the valud options available in part 1.
# If the user enters something that is not in this list, the program will back out to the main menu.
part1ValidOptions = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]



# --------------------Part 2-----------------------#
# All of the code is my own except for the functions isSafe and solveSudoku
# For those two functions I extensively commented all of the code to exhibit my understanding.

# puzzle1 through puzzle5 are arrays of arrays representing each sudoku matrix.
# They are read from left to right as rows and the top to bottom as columns.
# I have aligned them as they are read in a sudoku grid.
# Because valid entries in sudoku go from 1 to 9, I will use 0s to represent the empty slots.
puzzle1 = [
[5, 0, 0, 0, 0, 0, 1, 7, 0],
[1, 0, 6, 5, 0, 9, 0, 4, 0],
[4, 7, 2, 1, 0, 6, 0, 0, 0],
[9, 0, 0, 0, 0, 0, 5, 0, 0],
[0, 1, 8, 0, 9, 5, 4, 0, 0],
[6, 0, 0, 4, 0, 2, 3, 8, 9],
[0, 4, 0, 0, 0, 0, 9, 3, 0],
[0, 9, 0, 7, 0, 3, 0, 5, 0],
[2, 6, 3, 9, 5, 8, 7, 1, 4]]

puzzle2 = [
[5, 3, 0, 8, 0, 4, 0, 7, 6],
[1, 0, 6, 0, 7, 9, 0, 4, 3],
[0, 7, 0, 0, 3, 6, 0, 0, 5],
[9, 2, 4, 0, 8, 0, 5, 6, 0],
[3, 0, 8, 6, 9, 0, 4, 2, 7],
[0, 5, 0, 4, 1, 2, 3, 0, 0],
[7, 4, 5, 0, 6, 0, 9, 0, 8],
[8, 0, 1, 7, 0, 3, 6, 5, 2],
[0, 6, 3, 9, 5, 0, 7, 0, 4]]

puzzle3 = [
[7, 0, 0, 3, 0, 6, 0, 4, 0],
[3, 4, 0, 5, 0, 9, 6, 0, 8],
[6, 1, 9, 8, 0, 7, 5, 2, 3],
[4, 9, 0, 0, 8, 5, 0, 0, 7],
[1, 2, 0, 0, 0, 0, 3, 6, 5],
[0, 7, 6, 0, 3, 0, 8, 0, 0],
[2, 0, 1, 4, 9, 0, 0, 0, 6],
[0, 3, 0, 2, 0, 8, 4, 0, 1],
[8, 6, 4, 7, 0, 0, 9, 3, 2]]

puzzle4 = [
[7, 3, 2, 0, 8, 4, 6, 9, 1],
[9, 1, 0, 3, 0, 0, 5, 2, 0],
[8, 0, 0, 9, 0, 2, 7, 3, 4],
[5, 4, 9, 0, 0, 0, 8, 6, 3],
[1, 0, 0, 0, 3, 0, 2, 0, 7],
[0, 2, 3, 0, 4, 8, 9, 1, 0],
[3, 9, 0, 8, 5, 0, 4, 7, 2],
[0, 7, 0, 4, 0, 3, 0, 0, 6],
[4, 6, 8, 0, 7, 0, 0, 5, 9]]

puzzle5 = [
[0, 0, 0, 0, 0, 4, 2, 0, 1],
[0, 0, 0, 0, 7, 0, 0, 0, 5],
[0, 0, 8, 1, 0, 5, 7, 0, 0],
[0, 4, 1, 0, 3, 2, 8, 0, 0],
[3, 8, 9, 0, 5, 6, 1, 2, 7],
[2, 0, 0, 0, 0, 8, 3, 0, 0],
[0, 2, 4, 0, 0, 7, 0, 1, 0],
[8, 3, 6, 0, 9, 0, 4, 0, 0],
[0, 0, 7, 0, 0, 3, 5, 0, 0]]

# Make a list of all of the puzzles
part2Options = [puzzle1, puzzle2, puzzle3, puzzle4, puzzle5]

# This function takes a sudoku grid and prints it for the user to see.
# I made this function
# The puzzle should be given in the form of an array of arrays where each subarray is a row.
def printPuzzle(puzzle):
    # Loop through each row in the puzzle
    for row in range(9):
        # Print out a line to separate each row
        print("-—" * 18)
        # Loop through each column in the puzzle
        for col in range(9):
            # Print each entry in the sudoku puzzle
            # end = " | " is a separator that goes between each entry
            print(puzzle[row][col], end = " | ")
        # Print a new line after the entire row has been printed out.
        print()
    # This prints off a final line at the bottom of the puzzle.
    print("-—" * 18)


# The isSafe function comes from https://www.geeksforgeeks.org/sudoku-backtracking-7/
# The comments are my own.
# This function takes in a puzzle, a row, a column, and a number between 1 and 9
# It checks if num can be put in the given space in the puzzle. The given space is determined by the intersection of the column and the row.
# Returns a boolean value. True if the number can be put in the spot and False if the number cannot.
def isSafe(grid, row, col, num):
    # Loop through all columns
    for x in range(9):
        # Check if the number is already in the given row
        if grid[row][x] == num:
            # The number is already present so we can't put it in this row
            # Therefore this placement is invalid and we should return False
            return False
    # At this point, we haven't returned yet so there must not be a conflict in the row

    # Loop through all rows
    for x in range(9):
        # Check if the number is already in the given column
        if grid[x][col] == num:
            # The number is already present so we can't put it in this column
            # Therefore this placement is invalid and we should return False
            return False
    # At this point, we haven't returned yet so there must not be a conflict in the column

    # The last thing to check is if the number is already in the 3x3 box
    # We can loop through all 9 squares in the box by having both a dynamic row and dynamic column.
    # We need to know what row and column to start at. In other words, we need to know the upper left square of the 3x3 box.
    # To get the row we can take the current row we are looking at and subtract the remainder from dividing the row by 3. This makes sure we are in the top row of our box.
    # To get the column we take the current column we are looking at and subtract the remainder from dividing the column by 3. This makes sure we are in the left column of our box.
    # For instance, if we are currently looking at filling in the cell marked with _ (row 2 column 6 using zero-indexing)
    # ? ? ? ? ? ? ? ? ?
    # ? ? ? ? ? ? ? ? ?
    # ? ? ? ? ? ? _ ? ?
    # ? ? ? ? ? ? ? ? ?
    # ? ? ? ? ? ? ? ? ?
    # ? ? ? ? ? ? ? ? ?
    # ? ? ? ? ? ? ? ? ?
    # ? ? ? ? ? ? ? ? ?
    # ? ? ? ? ? ? ? ? ?
    # startRow = 2 - 2 % 3 = 2 - 2 = 0 (zero-based index)
    # startCol = 6 - 6 % 3 = 6 - 0 = 6 (zero-based index)
    # Then | marks the upper left cell of the 3x3 box:
    # ? ? ? ? ? ? | ? ?
    # ? ? ? ? ? ? ? ? ?
    # ? ? ? ? ? ? _ ? ?
    # ? ? ? ? ? ? ? ? ?
    # ? ? ? ? ? ? ? ? ?
    # ? ? ? ? ? ? ? ? ?
    # ? ? ? ? ? ? ? ? ?
    # ? ? ? ? ? ? ? ? ?
    # ? ? ? ? ? ? ? ? ?
    # We can see this is what we expect. Similar logic follows for every other cell.
    startRow = row - row % 3
    startCol = col - col % 3
    # Loop through 3 rows
    for i in range(3):
        # Loop through 3 columns
        for j in range(3):
            # Check if any cell contains num (the number we are trying to place)
            # startRow offsets i by the number of rows until the 3x3 box
            # startCol offsets j by the number of columns until the 3x3 box
            if grid[i + startRow][j + startCol] == num:
                # If the cell contains num already then the placement of num is invalid and we should return False
                return False
    # If we make it to this point, we have passed all three checks
    # (num in row, num in column, and num in box) and the placement is
    # valid so we return True
    return True

# solveSudoku is a function that comes from https://www.geeksforgeeks.org/sudoku-backtracking-7/
# The comments are my own.
# The function takes a sudoku puzzle in the form of an array of arrays.
# Each array is a row. Each elemnent in the row is in a successive column.
# 0s are expected for the cells that need to be filled in.
# It also takes a row and column value. The cell at the given row and column is the current number being solved for.
# This function solves one cell at a time and recursively calls itself to solve each cell until all cells have been filled in with a valid number.
# To be a valid solution there may be no duplicate numbers in any row, column, or 3x3 box. The only valid numbers are 1-9
# This uses a depth-first search with backtrackin. All possible entries are tried and therefore this method is exhaustive.
def solveSudoku(grid, row=0, col=0):
    # This function scans the cells from left to right, top to bottom.
    # So I set the default values of row and col to 0

    # Here is a base case. This is a base case because it is a terminating case.
    # If the given column goes out of bounds on the
    # last row then we know we have finished all of the puzzle without errors.
    # (Note that 9 is out of bounds because the row array is zero indexed
    # and contains 9 elements leading to the last valid row and col being 8 not 9.)
    if (row == 8 and col == 9):
        return True

    # If col has reached 9, and we are not on the last row
    # (as the if statement above already checked for)
    # then we need to increment the row and reset col to 0 before continuing
    if col == 9:
        # go to the next row
        row += 1
        # start at the first element
        col = 0

    # Because we use 0s to determine empty cells,
    # we can check if the number in the current cell is greater than 0
    # and if it is, we know this cell is not empty and we should move on.
    if grid[row][col] > 0:
        # Recursively call this function and pass it the coordinates of the next cell to the right
        return solveSudoku(grid, row, col + 1)

    # Loop through the numbers 1-9 and assign each value to the variable num
    for num in range(1, 10):
        # First we must check if the given num is allowed to be placed in the desired row and col.
        if isSafe(grid, row, col, num):

            # At this point we know the number can go in the row and column
            # without breaking any rules so let's assume
            # this is the correct place for the number
            grid[row][col] = num

            # Continue solving the puzzle recursively by moving to the cell on the right
            if solveSudoku(grid, row, col + 1):
                # If we were able to continue all the way down and find a
                # valid number in every cell given we put the number above
                # in the current cell, then this must be a valid solution to
                # the puzzle and we should return True
                return True

        # If we did not return True already then the placement is invalid
        # and we should erase the cell by setting it back to 0
        grid[row][col] = 0

        # The loop will continue and the next number in 1-9 will be tested

    # If we get to this point then we have looped through every possible
    # number for every possible cell and there are no valid solutions
    # The given puzzle is unsolvable so we return False.
    return False

# --------------------Main Menu-----------------------#
# All of this code is my own.

# Print out the main menu
print("OPTIONS:")
print("1. Functions and Relations\n2. Sudoku\nAnything else to quit")
# Get the user's choice
opt = input("Choose option: ")

# Continue computation until an invalid option is entered
while((opt == "1") or (opt == "2")):
    # If the user chooses option 1 then execute the functionality of Part 1 of the program.
    if(opt == "1"):
        # Print out all of the preconfigured options available for Part 1
        print("\nFunctions and Relations")
        print("\tOPTIONS:")
        for option in part1Options:
            print(option)
        opt1 = input("\tChoose option: ")

        # Continue getting choices from the user until they enter an invalid option
        while (opt1 in part1ValidOptions):
            # Assign the sets A and B, and the relation f, according to the user's choice
            # Then call the main handler for part 1 of assignment 5 passing it the newly defined A, B, and f
            if (opt1 == "a"):
                A = {a,b,c,d}
                B = {v,w,x,y,z}
                f = {(a,z),(b,y),(c,x),(d,w)}
                part1(A, B, f)
            elif (opt1 == "b"):
                A = {a,b,c,d}
                B = {x,y,z}
                f = {(a,z),(b,y),(c,x),(d,z)}
                part1(A, B, f)
            elif (opt1 == "c"):
                A = {a,b,c,d}
                B = {w,x,y,z}
                f = {(a,z),(b,y),(c,x),(d,w)}
                part1(A, B, f)
            elif (opt1 == "d"):
                A = {a,b,c,d}
                B = {1,2,3,4,5}
                f = {(a,4),(b,5),(c,1),(d,3)}
                part1(A, B, f)
            elif (opt1 == "e"):
                A = {a,b,c}
                B = {1,2,3,4}
                f = {(a,3),(b,4),(c,1)}
                part1(A, B, f)
            elif (opt1 == "f"):
                A = {a,b,c,d}
                B = {1,2,3}
                f = {(a,2),(b,1),(c,3),(d,2)}
                part1(A, B, f)
            elif (opt1 == "g"):
                A = {a,b,c,d}
                B = {1,2,3,4}
                f = {(a,4),(b,1),(c,3),(d,2)}
                part1(A, B, f)
            elif (opt1 == "h"):
                A = {a,b,c,d}
                B = {1,2,3,4}
                f = {(a,2),(b,1),(c,2),(d,3)}
                part1(A, B, f)
            elif (opt1 == "i"):
                A = {a,b,c}
                B = {1,2,3,4}
                f = {(a,2),(b,1),(a,4),(c,3)}
                part1(A, B, f)
            elif (opt1 == "j"):
                # Get custom input for A, B, and f

                # Get A from user
                stringA = input("Enter elements in A separated by commas. Ex: 'a1,a2,a3'\nA = set: ")
                # Remove all whitespace from the string (replace)
                # Split the string by commas into elements in a list (split)
                # and convert the list into a set (set)
                A = set(stringA.replace(" ", "").split(","))

                # Get B from user
                stringB = input("Enter elements in B separated by commas. Ex: 'b1,b2,b3'\nB = set: ")
                # Remove all whitespace from the string (replace)
                # Split the string by commas into elements in a list (split)
                # and convert the list into a set (set)
                B = set(stringB.replace(" ", "").split(","))

                # Get f from user
                stringf = input("Enter ordered pairs in f separated by commas. Ex: '(a,b),(c,d)'\nf = set: ")
                # Remove all whitespace
                stringf = stringf.replace(" ", "")

                # Split up each ordered pair
                listf = stringf.split("),(")

                # Initialize f as an empty set
                f = set()

                # Loop through each string representing an ordered pair
                for item in listf:
                    # Remove the first opening parentheses and last closing parentheses
                    item = item.replace("(", "")
                    item = item.replace(")", "")

                    # Split each string representation of an ordered pair into a list of 2 strings.
                    # So this goes from item = "a,b" to ab = ["a","b"]
                    ab = item.split(",")

                    # Lists are ordered and tuples are ordered so we don't risk messing up the order of a and b in the ordered pair

                    # Now that we have broken down the string into one
                    # ordered pair and then into a list of 2 elements,
                    # we can convert it to a tuple and add it to the f set
                    f.add(tuple(ab))

                part1(A, B, f)

            # Print out all of the preconfigured options available
            print("\nFunctions and Relations")
            print("\tOPTIONS:")
            # Loop through all options and print them out for the user
            for option in part1Options:
                print(option)
            # Prompt the user to choose one
            opt1 = input("\tChoose option: ")
    else:
        # Print out all of the preconfigured options available for Part 2
        print("Sudoku")
        print("\tOPTIONS:")
        # Loop through all puzzles and print them out for the user
        for i in range(0, len(part2Options)):
            # To print the options with the normal convention of starting at 1, we add 1 to i which starts at 0
            print("\tPuzzle" + str(i + 1) + ".txt ")
            # Print out each puzzle using the helper function I made
            printPuzzle(part2Options[i])
        # Prompt the user to choose one
        opt2 = input("Choose Puzzle:\n(Valid choices are between 1 and 5): ")
        # Check if we can convert opt2 to an integer
        if opt2.isdigit():
            # opt2 is a string so we convert it to an integer and subtract by 1 to get back to 0-indexing
            puzzleNum = int(opt2) - 1

        # Continue getting choices from the user until they enter an invalid option
        # Valid choices are from 0 to 4 so the user can enter a number between 1 and 5
        # If the string entered is not an integer then we know the user wants to quit this menu
        while (opt2.isdigit() and puzzleNum in range(0,5)):
            # Print out which puzzle is being solved
            print("\tPuzzle" + str(puzzleNum + 1) + ".txt Solution")

            # Call the solveSudoku function to solve the puzzle.
            # part2Options is a list of all of the preconfigured puzzles
            # Note we could also include the arguments 0, 0  for row and col.
            # But we don't have to because I made those the default values for row and col
            if solveSudoku(part2Options[puzzleNum]):
                # The puzzle was able to be solved
                # Print the newly solved puzzle using the printPuzzle helper function
                printPuzzle(part2Options[puzzleNum])
                print()
            else:
                # The puzzle was unable to be solved
                print("No solution found\n")
            # Since the puzzles are very long, I will skip printing them out
            # after each choice and allow the user to just scroll up
            # to view the options if needed.
            opt2 = input("Choose Puzzle:\n(Valid choices are between 1 and 5): ")

            # Check if we can convert opt2 to an integer
            if opt2.isdigit():
                # opt2 is a string so we convert it to an integer and subtract by 1 to get back to 0-indexing
                puzzleNum = int(opt2) - 1
    # Get new choice on main menu
    print("\nOPTIONS:")
    print("1. Functions\n2. Sudoku\nAnything else to quit")
    opt = input("Choose option: ")
