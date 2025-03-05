def initialize_grammar():
    """
    Initialize the CNF grammar with probabilities.

    Returns:
        binary_rules: dict mapping non-terminals to a list of (rhs, probability) pairs
                      for binary rules (e.g., S -> NP VP).
        lexical_rules: dict mapping non-terminals to a dict of terminal probabilities
                       (e.g., NN -> {"flight": 0.5, "cat": 0.5}).
    """
    # Binary (non-terminal) rules with probabilities
    binary_rules = {
        "S": [ (["NP", "VP"], 0.3), (["NN", "VP"], 0.2), (["PRP", "VBD"], 0.2), (["NN", "VBD"], 0.3) ],
        "NP": [ (["DT", "NN"], 0.1) ],
        "VP": [ (["VBD", "NP"], 0.6), (["VBD", "PP"], 0.4) ],
        "PP": [ (["IN", "NP"], 1.0) ]
    }

    # Lexical (terminal) rules with probabilities
    lexical_rules = {
        "DT": {"the": 1.0},
        "NN": {"flight": 0.5, "cat": 0.5},
        "PRP": {"She": 1.0},
        "VBD": {"left": 0.6, "saw": 0.4},
        "IN": {"to": 1.0}
    }

    return binary_rules, lexical_rules

def tokenize_sentence(sentence):
    """
    Tokenize the input sentence.

    For simplicity, we convert to lowercase and split by whitespace.
    Adjust as needed to handle punctuation or case sensitivity based on your grammar.

    Args:
        sentence (str): The input sentence.

    Returns:
        List[str]: A list of tokens.
    """
    # TODO: Consider handling punctuation or case sensitivity as required.
    return sentence.lower().split()

def initialize_cyk_table(tokens, lexical_rules):
    """
    Initialize the CYK table (a 2D list) for the tokens.

    The table[i][j] will eventually hold the set of non-terminals that derive the substring tokens[i:j+1].

    Args:
        tokens (List[str]): Tokenized sentence.
        lexical_rules (dict): The lexical rules of the grammar.

    Returns:
        list: A 2D list representing the CYK table.
    """
    n = len(tokens)
    table = [[set() for _ in range(n)] for _ in range(n)]

    # Fill the diagonal with non-terminals that produce the token via lexical rules.
    for i, token in enumerate(tokens):
        for lhs, productions in lexical_rules.items():
            # TODO: Check if token is produced by lhs and add lhs to table[i][i]
            if token in productions:
                table[i][i].add(lhs)
    return table

def fill_cyk_table(tokens, table, binary_rules):
    """
    Fill the CYK table using the binary production rules.

    Use dynamic programming to combine subparts of the sentence.

    Args:
        tokens (List[str]): Tokenized sentence.
        table (list): The current CYK table with initialized lexical entries.
        binary_rules (dict): The binary rules of the grammar.

    Returns:
        list: The completed CYK table.
    """
    n = len(tokens)
    # Loop over lengths of substrings
    for span in range(2, n+1):  # span length from 2 to n
        for start in range(n - span + 1):
            end = start + span - 1
            # Consider all possible splits
            for split in range(start, end):
                left_cell = table[start][split]
                right_cell = table[split+1][end]
                # TODO: For every combination in left_cell and right_cell,
                # check binary_rules to see if they can combine to form a new non-terminal.
                for lhs, productions in binary_rules.items():
                    for (rhs, prob) in productions:
                        # Check if rhs[0] is in left_cell and rhs[1] in right_cell.
                        if rhs[0] in left_cell and rhs[1] in right_cell:
                            table[start][end].add(lhs)
    return table

def is_sentence_valid(table):
    """
    Determine if the sentence is valid by checking if the start symbol 'S'
    appears in the top-right cell of the CYK table.

    Args:
        table (list): The filled CYK table.

    Returns:
        bool: True if 'S' is present, False otherwise.
    """
    n = len(table)
    return 'S' in table[0][n-1]

def print_cyk_table(sentence, table, tokens):
    n = len(tokens)

    # Print the header for the table with tokens centered in fixed-width fields.
    header = " " * 12  # Initial space for the row labels.
    for token in tokens:
        header += f"{token:^10}"
    print("CYK Table:")
    print(header)
    print("-" * len(header))

    # Print each row of the CYK table.
    for i in range(n):
        # Use the token at position i as the row label.
        row_label = tokens[i] if i < len(tokens) else ""
        row_str = f"{row_label:<12}"  # Left-align the row label within 12 spaces.
        for j in range(n):
            if j < i:
                # For lower triangle cells, print fixed-width blank space.
                row_str += " " * 10
            else:
                # Convert the set to a sorted list for consistency.
                cell = sorted(list(table[i][j]))
                cell_str = str(cell)
                row_str += f"{cell_str:^10}"  # Center-align the cell contents.
            row_str += " "  # Extra space between cells.
        print(row_str)



def main():
    # Step 1: Initialize grammar rules
    binary_rules, lexical_rules = initialize_grammar()

    # Step 2: Input sentence and tokenize
    sentence = "Cat saw the flight"
    tokens = tokenize_sentence(sentence)

    # Step 3: Initialize the CYK table with lexical rules
    table = initialize_cyk_table(tokens, lexical_rules)

    # Step 4: Fill the CYK table using binary rules (dynamic programming)
    table = fill_cyk_table(tokens, table, binary_rules)

    # Step 5: Check if the sentence is valid according to the grammar
    valid = is_sentence_valid(table)

    # Output the result
    print(f"Sentence: '{sentence}'")
    print("Valid sentence according to the grammar:" if valid else "Invalid sentence according to the grammar.")

    print_cyk_table(sentence, table, tokens)

if __name__ == "__main__":
    main()
