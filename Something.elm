module Something where

with decoder type alias Something =
  { name : String
  }


a = 5

b : String
b = "hello"


c : Something
c = { name = b }
