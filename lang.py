import pickle
import ui
from typing import Callable


def adjust_collection(collection, io_searcher : Callable, adjuster : Callable, intention : str = 'deletion'):

    obj = io_searcher(intention)

    if (obj in collection) == (intention == 'deletion'):
        adjuster(obj)
        print(f'\n{intention} was successful.')
    else:
        print(f'\n{intention} was redundant. Nothing was changed.')


def guess_words(collection : set, reverse_translation : bool = False):
    
    correctly_guessed_word_pairs = cg = set()
    incorrectly_guessed_word_pairs = ig = set()
    skipped_word_pairs = sg = set()

    collection = {WordPair(word_pair.span, word_pair.eng) for word_pair in collection} if reverse_translation else collection
    
    for word_pair in collection:

        word_guess = input(f'\nTranslate the word {word_pair.eng} (or enter 1 to skip or 0 to exit):\n')

        match word_guess:

            case word_pair.span:
                print('\nCorrect!')
                correctly_guessed_word_pairs.add(word_pair)
            
            case '1':
                print('\nWord skipped.')
                skipped_word_pairs.add(word_pair)
            
            case '0':
                break

            case _:
                print(f'\nIncorrect. Correct word was {word_pair.span}.')
                incorrectly_guessed_word_pairs.add(word_pair)
    
    print(f'\nPercentage guessed correctly: {(len(cg)*100)/(len(cg)+len(ig)+len(sg))}%')
    print(f'Percentage guessed incorrectly: {(len(ig)*100)/(len(cg)+len(ig)+len(sg))}%')
    print(f'Percentage skipped: {(len(sg)*100)/(len(cg)+len(ig)+len(sg))}%')
    
    collection = {WordPair(word_pair.span, word_pair.eng) for word_pair in collection} if reverse_translation else collection




class WordPair:

    eng : str
    span : str

    def __init__(self, eng, span):
        self.eng = eng
        self.span = span

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

        with open('data.txt', 'rb') as saved_data:
            self.word_sets = pickle.load(saved_data)

        self.main_menu()
    
    def __del__(self):

        with open('data.txt', 'wb') as saved_data:
            pickle.dump(self.word_sets, saved_data, pickle.HIGHEST_PROTOCOL)



    def main_menu(self):


        def io_searcher(intention : str):
            return input(f'\nEnter the name of the category intended for {intention}\n')

        def add_category():
            adjust_collection(cats.keys(), io_searcher, lambda cat : cats.update({ cat : set() }), intention = 'creation')
            self.main_menu()

        def remove_category():
            adjust_collection(cats.keys(), io_searcher, cats.pop, intention = 'deletion')
            self.main_menu()


        print('\nMain menu:\n')
        cats = self.word_sets
        menu_items = [ui.Item(cat, f'navigate to category "{cat}"', lambda cat = cat: self.navigate_category(cat)) for cat in cats.keys()]
        menu_items += [ui.Item(1, 'add a new category', add_category),
                      ui.Item(2, 'remove a category', remove_category),
                      ui.Item(0, 'exit', lambda: print('\nSaving and exiting...\n'))]

        final_menu : Callable = ui.generate_menu(menu_items)
        final_menu()

    
    
    def navigate_category(self, category_name : str):
        

        def see_word_pairs():
            
            print(f'\nAll word pairs:\n')
            [print(word_pair) for word_pair in pairs]
            self.navigate_category(category_name)
        

        def io_searcher(intention : str):

            span = input(f'\nEnter the spanish word of the pair intended for {intention}\n')
            eng = input(f'\nEnter the english word of the pair intended for {intention}\n')
            return WordPair(eng, span)


        def add_word_pair():
            adjust_collection(pairs, io_searcher, pairs.add, intention = 'creation')
            self.navigate_category(category_name)

        def remove_word_pair():
            adjust_collection(pairs, io_searcher, pairs.remove, intention = 'deletion')
            self.navigate_category(category_name)


        def see_sub_categories():
            
            menu_items = [ui.Item(cat, f'navigate to {cat}', lambda cat = cat: self.navigate_category(cat)) \
                          for cat in self.word_sets.keys() if self.word_sets[cat] < pairs]
            menu_items.append(ui.Item(0, f'return to original category', lambda: self.navigate_category(category_name)))

            sub_category_menu : Callable = ui.generate_menu(menu_items)
            sub_category_menu()
            

        def copy_category():
            
            menu_items = [ui.Item(cat, f'copy {category_name} into {cat}', lambda cat = cat: self.word_sets[cat].update(pairs)) \
                           for cat in self.word_sets.keys()]
            menu_items.append(ui.Item(0, f'abort copying', lambda: None))

            copy_category_menu : Callable = ui.generate_menu(menu_items)
            copy_category_menu()
            self.navigate_category(category_name)


        def guess_english():
            guess_words(pairs, True)
            self.navigate_category(category_name)

        def guess_spanish():
            guess_words(pairs)
            self.navigate_category(category_name)



        print(f'\ncategory "{category_name}":\n')
        pairs = self.word_sets[category_name]

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
        


if __name__ == '__main__':

    LangLearner()