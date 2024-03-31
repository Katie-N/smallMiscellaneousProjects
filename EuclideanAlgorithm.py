'''
Program Name: EECS 210 Assignment 6
Description:
Inputs: None
Output:
Collaborators: none
Other sources:
Author: Katie
Creation Date: 3/29/2024
'''

# -----------PART 1-----------
# 1. Calculate the Greatest Common Divisor using the Euclidean Algorithm
# The Euclidean Algorithm easily translates into Python as:
def gcdRemainder(a, b):
    # The algorithm only works properly if it divides the larger value and not the smaller value.
    # So we get copies of the values and put them into x and y based on their size
    x = max(a,b)
    y = min(a,b)
    # We need a way to output which step we are on so i will keep track of the number of loops
    i = 1
    # Loop until y (which will be the remainder) is 0
    while y != 0:
        # Get the remainder by utilizing the modulo operator
        r = x % y
        # 2. Show each step of the Euclidean Algorithm using the “remainder” format.
        # Note that // is the integer division operator in Python
        # It floors the division result to the nearest integer
        print(f"Step {i}. {x}/{y} = {x//y} R {r}")
        # Now we want to transfer the value of y into x
        x = y
        # Transfer the value of the remainder into y
        y = r
        # Increment the count
        i += 1
    # 3. Display the final results as: "gcd(a,b) = n"
    print(f"gcd({a}, {b}) = {x}")
    # x now contains the GCD so we should return it
    return x

# 4. Test with the following inputs:
# Tell the user which part is being evaluated
print("Part 1")
# 4a.
print("a) gcd(414, 662)")
gcdRemainder(414, 662)
# 4b.
print("\nb) gcd(6, 14)")
gcdRemainder(6, 14)
# 4c.
print("\nc) gcd(24, 36)")
gcdRemainder(24, 36)
# 4d.
print("\nd) gcd(12, 42)")
gcdRemainder(12, 42)
# 4e.
print("\ne) gcd(252, 198)")
gcdRemainder(252, 198)

# -----------PART 2-----------

# To understand algebraically how this function should work,
# let's examine the first step in the backwards process.
# One form of the euclidean algorithm is x = y * x//y + r
# To solve for r we get r = x - (x//y)*y
# Move backwards
# xValues = [252, 198, 54, 36]
# yValues = [198, 54, 36, 18]
# rValues = [54, 36, 18, 0]
# 18 = 54 − 1 * 36 -->
# rValues[-2] = xValues[-2] - xValues[-2]//yValues[-2] * yValues[-2]

# 1. Express gcd(a, b) as a linear combination: gcd(a, b) = sa + tb,
# where s and t are Bézout coefficients of a and b, using the Euclidean Algorithm (Method 1).
# This function takes a list of x values, y values, and r values created from doing a forward pass through the Euclidean algorithm
def bezout(xList, yList, rList):
    # If the expression is already in a form where we see the value of y then we don't need to separate any terms. Set i = -1 so the while loop is skipped
    if (yList[0] == xList[-1]): i = -1
    # If the expression is not in a form where we see the value of y then we need to separate the terms until we can pull out x and y. Set i = -2 so the while loop starts on the second to last step from the forward pass)
    else: i = -2

    # yco stands for y coefficient.
    # It keeps track of the multiplier in the second term.
    # We initialize it to xList[i] where xList[i] is the value of the numerator on the left side in the ith Euclidean step.
    yco = xList[i]
    # separateTerms holds the values of the coefficients.
    # In the first while loop it holds each yco value.
    # In the second while loop later on, it holds each xco value.
    separateTerms = []
    # Initialize toCombineWithX and toCombineWithY so we can use them outside the loops
    # These variables will store the values that we take out of the other terms so we can later add them back in and maintain the validity of the equation
    toCombineWithX = 0
    toCombineWithY = 0
    # b1Mults is a list of all of the multipliers applied to the second term.
    # We keep track of them so we can divide and multiply by them later to maintain the validity of the equation.
    b1Mults = []

    # Loop until we find the coefficient of y that equals min(a,b) (where a and b come from the function call gcd(a,b))
    while yco != yList[0]:
        # We want to initialize the x multiplier with 1 since x and y start fully simplified  and we must break them down into factors.
        multipleOfX = 1
        # Update the y coefficient with the new decremented value of i
        yco = xList[i]
        # Add the new coefficient to the list of terms
        separateTerms.append(yco)
        # Calculate the piece that will be combined with x after we finish factoring y
            # xList[i]//yList[i] gives the floored value of the fraction on the left side in the ith Euclidean step
            # * yList[i] multiplies the fraction by the current y value
            # - because the term is subtracted algebraically
        toCombineWithX = - (xList[i]//yList[i]) * yList[i]
        # Make a string with the value of the left term and the right term
        yBreakDown = ""
        # Print the terms outside the nested parentheses
        for j in range(len(separateTerms)):
            # The string should contain each separated term.
            # This if statement prints the left term
            if j == 0:
                # On the very first term we want to show the term is simplified and only multiplied by 1
                yBreakDown += f"1*{separateTerms[j]} "
            else:
                # On subsequent left terms, we don't want to expand the number to show it is being multiplied by 1. That is already clear. So we just print the term itself.
                yBreakDown += f"{separateTerms[j]} "

            # If we are not on the last term then we want to print the opening parentheses for the next term
            if j != (len(separateTerms) - 1):
                yBreakDown += f"{b1Mults[j]}*("

        # bMult1 is a variable to store the left number to be multiplied.
        # It tells us how many times we multiply bMult2 which is a special number in the list of y values
        bMult1 = toCombineWithX//yList[i]
        # We want to keep track of all of the left numbers we multiply by so we add bMult1 to our list of b1Mults
        b1Mults.append(bMult1)

        # bMult2 is a variable to store the right number being multiplied.
        # This is the second term found in the ith euclidean algorithm.
        bMult2 = yList[i]

        # Continue adding to the string by appending the rightmost term
            # ")"*(len(separateTerms)-1) allows us to add the correct number of closing parentheses.
            # There should be one less closing parentheses as there are terms in the separateTerms array.
            # * is an overloaded operator in Python and when given a string,
            # it will repeat the string the given number of times.
        yBreakDown += f"{bMult1}*{bMult2}" + ")"*(len(separateTerms)-1)
        # print the string showing how y factors
        # rList[-2] gives the second to last remainder
        # (In other words, it is the remainder right before r = 0 which always occurs at rList[-1])
        print(f"{rList[-2]} = {yBreakDown}")

        # Decrement i so the previous equation in the Euclidean algorithm will be used in the next run
        i -= 1

    # yToBeCombinedWith stores the value of the second term in the parentheses multiplied by the coefficient outside the parentheses
    yToBeCombinedWith = - yco * (xList[-2]//yList[-2])
    # baseX combines the first term with the remaining terms (except for the yco*floor(a*b) term)
    baseX = xList[-2] - toCombineWithX
    # Now that we have combined everything we can from the second term with the first term, we can find s by dividing the combined term and a
    s = baseX // xList[-2]

    # Separate the two terms into the form a*b + c*d
    # We use the index -2 in xList[-2] because we haven't separated the first term into xList[0]*something yet
    xMultiplier = baseX // xList[-2]
    # We use the index 0 in yList[0] because we HAVE separated the second term into yList[0]*something. That's exactly what we were doing in the above while loop
    yMultiplier = yToBeCombinedWith // yList[0]

    # Print the result from combining the rightmost terms with the left term.
    print(f"{rList[-2]} = {xMultiplier}*{xList[-2]} {yMultiplier}*{yList[0]}")

    # Reset the separateTerms array to be empty. Now we will store the values of xco in it.
    separateTerms = []
    # Repeat the same process but separate the first term this time
    # We already found s so we can get the first coefficient of x by dividing the combined term and s
    xco = baseX // s
    # Loop through the list of terms until we simplify to xco == max(a,b)
    # (where a and b come from the function call gcd(a,b))
    while xco != xList[0]:
        # Update the y coefficient with the new decremented value of i
        # We don't reinitialize i so it keeps the decremeneted value from the end of the y looping
        xco = xList[i]
        separateTerms.append(xco)
        # calculate the piece that will be combined with y after we finish factoring x
        # Multiply by s because we must distribute s before adding with the second term
        toCombineWithY = - (xList[i]//yList[i]) * yList[i] * s
        # Make a string with the value of the left term and the right term
        xBreakDown = ""
        # First we need to make the string contain the terms outside the nested parentheses
        for j in range(len(separateTerms)):
            # always print an opening parentheses to separate the first and second terms
            xBreakDown += f"{s}*({separateTerms[j]} "

        # aMult1*aMult2 gives the value of the left term.
        # We want to separate the value of the left term into a product of 2 numbers.
        # The value of the left term is really the variable toCombineWithY.
        # So we can separate it by assiging the integer dividision of toCombineWithY and the current value of y to aMult1.
        # And assigning  the current value of y to aMult2.
        # Then if multiplied, aMult1*aMult2 produces just toCombineWithY
        aMult1 = toCombineWithY// yList[i]
        aMult2 = yList[i]

        # Continue adding to the string by appending the rightmost term within the parentheses
            # ")"*(len(separateTerms)) allows us to add the correct number of closing parentheses.
            # * is an overloaded operator in Python and when given a string,
            # it will repeat the string the given number of times.
        xBreakDown += f"-{aMult2}" + ")"*(len(separateTerms))

        # print the string showing how x factors
        # To also print the y portion we include {yMultiplier}*{yList[0]}
        print(f"{rList[-2]} = {xBreakDown} {yMultiplier}*{yList[0]}")

        # Decrement i so the previous equation in the Euclidean algorithm will be used in the next run
        i -= 1

    # finalY combines the second term with the remaining terms (except for the xco*floor(a*b) term)
    finalY = yToBeCombinedWith + toCombineWithY

    # Now that we have combined everything we can from the first term with the second term, we can find t by dividing the combined term and b
    t = finalY // yList[0]

    # 2. Show each step of the Euclidean Algorithm using the “product & sum” format.
    # Print the results in the form gcd(a, b) = s*a + t*b
    # For example, the first step for gcd(252, 198) would be: 252 = 198 * 1 + 54
    print(f"{rList[-2]} = {s}*{xList[0]} {t}*{yList[0]}")
    print(f"Therefore s = {s} and t = {t} for a = {xList[0]} and b = {yList[0]} (Note that the order of a and b may be flipped from the input!)")

# gcdMethod1 is a function that finds the greatest common denominator
# of two numbers, a and b, by using the Euclidean Algorithm.
# After this forward pass, it then passes the results to the bezout function
# which finds the Bezout coefficients through working backwards.
def gcdMethod1(a, b):
    # The algorithm only works properly if it divides the larger value and not the smaller value.
    # So we get copies of the values and put them into x and y based on their size
    x = max(a,b)
    y = min(a,b)
    # We need a way to output which step we are on so i will keep track of the number of loops
    i = 1

    # Since we are going to work backwards through the algorithm,
    # we want to store the results from each loop in a list.
    # These lists will contain each successive value of x, y, and r
    xValues = []
    yValues = []
    rValues = []
    # Move foward through the Euclidean Algorithm.
    # Loop until y (which will be the remainder) is 0
    while y != 0:
        # Add the current values of x and y to the list
        xValues.append(x)
        yValues.append(y)
        # Get the remainder by utilizing the modulo operator
        r = x % y
        # Add the current value of r to the list
        rValues.append(r)
        # 2. Show each step of the Euclidean Algorithm using the “remainder” format.
        # Note that // is the integer division operator in Python
        # It floors the division result to the nearest integer
        print(f"Step {i}. {x}/{y} = {x//y} R {r}")

        # Now we want to transfer the value of y into x
        x = y
        # Transfer the value of the remainder into y
        y = r
        # Increment the count
        i += 1
    # x now contains the GCD so we want to keep track of it
    gcd = x

    # Print a new line to separate the forward pass and the backward pass
    print()
    # Call the bezout function and pass it the results from the algorithm
    bezout(xValues, yValues, rValues)

    # 3. Display the final results as: "gcd(a,b) = n"
    print(f"gcd({a}, {b}) = {gcd}")
    # Return the final result of the greatest common denominator
    return gcd

# 3. Show each step of working backwards through the steps of the Euclidean algorithm in the same way.
# For example, the “backward” steps for the gcd(252, 198) would be:
    # 18 = 54 − 1 * 36
    # 18 = 54 − 1 * (198 − 3 * 54)
    # 18 = 4 * 54 − 1 * 198
    # 18 = 4 * (252 − 1 * 198) − 1 * 198
    # 18 = 4 * 252 − 5 * 198
# 4. Show the final results as "gcd(a, b) = s*a + t*b"
# 5. Test with the following inputs:
print("Part 2")
# 5a.
print("a) gcd(414, 662)")
gcdMethod1(414, 662)
# 5b.
print("\nb) gcd(6, 14)")
gcdMethod1(6, 14)
# 5c.
print("\nc) gcd(24, 36)")
gcdMethod1(24, 36)
# 5d.
print("\nd) gcd(12, 42)")
gcdMethod1(12, 42)
# 5e.
print("\ne) gcd(252, 198)")
gcdMethod1(252, 198)

# -----------PART 3-----------
# 1. Express gcd(a, b) as a linear combination: gcd(a, b) = sa + tb,
# where s and t are Bézout coefficients of a and b, using the extended Euclidean Algorithm (Method 2).
# 2. Show the quotients q1 through qj and then the calculations for sj and tj.
# For example for gcd(252, 198):
    # q1 = 1, q2 = 3, q3 = 1, and q4 = 2
    # s0 = 1, s1 = 0, s2 = s0 − s1*q1 = 1 − 0 * 1 = 1, etc.
    # t0 = 0, t1 = 1, t2 = t0 − t1*q1 = 0 − 1 * 1 = −1, etc.
# 3. Show the final results as "gcd(a, b) = s*a + t*b"
# 4. Test your program with the following inputs:
    # 4a. gcd(414, 662)
    # 4b. gcd(6, 14)
    # 4c. gcd(24, 36)
    # 4d. gcd(12, 42)
    # 4e. gcd(252, 198)
