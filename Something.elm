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
