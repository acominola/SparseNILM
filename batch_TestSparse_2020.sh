#!/bin/bash
#
# RUN FOR STATUS: clear; tail -n 1 *.log
#

#TEST SPARSE VITERBI
./test_Algorithm.py sVa_BigO_L02 BigO_L02 AMPdsR1_1min_A_top2 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L02.log
./test_Algorithm.py sVa_BigO_L03 BigO_L03 AMPdsR1_1min_A_top3 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L03.log
./test_Algorithm.py sVa_BigO_L04 BigO_L04 AMPdsR1_1min_A_top4 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L04.log
./test_Algorithm.py sVa_BigO_L05 BigO_L05 AMPdsR1_1min_A_top5 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L05.log
./test_Algorithm.py sVa_BigO_L06 BigO_L06 AMPdsR1_1min_A_top6 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L06.log
./test_Algorithm.py sVa_BigO_L07 BigO_L07 AMPdsR1_1min_A_top7 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L07.log
./test_Algorithm.py sVa_BigO_L08 BigO_L08 AMPdsR1_1min_A_top8 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L08.log
./test_Algorithm.py sVa_BigO_L09 BigO_L09 AMPdsR1_1min_A_top9 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L09.log
./test_Algorithm.py sVa_BigO_L10 BigO_L10 AMPdsR1_1min_A_top10 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L10.log 
