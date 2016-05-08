data = load('sandbox/rrtpath.txt');
obstacles = load('sandbox/obstacles.txt')
hold on
plot(data(:,1),data(:,2),'o-');
for i=1:size(obstacles)(1)/2 % # of rows
	plot(obstacles(2*i-1,:),obstacles(2*i,:));
end
axis equal, grid on;
pause;