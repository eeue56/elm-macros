# elm-macros


```bash

elm-macro Something.elm

```

turn

```
module Something where

with decoder type alias Something =
  { name : String
  }


with decoder type Animal
    = Cat
    | Dog
    | Goat

a = 5

b : String
b = "hello"


c : Something
c = { name = b }

with enum type Month
    = Jan
    | Feb
    | March

```

into


```
module Something where

type alias Something =
  { name : String
  }

decodeSomething : Json.Decode.Decoder Something
decodeSomething =
    Json.Decode.succeed Something
        |: ("name" := string)


type Animal
    = Cat
    | Dog
    | Goat

decodeAnimal : Json.Decode.Decoder Animal
decodeAnimal =
    let
        decodeToType string =
            case string of
                "Cat" -> Result.Ok Cat
                "Dog" -> Result.Ok Dog
                "Goat" -> Result.Ok Goat
                _ -> Result.Err ("Not valid pattern for decoder to Animal. Pattern: " ++ (toString string))
    in
        Json.Decode.customDecoder Json.Decode.string decodeToType


a = 5

b : String
b = "hello"


c : Something
c = { name = b }

type Month
    = Jan
    | Feb
    | March

toIntMonth : Month -> Int
toIntMonth something =
    case something of
        Jan -> 0
        Feb -> 1
        March -> 2

```
