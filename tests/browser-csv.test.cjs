"use strict";
const {test} = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const source = fs.readFileSync(path.join(__dirname, "..", "docs", "csv-cleaner.js"), "utf8");
const end = source.indexOf("\n(function(){");
assert.ok(end > 0, "The pure CSV functions must precede DOM handlers");
const util = vm.runInNewContext(source.slice(0,end) + "\n;({parseCSV, cleanRows, serializeCSV});");

function plain(value) { return JSON.parse(JSON.stringify(value)); }
test("empty input stays empty", () => assert.deepEqual(plain(util.parseCSV("")), []));
test("handles UTF-8 BOM", () => assert.deepEqual(plain(util.parseCSV("\uFEFFa,b\n")), [["a","b"]]));
test("supports quoted commas", () => assert.deepEqual(plain(util.parseCSV('a,"b,c",d\n')), [["a","b,c","d"]]));
test("supports escaped quotes", () => assert.deepEqual(plain(util.parseCSV('a,"say ""hi""",b')), [["a",'say "hi"',"b"]]));
test("preserves quoted CRLF in a field", () => assert.deepEqual(plain(util.parseCSV('a,"x\r\ny",b\r\n')), [["a","x\r\ny","b"]]));
test("handles trailing empty fields", () => assert.deepEqual(plain(util.parseCSV("a,b,\n")), [["a","b",""]]));
test("rejects unclosed quotations", () => assert.throws(() => util.parseCSV('a,"bad'),/unclosed/i));
test("rejects malformed quotations", () => assert.throws(() => util.parseCSV('a,b"c'),/Unexpected quote/));
test("trims cells without removing duplicates", () => {
  const got = util.cleanRows(util.parseCSV("A,B\n Alice , Cairo \n , \n Alice , Cairo \n"));
  assert.equal(got.dropped,1);
  assert.deepEqual(plain(got.rows),[["A","B"],["Alice","Cairo"],["Alice","Cairo"]]);
});
test("properly escapes comma, quotes and multiline CSV fields", () => {
  const rows=[["a","b,c",'say "hi"'],["m\nn","x",""]];
  assert.equal(util.serializeCSV(rows),'a,"b,c","say ""hi"""\r\n"m\nn",x,\r\n');
  assert.deepEqual(plain(util.parseCSV(util.serializeCSV(rows))),rows);
});
test("client source does not transmit CSV through fetch or XHR", () => {
  assert.doesNotMatch(source,/\bfetch\s*\(|\bXMLHttpRequest\b|\bsendBeacon\s*\(/);
});
