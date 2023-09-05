def delete_stolb(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i]) - 1):
            if arr[i][j] == arr[i][j + 1]:
                arr[i].remove(arr[i][j + 1])
                break
    return arr


def delete_empty(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if None is arr[i][j]:
                del arr[i][j]
                break
    return arr


def delete_str(arr):
    for i in range(len(arr)-1):
        for z in range(1, len(arr)-i):
            if arr[i][0] == arr[i+z][0]:
                del arr[i+z]
                break

    return arr


def split_and_round(arr):
    for i in range(len(arr)):
        mystr = arr[i][0].split(':')
        if mystr[0] == "Да":
            mystr[0] = "Выполнено"
        else:
            mystr[0] = "Не выполнено"

        mystr[1] = str(round(float(mystr[1]), 1))
        arr[i][:1] = list(reversed(mystr))
    return arr


def transition(arr):
    arr = map(list, [*zip(*arr)])
    return list(arr)


def mail(arr):
    strs = arr[3]
    for i in range(len(strs)):
        strs[i] = str(strs[i].replace("@", '[at]'))
    return arr


def name(arr):
    strs = arr[2]
    for i in range(len(strs)):
        temp = strs[i].find('.')
        strs[i] = str(strs[i][temp - 1:temp + 1] + ' ' + strs[i][:temp - 2])
    return arr


def main(arr):
    arr = delete_stolb(arr)
    arr = delete_empty(arr)
    arr = delete_str(arr)
    arr = split_and_round(arr)
    arr = transition(arr)
    arr = mail(arr)
    arr = name(arr)
    return arr


mas = [['Да:0.26', 'Теседев М.Ш.', 'Теседев М.Ш.', None, 'tesedev34@rambler.ru'],
       ['Нет:0.12', 'Темацский О.Л.', 'Темацский О.Л.', None, 'temazskij55@rambler.ru'],
       ['Нет:0.12', 'Темацский О.Л.', 'Темацский О.Л.', None, 'temazskij55@rambler.ru'],
       ['Да:0.87', 'Зиняк З.С.', 'Зиняк З.С.', None, 'zinak11@yahoo.com']]

print(main(mas))
