import sys
import glob
from nbsuffixstrip import suffix_strip
from nbhelper import read_model, read_file, probability, max_of_positive_or_negative, max_of_truthful_or_deceptive, write_to_file


def main():
    input_dir = sys.argv[1]
    classes = ["p", "n", "t", "d"]
    li = []
    model = eval(read_model())
    for file_name in glob.glob(input_dir + '**/**/**/*.txt'):
        words = read_file(file_name)
        wordlist = []
        for word in words:
            word = suffix_strip(word)
            wordlist.append(word)
        c_p = probability(model, wordlist, classes[0])
        c_n = probability(model, wordlist, classes[1])
        c_t = probability(model, wordlist, classes[2])
        c_d = probability(model, wordlist, classes[3])
        li.append(max_of_truthful_or_deceptive(c_t, c_d) + ' ' + max_of_positive_or_negative(c_p, c_n) + ' ' + file_name)
    write_to_file(li)

main()
