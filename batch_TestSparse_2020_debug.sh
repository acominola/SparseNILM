#!/bin/bash
#
# RUN FOR STATUS: clear; tail -n 1 *.log
#

#TEST SPARSE VITERBI

#python3 ./test_Algorithm.py sVa_BigO_L10 BigO_L10 AMPdsR1_1min_A_top10 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L10.log
#python3 ./test_Algorithm.py sVa_BigO_L10 BigO_L10 AMPdsR1_1min_A_top10_m1 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L10_m1.log
#python3 ./test_Algorithm.py sVa_BigO_L10 BigO_L10 AMPdsR1_1min_A_top10_m2 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L10_m2.log
#python3 ./test_Algorithm.py sVa_BigO_L10 BigO_L10 AMPdsR1_1min_A_top10_m3 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L10_m3.log
#python3 ./test_Algorithm.py sVa_BigO_L10 BigO_L10 AMPdsR1_1min_A_top10_m4 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L10_m4.log
#python3 ./test_Algorithm.py sVa_BigO_L10 BigO_L10 AMPdsR1_1min_A_top10_m5 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L10_m5.log
#python3 ./test_Algorithm.py sVa_BigO_L10 BigO_L10 AMPdsR1_1min_A_top10_m6 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L10_m6.log

#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5_m1_1 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5_m1_1.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5_m1_2 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5_m1_2.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5_m1_3 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5_m1_3.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5_m1_4 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5_m1_4.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5_m1_5 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5_m1_5.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5_m1_6 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5_m1_6.log

#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5HPE_m2_1 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5HPE_m2_1.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5HPE_m2_2 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5HPE_m2_2.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5HPE_m2_3 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5HPE_m2_3.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5HPE_m2_4 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5HPE_m2_4.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5HPE_m2_5 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5HPE_m2_5.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5HPE_m2_6 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5HPE_m2_6.log

#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5CDE_m2_1 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5CDE_m2_1.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5CDE_m2_2 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5CDE_m2_2.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5CDE_m2_3 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5CDE_m2_3.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5CDE_m2_4 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5CDE_m2_4.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5CDE_m2_5 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5CDE_m2_5.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5CDE_m2_6 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5CDE_m2_6.log

#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5CDE_m3 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5CDE_m3.log

#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5HPE_m3 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5HPE_m3.log

#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5HPE_m4_0 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5HPE_m4_0.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5HPE_m4_1 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5HPE_m4_1.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5HPE_m4_2 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5HPE_m4_2.log
#python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5HPE_m4_3 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5HPE_m4_3.log

python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5CDE_m4_0 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5CDE_m4_0.log
python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5CDE_m4_1 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5CDE_m4_1.log
python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5CDE_m4_2 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5CDE_m4_2.log
python3 ./test_Algorithm.py sVa_BigO_L5 BigO_L05 AMPdsR1_1min_A_top5CDE_m4_3 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L5CDE_m4_3.log

#python3 ./test_Algorithm.py sVa_BigO_L10 BigO_L10 AMPdsR1_1min_A_top10_m2_1 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L10_m2_1.log
#python3 ./test_Algorithm.py sVa_BigO_L10 BigO_L10 AMPdsR1_1min_A_top10_m2_2 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L10_m2_2.log
#python3 ./test_Algorithm.py sVa_BigO_L10 BigO_L10 AMPdsR1_1min_A_top10_m2_3 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L10_m2_3.log
#python3 ./test_Algorithm.py sVa_BigO_L10 BigO_L10 AMPdsR1_1min_A_top10_m2_4 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L10_m2_4.log
#python3 ./test_Algorithm.py sVa_BigO_L10 BigO_L10 AMPdsR1_1min_A_top10_m2_5 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L10_m2_5.log
#python3 ./test_Algorithm.py sVa_BigO_L10 BigO_L10 AMPdsR1_1min_A_top10_m2_6 10 A noisy 52000 SparseViterbi > logs/sVa_BigO_L10_m2_6.log
