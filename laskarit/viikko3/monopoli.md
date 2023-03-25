::: mermaid
classDiagram
    Monopoly *-- Board : composition
    Monopoly <-- Player
    Player -- PlayerPiece : link
    Board <-- Square : association
    Square <.. PlayerPiece : dependency

    class Monopoly
    Monopoly : +Integer(2-8) Player()
    Monopoly : +Board()

    class Board
    Board : +Integer(39) Square()

    class Square
    Square : +String name
    Square : +String action
    Square : +String next_square

    class Player
    Player : +String name
    Player : +PlayerPiece()

    class PlayerPiece
    PlayerPiece : +Integer(0-40) current sqaure



:::