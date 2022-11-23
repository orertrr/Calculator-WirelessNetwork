import enum

class CalculatorInvalidTokenError(Exception):
    def __init__(self, token, message = "Invalid TokenType") -> None:
        self.token = token
        self.message = message
        super().__init__(message)
    
    def __str__(self):
        return f"{self.message}: '{self.token}'"

class CalculatorInvalidFormulaError(Exception):
    def __init__(self, formula, message = "Invalid Formula") -> None:
        self.formula = formula
        self.message = message
        super().__init__(message)
    
    def __str__(self):
        return f"{self.message}: '{self.formula}'"

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
    if char in "0123456789":
        return TokenType.NUMERIC
    if char == "(":
        return TokenType.LEFT_BRACKET
    if char == ")":
        return TokenType.RIGHT_BRACKET
    if char == " ":
        return TokenType.SPACE
    
    return TokenType.INVALID

def formula_to_tokens(formula: str) -> list:
    """
    Separates formula(String) into tokens(String or Integer) with queue
    
    Arguments:
    formula : str

    Return a list of tokens
    """

    if formula == "":
        raise CalculatorInvalidFormulaError(formula, "Empty Formula")

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
                raise CalculatorInvalidFormulaError(formula, "Empty bracket")

            # Check if the tokentype of the current and last char are different
            # If true, dequeue all chars in the queue and merge them into a token
            if char_tokentype != last_tokentype:
                token = ""
                while len(queue) > 0:
                    token += queue.pop(0)
                if token != "":
                    if token.isdigit():
                        tokens.append(int(token))
                    else:
                        tokens.append(token)
                        
        queue.append(char)

    # Clear the queue
    if len(queue) > 0:
        token = ""
        while len(queue) > 0:
            token += queue.pop(0)
        if token != "":
            if token.isdigit():
                tokens.append(int(token))
            else:
                tokens.append(token)

    queue.append(char)

    return tokens