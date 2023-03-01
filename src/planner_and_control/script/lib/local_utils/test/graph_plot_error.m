close all
clear all

high = csvread('data2High.csv');
low = csvread('data2Low.csv');

high_iter = high(:,1);
high_ahrs_error = high(:,4);
high_gps_error = high(:,5);

low_iter = low(:,1);
low_ahrs_error = low(:,4);
low_gps_error = low(:,5);

plot(high_iter, high_ahrs_error,'-',high_iter,high_gps_error,'-.')
title('High speed heading error (Ref 45[deg])')
xlabel('iteration')
ylabel('Error[%]')
grid on
xlim([0,100])
ylim([5, 25])
legend('AHRS','GPS')