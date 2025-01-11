% N = 30;
% 
% mycolor6 = [
% 1 1 1
% 0.7529 0.7529 0.7529
% 0 1 0
% 1 0 0
% 0 0 0
% ];
% 
% A=ones(N) * 3;
% A(30,30)=1;
% 
% 
% set(gca,'YDir','reverse')
% set(gca,'XDir','reverse')
% imagesc(1, 1, A);
% 
% caxis([-0.5 3.5])
% colormap(mycolor6)
% hold on
fileID = fopen('test.txt','r');
[command, count] = fscanf(fileID, '%d %d %d %d', [4 Inf]);
fclose(fileID);
count = count / 4;

map_paint(command(4,1) ,command(2, 1) * 2 + 1);
% point_paint(1,1, 1)
% square_paint(2,2, 2)
% point_paint(2, 2, 0)

colorbar
for i = 2:count
    if command(1, i) == 22222
        square_paint(command(2, i) + 1, command(3, i) + 1, command(4, i))
    end
    if command(1, i) == 33333
        point_paint(command(2, i) + 1, command(3, i) + 1, command(4, i))
    end
end



