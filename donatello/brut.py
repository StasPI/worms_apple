from datetime import datetime
from itertools import permutations

start_time = datetime.now()
cont_pass = 'w_t2w'

# Blanks for the combination.
small_eng_letters = 'qwertyuiopasdfghjklzxcvbnm'
big_eng_letters = 'QWERTYUIOPASDFGHJKLZXCVBNM'
small_rus_letters = 'йцукенгшщзхъфывапролджэячсмитьбю'
big_rus_letters = 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
symbols = r'!"#$%&\'()*+,-./:;<=>?@[]^_`{|}~'
numbers = '1234567890'
# Password character limits from \ to (inclusive).
min_long_pass = 1
max_long_pass = 4


def brut(min_long_pass, max_long_pass, *args, **kwargs):
    # Password function.
    args_mix = ''.join(args)
    run = True
    while run:
        combinations = permutations(args_mix, min_long_pass)
        for find_pass in combinations:
            find_pass = ''.join(find_pass)
            if cont_pass == find_pass:
                run = False
                return find_pass
        if min_long_pass < max_long_pass:
            min_long_pass += 1
        else:
            find_pass = None
            return find_pass


find_pass = brut(min_long_pass, max_long_pass, small_eng_letters, numbers, symbols)

finish_time = datetime.now()

if find_pass is None:
    print('The time wasted: ' + str(finish_time - start_time))
else:
    print(find_pass + ' correct password! Time spent on searching: ' +
          str(finish_time - start_time))
