import os
from build_test_LM_funcs import build_LM, test_LM

input_file_b = 'input.train.txt'
input_file_t = 'input.test.txt'
input_file_u = 'input.unlabeled_train.txt'
output_file = 'input.predict.txt'

for pad in [True, False]:
    for homogenize_digits in [True, False]:
        for no_punc in [True, False]:
            for lowercase in [True, False]:
                for smooth_unseen in [True, False]:
                    print(f'pad={pad}, homogenize_digits={homogenize_digits}, no_punc={no_punc}, lowercase={lowercase}, smooth_unseen={smooth_unseen}')

                    LM = build_LM(input_file_b, pad, homogenize_digits, no_punc, lowercase)
                    test_LM(input_file_t, output_file, LM, pad, homogenize_digits, no_punc, lowercase, smooth_unseen)
                    os.system('python3 eval.py input.predict.txt input.correct.txt')
                    
                    test_LM(input_file_u, output_file, LM, pad, homogenize_digits, no_punc, lowercase, smooth_unseen)
                    os.system('python3 eval.py input.predict.txt input.train.txt')
