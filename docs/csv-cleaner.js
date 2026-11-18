"use strict";
function parseCSV(input){
  const source=input.charCodeAt(0)===0xFEFF?input.slice(1):input;
  if(!source.length)return [];
  const rows=[];let row=[],field="",state="start";
  const pushField=()=>{row.push(field);field="";};
  const pushRow=()=>{pushField();rows.push(row);row=[];state="start";};
  for(let i=0;i<source.length;i++){
    const ch=source[i], newline=(ch==="\r"||ch==="\n");
    if(state==="quoted"){
      if(ch==='"'){if(source[i+1]==='"'){field+='"';i++;}else state="after_quote";}
      else field+=ch;
    }else if(state==="after_quote"){
      if(ch===","){pushField();state="start";}
      else if(newline){pushRow();if(ch==="\r"&&source[i+1]==="\n")i++;}
      else throw new Error("Unexpected character after closing quote at position "+(i+1));
    }else if(state==="start"){
      if(ch==='"')state="quoted";
      else if(ch===",")pushField();
      else if(newline){pushRow();if(ch==="\r"&&source[i+1]==="\n")i++;}
      else {field+=ch;state="plain";}
    }else if(state==="plain"){
      if(ch===","){pushField();state="start";}
      else if(newline){pushRow();if(ch==="\r"&&source[i+1]==="\n")i++;}
      else if(ch==='"')throw new Error("Unexpected quote in unquoted field at position "+(i+1));
      else field+=ch;
    }
  }
  if(state==="quoted")throw new Error("CSV has an unclosed quoted field");
  if(row.length||field.length||state==="after_quote"||state==="plain")pushRow();
  return rows;
}
function cleanRows(rows){
  let dropped=0;
  const cleaned=[];
  for(const row of rows){
    const normalized=row.map(value=>value.trim());
    if(normalized.every(value=>!value)){dropped++;continue;}
    cleaned.push(normalized);
  }
  return {rows:cleaned,dropped};
}
function serializeCSV(rows){
  return rows.map(row=>row.map(value=>{
    const s=String(value);
    return /[,"\r\n]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s;
  }).join(",")).join("\r\n")+(rows.length?"\r\n":"");
}
(function(){
const area=document.getElementById("csv-text");
const fileInput=document.getElementById("csv-file");
const run=document.getElementById("csv-run");
const download=document.getElementById("csv-download");
const message=document.getElementById("csv-status");
const preview=document.getElementById("csv-preview");
const MAX_BYTES=8*1024*1024;
let result="",name="cleaned.csv";
function status(text){message.textContent=text;}
function reset(){result="";download.disabled=true;preview.textContent="";}
fileInput.addEventListener("change",async()=>{
  reset();const f=fileInput.files&&fileInput.files[0];
  if(!f)return;
  if(f.size>MAX_BYTES){status("File exceeds the 8 MB limit. No file was processed.");return;}
  try{area.value=await f.text();name=f.name.replace(/\.csv$/i,"").replace(/[^a-zA-Z0-9._-]/g,"_")+"-cleaned.csv";status("File loaded locally. Click Clean CSV.");}
  catch(_e){status("Cannot read this file in your browser.");}
});
area.addEventListener("input",()=>{reset();status("Ready to clean CSV. No data is uploaded.");});
run.addEventListener("click",()=>{
  reset();
  if(new Blob([area.value]).size>MAX_BYTES){status("Input exceeds the 8 MB limit.");return;}
  try{
    const input=parseCSV(area.value);
    const output=cleanRows(input);
    result=serializeCSV(output.rows);
    download.disabled=output.rows.length===0;
    const show=output.rows.slice(0,8).map(row=>row.join(" | "));
    preview.textContent=show.length?"First "+show.length+" cleaned rows (text preview):\n"+show.join("\n"):"No nonempty rows to export.";
    status("Ready: "+input.length+" parsed rows; "+output.rows.length+" saved; "+output.dropped+" blank rows removed. Duplicate rows preserved.");
  }catch(err){status("CSV parsing error: "+err.message);}
});
download.addEventListener("click",()=>{
  if(!result)return;
  const url=URL.createObjectURL(new Blob([result],{type:"text/csv;charset=utf-8"}));
  const a=document.createElement("a");a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),5000);
});
})();
