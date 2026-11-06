
def generate_demo_quiz(subject, topic, level, question_type):

    if question_type == "Maths / Aptitude":
        return [
            {
                "question": "What is 20% of 150?",
                "options": {
                    "A": "20",
                    "B": "25",
                    "C": "30",
                    "D": "35"
                },
                "correct_answer": "C",
                "explanation": {
                    "formula": "Percentage = (Percentage / 100) × Number",
                    "symbols": [
                        "Percentage means the given rate out of 100.",
                        "Number means the original value."
                    ],
                    "given_values": [
                        "Percentage = 20%",
                        "Number = 150"
                    ],
                    "steps": [
                        "Step 1: Write the formula: (20 / 100) × 150.",
                        "Step 2: Divide 20 by 100 = 0.2.",
                        "Step 3: Multiply 0.2 × 150 = 30."
                    ],
                    "reasoning": "We calculate 20 parts out of every 100 parts of 150.",
                    "shortcut": "10% of 150 is 15. Therefore, 20% is 15 × 2 = 30.",
                    "final_answer": "30 (Option C)",
                    "memory_tip": "To find 20%, calculate 10% and multiply by 2."
                }
            },
            {
                "question": "What is 25% of 200?",
                "options": {
                    "A": "25",
                    "B": "40",
                    "C": "50",
                    "D": "75"
                },
                "correct_answer": "C",
                "explanation": {
                    "formula": "Percentage = (Percentage / 100) × Number",
                    "symbols": [
                        "Percentage = 25%",
                        "Number = 200"
                    ],
                    "given_values": [
                        "Percentage = 25",
                        "Number = 200"
                    ],
                    "steps": [
                        "Step 1: Calculate (25 / 100) × 200.",
                        "Step 2: 25 / 100 = 0.25.",
                        "Step 3: 0.25 × 200 = 50."
                    ],
                    "reasoning": "25% is one-fourth. One-fourth of 200 is 50.",
                    "shortcut": "Divide 200 by 4 to get 50.",
                    "final_answer": "50 (Option C)",
                    "memory_tip": "Remember that 25% means one-fourth."
                }
            },
            {
                "question": "What is 10% of 450?",
                "options": {
                    "A": "35",
                    "B": "40",
                    "C": "45",
                    "D": "50"
                },
                "correct_answer": "C",
                "explanation": {
                    "formula": "10% of a number = Number / 10",
                    "symbols": [
                        "Number = 450"
                    ],
                    "given_values": [
                        "Number = 450"
                    ],
                    "steps": [
                        "Step 1: Divide 450 by 10.",
                        "Step 2: 450 / 10 = 45."
                    ],
                    "reasoning": "10% means one-tenth of the original number.",
                    "shortcut": "Move the decimal point one place to the left: 450 becomes 45.",
                    "final_answer": "45 (Option C)",
                    "memory_tip": "To find 10%, divide by 10."
                }
            },
            {
                "question": "A student scores 80 marks out of 100. What is the percentage?",
                "options": {
                    "A": "60%",
                    "B": "70%",
                    "C": "80%",
                    "D": "90%"
                },
                "correct_answer": "C",
                "explanation": {
                    "formula": "Percentage = (Obtained Marks / Total Marks) × 100",
                    "symbols": [
                        "Obtained Marks = Marks scored",
                        "Total Marks = Maximum marks"
                    ],
                    "given_values": [
                        "Obtained Marks = 80",
                        "Total Marks = 100"
                    ],
                    "steps": [
                        "Step 1: Substitute the values: (80 / 100) × 100.",
                        "Step 2: Simplify the expression.",
                        "Step 3: The result is 80%."
                    ],
                    "reasoning": "Percentage expresses marks as a value out of 100.",
                    "shortcut": "When the total is already 100, the obtained marks are the percentage.",
                    "final_answer": "80% (Option C)",
                    "memory_tip": "Percentage always means out of 100."
                }
            },
            {
                "question": "What is 50% of 360?",
                "options": {
                    "A": "120",
                    "B": "150",
                    "C": "180",
                    "D": "200"
                },
                "correct_answer": "C",
                "explanation": {
                    "formula": "50% of a number = Number / 2",
                    "symbols": [
                        "Number = 360"
                    ],
                    "given_values": [
                        "Number = 360"
                    ],
                    "steps": [
                        "Step 1: 50% means half.",
                        "Step 2: Divide 360 by 2.",
                        "Step 3: 360 / 2 = 180."
                    ],
                    "reasoning": "50% represents half of the original value.",
                    "shortcut": "Simply divide the number by 2.",
                    "final_answer": "180 (Option C)",
                    "memory_tip": "50% always means half."
                }
            }
        ]

    # Default demo quiz: Python Variables
    return [
        {
            "question": "Which symbol is used to assign a value to a variable in Python?",
            "options": {
                "A": "==",
                "B": "=",
                "C": "+",
                "D": "*"
            },
            "correct_answer": "B",
            "explanation": {
                "concept": "The assignment operator = stores a value in a variable.",
                "key_points": [
                    "A variable stores data.",
                    "The = operator assigns a value to a variable."
                ],
                "example": "age = 22 stores 22 in the variable age.",
                "option_analysis": {
                    "A": "== checks whether two values are equal.",
                    "B": "= assigns a value to a variable.",
                    "C": "+ performs addition or concatenation.",
                    "D": "* performs multiplication or repetition."
                },
                "memory_tip": "One equal sign assigns; two equal signs compare."
            }
        },
        {
            "question": "Which of the following is a valid Python variable name?",
            "options": {
                "A": "2name",
                "B": "my-name",
                "C": "my_name",
                "D": "class"
            },
            "correct_answer": "C",
            "explanation": {
                "concept": "A Python variable name can contain letters, numbers and underscores, but cannot start with a number or use a reserved keyword.",
                "key_points": [
                    "Variable names cannot start with a digit.",
                    "Spaces and hyphens are not allowed.",
                    "Reserved keywords cannot be used as variable names."
                ],
                "example": "student_name = 'Ravi' is a valid variable name.",
                "option_analysis": {
                    "A": "A variable name cannot start with a digit.",
                    "B": "A hyphen is not allowed in a variable name.",
                    "C": "An underscore is allowed in a variable name.",
                    "D": "class is a reserved Python keyword."
                },
                "memory_tip": "Start variable names with a letter or underscore."
            }
        },
        {
            "question": "What will be the output of this code? x = 10; print(x)",
            "options": {
                "A": "x",
                "B": "10",
                "C": "None",
                "D": "Error"
            },
            "correct_answer": "B",
            "explanation": {
                "concept": "The print() function displays the value stored in a variable.",
                "key_points": [
                    "x stores the value 10.",
                    "print(x) displays the stored value."
                ],
                "example": "x = 10 followed by print(x) displays 10.",
                "option_analysis": {
                    "A": "print(x) displays the value, not the variable name.",
                    "B": "The stored value is 10, so this is the output.",
                    "C": "The variable contains an integer, not None.",
                    "D": "The code is valid Python."
                },
                "memory_tip": "print(variable) displays the value stored in it."
            }
        },
        {
            "question": "Which Python data type is used to store a whole number?",
            "options": {
                "A": "str",
                "B": "float",
                "C": "int",
                "D": "bool"
            },
            "correct_answer": "C",
            "explanation": {
                "concept": "The int data type represents integer values without a decimal part.",
                "key_points": [
                    "int stores whole numbers.",
                    "float stores decimal numbers.",
                    "str stores text."
                ],
                "example": "age = 22 stores an integer.",
                "option_analysis": {
                    "A": "str is used for text.",
                    "B": "float is used for decimal numbers.",
                    "C": "int is used for whole numbers.",
                    "D": "bool stores True or False."
                },
                "memory_tip": "int means integer or whole number."
            }
        },
        {
            "question": "Which function is used to find the data type of a variable?",
            "options": {
                "A": "type()",
                "B": "print()",
                "C": "input()",
                "D": "len()"
            },
            "correct_answer": "A",
            "explanation": {
                "concept": "The type() function returns the data type of an object.",
                "key_points": [
                    "type() identifies the data type.",
                    "It can be used with variables and values."
                ],
                "example": "x = 10; type(x) returns int.",
                "option_analysis": {
                    "A": "type() returns the data type.",
                    "B": "print() displays information.",
                    "C": "input() receives user input.",
                    "D": "len() returns the length of an object."
                },
                "memory_tip": "Use type() when you want to know a variable's data type."
            }
        }
    ]
