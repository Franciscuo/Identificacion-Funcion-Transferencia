clear all;
close all;
clc;

h=openfig('Enfriamento.fig','invisible');
h=findobj(gca,'Type','line');
x=get(h,'XData');
x=x{2};
y=get(h,'YData');
y=y{2};
A=[];
A(:,1)=x;
A(:,2)=y;
dlmwrite('prueba1.txt',A,',');
