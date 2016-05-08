data = load('sandbox/rrtpath.txt');
obstacles = load('sandbox/obstacles.txt')
hold on
plot(data(:,1),data(:,2),'o-');
plot(obstacles(:,1),data(:))
axis equal, grid on;
pause