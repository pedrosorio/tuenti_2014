#!/usr/bin/env node

if ((process.version.split('.')[1]|0) < 10) {
	console.log('Please, upgrade your node version to 0.10+');
	process.exit();
}

var net = require('net');
var util = require('util');
var crypto = require('crypto');
var fs = require('fs');

var options = {
	'port': 6969,
	'host': '54.83.207.90',
}

//read the keyphrase synchronously from the stdin
fs=require('fs');
var KEYPHRASE = fs.readFileSync('/dev/stdin').toString().trim();


var dh_client, secret_client, state_client = 0;
var dh_server, secret_server = 0;

var socket = net.connect(options);
server_response = "";
//cutting and pasting client/server code does the trick
socket.on('data', function(data) {

	data = data.toString().trim().split(':');

	communication_path = data[0];
	message = data[1];

	if (communication_path == "CLIENT->SERVER") {
		if (state_client == 0) {
			socket.write(message);
			state_client++;
		} else if (state_client == 1) {
			dh_client = crypto.createDiffieHellman(256);
			dh_client.generateKeys();
			socket.write(util.format('key|%s|%s\n', dh_client.getPrime('hex'), dh_client.getPublicKey('hex')));
			state_client++;
			//simulate_server_response
			data = message.split('|');
			dh_server = crypto.createDiffieHellman(data[1], 'hex');
			dh_server.generateKeys();
			secret_server = dh_server.computeSecret(data[2], 'hex');
			server_response = util.format('key|%s\n', dh_server.getPublicKey('hex'));
		} else if (state_client == 2) {
			data = last_message.split('|');
			secret_client = dh_client.computeSecret(data[1], 'hex');
			var cipher = crypto.createCipheriv('aes-256-ecb', secret_client, '');
			var keyphrase = cipher.update(KEYPHRASE, 'utf8', 'hex') + cipher.final('hex');
			socket.write(util.format('keyphrase|%s\n', keyphrase));
			state_client++;
			//no need to simulate last server_response, tough luck client ahahah
			server_response = "";
		}
	} else if (communication_path == "SERVER->CLIENT") {
		last_message = message;
		//write what the server sent unless we want to impersonate the server
		//in which case we computed the appropriate response when the client sent the message
		if (server_response == "") {
			socket.write(message);
		} else {
			socket.write(server_response);
		}
		//On the last message from the server, output the result
		if (state_client == 3) {
			data = message.split('|');
			var decipher = crypto.createDecipheriv('aes-256-ecb', secret_client, '');
			var message = decipher.update(data[1], 'hex', 'utf8') + decipher.final('utf8');
			console.log(message);
			socket.end();
		}
	}

});
