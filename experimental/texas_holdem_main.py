import experimental.texas_holdem as texas_holdem

# -*- coding: utf-8 -*-
# import sys
# from io import TextIOWrapper
# sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding='UTF-8', errors='replace')

def main():
    runner = texas_holdem.TexasHoldem()

    runner.play_one_hand()

if __name__ == "__main__":
    main()