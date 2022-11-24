import enum

class CalculatorInvalidTokenError(Exception):
    def __init__(self, token, message = "Invalid TokenType") -> None:
        self.token = token
        self.message = message
        super().__init__(message)
    
    def __str__(self):
        return f"{self.message}: '{self.token}'"

class CalculatorInvalidFormulaError(Exception):
    def __init__(self, message = "Invalid Formula") -> None:
        self.message = message
        super().__init__(message)
    
    def __str__(self):
        return self.message

class TokenType(enum.IntEnum):
    NUMERIC = 1
    OPERATOR = 2
    RIGHT_BRACKET = 3
    LEFT_BRACKET = 4
    SPACE = 5
    INVALID = 0

def __get_tokentype(char):
    if char in "+-*/%^":
        return TokenType.OPERATOR
    if char in "0123456789.":
        return TokenType.NUMERIC
    if char == "(":
        return TokenType.LEFT_BRACKET
    if char == ")":
        return TokenType.RIGHT_BRACKET
    if char == " ":
        return TokenType.SPACE
    
    return TokenType.INVALID

def __isnumber(token):
    for char in token:
        if char not in "0123456789.":
            return False

    return True

def formula_to_tokens(formula):
    """
    Separates formula(String) into tokens(String or Integer) with queue
    
    Arguments:
    formula : str

    Return a list of tokens
    """

    if formula == "":
        raise CalculatorInvalidFormulaError("Empty Formula")

    tokens = []
    queue = []

    for char in formula:
        char_tokentype = __get_tokentype(char)
        
        if char_tokentype == TokenType.INVALID:
            raise CalculatorInvalidTokenError(char)
        
        # Trim
        if char_tokentype == TokenType.SPACE:
            continue

        if len(queue) > 0:
            last_tokentype = __get_tokentype(queue[-1])

            if char_tokentype == TokenType.RIGHT_BRACKET and last_tokentype == TokenType.LEFT_BRACKET:
                raise CalculatorInvalidFormulaError("Empty bracket")

            # Check if the tokentype of the current and last char are different
            # If true, dequeue all chars in the queue and merge them into a token
            if char_tokentype != last_tokentype:
                token = ""
                while len(queue) > 0:
                    token += queue.pop(0)
                if token != "":
                    if __isnumber(token):
                        tokens.append(float(token))
                    else:
                        tokens.append(token)
                        
        queue.append(char)

    # Clear the queue
    if len(queue) > 0:
        token = ""
        while len(queue) > 0:
            token += queue.pop(0)
        if token != "":
            if __isnumber(token):
                tokens.append(float(token))
            else:
                tokens.append(token)

    queue.append(char)

    return tokens

def __get_level(operator):
    """
    Smaller level, higher priority
    """
    if operator in "^":
        return 1
    if operator in "*/%":
        return 2
    if operator in "+-":
        return 3
    
    return 4

def infix_to_postfix(tokens):
    result = []
    stack = []

    for token in tokens:
        if type(token) == float:
            result.append(token)
            continue

        # Execute the below block if the token is an operator
        current_level = __get_level(token)
        current_type = __get_tokentype(token)

        if current_type == TokenType.LEFT_BRACKET:
            stack.append(token)
            continue

        if current_type == TokenType.RIGHT_BRACKET:
            while len(stack) > 0 and stack[-1] != "(":
                result.append(stack.pop())

            # If the left bracket is not exist
            if len(stack) == 0:
                raise CalculatorInvalidFormulaError("The left bracket is not exist")

            stack.pop()
            continue

        while len(stack) > 0 and __get_level(stack[-1]) <= current_level:
            result.append(stack.pop())

        stack.append(token)

    while len(stack) > 0:
        result.append(stack.pop())

    return result

def compute_postfix(tokens):
    stack = []
    for token in tokens:
        if type(token) != float:
            if len(stack) < 2:
                raise CalculatorInvalidFormulaError("Need two operants")

            operant_right = stack.pop()
            operant_left = stack.pop()
            if token == "+":
                stack.append(operant_left + operant_right)
            elif token == "-":
                stack.append(operant_left - operant_right)
            elif token == "*":
                stack.append(operant_left * operant_right)
            elif token == "/":
                if operant_right == 0:
                    raise CalculatorInvalidFormulaError("Can't divided 0")
                stack.append(operant_left / operant_right)
            elif token == "%":
                stack.append(operant_left % operant_right)
            elif token == "^":
                stack.append(operant_left ** operant_right)
        else:
            stack.append(token)

    return stack[0]

def compute(formula):
    try:
        infix = formula_to_tokens(formula)
        postfix = infix_to_postfix(infix)
        return f"{compute_postfix(postfix):.2f}"
    except:
        return "invalid input"