function toggleMode(){
document.body.classList.toggle('light')
}

function getId(url){
const m=url.match(/(?:v=|youtu\.be\/|shorts\/)([A-Za-z0-9_-]{11})/);
return m?m[1]:null
}

function previewThumb(){
const url=document.getElementById('url').value;
const id=getId(url);
const img=document.getElementById('thumb');
const meta=document.getElementById('meta');

if(id){
img.src=`https://img.youtube.com/vi/${id}/maxresdefault.jpg`;
img.style.display='block';
meta.innerHTML='Video detected ✔';
}else{
img.style.display='none';
meta.innerHTML='';
}
}

async function startDownload(){

const url=document.getElementById('url').value;
const type=document.getElementById('type').value;
const status=document.getElementById('status');
const bar=document.getElementById('bar');

status.innerHTML='Processing...';
bar.style.width='10%';

let p=10;

const fake=setInterval(()=>{
p=Math.min(p+12,90);
bar.style.width=p+'%';
},500);

const res=await fetch('/download',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({url,type})
// body:JSON.stringify({url,type})
});

const data=await res.json();

clearInterval(fake);

bar.style.width='100%';

if(data.success){

status.innerHTML=`<a href='/file/${data.file}' download>⬇ Download File</a>`;

}else{

status.innerText=data.error;
bar.style.width='0%';

}

}

