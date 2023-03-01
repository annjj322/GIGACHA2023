close all
clear all

high = csvread('high_emit.csv');
low = csvread('low_emit.csv');
static = csvread('static.csv');

high_iter = high(:,1);
high_value = high(:,2);

low_iter = low(:,1);
low_value = low(:,2);

static_iter = static(:,1);
static_value = static(:,2);

plot(high_iter,high_value,'-',low_iter,low_value,'-.',static_iter,static_value,'.')
title('RTK OFF')
xlabel('iteration')
ylabel('hAcc[mm]')
grid on
xlim([0,80])
ylim([200, 1400])
legend('10km/h','5km/h','static')