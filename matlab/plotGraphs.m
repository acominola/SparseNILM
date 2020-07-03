clear

close all

HPE = 1;
FRE = 2;
CDE = 3;
UTE = 4;
GRE = 5;


%% Method 1

% Top5
% cell index: std of Gaussian noise
% [NDE, MAPE, F-Score] : columns
% [HPE, FRE, CDE, UTE, GRE] : rows

result1 = cell(1,5);
for i=1:5
    result1{i} = zeros(5,3);
end

batterySize1 = [2466, 3510, 8731, 8958, 11600];

result1{1}(:,1) = [1.14; 0.02; 13.39; 6.46; 0.2];
result1{1}(:,2) = [4.87; 4.19; 0.40; 22.54; 0.25];
result1{1}(:,3) = [98.92;99.77;99.73;98.10;99.72];

result1{2}(:,1) = [2.72;35.47;41.79;6.32;33.31];
result1{2}(:,2) = [74.89;10.92;6.02;150.24;9.28];
result1{2}(:,3) = [68.38;67.29;72.72;59.11;70.16];

result1{3}(:,1) = [5.15;45.62;51.86;11.16;41.99];
result1{3}(:,2) = [98.79;10.28;15.80;128.61;11.53];
result1{3}(:,3) = [59.56;58.60;62.95;50.98;59.73];

result1{4}(:,1) = [4.74;50.64;55.44;22.07;48.34];
result1{4}(:,2) = [152.11;10.60;19.60;114.62;11.25];
result1{4}(:,3) = [53.73;52.95;56.95;46.00;53.77];

result1{5}(:,1) = [5.20;53.87;61.78;29.10;52.76];
result1{5}(:,2) = [208.14;10.66;19.53;104.95;10.53];
result1{5}(:,3) = [49.47;49.21;53.10;42.87;50.06];

% NDE vs Battery size
nde = zeros(1,5);
for i=1:5
    nde(i)=mean(result1{i}(:,1));
end
subplot(3,1,1)
hold on
plot(batterySize1, nde)
title('Mean NDE vs Battery Size')

% MAPE vs Battery Size
mape = zeros(1,5);
for i=1:5
    mape(i)=mean(result1{i}(:,2));
end
subplot(3,1,2)
hold on
plot(batterySize1, mape)
title('Mean MAPE vs Battery Size')

% f-score vs battery size
fscore = zeros(1,5);
for i=1:5
    fscore(i)=mean(result1{i}(:,3));
end
subplot(3,1,3)
hold on
plot(batterySize1, fscore)
title('Mean F-score vs Battery Size')


%% Method 2

% Top5: Focus HPE
% cell index: std of Gaussian noise
% [NDE, MAPE, F-Score] : columns
% [HPE, FRE, CDE, UTE, GRE] : rows
result2HPE = cell(1,5);
for i=1:5
    result2HPE{i} = zeros(5,3);
end

batterySize2HPE  = [492, 1689, 2530, 3374, 2223, 2648];

result2HPE{1}(:,1) = [0.07;0.13;0.44;13.40;0.10];
result2HPE{1}(:,2) = [3.79;4.17;0.43;43.16;0.150];
result2HPE{1}(:,3) = [98.99;99.87;99.89;96.78;99.85];

result2HPE{2}(:,1) = [3.81;0.16;0.49;14.93;0.78];
result2HPE{2}(:,2) = [3.78;4.52;2.00;48.06;0.19];
result2HPE{2}(:,3) = [98.61;99.34;99.48;96.17;99.48];

result2HPE{3}(:,1) = [8.33;0.46;0.07;14.24;1.51];
result2HPE{3}(:,2) = [3.81;5.84;3.72;47.33;0.27];
result2HPE{3}(:,3) = [98.18;98.54;99.04;95.83;99.96];

result2HPE{4}(:,1) = [12.57;1.49;0.26;13.08;2.07];
result2HPE{4}(:,2) = [3.89;7.31;4.72;45.63;0.41];
result2HPE{4}(:,3) = [97.80;97.77;98.66;95.58;98.67];

result2HPE{5}(:,1) = [19.53;1.62;0.86;11.27;2.99];
result2HPE{5}(:,2) = [4.10;8.39;4.39;42.54;0.57];
result2HPE{5}(:,3) = [97.15;96.91;98.11;95.23;98.07];

result2HPE{6}(:,1) = [25.72;1.66;0.13;9.6;3.85];
result2HPE{6}(:,2) = [4.32;9.23;6.86;40.48;3.85];
result2HPE{6}(:,3) = [96.57;92.20;97.60;94.89;97.57];

% NDE vs Battery size
nde = zeros(1,6);
for i=1:6
    nde(i)=mean(result2HPE{i}(:,1));
end
subplot(3,1,1)
plot(batterySize2HPE, nde)
%title('NDE vs Battery Size')

% MAPE vs Battery Size
mape = zeros(1,6);
for i=1:6
    mape(i)=mean(result2HPE{i}(:,2));
end
subplot(3,1,2)
plot(batterySize2HPE, mape)
%title('MAPE vs Battery Size')

% f-score vs battery size
fscore = zeros(1,6);
for i=1:6
    fscore(i)=mean(result2HPE{i}(:,3));
end
subplot(3,1,3)
plot(batterySize2HPE, fscore)
%title('F-score vs Battery Size')

%% Method 2
% Top5: Focus CDE
% cell index: std of Gaussian noise
% [NDE, MAPE, F-Score] : columns
% [HPE, FRE, CDE, UTE, GRE] : rows
result2CDE = cell(1,5);
for i=1:5
    result2CDE{i} = zeros(5,3);
end

batterySize2CDE = [282, 345, 797, 1398, 2198, 1759];

result2CDE{1}(:,1) = [1.15;0.00;14.29;6.49;0.22];
result2CDE{1}(:,2) = [4.83;4.19;0.39;22.96;0.25];
result2CDE{1}(:,3) = [98.90;99.76;99.73;98.06;99.71];

result2CDE{2}(:,1) = [1.26;0.18;23.74;6.28;0.49];
result2CDE{2}(:,2) = [6.17;4.23;0.46;22.70;0.22];
result2CDE{2}(:,3) = [98.79;99.63;99.59;97.96;99.61];

result2CDE{3}(:,1) = [1.26;0.47;33.44;5.92;0.81];
result2CDE{3}(:,2) = [6.79;4.19;0.43;22.00;0.15];
result2CDE{3}(:,3) = [98.66;99.51;99.47;97.88;99.50];

result2CDE{4}(:,1) = [1.24;0.57;38.56;5.68;0.92];
result2CDE{4}(:,2) = [6.78;4.19;0.41;21.58;0.16];
result2CDE{4}(:,3) = [98.61;99.45;99.41;97.85;99.44];

result2CDE{5}(:,1) = [1.38;0.63;40.20;5.56;0.99];
result2CDE{5}(:,2) = [7.43;4.19;0.39;5.56;0.99];
result2CDE{5}(:,3) = [98.58;99.43;99.39;97.83;99.41];

result2CDE{6}(:,1) = [1.25;0.80;43.99;5.32;1.16];
result2CDE{6}(:,2) = [6.97;4.15;0.34;21.00;0.10];
result2CDE{6}(:,3) = [98.52;99.37;99.34;97.80;99.36];

% NDE vs Battery size
nde = zeros(1,6);
for i=1:6
    nde(i)=mean(result2CDE{i}(:,1));
end
subplot(3,1,1)
plot(batterySize2CDE, nde)
%title('NDE vs Battery Size')

% MAPE vs Battery Size
mape = zeros(1,6);
for i=1:6
    mape(i)=mean(result2CDE{i}(:,2));
end
subplot(3,1,2)
plot(batterySize2CDE, mape)
%title('MAPE vs Battery Size')

% f-score vs battery size
fscore = zeros(1,6);
for i=1:6
    fscore(i)=mean(result2CDE{i}(:,3));
end
subplot(3,1,3)
plot(batterySize2CDE, fscore)
%title('F-score vs Battery Size')

%% Method 3: Focus HPE
% [NDE, MAPE, F-Score] : columns
% [HPE, FRE, CDE, UTE, GRE] : rows

result3HPE = zeros(5,3);
batterySize3HPE = 11571;

result3HPE(:,1) = [0.43;0.15;0.42;0.96;0.18];
result3HPE(:,2) = [3.77;4.16;0.43;3.42;0.01];
result3HPE(:,3) = [99.05;99.91;99.92;99.69;99.92];

subplot(3,1,1)
plot(batterySize3HPE,mean(result3HPE(:,1)),'r*')
subplot(3,1,2)
plot(batterySize3HPE,mean(result3HPE(:,2)),'r*')
subplot(3,1,3)
plot(batterySize3HPE,mean(result3HPE(:,3)),'r*')

%% Method 3 : Focus CDE
% [NDE, MAPE, F-Score] : columns
% [HPE, FRE, CDE, UTE, GRE] : rows

result3CDE = zeros(5,3);
batterySize3CDE = 6015;

result3CDE(:,1) = [6.24;2.07;51.58;6.75;0.62];
result3CDE(:,2) = [47.70;6.41;1.30;24.67;0.02];
result3CDE(:,3) = [98.56;99.18;99.27;97.87;99.69];

subplot(3,1,1)
plot(batterySize3CDE,mean(result3CDE(:,1)),'b*')
subplot(3,1,2)
plot(batterySize3CDE,mean(result3CDE(:,2)),'b*')
subplot(3,1,3)
plot(batterySize3CDE,mean(result3CDE(:,3)),'b*')

%% Method 4: Focus HPE
% cell index: change in mean appliance power 0, 5, 10, 15
% [NDE, MAPE, F-Score] : columns
% [HPE, FRE, CDE, UTE, GRE] : rows
result4HPE = cell(1,4);
for i=1:4
    result4HPE{i} = zeros(5,3);
end

batterySize4HPE = [11571, 162872, 317692, 472511];

result4HPE{1}(:,1) = [0.43; 0.15;0.42;0.96;0.18];
result4HPE{1}(:,2) = [3.77;4.16;0.43;3.42;0.01];
result4HPE{1}(:,3) = [99.05;99.91;99.92;99.69;99.92];

result4HPE{2}(:,1) = [5.43;3.91;1.40;91.18;1.67];
result4HPE{2}(:,2) = [10.00;8.24;0.20;269.00;1.78];
result4HPE{2}(:,3) = [97.37;97.74;99.97;81.45;99.55];

result4HPE{3}(:,1) = [85.50;37.20;48.36;108.14;3.03];
result4HPE{3}(:,2) = [28.99;41.16;108.60;318.07;5.42];
result4HPE{3}(:,3) = [91.48;77.13;96.15;77.36;97.51];

result4HPE{4}(:,1) = [85.60;38.19;1.29;110.75;33.79];
result4HPE{4}(:,2) = [36.27;41.75;1.29;110.75;33.79];
result4HPE{4}(:,3) = [90.29;79.22;99.86;79.06;91.85];

% NDE vs Battery size
nde = zeros(1,4);
for i=1:4
    nde(i)=mean(result4HPE{i}(:,1));
end
subplot(3,1,1)
plot(batterySize4HPE, nde)
%title('NDE vs Battery Size')

% MAPE vs Battery Size
mape = zeros(1,4);
for i=1:4
    mape(i)=mean(result4HPE{i}(:,2));
end
subplot(3,1,2)
plot(batterySize4HPE, mape)
%title('MAPE vs Battery Size')

% f-score vs battery size
fscore = zeros(1,4);
for i=1:4
    fscore(i)=mean(result4HPE{i}(:,3));
end
subplot(3,1,3)
plot(batterySize4HPE, fscore)
%title('F-score vs Battery Size')

%% Method 4: Focus CDE
% cell index: change in mean appliance power 0, 5, 10, 15
% [NDE, MAPE, F-Score] : columns
% [HPE, FRE, CDE, UTE, GRE] : rows

result4CDE = cell(1,4);
for i=1:4
    result4CDE{i} = zeros(5,3);
end

batterySize4CDE = [6015,10826, 19682, 29487];

result4CDE{1}(:,1) = [6.24;2.07;51.58;6.75;0.62];
result4CDE{1}(:,2) = [47.70;6.41;1.30;24.67;0.02];
result4CDE{1}(:,3) = [98.56;99.18;99.27;97.87;99.69];

result4CDE{2}(:,1) = [9.30;1.59;48.76;7.91;0.09];
result4CDE{2}(:,2) = [69.01;5.36;1.31;26.08;0.02];
result4CDE{2}(:,3) = [98.70;99.68;99.55;98.05;99.95];

result4CDE{3}(:,1) = [9.08;0.28;53.37;28.96;0.10];
result4CDE{3}(:,2) = [83.31;4.13;1.87;83.95;0.05];
result4CDE{3}(:,3) = [93.84;99.95;99.28;94.24;99.93];

result4CDE{4}(:,1) = [7.19;0.50;53.27;84.87;0.05];
result4CDE{4}(:,2) = [92.34;4.27;2.08;241.78;0.17];
result4CDE{4}(:,3) = [88.21;99.88;99.29;83.70;99.92];

% NDE vs Battery size
nde = zeros(1,4);
for i=1:4
    nde(i)=mean(result4CDE{i}(:,1));
end
subplot(3,1,1)
plot(batterySize4CDE, nde)
%title('NDE vs Battery Size')

% MAPE vs Battery Size
mape = zeros(1,4);
for i=1:4
    mape(i)=mean(result4CDE{i}(:,2));
end
subplot(3,1,2)
plot(batterySize4CDE, mape)
%title('MAPE vs Battery Size')

% f-score vs battery size
fscore = zeros(1,4);
for i=1:4
    fscore(i)=mean(result4CDE{i}(:,3));
end
subplot(3,1,3)
plot(batterySize4CDE, fscore)
%title('F-score vs Battery Size')

%% Method 7

result7 = zeros(5,3);

batterySize7 = 12044;

result7(:,1) = [71.97; 10.14;74.26;92.57;70.80];
result7(:,2) = [132.48;15.75;271.53;293.22;73.66];
result7(:,3) = [89.96;91.45;91.21;77.98;80.79];

subplot(3,1,1)
plot(batterySize7,mean(result7(:,1)),'g*')
subplot(3,1,2)
plot(batterySize7,mean(result7(:,2)),'g*')
subplot(3,1,3)
plot(batterySize7,mean(result7(:,3)),'g*')

legend('m1','m2hpe','m2cde','m3hpe','m3cde','m4hpe','m4cde','m7')

%% Appliance-wise plot

% HPE
applIdx = 1;
figure
subplot(3,1,1) % HPE nde
hold on
nde = zeros(1,5);
for i=1:5
    nde(i)=result1{i}(applIdx,1);
end
plot(batterySize1, nde)
subplot(3,1,2) % HPE mape
hold on
mape = zeros(1,5);
for i=1:5
    mape(i)=result1{i}(applIdx,2);
end
plot(batterySize1, mape)
subplot(3,1,3) % HPE fscore
hold on
fscore = zeros(1,5);
for i=1:5
    fscore(i)=result1{i}(applIdx,3);
end
plot(batterySize1, fscore)

% NDE vs Battery size
nde = zeros(1,6);
for i=1:6
    nde(i)=result2HPE{i}(applIdx,1);
end
subplot(3,1,1)
plot(batterySize2HPE, nde)
title('HPE NDE vs Battery Size')

% MAPE vs Battery Size
mape = zeros(1,6);
for i=1:6
    mape(i)=result2HPE{i}(applIdx,2);
end
subplot(3,1,2)
plot(batterySize2HPE, mape)
title('HPE MAPE vs Battery Size')

% f-score vs battery size
fscore = zeros(1,6);
for i=1:6
    fscore(i)=result2HPE{i}(applIdx,3);
end
subplot(3,1,3)
plot(batterySize2HPE, fscore)
title('HPE F-score vs Battery Size')

% NDE vs Battery size
nde = zeros(1,6);
for i=1:6
    nde(i)=result2CDE{i}(applIdx,1);
end
subplot(3,1,1)
plot(batterySize2CDE, nde)
%title('NDE vs Battery Size')

% MAPE vs Battery Size
mape = zeros(1,6);
for i=1:6
    mape(i)=result2CDE{i}(applIdx,2);
end
subplot(3,1,2)
plot(batterySize2CDE, mape)
%title('MAPE vs Battery Size')

% f-score vs battery size
fscore = zeros(1,6);
for i=1:6
    fscore(i)=result2CDE{i}(applIdx,3);
end
subplot(3,1,3)
plot(batterySize2CDE, fscore)
%title('F-score vs Battery Size')

subplot(3,1,1)
plot(batterySize3HPE,result3HPE(applIdx,1),'r*')
subplot(3,1,2)
plot(batterySize3HPE,result3HPE(applIdx,2),'r*')
subplot(3,1,3)
plot(batterySize3HPE,result3HPE(applIdx,3),'r*')

subplot(3,1,1)
plot(batterySize3CDE,result3CDE(applIdx,1),'b*')
subplot(3,1,2)
plot(batterySize3CDE,result3CDE(applIdx,2),'b*')
subplot(3,1,3)
plot(batterySize3CDE,result3CDE(applIdx,3),'b*')

% NDE vs Battery size
nde = zeros(1,4);
for i=1:4
    nde(i)=result4HPE{i}(applIdx,1);
end
subplot(3,1,1)
plot(batterySize4HPE, nde)
%title('NDE vs Battery Size')

% MAPE vs Battery Size
mape = zeros(1,4);
for i=1:4
    mape(i)=result4HPE{i}(applIdx,2);
end
subplot(3,1,2)
plot(batterySize4HPE, mape)
%title('MAPE vs Battery Size')

% f-score vs battery size
fscore = zeros(1,4);
for i=1:4
    fscore(i)=result4HPE{i}(applIdx,3);
end
subplot(3,1,3)
plot(batterySize4HPE, fscore)
%title('F-score vs Battery Size')

% NDE vs Battery size
nde = zeros(1,4);
for i=1:4
    nde(i)=result4CDE{i}(applIdx,1);
end
subplot(3,1,1)
plot(batterySize4CDE, nde)
%title('NDE vs Battery Size')

% MAPE vs Battery Size
mape = zeros(1,4);
for i=1:4
    mape(i)=result4CDE{i}(applIdx,2);
end
subplot(3,1,2)
plot(batterySize4CDE, mape)
%title('MAPE vs Battery Size')

% f-score vs battery size
fscore = zeros(1,4);
for i=1:4
    fscore(i)=result4CDE{i}(applIdx,3);
end
subplot(3,1,3)
plot(batterySize4CDE, fscore)
%title('F-score vs Battery Size')

subplot(3,1,1)
plot(batterySize7,result7(applIdx,1),'g*')
subplot(3,1,2)
plot(batterySize7,result7(applIdx,2),'g*')
subplot(3,1,3)
plot(batterySize7,result7(applIdx,3),'g*')

legend('m1','m2hpe','m2cde','m3hpe','m3cde','m4hpe','m4cde','m7')

%% CDE

applIdx = 3;
figure
subplot(3,1,1) 
hold on
nde = zeros(1,5);
for i=1:5
    nde(i)=result1{i}(applIdx,1);
end
plot(batterySize1, nde)
subplot(3,1,2) 
hold on
mape = zeros(1,5);
for i=1:5
    mape(i)=result1{i}(applIdx,2);
end
plot(batterySize1, mape)
subplot(3,1,3)
hold on
fscore = zeros(1,5);
for i=1:5
    fscore(i)=result1{i}(applIdx,3);
end
plot(batterySize1, fscore)

% NDE vs Battery size
nde = zeros(1,6);
for i=1:6
    nde(i)=result2HPE{i}(applIdx,1);
end
subplot(3,1,1)
plot(batterySize2HPE, nde)
title('CDE NDE vs Battery Size')

% MAPE vs Battery Size
mape = zeros(1,6);
for i=1:6
    mape(i)=result2HPE{i}(applIdx,2);
end
subplot(3,1,2)
plot(batterySize2HPE, mape)
title('CDE MAPE vs Battery Size')

% f-score vs battery size
fscore = zeros(1,6);
for i=1:6
    fscore(i)=result2HPE{i}(applIdx,3);
end
subplot(3,1,3)
plot(batterySize2HPE, fscore)
title('CDE F-score vs Battery Size')

% NDE vs Battery size
nde = zeros(1,6);
for i=1:6
    nde(i)=result2CDE{i}(applIdx,1);
end
subplot(3,1,1)
plot(batterySize2CDE, nde)
%title('NDE vs Battery Size')

% MAPE vs Battery Size
mape = zeros(1,6);
for i=1:6
    mape(i)=result2CDE{i}(applIdx,2);
end
subplot(3,1,2)
plot(batterySize2CDE, mape)
%title('MAPE vs Battery Size')

% f-score vs battery size
fscore = zeros(1,6);
for i=1:6
    fscore(i)=result2CDE{i}(applIdx,3);
end
subplot(3,1,3)
plot(batterySize2CDE, fscore)
%title('F-score vs Battery Size')

subplot(3,1,1)
plot(batterySize3HPE,result3HPE(applIdx,1),'r*')
subplot(3,1,2)
plot(batterySize3HPE,result3HPE(applIdx,2),'r*')
subplot(3,1,3)
plot(batterySize3HPE,result3HPE(applIdx,3),'r*')

subplot(3,1,1)
plot(batterySize3CDE,result3CDE(applIdx,1),'b*')
subplot(3,1,2)
plot(batterySize3CDE,result3CDE(applIdx,2),'b*')
subplot(3,1,3)
plot(batterySize3CDE,result3CDE(applIdx,3),'b*')

% NDE vs Battery size
nde = zeros(1,4);
for i=1:4
    nde(i)=result4HPE{i}(applIdx,1);
end
subplot(3,1,1)
plot(batterySize4HPE, nde)
%title('NDE vs Battery Size')

% MAPE vs Battery Size
mape = zeros(1,4);
for i=1:4
    mape(i)=result4HPE{i}(applIdx,2);
end
subplot(3,1,2)
plot(batterySize4HPE, mape)
%title('MAPE vs Battery Size')

% f-score vs battery size
fscore = zeros(1,4);
for i=1:4
    fscore(i)=result4HPE{i}(applIdx,3);
end
subplot(3,1,3)
plot(batterySize4HPE, fscore)
%title('F-score vs Battery Size')

% NDE vs Battery size
nde = zeros(1,4);
for i=1:4
    nde(i)=result4CDE{i}(applIdx,1);
end
subplot(3,1,1)
plot(batterySize4CDE, nde)
%title('NDE vs Battery Size')

% MAPE vs Battery Size
mape = zeros(1,4);
for i=1:4
    mape(i)=result4CDE{i}(applIdx,2);
end
subplot(3,1,2)
plot(batterySize4CDE, mape)
%title('MAPE vs Battery Size')

% f-score vs battery size
fscore = zeros(1,4);
for i=1:4
    fscore(i)=result4CDE{i}(applIdx,3);
end
subplot(3,1,3)
plot(batterySize4CDE, fscore)
%title('F-score vs Battery Size')

subplot(3,1,1)
plot(batterySize7,result7(applIdx,1),'g*')
subplot(3,1,2)
plot(batterySize7,result7(applIdx,2),'g*')
subplot(3,1,3)
plot(batterySize7,result7(applIdx,3),'g*')

legend('m1','m2hpe','m2cde','m3hpe','m3cde','m4hpe','m4cde','m7')