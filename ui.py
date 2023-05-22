from typing import Callable


class Item:

    option : str
    description : str
    operation : Callable

    def __init__(self, option, description, operation):

        self.option = option
        self.description = description
        self.operation = operation


def generate_menu(ui_object : list) -> Callable:

    menu_options = [f'Enter "{item.option}" to {item.description}.\n' for item in ui_object]

    def menu():
        
        while True:

            [print(option) for option in menu_options]
            choice = input()

            try:
                chosen_item : Item = next(item for item in ui_object if str(item.option) == choice)
                break
            except:
                print('\nInvalid input. Must choose from listed options:\n')
            
        chosen_item.operation()
        
    return menu



if __name__ == '__main__':

    x = lambda : print('\nhi!')
    y = lambda : print('\nhello!')
    z = lambda : print('\ngreetings!')

    my_list = [Item(1, 'greet informally', x),
               Item(2, 'greet formally', y),
               Item(3, 'greet very formally', z)]
    
    my_menu : Callable = generate_menu(my_list)
    my_menu()