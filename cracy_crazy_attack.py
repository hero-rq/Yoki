import itertools

class LFSR:
    def __init__(self, seed, feedback_positions):
        self.state = [int(bit) for bit in seed]
        self.feedback_positions = [int(pos) for pos in feedback_positions]

    def shift(self):
        feedback_bit = self.state[self.feedback_positions[0]]
        for pos in self.feedback_positions[1:]:
            feedback_bit ^= self.state[pos]
        stream_bit = self.state[-1]
        self.state = [feedback_bit] + self.state[:-1]
        return stream_bit

def combining_function(x1, x2, x3):
    if (x1, x2, x3) == (0, 0, 0):
        return 0
    elif (x1, x2, x3) == (0, 0, 1):
        return 1
    elif (x1, x2, x3) == (0, 1, 0):
        return 0
    elif (x1, x2, x3) == (0, 1, 1):
        return 1
    elif (x1, x2, x3) == (1, 0, 0):
        return 0
    elif (x1, x2, x3) == (1, 0, 1):
        return 0
    elif (x1, x2, x3) == (1, 1, 0):
        return 1
    elif (x1, x2, x3) == (1, 1, 1):
        return 1

def run_lfsr_for_keystream(lfsr, length):
    return [lfsr.shift() for _ in range(length)]

if __name__ == "__main__":
    provided_keystream = "1010111000011110011000101111110110101100010110011110101011011011111100111100100001011110011001011000101110100100110000011111110110100111111000101001100011011000110101011011011101111111111000001001110010100101100100110011010101111110010001110010001110110111001100100101111101110011001100001100001000010101111111110100000000001111110010101001101011000001001110011111011011011111001101011011110001001101110001100101010101101000011010000111011111111111111111011111111010111111111100011000101101000111011110011011100110010001110101010000111111101011000000000100001001111111111101111110100000000011011111101110111110011010010000011111111010000000000110000101100111010101011011011110001001100001001100111110111100111100000100000001000010111011110111111111111111111011111101000011001111001101100111111010011101100011001001110000000000001000000010100111101101101101010110000100000100110011011001011001011011100011111011111011010100111000000111000000100000001010011110110110111101111010000111000111010001110011001001110000000000000110101010101010010000000001010101011001111100000110000101000100110001110001110000001100001011110111010101111011011111111101111100101100011001111111101001111001111001000111100000110000000100000001010000010011111101101101111011110100001100011101000111001100100111000000000000011010101010101001000000000010101010110011111000001100001010001001100011100011100000011000010111101110101011110110111111111011111001011000110011111111010011110011110010001111000001100000001000000010100000100111111011011011110111101000011000111010001110011001001110000000000000110101010101010010000000001010101011001111100000110000101000100110001110001110000001100001011110111010101111011011111111101111100101100011001111111101001111001111001000111100000110000000100000001010000010"
    provided_keystream_list = [int(bit) for bit in provided_keystream]
    chunk_size = len(provided_keystream_list)

    initial_states_list2 = [f"{i:011b}" for i in range(128)]
    initial_states_list3 = [f"{i:013b}" for i in range(128)]
    feedback2 = [10, 1]
    feedback3 = [12, 2, 3, 0]

    initial_states_list1 = [f"{i:07b}" for i in range(128)]
    feedback1 = [6, 0]
    lfsr1_outputs = {}
    for state in initial_states_list1:
        lfsr = LFSR(state, feedback1)
        output = tuple(run_lfsr_for_keystream(lfsr, chunk_size))
        lfsr1_outputs[output] = state

    match_found = False
    for initial_state2 in initial_states_list2:
        lfsr2 = LFSR(initial_state2, feedback2)
        e_keystream = run_lfsr_for_keystream(lfsr2, chunk_size)

        for initial_state3 in initial_states_list3:
            lfsr3 = LFSR(initial_state3, feedback3)
            f_keystream = run_lfsr_for_keystream(lfsr3, chunk_size)

            d_keystream = []
            conflict = False
            for i in range(chunk_size):
                if e_keystream[i] == f_keystream[i]:
                    if provided_keystream_list[i] != e_keystream[i]:
                        conflict = True
                        break
                    else:
                        d_keystream.append(None)
                else:
                    if provided_keystream_list[i] == e_keystream[i]:
                        d_keystream.append(1)
                    elif provided_keystream_list[i] == f_keystream[i]:
                        d_keystream.append(0)
                    else:
                        conflict = True
                        break

            if conflict:
                continue

            possible_d_keystreams = []
            indices = [i for i, bit in enumerate(d_keystream) if bit is None]
            for bits in itertools.product([0, 1], repeat=len(indices)):
                temp_keystream = d_keystream[:]
                for idx, bit in zip(indices, bits):
                    temp_keystream[idx] = bit
                possible_d_keystreams.append(tuple(temp_keystream))

            for d_keystream_candidate in possible_d_keystreams:
                if d_keystream_candidate in lfsr1_outputs:
                    print(f"Matching keystream found!")
                    print(f"Initial state for LFSR1 (d_j): {lfsr1_outputs[d_keystream_candidate]}")
                    print(f"Initial state for LFSR2 (e_j): {initial_state2}")
                    print(f"Initial state for LFSR3 (f_j): {initial_state3}")
                    match_found = True
                    break

            if match_found:
                break
        if match_found:
            break

    if not match_found:
        print("No matching keystream found.")
