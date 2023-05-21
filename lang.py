import json
import ui
from typing import Callable


class WordPair:

    eng : str
    span : str

    def __hash__(self):
        return hash( (self.eng, self.span) )
    
    def __eq__(self, other):
        
        try:
            if self.eng == other.eng and self.span == other.span:
                return True
            return False
        
        except:
            return False
    
    def __str__(self):
        
        spacing = ' ' * (20 - len(self.span))
        return f'Spanish: {self.span}{spacing}English: {self.eng}'



class LangLearner:


    word_sets : dict


    def __init__(self):

        print('Welcome to lang-learner.')

        with open('data.txt') as saved_data:
            self.word_sets = saved_data

        self.main_menu()
    
    def __del__(self):

        with open('data.txt') as saved_data:
            saved_data.write(json.dumps(self.word_sets))



    def main_menu(self):
        
        print('\nMain menu:\n\n')

        menu_items = [ui.Item(cat, f'navigate to category {cat}', self.navigate_category(cat)) for cat in self.word_sets.keys()]
        menu_items += [ui.Item(1, 'add a new category', add_category),
                      ui.Item(2, 'remove a category', remove_category),
                      ui.Item(0, 'exit', lambda: print('\n Saving and exiting...'))]
        
        final_menu : Callable = ui.generate_menu(menu_items)
        final_menu()


        def add_category():

            new_category = input(f'\nEnter the name of the new category you wish to create.')

            if new_category not in self.word_sets.keys():
                self.word_sets[new_category] = {}
                print('\nNew category created.')
            else:
                print('\nNew category already exists! Nothing was changed.')


        def remove_category():
            
            old_category = input(f'\nEnter the name of the category you wish to remove.')

            if old_category in self.word_sets.keys():
                self.word_sets.pop(old_category)
                print('\nCategory successfully removed.')
            else:
                print('\nCategory not found! Nothing was changed.')

    
    
    def navigate_category(self, category_name : str):
        
        print(f'\n category "{category_name}":\n\n')
        word_pairs = self.word_sets[category_name]

        menu_items = [ui.Item(1, 'see word pairs', see_word_pairs),
                      ui.Item(2, 'add a new word pair', add_word_pair),
                      ui.Item(3, 'remove a word pair', remove_word_pair),
                      ui.Item(4, 'see sub_categories of current category', see_sub_categories),
                      ui.Item(5, 'copy this category to another category', copy_category),
                      ui.Item(6, 'guess the english for words in this category', guess_english),
                      ui.Item(7, 'guess the spanish for words in this category', guess_spanish),
                      ui.Item(0, 'return to main menu', self.main_menu)
                      ]
        
        final_menu : Callable = ui.generate_menu(menu_items)
        final_menu()
        

        def see_word_pairs():
            
            print(f'\nAll word pairs:\n')
            [print(word_pair) for word_pair in word_pairs]
            self.navigate_category(category_name)
        

        def add_word_pair():
            
            new_pair = WordPair()
            new_pair.span = input(f'\nEnter the spanish word of the new word pair:')
            new_pair.eng = input(f'\nEnter the english word of the new word pair:')

            if new_pair not in word_pairs:
                word_pairs.add(new_pair)
                print(f'\nNew pair successfully added.')
            else:
                print(f'\nPair already exists. Nothing was changed.')


        def remove_word_pair():
            
            pair = WordPair()
            pair.span = input(f'\nEnter the spanish word of the pair to delete:')
            pair.eng = input(f'\nEnter the english word of the pair to delete:')

            if pair in word_pairs:
                word_pairs.delete(pair)
                print(f'\nPair successfully deleted.')
            else:
                print(f'\nPair does not exist. Nothing was changed.')


        def see_sub_categories():
            
            pass

        def copy_category():
            pass

        def guess_english():
            pass

        def guess_spanish():
            pass




if __name__ == '__main__':

    WordPair()