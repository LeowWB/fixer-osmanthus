python3 build_test_LM.py -b input.train.txt -t input.test.txt -o input.predict.txt
python3 eval.py input.predict.txt input.correct.txt

