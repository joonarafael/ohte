```mermaid
classDiagram
    Monopoly *-- Board : consists of
    Monopoly *-- Player : consists of
    Player -- PlayerPiece : linked
    Board <-- Square : associated
    Board <.. PlayerPiece : players located on the board
    Square o-- GetStreet : data request method
    GetStreet -- Street Database : database access
    Chance And Community Chest o-- GetRandomCard : data request method
    GetRandomCard -- Random Card Database : database access
    Square <|-- Start : inherits Square class
    Square <|-- Jail : inherits Square class
    Square <|-- ExampleStreet : inherits Square class
    Square <|-- Chance And Community Chest : inherits Square class

    class Monopoly
    Monopoly : +Player() * int(2-8)
    Monopoly : +Board()

    class Board
    Board : lists all 40 squares

    class Square
    Square : +int id
    Square : +string name = GetStreet(name)
    Square : +string action = GetStreet(action)
    Square : +int owner_id (if any)
    Square : +int house_amount
    Square : +int next_square = id + 1 (0 if 40)

    class Player
    Player : +int id
    Player : +string name
    Player : +int money
    Player : +PlayerPiece()

    class PlayerPiece
    PlayerPiece : +int(0-39) current_square

    class Start
    Start : Square.id = 0
    Start : Square.name = "Start"
    Start : Square.owner_id = None
    Start : Square.house_amount = None
    Start : Square.action = ("game start" and "money +200 when passed")
    Start : Square.next_square = 1

    class Jail
    Jail : Square.id = 10
    Jail : Square.name = "Jail"
    Jail : Square.owner_id = None
    Jail : Square.house_amount = None
    Jail : Square.action = ("jail passing" or "jail serving")
    Jail : Square.next_square = 11

    class Chance And Community Chest
    Chance And Community Chest : Square.id = 2 or 7 or 17 or 22 or 33 or 36
    Chance And Community Chest : Square.name = "Chance" or "Community Chest"
    Chance And Community Chest : Square.owner_id = None
    Chance And Community Chest : Square.house_amount = None
    Chance And Community Chest : Square.action = GetRandomCard()
    Chance And Community Chest : Square.next_square = 3 or 8 or 18 or 23 or 34 or 37 

    class GetStreet
    GetStreet : return street info from street database
    GetStreet : Square.id links every square in the db

    class Street Database
    Street Database : id, street_name, cost, owner, house_price, houses, rents, action
    Street Database : 0, "Start", None, None, None, None, (None), ("game start" and "money +200 when passed")
    Street Database : 1, "Mediterranean Avenue", 60, None, 50, 0, (2, 10, 30, 90, 160, 250), ("pass" or "buy" or "pay rent")
    Street Database : 2, "Community Chest", None, None, None, None, (None), GetRandomCard()
    Street Database : 3, "Baltic Avenue", 60, 4, 50, 2, (4, 20, 60, 180, 320, 450),("pass" or "buy" or "pay rent")
    Street Database : (...)
    Street Database : 39, "Boardwalk", 400, None, 200, 0, (50, 200, 600, 1400, 1700, 2000), ("pass" or "buy" or "pay rent")

    class GetRandomCard
    GetRandomCard : returns a random card from a shuffled deck for the player
    GetRandomCard : random card deck is uniquely random for each game

    class Random Card Database
    Random Card Database : id, action, image
    Random Card Database : 0, "Bank pays you dividend of $50.", happy01.png
    Random Card Database : 1, "Pay School Tax of $150.", caring01.png
    Random Card Database : 2, "Income Tax refund, collect $20.", happy02.png
    Random Card Database : ...
    Random Card Database : 31, "Advance to 'Go', collect $200.", leap01.png

    class ExampleStreet
    ExampleStreet : Square.id = 18
    ExampleStreet : Square.name = "Tennessee Avenue"
    ExampleStreet : Square.action = ("pass" or "pay rent")
    ExampleStreet : Square.owner_id = 5
    ExampleStreet : Square.house_amount = 2
    ExampleStreet : Square.next_square = 19
    
    note for ExampleStreet "buy option removed from Square.action as the street has an owner already"
```
