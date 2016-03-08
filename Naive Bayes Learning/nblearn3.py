import sys
from nbhelper import build_class_from_file, smoothing_the_words, calculate_total_words_in_class, build_count_values, write_model


def main():
    word_list = {}
    classes = ["p", "n", "t", "d"]
    input_directory = sys.argv[1]
    directory_list = ["/positive*/**/**/*.txt", "/negative*/**/**/*.txt", "/**/truthful*/**/*.txt", "/**/deceptive*/**/*.txt"]
    for path in range(len(directory_list)):
        build_class_from_file(input_directory + directory_list[path], classes[path], classes, word_list)
    smoothing_the_words(word_list, classes)

    prob_matrix = {'data': word_list}
    c_1 = calculate_total_words_in_class(word_list, classes[0])
    c_2 = calculate_total_words_in_class(word_list, classes[1])
    c_3 = calculate_total_words_in_class(word_list, classes[2])
    c_4 = calculate_total_words_in_class(word_list, classes[3])
    build_count_values(prob_matrix, classes, c_1, c_2, c_3, c_4)

    write_model(prob_matrix)
    return


if __name__ == "__main__":
    main()

