def initialize_game():
    print("Welcome to Minesweeper!")
    columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    print("  ", end="")
    for i in range(10):
        print(columns[i], end=" ")
    print()
    for i in range(10):
        print(f"{i} ", end="")
        print(" ".join("X" * 10))

initialize_game()