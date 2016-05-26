from type_alias import create_type_alias, find_macro_type_aliases, find_union_types, find_type_aliases
from decoder import create_decoder, create_encoder, create_union_type_decoder, create_union_type_encoder


exampleAlias = """

with decoder type alias Something =
  { name : String
  }

"""

exampleOutput = """

type alias Something =
  { name : String
  }

decodeSomething : Json.Decode.Decoder Something
decodeSomething =
    Json.Decode.succeed Something
        |: ("name" := string)

"""

def with_decoder(file):
    """ generate a decoder for a type definition """
    aliases = find_macro_type_aliases(file)

    results = []

    for alias in aliases:
        solo_alias = find_type_aliases(alias)[0]
        results.append({
            "original" : alias,
            "alias" : solo_alias,
            "decoder": create_decoder(alias)
        })

    return results


def replace_original(text, result):
    replacement = '\n\n'.join([ result['alias'], result['decoder'] ])
    print(result['original'])
    return text.replace(result['original'], replacement)

def test():
    result = with_decoder(exampleAlias)[0]
    with_decode = replace_original(exampleAlias, result)
    assert with_decode.strip() == exampleOutput.strip()


if __name__ == '__main__':
    test()
