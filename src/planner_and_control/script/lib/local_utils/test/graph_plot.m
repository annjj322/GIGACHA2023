close all
clear all

high = csvread('data2High.csv');
low = csvread('data2Low.csv');

high_iter = high(:,1);
high_ahrs = high(:,2);
high_gps = high(:,3);

low_iter = low(:,1);
low_ahrs = low(:,2);
low_gps = low(:,3);

plot(low_iter, low_ahrs,'-',low_iter,low_gps,'-.')
title('Low speed heading')
xlabel('iteration')
ylabel('Heading[deg]')
grid on
xlim([0,100])
ylim([45, 65])
legend('AHRS','GPS')