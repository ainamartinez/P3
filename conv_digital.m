%Convolució digital
function [y,ny] = conv_digital(x,nx,h,nh)
% x: senyal d’entrada
% nx: vector d’índex mostral de x
% h: filtre
% nh: vector d’índex mostral de h
y = conv(x,h);
nxi = nx(1);
nxf = nx(end);
nhi = nh(1);
nhf = nh(end);
nyi = nxi+nhi;
nyf = nxf + nhf;
ny = [nyi:nyf];
end