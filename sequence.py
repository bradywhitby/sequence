'''
The sequence module takes a pecified sequence
and provides an iterable implementatin to loop through
the specified sequence
'''

SEQ_TYPES = [
    "alpha_numerical_both_case",
    "alpha_numerical_lower_case",
    "alpha_numerical_upper_case",
    "alpha_lower_case",
    "alpha_upper_case",
    "numerical",
    "hex",
    "custom"
]

class Seq:


    '''
    The Seq class is designed count in a specified sequence
    The class implements the __iter__ and __next__ methods
    to be an iteratable class
    '''
    def __init__(self, start_sequence, end_sequence=None,
            sequence_type="alpha_numerical_both_case", sequence_list=None):
        '''
        An iterable class to generate a specified sequence.

        Args:
            start_sequence (str): the start of the sequence
            end_sequence (str): the end of the sequence
            sequence_type (str): the type of the sequence
            sequence_list (list(str)): a custom sequence
        Returns:
            The instantiated instance of Seq
        Raises:
            ValueError: if sequence_type not in self.sequence_map.keys()

        Seq(str, str, str, [str,]) -> Seq()
        '''
        self.sequence_type = sequence_type
        self.__alpha_num = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
            'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
            'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4',
            '5', '6', '7', '8', '9'
        ]

        # converts string to list
        if isinstance(sequence_list, str):
            list(sequence_list)

        self.sequence_map = {
            "alpha_numerical_both_case": self.__alpha_num,
            "alpha_numerical_lower_case": self.sublist('a','z','0','9'),
            "alpha_numerical_upper_case": self.sublist('A','Z','0','9'),
            "alpha_lower_case": self.sublist('a','z'),
            "alpha_upper_case": self.sublist('A','Z'),
            "numerical": self.sublist('0','9'),
            "hex": self.sublist('0','9','A','F'),
            "custom": sequence_list
        }

        if sequence_type not in self.sequence_map.keys():
            raise ValueError("ValueError thrown. Argument \"sequence_type\" \
                must be in this list:\n{}".format(SEQ_TYPES))
        if sequence_type == "custom" \
                and (sequence_list is None \
                    or not isinstance(sequence_list, list)
                    or not isinstance(sequence_list, str)
                    or (
                        (isinstance(sequence_list, list)
                            or isinstance(sequence_list, str)
                        )
                        and len(sequence_list) < 2
                    )
                ):
            raise ValueError("ValueError thrown. Argument \"sequence_list\" must \
                contain a list of at least 2 strings elements or a string of at least 2 characters \
                when sequence_type == \"custom\"")

        self.sequence_list = self.sequence_map[self.sequence_type]
        self.start_sequence = start_sequence
        self.current_sequence = start_sequence
        self.end_sequence = end_sequence

        self.length = ""

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_sequence == self.end_sequence:
            raise StopIteration
        self.current_sequence = self.next_sequence()
        return self.current_sequence

    def next_sequence(self):
        ''''
        Sets self.current_sequence to the next sequence

        Returns self.current_sequence
        '''
        index_pos = [self.sequence_list.index(str(char)) for char in self.current_sequence]

        for index, value in reversed(list(enumerate(index_pos))):
            index_pos[index] = self.next_char_in_sequence(value)
            if index_pos[index] != 0:
                return ''.join([self.sequence_list[c] for c in index_pos])
        return self.current_sequence

    def next_char_in_sequence(self, index):
        '''
        Helper function to return the next character in the sequence
        given the current index position of the current sequence character
        '''
        if int(index) == len(self.sequence_list) - 1:
            return 0
        return int(index) + 1

    def sublist(self, *args):
        '''
        Helper function to generate different sublists from
        self.__alpha_num
        '''
        if len(args) == 2:
            return self.__alpha_num[self.__alpha_num.index(args[0]):
                self.__alpha_num.index(args[1]) + 1]
        return self.__alpha_num[self.__alpha_num.index(args[0]):
            self.__alpha_num.index(args[1]) + 1] + self.sublist(*args[2:])

    def __len__(self):
        return self.get_length()

    def get_length(self):
        '''
        Helper function to calculate the number of variations between the start and end sequence
        '''
        #101 = (1 × 2^0) + (0 × 2^1) + (1 × 2^2) = 5.
        #(value x base array length ^ index pos)
        if self.end_sequence is None:
            return ValueError

        num_list = []
        start_num = 0
        end_num = 0

        # get the value of each character
        for i in range(len(self.start_sequence)):
            start = self.start_sequence[i]
            start_index = self.sequence_list.index(start)

            end = self.end_sequence[i]
            end_index = self.sequence_list.index(end)

            num_entry = [start_index, end_index]
            num_list.append(num_entry)

        # reverse the list as bases conversion goes from right to left
        num_list.reverse()
        # get the total numerical value of the start and end sequence
        for j, value in list(enumerate(num_list)):
            start_num += (value[0] * len(self.sequence_list)**j)
            end_num += (value[1] * len(self.sequence_list)**j)

        return end_num - start_num

if __name__ == "__main__":
    start_seq = input("Start sequence: ")
    end_seq = input("End sequence: ")
    print("")
    for seq_types_index, seq_types_value in enumerate(SEQ_TYPES):
        print("{}: {}".format(seq_types_index, seq_types_value))
    seq_type = input("\nPlease enter a sequence type from the above selection\n\
   # you can enter the string or the corrisponding number: ")
    if seq_type.strip().isdigit():
        seq_type = SEQ_TYPES[int(seq_type)]
    seq_list = []
    if seq_type == "custom":
        seq_list = input("Please enter a sequence string or list: ")
    seq = Seq(start_seq, end_seq, seq_type, seq_list)
    print(seq.current_sequence)
    for each in seq:
        print(each)
    seq.get_length()
