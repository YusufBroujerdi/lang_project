import json

if __name__ == '__main__':

    mydict = dict()

    # mydict = {'a' : 'b',
    #           'c' : '14',
    #           'd' : 'z',
    #           'b' : 'qeffqe'}

    with open('data.txt', 'w') as saved_data:
        saved_data.write(json.dumps(mydict))
    saved_data.close()

    with open('data.txt') as saved_data:
        anotherdict = json.load(saved_data)
    saved_data.close()

    print(anotherdict)