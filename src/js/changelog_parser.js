// Sample usage: node changelog_parser.js "../tmp/1.json" 
'use strict';

var Changeset = require("./../../lib/etherpad-lite/src/static/js/Changeset");

if (process.argv.length <= 2) {
    console.log("Usage: <node> " + __filename + " path/to/directory");
    process.exit(-1);
}
var path = process.argv[2];
//console.log(path)
let jsonData = require(path);
//console.log(path.slice(0, -5).concat("df.json"));

var df = [];
var ops = [];
var j = 0;

//for (var i = 0; i < jsonData.revs.length; i++) { 
for (var i = 0; i < jsonData.revs.length; i++) { 

    var upkd = Changeset.unpack(jsonData.revs[i].changeset);

    var opiterator = Changeset.opIterator(upkd.ops);

    var nops = 0;

    var nentry = {
    	_timestamp: jsonData.revs[i].meta.timestamp,
    	char_bank: upkd.charBank,
    	o_len: upkd.oldLen,
    	n_len: upkd.newLen,

    	// for debugging purposes
    	z_string: jsonData.revs[i].changeset,
    	z_opstring: upkd.ops,
    	//atext: jsonData.revs[i].meta.atext.text,
    	//attribs: jsonData.revs[i].meta.atext.attribs
    };

    while (opiterator.hasNext()) {
    	nops = nops + 1;
    	var varname = "op".concat(nops.toString(10));

        var a = opiterator.next();
        //console.log(a.opcode);
        var mya = {
            opcode: a.opcode,
            chars: a.chars,
            lines: a.lines,
            attribs: a.attribs
        };
    	ops.push(mya);
        //console.log(ops[ops.length-1].opcode);
    	nentry[varname] = j;
    	j++;
    }
    nentry.op_no = nops;

    df.push(nentry);
}
//console.log(ops);

var myJSON = JSON.stringify(df);
var fs = require("fs");
fs.writeFile(path.slice(0, -5).concat("df.json"), myJSON, (err) => {
  if (err) console.log(err);
});
var myJSON2 = JSON.stringify(ops);
fs.writeFile(path.slice(0, -5).concat("ops.json"), myJSON2, (err) => {
  if (err) console.log(err);
});

//console.log("df\n");
//console.log(df)
