<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAVI AI VIDEO CREATOR</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#10121b;color:#fff;font-family:Arial,sans-serif}
header{background:#191d2c;padding:20px;text-align:center;border-bottom:2px solid #6b5cff}
header h1{font-size:23px;margin:0;color:#a99fff}
header p{color:#bbb;font-size:13px}
main{max-width:600px;margin:auto;padding:18px}
.card{background:#1b2030;border:1px solid #343b53;border-radius:14px;padding:17px;margin-bottom:16px}
h2{font-size:17px;margin-top:0}
label{display:block;margin:14px 0 7px;font-size:14px}
textarea,select,input{width:100%;padding:12px;border-radius:8px;border:1px solid #424962;background:#101522;color:#fff;font-size:15px}
textarea{height:115px;resize:vertical}
button{width:100%;padding:14px;margin-top:12px;background:#7062ff;color:white;border:0;border-radius:9px;font-size:15px;font-weight:bold}
button:active{opacity:.8}
.note{font-size:12px;color:#b9bfd0;line-height:1.6}
#status{white-space:pre-wrap;line-height:1.7;color:#bdb4ff;font-size:14px}
footer{text-align:center;padding:20px;color:#999;font-size:12px}
</style>
</head>
<body>
<header>
<h1>🎬 RAVI AI VIDEO CREATOR</h1>
<p>आपके वीडियो, आपकी क्रिएटिविटी</p>
</header>
<main>
<section class="card">
<h2>✍️ अपना वीडियो बनाएँ</h2>
<label for="prompt">वीडियो में क्या दिखाना है?</label>
<textarea id="prompt" placeholder="उदाहरण: प्राचीन मिस्र के पिरामिड, रहस्यमयी वातावरण और सिनेमैटिक दृश्य..."></textarea>

<label for="mode">वीडियो बनाने का तरीका</label>
<select id="mode">
<option value="text">Text to Video — टेक्स्ट से वीडियो</option>
<option value="image">Image to Video — फोटो से वीडियो</option>
<option value="story">पूरी कहानी वाला वीडियो</option>
</select>

<label for="ratio">वीडियो का आकार</label>
<select id="ratio">
<option value="9:16">9:16 — YouTube Shorts</option>
<option value="16:9">16:9 — YouTube वीडियो</option>
<option value="1:1">1:1 — Square वीडियो</option>
</select>

<label for="duration">वीडियो की अवधि</label>
<select id="duration">
<option value="5">5 सेकंड</option>
<option value="10">10 सेकंड</option>
<option value="30">30 सेकंड</option>
<option value="60">1 मिनट</option>
<option value="120">2 मिनट</option>
</select>

<button onclick="prepareVideo()">वीडियो बनाने की तैयारी करें</button>
</section>

<section class="card">
<h2>🖼️ फोटो से वीडियो</h2>
<label for="photo">अपनी फोटो चुनें</label>
<input type="file" id="photo" accept="image/*">
<p class="note">फोटो चुनने के बाद AI वीडियो मॉडल जोड़कर उसमें मूवमेंट बनाया जा सकेगा।</p>
</section>

<section class="card">
<h2>📋 वीडियो प्रोजेक्ट</h2>
<div id="status">आपका प्रोजेक्ट यहाँ दिखाई देगा।</div>
<button onclick="downloadProject()">प्रोजेक्ट निर्देश डाउनलोड करें</button>
<p class="note">यह शुरुआती इंटरफेस है। वास्तविक AI वीडियो जनरेशन के लिए अगला चरण पूरा करना होगा।</p>
</section>
</main>
<footer>RAVI AI VIDEO CREATOR · Version 0.1</footer>

<script>
let currentProject=null;

function prepareVideo(){
 const prompt=document.getElementById('prompt').value.trim();
 if(!prompt){
  alert('पहले वीडियो का विवरण लिखिए।');
  return;
 }
 currentProject={
  app:'RAVI AI VIDEO CREATOR',
  prompt:prompt,
  mode:document.getElementById('mode').value,
  aspect_ratio:document.getElementById('ratio').value,
  duration_seconds:Number(document.getElementById('duration').value),
  created_at:new Date().toISOString(),
  status:'READY_FOR_AI_MODEL'
 };
 document.getElementById('status').textContent=
  'प्रोजेक्ट तैयार है।\n\n'+
  'विवरण: '+currentProject.prompt+'\n'+
  'तरीका: '+currentProject.mode+'\n'+
  'आकार: '+currentProject.aspect_ratio+'\n'+
  'अवधि: '+currentProject.duration_seconds+' सेकंड\n\n'+
  'अगला चरण: AI वीडियो मॉडल जोड़ना।';
}

function downloadProject(){
 if(!currentProject){
  alert('पहले वीडियो का विवरण लिखकर तैयारी करें।');
  return;
 }
 const blob=new Blob(
  [JSON.stringify(currentProject,null,2)],
  {type:'application/json'}
 );
 const url=URL.createObjectURL(blob);
 const a=document.createElement('a');
 a.href=url;
 a.download='ravi-video-project.json';
 a.click();
 URL.revokeObjectURL(url);
}
</script>
</body>
</html>
