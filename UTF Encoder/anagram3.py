import sys


def main():
    # Get the words as input and convert into the character list
    characters = list(sys.argv[1])

    # Start preparing the list
    final_anagram_list = []

    # Append the first character
    final_anagram_list.append(characters[0])
    permutation = 1

    # Loop through the rest of the characters
    for i in range(1, len(characters)):
        k = 0

        # Copy into a temp table and initialize the final list
        temp = final_anagram_list
        final_anagram_list = []

        # Calculate the permutation
        permutation = permutation * (i + 1)

        # Length of the final list less than the permutation
        while len(final_anagram_list) < permutation:
            # Start with position 0
            position = 0

            # Assign the current word to the
            current_word = list(temp[k])

            # Do the loop until you
            while position < len(current_word) + 1:
                anagram = []
                m = 0
                for l in range(len(current_word) + 1):
                    if l == position:
                        anagram.append(characters[i])
                    else:
                        anagram.append(current_word[m])
                        m = m + 1
                position = position + 1
                final_anagram_list.append(''.join(anagram))
            k += 1

    final_anagram_list.sort()

    file = open('anagram_out.txt', 'w+')
    for k in range(len(final_anagram_list)):
        file.write("%s\n" % final_anagram_list[k])
    file.close()


if __name__ == '__main__':
    main()
