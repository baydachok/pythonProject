import re


def main(s):
    s = s.replace('\n', ' ')
    str1 = re.findall(r"\[.+?\]", s)
    str2 = re.findall(r"\|>[^|]+", s)

    result1 = []
    result2 = []
    for _ in str1:
        if _[1] == ' ':
            if _[-2] == ' ':
                newstr = _[2:-2]
            else:
                newstr = _[2:-1]
            numbers_list = list(map(int, newstr.split(" ")))
        else:
            if _[-2] == ' ':
                newstr = _[1:-2]
            else:
                newstr = _[1:-1]
            numbers_list = list(map(int, newstr.split(" ")))

        result1.append(numbers_list)

    for newstr2 in str2:
        result2.append(newstr2.replace(' ', '')[2:])

    return list(zip(result2, result1))


print(main('''
.begin|| glob [ -4920 4423 5058] |>ened_23 || || glob [ -6666 5866
-9931 -3490]|> raan_428|| || glob [ -8445 9934 ] |> endima ||||
glob[-9607 6243 -1829 4220 ] |> requ_21 || .end
'''))
