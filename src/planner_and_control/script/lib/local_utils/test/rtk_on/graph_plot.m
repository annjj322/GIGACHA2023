close all
clear all

high = csvread('gps_high2.csv');
low = csvread('gps_low1.csv');
static = csvread('gps_static1.csv');

high_iter = high(:,1);
high_value = high(:,2);

low_iter = low(:,1);
low_value = low(:,2);

static_iter = static(:,1);
static_value = static(:,2);

plot(high_iter,high_value,'-',low_iter,low_value,'-.',static_iter,static_value,'.')
title('RTK ON')
xlabel('iteration')
ylabel('hAcc[mm]')
grid on
xlim([0,80])
ylim([10, 20])
legend('high','low','static')