function []  = point_paint(x, y, color)

% calculate the sum of 1..n
if color == 0
scatter(x, y,30, 'white', 'filled')

end
if color == 1
scatter(x, y,30, [0.75, 0.75, 0.75], 'filled')

end
if color == 2
scatter(x, y,30, 'red', 'filled')

end
if color == 3
scatter(x, y,30, 'black', 'filled')

end
pause(0.5)
imagesc(x, y , color)
pause(0.5)
hold on