-- Sources:
-- https://www.schoolofhaskell.com/user/adlew/calculator Basic calculator tutorial in Haskell
-- https://stackoverflow.com/a/13962931 Getting a substring in Haskell

-- data CalculationError = UnknownOperator String | UnmatchedParentheses deriving Show

-- This is necessary because I am using checks for the results of maybe such as "isJust" and "fromJust"
import Data.Maybe
import Data.Either

-- Define the custom types we will use
-- We want to make an operatorRegister that contains a string to represent the operation, and the function itself to apply
-- So the Register type should be a list of something. We call it Entry
type Register = [Entry]
-- Each entry should have both the string to represent it and the operation to use so we can make it a tuple and a special Operator type
type Entry = (String, Operator)
type Operator = Double -> Double -> Double

-- This is a function that was given from https://www.schoolofhaskell.com/user/adlew/calculator
-- I did not do change anything with it
-- It works by using the modulo operation on two integers it is passed.
-- Since we were working with Doubles, but mod needs integers, we had to round the Doubles.
-- The $ is a way to say that the function should be evaluated last. Normally in Haskell the function gets evaluated ASAP. But this is another way of writing fromIntegral (mod (round a) (round b))
modulu :: Double -> Double -> Double
-- fromIntegral is used to convert to a Double
modulu a b = fromIntegral $ mod (round a) (round b)

-- The lower the character in the register, the higher precedence it has
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

-- countParentheses takes in a string and returns a list of tuples of the form ('characterMatched', occurrencesInt)
-- It is searching for open and close parentheses so we can use this function to check if there is an invalid amount of parentheses. I modified it from this StackOverflow answer about how to get a substring https://stackoverflow.com/a/13962931
-- It works by returning a list of tuples. Anytime the specified characters are found in the string, their count is incremented. When the string has finished, the character that was found and the number of occurrences is added to the list as a tuple.
countParentheses string = [ (x,c) | x<-['(', ')'], let c = (length.filter (==x)) string, c>0 ]

-- handleParenth takes in a well-formed string expression containing opening and closing parentheses.
-- I made this function by myself.
-- It finds the substring inside the first pair of parentheses and evaluates it then returns the original string but with the parentheses part replaced with the evaluated string.
-- Note, this function does not do error checking. It expects a well-formed string containing both opening and closing parentheses.
handleParenth :: String -> Either String String
handleParenth stringExpression =
  let
      -- get a copy of the substring before the opening parentheses.
      beforeParentheses = takeWhile (/= '(') stringExpression
      -- get the inside of the parentheses. The + 1 is to skip the opening parentheses.
      innerExpression = drop (length beforeParentheses + 1) (takeWhile (/= ')') stringExpression)
      -- get the rest of the string after the first closing parentheses
      -- It does this by dropping characters from the beginning of the stringExpression. The two +1s are for the opening and closing parentheses.
      afterExpression = drop (length beforeParentheses + 1 + length innerExpression + 1) stringExpression
      -- In case the result of the calculation does not return a valid Double
      innerValueUnsafe = calculate innerExpression -- Returns a Left string or Right double
      -- If the parentheses are empty then it will return 0.
      -- This function assumes the string is well formed so we won't return an error message, just a default value of 0 which hopefully will never be returned.
      -- innerValue = if isRight innerValueUnsafe then fromRight innerValueUnsafe else
  in
    -- return the original string but replace the parentheses with the value
    if isRight innerValueUnsafe -- must be a Double
      then
        Right (beforeParentheses ++ show (fromRight 0 innerValueUnsafe) ++ afterExpression)
      else
        Left (fromLeft "Error: Unexpected error" innerValueUnsafe) -- this must be an error value so we will just pass it back
    --Right beforeParentheses ++ show innerValue ++ afterExpression

-- I made most of this function, particularly the part that handles parentheses.
-- I modified the final else statement from https://www.schoolofhaskell.com/user/adlew/calculator
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
        -- The default value shouldn't ever be passed because of our error checking up to this point. But it is required just in case.
        in -- Right (fromRight 0 (calculate stringWithoutInnerParenth))

          if isRight unsafeStringWithoutInnerParenth
            then calculate (fromRight "0" unsafeStringWithoutInnerParenth)
            -- unfortunately, even though this error is the same type and we know it must be an error, Haskell will not compile if we just return the unsafeStringWithoutInnerParenth
            -- Instead we have to specifically pull out the Left value from it and return that
            else Left (fromLeft "Error: Unexpected error" unsafeStringWithoutInnerParenth)
      else Left "Error: Mismatched parentheses" -- mismatched parentheses error
  -- The string must not have any parentheses so evaluate it according to the regular order of operations
  else
    if isRight (eval operatorRegister (words stringExpression))
      then
        Right (fromRight 0 (eval operatorRegister (words stringExpression)))
      else
        Left (fromLeft "Error: Unexpected error" (eval operatorRegister (words stringExpression)))

-- We made a type called Register that is comprised of a tuple with the string that represents an operation and the function that executes the operation.
-- So when calling eval we pass in a register tuple and a list of strings.
-- The register tuple is just the operation that should be applied.
-- The list of strings is the
eval :: Register -> [String] -> Either String Double
eval [] _ = Left "Error: Missing operator" -- No operator found.
eval _ [] = Left "Error: Missing argument for operator" -- If a operator don't have anything to operate on.
eval _ [number] = Right $ read number
eval ((operator, function):rest) unparsed =
    -- until we loop through the operator list and find the operator to use, continue searching
    case span (/=operator) unparsed of
        (_, []) -> eval rest unparsed -- Recursively call eval and pass in the rest of the tuple operators and the unparsed string
        (beforeOperator, afterOperator) -> do -- added the do
          arg1 <- eval operatorRegister beforeOperator
          arg2 <- eval operatorRegister $ drop 1 afterOperator
          Right (function arg1 arg2)

-- parse stringExpression = if isRight (calculate stringExpression) then (calculate stringExpression) else 0.0
-- Data MyType = String | Double
parse :: String -> String
-- This will return just the value from the Left or Right type
-- The second parameter is the default value that it will return if calculate stringExpression is not Right
-- parse stringExpression = fromRight (fromLeft "Error: Unexpected error" (calculate stringExpression)) (calculate stringExpression)
parse stringExpression = if isRight (calculate stringExpression) then show (fromRight 0 (calculate stringExpression)) else fromLeft "Error: Unexpected error" (calculate stringExpression)
