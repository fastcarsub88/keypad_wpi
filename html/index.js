var codesObj = {};
var scheduleObj = {};
var codesDiv = document.getElementById('codesDiv');
var lockBtn = document.getElementById('lock_btn');
var schDiv = document.getElementById('scheduleDiv');
var lockLogDiv = document.getElementById('lockLogDiv');

document.getElementById('apiKeyFmBtn').onclick = function(){
  localStorage.apiKey = document.getElementById('apiKeyInput').value;
  closeModal('apiModal');
  get_schedule();
  get_status();
};
document.getElementById('editElemBtn').onclick = ()=>{
  get_codes();
  get_schedule();
  get_lock_log();
  openModal('editElem');
};
document.getElementById('select2').onchange = function () {
  if (this.value == 'keepunlock') {
    openModal('keepunlockinput')
    closeModal('defaultinput')
  }else {
    closeModal('keepunlockinput')
    openModal('defaultinput')
  }
}
document.getElementById('addSchedule').onclick = ()=>{openModal('schModal')};
document.getElementById('addBreak').onclick = ()=>{openModal('breaksModal')};
document.getElementById('addCodes').onclick = ()=>{openModal('codesModal')};
document.getElementById('editCodesTab').onclick = function(e){switchTab('codesTab',e.target)};
document.getElementById('editScheduleTab').onclick = function(e){switchTab('scheduleTab',e.target)};
document.getElementById('editLockLogTab').onclick = function(e){switchTab('lockLogTab',e.target)};
document.getElementById('saveSch').onclick = () => {addSch(document.forms.scheduleForm,scheduleObj)}
document.getElementById('saveBreak').onclick = () => {addBreak(document.forms.breaksForm,scheduleObj)}
document.getElementById('saveCdsBtn').onclick = () => {addCodes(document.forms.addCodes,codesObj)}
window.addEventListener('click',function (e) {
  if (e.target.classList.contains('modal')) {
    e.target.classList.add('hidden')
  }
})
lockBtn.onclick = lock_unl
function capitalize(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}
async function lock_unl () {
  var f = new FormData();
  f.append("method","lock_unl");
  await send_data(f);
  get_status();
}
async function send_data(request) {
  request.append('key',localStorage.apiKey);
  var r = await fetch(
      window.location.href+'api',
      {method: 'POST',body: request}
    )
    .then(response => {return response.json()})
    .catch(()=>{alert("Network Error!")});
  if (r.status != '200') {keyInput()};
  return r;
}
async function upload(method,name,obj) {
  openModal('loader');
  var f = new FormData();
  f.append('method',method);
  f.append(name,JSON.stringify(obj))
  send_data(f).then(() => {closeModal('loader')});
}
async function get_codes() {
  openModal('loader');
  var f = new FormData();
  f.append("method","get_codes");
  var rsp = await send_data(f);
  closeModal('loader');
  if (rsp.status == '200') {
    codesObj = JSON.parse(rsp.codes);
    displayCodes(codesObj);
  }
}
async function get_schedule() {
  openModal('loader');
  var f = new FormData();
  f.append("method","get_schedule");
  var rsp = await send_data(f);
  closeModal('loader');
  if (rsp.status == '200') {
    scheduleObj = JSON.parse(rsp.schedule);
    displaySch(scheduleObj);
  }
}
async function get_lock_log() {
  openModal('loader');
  var f = new FormData();
  f.append("method","get_lock_log");
  var rsp = await send_data(f);
  closeModal('loader');
  if (rsp.status == '200') {
    displayLockLog(rsp.lock_log);
  }
}
async function get_status() {
  var f = new FormData();
  f.append("method","get_status");
  var r = await send_data(f);
  if (r.d_status == 'locked') {lockBtn.innerText = "Unlock Doors"};
  if (r.d_status == 'unlocked') {lockBtn.innerText = "Lock Doors"};
}
async function deleteSch() {
  if (this.day == 'Breaks') {
    if (confirm("Delete "+ this.day+" "+this.action)) {
      var a = scheduleObj.Breaks;
      for (var i = 0; i < a.length; i++) {
        if (a[i] == this.action) {a.splice(i,1)};
      };
    };
  }else {
    if (confirm('Delete '+ this.day+' - '+this.time+' - '+this.action)) {
      delete scheduleObj[this.day][this.time];
      if (!Object.keys(scheduleObj[this.day]).length) {
        delete scheduleObj[this.day];
      };
    };
  };
  await upload('put_schedule','schedule',scheduleObj)
  displaySch(scheduleObj);
}
async function deleteCode() {
  if (confirm('Delete '+this.name)) {
    delete codesObj[this.code];
    await upload('put_codes','codes',codesObj);
    displayCodes(codesObj);
  }
}
function switchTab(id,tgt) {
  var a = document.getElementById('tabsDiv')
  var b = a.querySelectorAll('.tab');
  for (var i = 0; i < b.length; i++) {b[i].style.display = 'none'};
  a.querySelector('#'+id).style.display = 'block';
  var c = document.querySelectorAll('.tabBtn');
  for (var i = 0; i < c.length; i++) {c[i].classList.remove('tabActive')};
  tgt.classList.add('tabActive');
}
function keyInput() {
  alert('Unauthorized! Please input correct api key..');
  openModal('apiModal');
}
function displayCodes(cds) {
  codesDiv.innerHTML = "";
  for (let [code,name] of Object.entries(cds)){
    var p = document.createElement('p');
    p.onclick = deleteCode;
    p.innerText = name+' : '+code;
    p.name = name;
    p.code = code;
    codesDiv.append(p);
  }
}
function displayLockLog(arg) {
  lockLogDiv.innerHTML = "";
  var a = document.createElement('p');
  a.innerText = arg;
  lockLogDiv.append(a);
}
function displaySch(arg) {
  scheduleDiv.innerHTML = "";
  function z(obj,a) {
    for (let [d,e] of Object.entries(obj)){
      var f = document.createElement('p');
      if (d == 'keepunlock') {
        f.innerText = "Keep Unlocked : "+e
      }else if (d.length > 1) {
        f.innerText = capitalize(e)+' : '+d
      }else {
        f.innerText = e
      }
      f.onclick = deleteSch;
      f.day = a;
      f.time = d;
      f.action = e;
      c.append(f);
    }
  }
  for (let [a,b] of Object.entries(arg)){
    if (a == 'Breaks') {continue}
    var c = document.createElement('div');
    c.innerText = a;
    z(b,a);
    scheduleDiv.append(c);
  }
  var c = document.createElement('div');
  var a = 'Breaks';
  c.innerText = a;
  z(arg.Breaks,a);
  scheduleDiv.append(c);
}
function addSch(form,obj) {
  if (!scheduleObj[form.day.value]) {scheduleObj[form.day.value] = {}}
  if (form.action.value == 'keepunlock'){
    if (form.time2.value == '' || form.time3.value == '') {
      alert('Please input 2 times..')
      return
    }
    if (form.time2.value > form.time3.value) {
      alert("End time before start time..")
      return
    }
    scheduleObj[form.day.value][form.action.value] = form.time2.value+'-'+form.time3.value;;
  }else {
    scheduleObj[form.day.value][form.time1.value] = form.action.value;
  }
  upload('put_schedule','schedule',scheduleObj);
  displaySch(scheduleObj);
  closeModal('schModal');
}
function addBreak(form,obj) {
  var a = form.st_date.value.split('-');
  var b = form.end_date.value.split('-');
  var c = a[1]+'/'+a[2]+'/'+a[0].substring(2);
  var d = b[1]+'/'+b[2]+'/'+b[0].substring(2);
  scheduleObj.Breaks.push(c+'-'+d);
  upload('put_schedule','schedule',scheduleObj);
  displaySch(scheduleObj);
  closeModal('breaksModal');
}
function addCodes(form,obj) {
  if (form.ctitle.value == '') {return};
  if (form.new_card.checked) {
    codesObj['new_card'] = form.ctitle.value;
  }else {
    if (form.ccode.value == '') {return};
    codesObj[form.ccode.value] = form.ctitle.value;
  }
  upload('put_codes','codes',codesObj);
  displayCodes(codesObj);
  closeModal('codesModal');
}
function openModal(id) {
  document.getElementById(id).classList.remove('hidden');
}
function closeModal(id) {
  document.getElementById(id).classList.add('hidden');
}
if (!localStorage.apiKey) {
  keyInput();
}
else {
  get_status();
}
