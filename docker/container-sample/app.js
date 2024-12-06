const http = require('http');
const server = http.createServer().listen(6060);
server.on('request', (req, res) => {
	console.log('요청 처리중');
	res.write("HostName: " + process.env.HOSTNAME + "\n");
	res.end();
});
server.on('connection', (socket) => {
	console.log("연결 완료.");
});
