function []  = map_paint(color, size)

% calculate the sum of 1..n

N = size;

mycolor6 = [
1 1 1
0.7529 0.7529 0.7529
0 1 0
1 0 0
0 0 0
];

A= ones(N) ;
for i=1:N
    for j = 1:N
        A(i, j) = color;
    end
end

set(gca,'YDir','reverse')
set(gca,'XDir','reverse')
imagesc(1, 1, A);
caxis([-0.5 3.5])
colormap(mycolor6)
pause(0.5)
hold on


