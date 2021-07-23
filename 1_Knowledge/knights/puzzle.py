from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Or(AKnight, AKnave),                            # either is a knigh or a knave
    # Not(And(AKnight, AKnave)),                      # can't be both at same time
    Biconditional(AKnight, Not(AKnave)),            # if a is knight can't be knave and if is a knave is not a knight
    
    Implication(AKnight, And(AKnight, AKnave)),     # if is a knight the sentece is true
    Implication(AKnave, Not(And(AKnight, AKnave)))  # if is a knva the sentence is false
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Biconditional(AKnight, Not(AKnave)),            # if a is knight can't be knave and if is a knave is not a knight
    Biconditional(BKnight, Not(BKnave)),            # if a is knight can't be knave and if is a knave is not a knight
    
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Biconditional(AKnight, Not(AKnave)),            # if is knight can't be knave and if is knave is not a knight
    Biconditional(BKnight, Not(BKnave)),            # if is knight can't be knave and if is knave is not a knight
    
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight)))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Biconditional(AKnight, Not(AKnave)),            # if is knight can't be knave and if is knave is not a knight
    Biconditional(BKnight, Not(BKnave)),            # if is knight can't be knave and if is knave is not a knight
    Biconditional(CKnight, Not(CKnave)),            # if is knight can't be knave and if is knave is not a knight
    
    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    Or(
        And(Implication(AKnight, AKnight), Implication(AKnave, Not(AKnight))),
                                                    # if a is knight
        And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))
                                                    # if a is knave
    ),
    Not(                                            # cant be both a knight and a knave
        And(
            And(
                Implication(AKnight, AKnight),
                Implication(AKnave, Not(AKnight))
            ),
        
            And(
                Implication(AKnight, AKnave),
                Implication(AKnave, Not(AKnave))
            )
        )
    ),

    # B says "A said 'I am a knave'."
    Implication(BKnight, And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))),
                                                    # b knight then if a knight then knave, if a knave then a not knave
    Implication(BKnave, Not(And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave))))),
                                                    # b knight then if a knight then knave and if a knave then a not knave is false

    # B says "C is a knave."
    Implication(BKnight, CKnave),                   # b knight then c knave
    Implication(BKnave, Not(CKnave)),               # b knave then c not knave

    # C says "A is a knight."
    Implication(CKnight, AKnight),                  # c knight then a is knight
    Implication(CKnave, Not(AKnight)),              # c is knave then a is not knight
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
