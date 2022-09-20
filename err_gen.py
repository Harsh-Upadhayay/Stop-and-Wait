import random

class err_gen() :

    def induce_err(self, in_str) :
        chk = (int)(random.random() * 1000) % 2
        
        if not chk :
            return in_str

        idx = (int)(random.random() * 1000) % len(in_str)
        f_bit = '*'
        if in_str[idx] == '0':
            f_bit = '1'
        else :
            f_bit = '0'

        out_str = in_str[ : idx] + f_bit + in_str[idx + 1 : ]

        return out_str

if __name__ == "__main__":
    print(" 1001010", '\n', err_gen().induce_err("1001010"))
