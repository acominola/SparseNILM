#!/bin/bash
#
# RUN FOR STATUS: clear; tail -n 1 *.log
#

#BUILD SSHMM FOR TESTING
./train_SSHMM.py BigO_L02 AMPdsR1_1min_A_top2 10 200 noisy 4 3 HPE,FRE > logs/BigO_L02.log &
./train_SSHMM.py BigO_L03 AMPdsR1_1min_A_top3 10 200 noisy 4 3 HPE,FRE,CDE > logs/BigO_L03.log&
./train_SSHMM.py BigO_L04 AMPdsR1_1min_A_top4 10 200 noisy 4 3 HPE,FRE,CDE,UTE > logs/BigO_L04.log &
./train_SSHMM.py BigO_L05 AMPdsR1_1min_A_top5 10 200 noisy 4 3 HPE,FRE,CDE,UTE,GRE > logs/BigO_L05.log &
./train_SSHMM.py BigO_L06 AMPdsR1_1min_A_top6 10 200 noisy 4 3 HPE,FRE,CDE,UTE,GRE,TVE > logs/BigO_L06.log &
./train_SSHMM.py BigO_L07 AMPdsR1_1min_A_top7 10 200 noisy 4 3 HPE,FRE,CDE,UTE,GRE,TVE,FGE > logs/BigO_L07.log &
./train_SSHMM.py BigO_L08 AMPdsR1_1min_A_top8 10 200 noisy 4 3 HPE,FRE,CDE,UTE,GRE,TVE,FGE,EQE > logs/BigO_L08.log &
./train_SSHMM.py BigO_L09 AMPdsR1_1min_A_top9 10 200 noisy 4 3 HPE,FRE,CDE,UTE,GRE,TVE,FGE,EQE,BME > logs/BigO_L09.log &
./train_SSHMM.py BigO_L10 AMPdsR1_1min_A_top10 10 200 noisy 4 3 HPE,FRE,CDE,UTE,GRE,TVE,FGE,EQE,BME,OFE > logs/BigO_L10.log &
