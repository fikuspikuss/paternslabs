from abc import ABC, abstractmethod


class Piece(ABC):
    def __init__(self, position, color, move_rule):
        self.position = position  # Позиція фігури на дошці
        self.color = color  # Колір фігури
        self.number_of_moves = 0  # Кількість виконаних ходів
        self.move_rule = move_rule  # Правило руху

    @staticmethod
    def check_position_range(position):
        """Перевіряє, чи координати знаходяться в межах шахової дошки."""
        return all(1 <= coord <= 8 for coord in position)

    def move(self, new_position):
        """Виконує хід, якщо нова позиція допустима."""
        if not self.check_position_range(new_position):
            raise ValueError(f"Позиція {new_position} виходить за межі дошки.")

        possible_moves = self.move_rule.get_all_moves()
        if new_position not in possible_moves:
            raise ValueError(f"Позиція {new_position} не є допустимим ходом.")

        self.position = new_position  # Оновлення позиції
        self.number_of_moves += 1  # Збільшення лічильника ходів
        self.move_rule.position = new_position  # Оновлення позиції в правилі руху
        return {"нова позиція": self.position, "кількість ходів": self.number_of_moves}

    def __str__(self):
        return f"{self.__class__.__name__} ({self.color}) на позиції {self.position}"


class MoveRule(ABC):
    def __init__(self, position):
        self.position = position  # Позиція фігури

    @abstractmethod
    def get_all_moves(self):
        """Повертає всі допустимі ходи для фігури."""
        pass


class KnightMove(MoveRule):
    def get_all_moves(self):
        """Генерує всі допустимі ходи для коня."""
        x, y = self.position
        moves = [
            [x + 2, y + 1], [x + 2, y - 1],
            [x - 2, y + 1], [x - 2, y - 1],
            [x + 1, y + 2], [x + 1, y - 2],
            [x - 1, y + 2], [x - 1, y - 2]
        ]
        return [move for move in moves if Piece.check_position_range(move)]


class BishopMove(MoveRule):
    def get_all_moves(self):
        """Генерує всі допустимі ходи для слона."""
        moves = []
        x, y = self.position
        for i in range(1, 8):
            moves.extend([
                [x + i, y + i], [x + i, y - i],
                [x - i, y + i], [x - i, y - i],
            ])
        return [move for move in moves if Piece.check_position_range(move)]


class RookMove(MoveRule):
    def get_all_moves(self):
        """Генерує всі допустимі ходи для туру."""
        moves = []
        x, y = self.position
        for i in range(1, 8):
            moves.extend([
                [x + i, y], [x - i, y],
                [x, y + i], [x, y - i],
            ])
        return [move for move in moves if Piece.check_position_range(move)]


class QueenMove(MoveRule):
    def get_all_moves(self):
        """Генерує всі допустимі ходи для ферзя."""
        return RookMove(self.position).get_all_moves() + BishopMove(self.position).get_all_moves()


class KingMove(MoveRule):
    def get_all_moves(self):
        """Генерує всі допустимі ходи для короля."""
        x, y = self.position
        moves = [
            [x + 1, y], [x - 1, y],
            [x, y + 1], [x, y - 1],
            [x + 1, y + 1], [x + 1, y - 1],
            [x - 1, y + 1], [x - 1, y - 1],
        ]
        return [move for move in moves if Piece.check_position_range(move)]


class PawnMove(MoveRule):
    def __init__(self, position, color):
        super().__init__(position)
        self.color = color

    def get_all_moves(self):
        """Генерує всі допустимі ходи для пішака."""
        x, y = self.position
        direction = 1 if self.color == "White" else -1
        moves = [[x + direction, y]]
        if (self.color == "White" and x == 2) or (self.color == "Black" and x == 7):
            moves.append([x + 2 * direction, y])
        return [move for move in moves if Piece.check_position_range(move)]


class Knight(Piece):
    def __init__(self, position, color):
        super().__init__(position, color, KnightMove(position))


class Bishop(Piece):
    def __init__(self, position, color):
        super().__init__(position, color, BishopMove(position))


class Rook(Piece):
    def __init__(self, position, color):
        super().__init__(position, color, RookMove(position))


class Queen(Piece):
    def __init__(self, position, color):
        super().__init__(position, color, QueenMove(position))


class King(Piece):
    def __init__(self, position, color):
        super().__init__(position, color, KingMove(position))


class Pawn(Piece):
    def __init__(self, position, color):
        super().__init__(position, color, PawnMove(position, color))


def initialize_chess_board():
    """Ініціалізує шахову дошку зі стандартним розташуванням."""
    board = {}

    # Розміщення пішаки
    for i in range(1, 9):
        board[(2, i)] = Pawn([2, i], "White")
        board[(7, i)] = Pawn([7, i], "Black")

    # Розміщення інших фігур
    pieces_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    for i, piece_cls in enumerate(pieces_order):
        board[(1, i + 1)] = piece_cls([1, i + 1], "White")
        board[(8, i + 1)] = piece_cls([8, i + 1], "Black")

    return board


def chess_game():
    board = initialize_chess_board()

    while True:
        print("\nШахова гра:")
        print("1. Показати шахову дошку")
        print("2. Виконати хід")
        print("3. Завершити гру")

        choice = input("Оберіть дію: ")
        if choice == "1":
            print("\nШахова дошка:")
            for position, piece in sorted(board.items()):
                print(f"Координати: {position}, Фігура: {piece}")

        elif choice == "2":
            x, y = map(int, input("Введіть координати фігури (x y): ").split())
            if (x, y) not in board:
                print("На цій позиції немає фігури! Спробуйте ще раз.")
                continue

            piece = board[(x, y)]
            print(f"Ви обрали: {piece}")
            print("Можливі ходи:", piece.move_rule.get_all_moves())

            new_x, new_y = map(int, input("Введіть нову позицію (x y): ").split())
            try:
                result = piece.move([new_x, new_y])
                del board[(x, y)]  # Видаляємо стару позицію
                board[(new_x, new_y)] = piece  # Додаємо фігуру на нову позицію
                print(f"Хід виконано: {result}")
            except ValueError as e:
                print(e)

        elif choice == "3":
            print("Гра завершена. До побачення!")
            break
        else:
            print("Неправильний вибір! Спробуйте ще раз.")


if __name__ == "__main__":
    chess_game()
