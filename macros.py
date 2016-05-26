from type_alias import create_type_alias, find_macro_type_aliases, find_union_types, find_type_aliases, find_macro_union_types
from decoder import create_decoder, create_encoder, create_union_type_decoder, create_union_type_encoder


exampleAlias = """

with decoder type alias Something =
  { name : String
  }

with decoder type Animal
    = Cat
    | Dog

"""

exampleOutput = """

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

decodeAnimal : Json.Decode.Decoder Animal
decodeAnimal =
    let
        decodeToType string =
            case string of
                "Cat" -> Result.Ok Cat
                "Dog" -> Result.Ok Dog
                _ -> Result.Err ("Not valid pattern for decoder to Animal. Pattern: " ++ (toString string))
    in
        Json.Decode.customDecoder Json.Decode.string decodeToType

"""

def with_decoder(file):
    """ generate a decoder for a type definition """
    aliases = find_macro_type_aliases(file)
    unions = find_macro_union_types(file)

    results = []

    for alias in aliases:
        solo_alias = find_type_aliases(alias)[0]
        results.append({
            "original" : alias,
            "alias" : solo_alias,
            "decoder": create_decoder(alias)
        })

    for union in unions:
        solo_union = find_union_types(union)[0]
        results.append({
            "original" : union,
            "alias" : solo_union,
            "decoder": create_union_type_decoder(union)
        })


    return results


def replace_original(text, result):
    replacement = '\n\n'.join([ result['alias'], result['decoder'] ])
    return text.replace(result['original'], replacement)

def test():
    with_decode = exampleAlias

    for result in with_decoder(with_decode):
        with_decode = replace_original(with_decode, result)

    assert with_decode.strip() == exampleOutput.strip()



def run_on_file(filename):
    with open(filename) as f:
        text = f.read()

    for result in with_decoder(text):
        text = replace_original(text, result)

    with open(filename, 'w') as f:
        f.write(text)


if __name__ == '__main__':
    test()
