// Creates a websocket with socket.io
// Make sure to install socket.io: terminal, goto /var/lib/cloud9 and enter: npm install socket.io
// Installing this takes a few minutes; wait until the installation is complete

var b = require('/usr/local/lib/node_modules/bonescript');
var SerialPort = require("/usr/local/lib/node_modules/serialport").SerialPort;
var fs = require('fs');

var express = require('express');
var app = express();
var server = require('http').Server(app);
var io = require('socket.io')(server);

app.use(express.static(__dirname + '/static'));

var port = 8090;
server.listen(port);
console.log('Server running on: http://' + getIPAddress() + ':' + port);

// app.get('/', function (req, res) {
//   res.sendfile(__dirname + '/index.html');
// });

var exec_vnc = require('child_process').exec;
var exec_stop = require('child_process').exec;

var file = "/media/Dilbert_qqvga.mp4";
var Mplayer = require('./node-mplayer'); 
var player = new Mplayer(file);
player.play();

vnc_process = exec_vnc('/usr/bin/x11vnc -bg -display :0  -forever', function(code, output) {
    console.log('Exit code:', code);
    console.log('Program output:', output);
});


var serial2 = new SerialPort("/dev/ttyO4", {
    baudrate: 9600
});

var serial1 = new SerialPort("/dev/ttyO1", {
    baudrate: 9600
});


function chr(bin) {
    return String.fromCharCode(bin)
};

function bchr(bin) {
	var e = parseInt(bin, 2);
	return chr(e);
}

// function chr_data(value) {
//     var value1 = (value*4);
//     var str = chr(Math.floor(value1/256)) + chr(Math.floor((value1%256)/16)) + chr(value1%16);
//     return str;
// }

function chr_data(value) {
     var str = chr(Math.floor(value/256)) + chr(Math.floor((value%256)/16)) + chr(value%16);
     return str;
}

var dac_addr = '3'; //dummy bchr("10100100");
 
io.sockets.on('connection', function (socket) {
  
  socket.on('preset', function (data) {
    if (data == "0") {
      // AMLED 120x160 TOP - RGB   ROTADED NO GIP
      serial2.write('3' + 'R' + bchr("00000001") + bchr("00000011") + bchr("00000001") + ';');
      // Set FREQ to 6Mhz
      serial2.write('3' + 'F' + '1' + ';');
      // 9 Subframes
      serial2.write('3' + 'S' + '9' + ';');
      // data 120 (*3) select 160
      serial2.write('3' + 'D' + chr_data(120) + chr_data(160) + ';');
      serial2.write('3' + 'W' + bchr("001110") + ';'); 
    }
    else if (data == "1") {
      // AMLED 120x160 BOT - RGB ROTADED NO GIP
      serial2.write('3' + 'R' + bchr("00000001") + bchr("00000001") + bchr("00000010") + ';');
      // Set FREQ to 6Mhz
      serial2.write('3' + 'F' + '1' + ';');
      // 9 Subframes
      serial2.write('3' + 'S' + '9' + ';');
      serial2.write('3' + 'D' + chr_data(120) + chr_data(160) + ';');
      serial2.write('3' + 'W' + bchr("010000") + ';'); // is not yet correct
    }
    else if (data == "2") {
      // CPT 240 x 320 GIP GRAY ROTATED
      serial2.write('3' + 'R' + bchr("00001000") + bchr("00000001") + bchr("00000000") + ';');
      // Set FREQ to 6Mhz
      serial2.write('3' + 'F' + '1' + ';');
      // 9 Subframes
      serial2.write('3' + 'S' + '9' + ';');
      serial2.write('3' + 'D' + chr_data(240) + chr_data(320) + ';');
      serial2.write('3' + 'W' + bchr("010000") + ';'); // is not yet correct
    }
    else if (data == "3") {
      // QVGA 320 x 240 GRAY
      serial2.write('3' + 'R' + bchr("00000000") + bchr("00000001") + bchr("00000000") + ';');
      // Set FREQ to 6Mhz
      serial2.write('3' + 'F' + '1' + ';');
      // 9 Subframes
      serial2.write('3' + 'S' + '9' + ';');
      serial2.write('3' + 'D' + chr_data(320) + chr_data(240) + ';');
      serial2.write('3' + 'W' + bchr("010000") + ';'); // is not yet correct
    }
  });
  
  socket.on('color_select', function (data) {
     if (data == '0') 
       serial2.write('3' + 'A' + bchr("00000000") + ';');
     else if (data == '1')
       serial2.write('3' + 'A' + bchr("00000001") + ';');
     else if (data == '2')
       serial2.write('3' + 'A' + bchr("00000011") + ';');
     else if (data == '3')
       serial2.write('3' + 'A' + bchr("00000101") + ';');
     else if (data == '4')
       serial2.write('3' + 'A' + bchr("00001001") + ';');
    });
    
  socket.on('color_seq', function (data) {
     if (data == '0') 
       serial2.write('3' + 'B' + bchr("00000000") + ';');
     else if (data == '1')
       serial2.write('3' + 'B' + bchr("00000001") + ';');
     else if (data == '2')
       serial2.write('3' + 'B' + bchr("00000010") + ';');
     else if (data == '3')
       serial2.write('3' + 'B' + bchr("00000011") + ';');
     else if (data == '4')
       serial2.write('3' + 'B' + bchr("00000100") + ';');
     else if (data == '5')
       serial2.write('3' + 'B' + bchr("00000101") + ';');
    });
  
   socket.on('display_size', function (data) {
    var hcol = data.col;
    var vrow = data.row;
    var str = '3' + 'D' + chr_data(hcol) + chr_data(vrow) + ';';
    serial2.write(str);
    console.log(str);
    console.log("col=%d, row=%d, str=%s",hcol,vrow,str);
  });
  
  socket.on('gip', function (data) {
    var str = '3' + 'G' + chr(data) + ';';
    serial2.write(str);
    console.log(str);
  });
  
  socket.on('frequency', function (data) {
    var str = '3' + 'F' + chr(data) + ';';
    serial2.write(str);
    console.log(str);
  });
  
  socket.on('orientation', function (data) {
    var str = '3' + 'R' + chr(data) + ';';
    serial2.write(str);
    console.log(str);
  });
  
  socket.on('select_lr', function (data) {
    var str = '3' + 'C' + chr(data) + ';';
    serial2.write(str);
    console.log(str);
  });
  
  socket.on('direction', function (data) {
    var str = '3' + 'T' + chr(data) + ';';
    serial2.write(str);
    console.log(str);
  });
  
  socket.on('subframe', function (data) {
    var str = '3' + 'S' + chr(data) + ';';
    serial2.write(str);
    console.log(str);
  });
  
  socket.on('wait', function (data) {
    var str = '3' + 'W' + chr(data) + ';';
    serial2.write(str);
    console.log(str);
  });
  
  socket.on('play', function (data) {
    //player.stop();
    player.setFile(file);
    player.play();
  });
  
  socket.on('pause', function (data) {
    player.pause();
  });
  
  socket.on('stop', function (data) {
    //player.stop();
    stop_process = exec_stop('ps -e | grep mplayer && pkill mplayer', function(code, output) {
        console.log('Exit code:', code);
        console.log('Program output:', output);
    });
  });
  
  socket.on('select', function (data) {
    if (data == "mov0")
       file = "/media/Dilbert.mp4";
    else if (data == "mov1")
       file = "/media/ball.mp4";
    else if (data == "mov2")
       file = "/media/test_images.avi";
    else if (data == "mov3")
       file = "/media/output.avi";
    else if (data == "mov4")
       file = "/media/imecVid.avi";
    else if (data == "mov7")
       file = "/media/Dilbert_qqvga.mp4";
    else if (data == "mov8")
       file = "/media/ball_qqvga.mp4";
    else
       file = "/media/Maus.mp4";
    });
});


// Get server IP address on LAN
function getIPAddress() {
  var interfaces = require('os').networkInterfaces();
  for (var devName in interfaces) {
    var iface = interfaces[devName];
    for (var i = 0; i < iface.length; i++) {
      var alias = iface[i];
      if (alias.family === 'IPv4' && alias.address !== '127.0.0.1' && !alias.internal)
        return alias.address;
    }
  }
  return '0.0.0.0';
}