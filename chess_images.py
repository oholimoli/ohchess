import os
import csv
import chess.svg
import chess
import chess.engine

from ohchess import generate_svg_gallery

# engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

board = chess.Board()


game = "d4"

directory = game

# Check if the directory already exists
if not os.path.exists(directory):
    # Create the directory
    os.makedirs(directory)
    print(f"Directory '{directory}' created successfully.")
else:
    print(f"Directory '{directory}' already exists.")

with open(f'{game}.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    moves_list = [row[0] for row in reader]

# N = 3

image_files = []

for move_no in range(len(moves_list)):

    move = moves_list[move_no]

    board.push_san(move)

    # Export image
    boardsvg = chess.svg.board(board=board, flipped=True)

    image_file = f'{move_no + 1}_{move}.svg'

    image_files += [image_file]

    with open(f"{directory}/{image_file}", "w") as image:
        image.write(boardsvg)


# result = engine.play(board, chess.engine.Limit(time=1))

# engine.quit()

# print(f"Best move: {result.move}")

# board.push_san("Nf6")

# board.push_san("c4")

print(image_files)

# print(board)

# outputfile = open('name.svg', "w")
# outputfile.write(boardsvg)
# outputfile.close()

generate_svg_gallery(image_files, f"{directory}/index.html")