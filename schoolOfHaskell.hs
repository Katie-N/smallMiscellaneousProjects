-- Program Name: EECS 468 Assignment 8
-- Description: This program is a robust little calulator.
  -- Input: parse "expression"
  -- Output:
    -- The evaluated expression respecting order of operation rules including parentheses and nested parentheses.
    -- If an error occurs, it will instead return a descriptive error message.
-- Collaborators: None
-- Sources:
  -- https://www.schoolofhaskell.com/user/adlew/calculator Basic calculator tutorial in Haskell
  -- https://stackoverflow.com/a/13962931 Getting a substring in Haskell
-- Author: Katie Nordberg
-- Date: 11/13/2023

-- This is necessary because I am using checks for the results of Either such as "isRight" and "fromRight"
import Data.Either

-- I modified the types from https://www.schoolofhaskell.com/user/adlew/calculator in order to match the types given in our instructions
-- Define the custom types we will use
-- We want to make an operatorRegister that contains a string to represent the operation, and the function itself to apply
-- So the Register type should be a list of something. We call it Entry
type Register = [Entry]
-- Each entry should have both the string to represent it and the operation to use so we can make it a tuple and a special Operator type
type Entry = (String, Operator)
type Operator = Double -> Double -> Double

-- This is a function that was given from https://www.schoolofhaskell.com/user/adlew/calculator
-- I did not change anything with it
-- It works by using the modulo operation on two integers it is passed.
-- Since we were working with Doubles, but mod needs integers, we had to round the Doubles.
-- The $ is a way to say that the function should be evaluated last.
-- Normally in Haskell the function gets evaluated ASAP. But this is another way of writing: fromIntegral (mod (round a) (round b))
modulu :: Double -> Double -> Double
-- fromIntegral is used to convert to a Double
-- round is used to convert to an int
-- mod is the built in modulo operator in Haskell
modulu a b = fromIntegral $ mod (round a) (round b)

isInf val = if (show val == "Infinity") then True else False

-- The farther down in the register the function is, the higher precedence it has.
-- This is done using span and recursively calling eval within the eval function. See there for more details
-- operatorRegister is a list of tuples that take the form (String, on)
-- Register is a special type defined above.
-- I added the exponent operator but I got the rest from https://www.schoolofhaskell.com/user/adlew/calculator
-- It works because in Haskell, operators are considered functions. So we can apply the functions by accessing their index in the tuple
operatorRegister :: Register
operatorRegister = [
                ("-", (-)),
                ("+", (+)),
                ("%", modulu),
                ("/", (/)),
                ("*", (*)),
                ("**", (**)) -- I added the exponent operator and it was as simple as appending it to this list of operators
            ]

-- I modified this function from this StackOverflow answer about how to get a substring https://stackoverflow.com/a/13962931
-- countParentheses takes in a string and returns a list of tuples of the form ('characterMatched', occurrencesInt)
-- It is searching for open and close parentheses so we can use this function to check if there is an invalid amount of parentheses.
-- It works by returning a list of tuples. Anytime the specified characters are found in the string, their count is incremented.
-- When the string has finished, the character that was found and the number of occurrences is added to the list as a tuple.
countParentheses string = [ (x,c) | x<-['(', ')'], let c = (length.filter (==x)) string, c>0 ]

altParenth str =
  let
    beforeParentheses = takeWhile (/= '(') str
    -- I figured out a clever way to find the outermost closing parentheses:
    -- If I find the first instance of ')' then strings with nested parentheses would stop too early
    -- But if I reverse the string and THEN find the first instance of ')' I am actually finding the LAST instance. Then I can reverse the string and have it back in the correct order
    afterParentheses = reverse (takeWhile (/= ')') (reverse str))
    -- This expression took a while to come up with. I had to build it up piece by piece:
      -- Basically I am taking the string and I need to pull out the middle part.
      -- So I need to drop a certain number of characters from the beginning of the string and the end of the string
      -- To drop from the front, I can use the drop function. I pass it the number of characters before the first opening parentheses. I also add 1 because I want to skip the '('
      -- To drop from the end, I will take less characters from the string then it is long.I figured out how many characters to take by subtracting the total string length, the length of the string after the last closing parentheses, and I subtracted a 1 because I wanted to skip the closing parentheses.
    innerExpression = drop (length beforeParentheses + 1) (take ((length str) - (length afterParentheses) - 1) str)
  in beforeParentheses ++ innerExpression ++ afterParentheses

-- handleParenth takes in a well-formed string expression containing opening and closing parentheses.
-- It finds the substring inside the first pair of parentheses and evaluates it then returns the original string but with the parentheses part replaced with the evaluated string.
-- I made this function by myself.
-- Note, this function does not do error checking. It expects a well-formed string containing both opening and closing parentheses.
handleParenth :: String -> Either String String
handleParenth stringExpression =
  let
      -- get a copy of the substring before the opening parentheses.
      beforeParentheses = takeWhile (/= '(') stringExpression

      -- I figured out a clever way to find the outermost closing parentheses:
      -- Problem: If I find the first instance of ')' then strings with nested parentheses would stop too early
      -- Solution: If I reverse the string and THEN find the first instance of ')' I am actually finding the LAST instance.
      -- Then I can reverse the string and have it back in the correct order
      afterParentheses = reverse (takeWhile (/= ')') (reverse stringExpression))

      -- This next expression (innerExpression) took a while to come up with. I had to build it up piece by piece:
        -- Basically I am taking the string and I need to pull out a piece of the middle.
        -- So I need to drop a certain number of characters from the beginning of the string and the end of the string
        -- To drop from the front, I can use the built in drop function.
        -- I pass it the number of characters before the first opening parentheses. I also add 1 because I want to skip the '('
        -- To drop from the end, I will take less characters from the string then it is long.
        -- I figured out how many characters to take by subtracting the total string length, the length of the string after the last closing parentheses, and 1 because I wanted to skip the ')'.
      innerExpression = drop (length beforeParentheses + 1) (take ((length stringExpression) - (length afterParentheses) - 1) stringExpression)

      -- In case the result of the calculation does not return a valid Double
      innerValueUnsafe = calculate innerExpression -- Returns a Left string or Right double
      -- If the parentheses are empty then it will return 0.
      -- This function assumes the string is well formed so we won't return an error message, just a default value of 0 which hopefully will never have to be returned.
  in
    -- return the original string but replace the parentheses with the value
    if isRight innerValueUnsafe -- must be a Double
      then Right (beforeParentheses ++ show (fromRight 0 innerValueUnsafe) ++ afterParentheses)
      else
        Left (fromLeft "Error: Unexpected error" innerValueUnsafe) -- this must be an error value so we will just pass it back

-- I made most of this function, particularly the part that handles parentheses and the error checking.
calculate :: String -> Either String Double
calculate stringExpression = if length (countParentheses stringExpression) > 0
  -- Handle parentheses
  -- If the string does have parentheses then the innermost expression should be done first following the order of operations.
  -- Then the next innermost expresion should be evaluated. And so on and so forth until all instances of parentheses have been replaced with the equivalent value.
  then

    -- First checks if there are both opening and closing parentheses. If this passes then:
    -- It checks if there are the same amount of opening parentheses as there are closing parentheses.
    -- If this passes then all of the parentheses are matched.
    -- The first check is necessary to avoid an invalid index error in the second check.
    if ((length (countParentheses stringExpression) == 2) && snd (countParentheses stringExpression !! 0) == (snd (countParentheses stringExpression !! 1)))
      then
        -- Replace the first term in parentheses with the equivalent value
        let unsafeStringWithoutInnerParenth = handleParenth stringExpression -- Returns a Left (error message string) or a Right (new string expression)
        -- recursively call calculate with the new string expression containing one less pair of parentheses
        -- Return it as the "Right" value of this function by extracting the "Right" value from the function call. fromRight takes a default value and the value to pass if it is of the "Right" type.
        -- The default value (0) shouldn't ever be passed because of our error checking up to this point. But it is required just in case.
        in
          if isRight unsafeStringWithoutInnerParenth
            then calculate (fromRight "0" unsafeStringWithoutInnerParenth)
            -- unfortunately, even though this error is the same type and we know it must be an error, Haskell will not compile if we just return the unsafeStringWithoutInnerParenth
            -- Instead we have to specifically pull out the Left value from it and return that
            else Left (fromLeft "Error: Unexpected error" unsafeStringWithoutInnerParenth)

      else Left "Error: Mismatched Parentheses" -- mismatched parentheses error

  -- The string must not have any parentheses so evaluate it according to the regular order of operations
  -- I modified this from https://www.schoolofhaskell.com/user/adlew/calculator
  else
    -- words takes a string and returns a list of substrings that were separated by whitespace
    -- eval takes two arguments: an operation Register, and a list of strings with the pattern ["number", "operator", "number"]
    if isRight (eval operatorRegister (words stringExpression))
      then
        -- Return the evaluated expression
        Right (fromRight 0 (eval operatorRegister (words stringExpression)))
      else
        -- Return the error message
        -- Note that we have to give a default error message in case the result is Right not Left.
        -- But because we checked for Rightness, this default error message should hopefully never return.
        -- And the error message within the called functions will be returned
        Left (fromLeft "Error: Unexpected error" (eval operatorRegister (words stringExpression)))


-- We made a type called Register that is comprised of a tuple with the string that represents an operation and the function that executes the operation.
-- So when calling eval we pass in a register tuple and a list of strings.
-- The register tuple is just all of the valid operations that can be applied.
-- The list of strings is the expression separated by its whitespace and in the order the expression was given in
-- This function will return Double if the evaluations had no errors. And if there was an error it will instead return a string (the error message)
-- Either is a data type that uses the keyword Left to represent an error case and Right for a success case.
-- It allows us to have error checking more easily and handle errors more gracefully than throwing exceptions
eval :: Register -> [String] -> Either String Double
eval [] _ = Left "Error: Missing operator" -- If eval is called with an empty operator register then there is no operator found.
eval _ [] = Left "Error: Operators Without Operands" -- If an operator doesn't have anything to operate on. (Missing argument)
eval _ [singleVal] =
  if elem singleVal ["+", "-", "*", "/", "%", "(", ")"]
    -- singleVal must be an operator (and has no numbers to operate on!) so we return an error
    then Left "Error: Operators Without Operands"
    else Right (read singleVal) -- singleVal is just a number

eval ((operator, function):rest) unparsed = -- This is where most of the heavy lifting happens
    -- loop through the operator list and find the operator to use
      -- span takes a predicate (condition) and a list to check
      -- It will loop through the list and check each element against the condition.
      -- For each element in a row that matches the condition, it is put in one list
      -- As soon as it hits an element that does not meet the condition, the rest of the list (even elements that do meet the condition) get put into a second list.
      -- Then a tuple with the first list and second list is returned by span.
    -- Essentially this means that the first element of the second list is the
    case span (/=operator) unparsed of
        -- This case is for when the operator was not found in the operatorRegister
        -- This happens when the "operator" was actually a number not an operator. So we
        (_, []) -> eval rest unparsed -- Recursively call eval and pass in the rest of the tuple operators and the unparsed string
        -- I modified this part to not use control applicatives
        -- The afterOperator list must not be empty so we will pattern match here
        (beforeOperator, afterOperator) -> do
          -- Recursively call eval on the string before the operator
          arg1 <- eval operatorRegister beforeOperator
          -- Recursively call eval on the string after the operator
          -- drop 1 removes the matched operator so the unparsed string is left
          arg2 <- eval operatorRegister (drop 1 afterOperator)
          -- Because we recursively find the values of arg1 and arg2, and span matches elements UNTIL the condition is met, we are able to follow the order of operations
          -- By this point, arg1 and arg2 are doubles so we can apply the matched function to them
          -- Perform the operation on the first and second argument and return it as a Right value

          -- I created this part to check for division by 0
          -- If division by 0 occurs it will be returned as "Infinity." But we only want real answers so we will return an error if this happens
          -- Otherwise we will return the result of applying the function to the arguments
          if isInf (function arg1 arg2) then Left "Error: Invalid Operator Usage" else Right (function arg1 arg2)
          -- Note that "function" is a parameter name we defined in this pattern of eval

-- I created this function
-- It is what the user will interface with on the console
-- Input: a typed string expression
-- Output: The evaluated expression or a descriptive error message
parse :: String -> String
parse stringExpression =
  -- check that the characters in the string are all included in our valid characters list before attempting to evaluate
  if validCharacters stringExpression
    then
      -- This will return just the value from the Left or Right type
      -- The second parameter is the default value that it will return if calculate stringExpression is not Right
      -- note the strange arguments in the fromRight or fromLeft function calls. The first value is what to return IF THE SECOND VALUE DOES NOT EVALUATE TO THE CORRECT LEFT OR RIGHT TYPE.
      -- But shouldn't ever be seen if the values are returned correctly.
      if isRight (calculate stringExpression) then show (fromRight 0 (calculate stringExpression))
        else fromLeft "Error: Unexpected error" (calculate stringExpression)

    -- At least one character in the string is not allowed. We return a string not a Left value (because this is getting returned to the user, not another function).
    else "Error: Invalid characters"

-- I created this function
-- Check if every character in the string is in the valid characters list
-- all will return true when every item in a list meets a condition.
  -- Our list is the passed string.
  -- Our condition is that the character in the string is a member of the hardcoded list of valid characters
-- If every character in the string expression passes this condition then return True
validCharacters :: String -> Bool
validCharacters string = all (`elem` ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '+', '-', '*', '/', '%', '(', ')']) string
