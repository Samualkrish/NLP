import sys


def main():
    characters = list(sys.argv[1])
    final_anagram_list = []
    final_anagram_list.append(characters[0])
    permutation = 1
    for i in range(1, len(characters)):
        k = 0
        temp = final_anagram_list
        final_anagram_list = []
        permutation = permutation * (i + 1)
        while len(final_anagram_list) < permutation:
            position = 0
            current_word = list(temp[k])
            while position < len(current_word) + 1:
                anagram = current_word
                anagram.insert(position, characters[i])
                position = position + 1
                final_anagram_list.append(''.join(anagram))
            k = k + 1

    final_anagram_list.sort()
    try:
        output_file_name = "anagram_out.txt"
        file = open(output_file_name, "w+")
        for k in range(len(final_anagram_list)):
            file.write("%s\n" % final_anagram_list[k])
        file.close()
    except IOError as e:
        print("I/O Error {0}-{1}".format(e.errno,e.strerror))


if __name__ == '__main__':
    main()
