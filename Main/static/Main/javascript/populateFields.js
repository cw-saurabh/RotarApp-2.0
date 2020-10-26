let gbmsIndex=0;
let bodsIndex=0;
let feventsIndex=0;
let eventsIndex=0;
let bulletinsIndex=0;
let month="";
// Dues section
let countN=0;
let countn=0;
let paidAlready = 0;
let paid=0;
let owedMoney=0;
let pending=0;
let monthNo = "00";

var today = new Date();
var year = today.getFullYear();


let rowCount = 1;

data={'gbm':{},'bod':{},'event':{},'fevent':{},'feedback':{},'bulletin':{},'matrix':{}};
deletedData={'gbm':[],'bod':[],'event':[],'fevent':[]};

function appendGeneralBodyMeeting(meetingId=null,meetingNo=null, meetingDate=null,meetingAgenda=null,bylawsBoolean='None',budgetBoolean='None',meetingAttendance=null) {
  gbmsIndex+= 1;
  if (meetingId == null)
  meetingId="M-"+gbmsIndex+"-"+month+"-"+makeid(5);
  
  $("#generalBodyMeetings").append(`
  <div class="row" id="gbm`+meetingId+`">
    <div class="col-lg-2">
      <p class="label"><i class="fa fa-hashtag" aria-hidden="true"></i>&nbsp;&nbsp;Meeting No.<b style="color:red"> *</b></p><br>
      <input tab="Admin" type="number" min=0 step=1 max=31 oninput="validity.valid||(value='');updateList(this.id,'gbm','`+meetingId+`')" id="gbm`+gbmsIndex+`-no" name="meetingNo">
    </div>
    <div class="col-lg-3">
      <p class="label"><i class="fa fa-calendar" aria-hidden="true"></i>&nbsp;&nbsp;Date</p><br>
      <input tab="Admin" oninput="updateList(this.id,'gbm','`+meetingId+`')"  type="date" id="gbm`+gbmsIndex+`-date" name="meetingDate">
    </div>
    <div class="col-lg-3">
      <p class="label"><i class="fa fa-user-times" aria-hidden="true"></i>&nbsp;&nbsp;Attendees</p><b style="color:red"> *</b><br>
      <input tab="Admin" type="number" min=0 step=1 max=99999 oninput="validity.valid||(value='');updateList(this.id,'gbm','`+meetingId+`');" id="gbm`+gbmsIndex+`-attendance" name="meetingAttendance">
    </div>
    <div class="col-lg-2">
      <p class="label">ByLaws Passed?</p><br>
      <select tab="Admin" id="gbm`+gbmsIndex+`-bylawsBoolean" name="bylawsBoolean" oninput="updateList(this.id,'gbm','`+meetingId+`')">
        <option disabled selected value>Select :</option>
        <option value="True">Yes</option>
        <option value="False">No</option>
      </select>
    </div>
    <div class="col-lg-2">
      <p class="label">Budget Passed?</p><br>
      <select tab="Admin" id="gbm`+gbmsIndex+`-budgetBoolean" value="False" name="budgetBoolean" oninput="updateList(this.id,'gbm','`+meetingId+`')">
      <option disabled selected value>Select :</option>
      <option value="True">Yes</option>
      <option value="False">No</option>
      </select>
    </div>
    <div class="col-lg-9">
      <p class="label"><i class="fa fa-file-text" aria-hidden="true"></i>&nbsp;&nbsp;Agenda of the Meeting (brief)</p><br>
      <input tab="Admin" oninput="updateList(this.id,'gbm','`+meetingId+`')"  type="text" maxlength='1000' id="gbm`+gbmsIndex+`-agenda" name="meetingAgenda">
    </div>
    <div class="col-lg-3">
      <br>
      <button type="button" id="gbm`+meetingId+`Del" onclick="deleteRow('gbm',this.id)">Delete Row</button>
    </div>
    <div class="col-lg-12">
      <hr style="border-width : thin; border-color:grey;border-radius : 4px;">
    </div>
  </div>

  `);

  day1 = year+'-'+monthNo+'-01';
  daylast = year+'-'+monthNo+'-31';
  $("#gbm"+gbmsIndex+"-date").attr("min", day1);
  $("#gbm"+gbmsIndex+"-date").attr("max", daylast);


  if(meetingNo!=null) $("#"+"gbm"+gbmsIndex+"-no").val(meetingNo); 
  $("#"+"gbm"+gbmsIndex+"-date").val(meetingDate);
  if(meetingAgenda!=null) $("#"+"gbm"+gbmsIndex+"-agenda").val(meetingAgenda); 
  if(bylawsBoolean!='None')
  $("#"+"gbm"+gbmsIndex+"-bylawsBoolean").val(bylawsBoolean);
  if(budgetBoolean!='None')
  $("#"+"gbm"+gbmsIndex+"-budgetBoolean").val(budgetBoolean);
  if(meetingAttendance!=null) $("#"+"gbm"+gbmsIndex+"-attendance").val(meetingAttendance); 

  updateProgress();

}


function appendBODMeeting(meetingId=null,meetingNo=null, meetingDate=null,meetingAgenda=null,bylawsBoolean='None',budgetBoolean='None',meetingAttendance=null) {
  bodsIndex+=1;
  if (meetingId==null)
  meetingId="M-"+bodsIndex+"-"+month+"-"+makeid(5);
  
  $("#boardOfDirectorsMeetings").append(`
  <div class="row" id="bod`+meetingId+`">
    <div class="col-lg-2">
      <p class="label"><i class="fa fa-hashtag" aria-hidden="true"></i>&nbsp;&nbsp;Meeting No.<b style="color:red"> *</b></p><br>
      <input tab="Admin" type="number" min=0 step=1 max=31 oninput="validity.valid||(value='');updateList(this.id,'bod','`+meetingId+`')" id="bod`+bodsIndex+`-no" name="meetingNo">
    </div>
    <div class="col-lg-3">
      <p class="label"><i class="fa fa-calendar" aria-hidden="true"></i>&nbsp;&nbsp;Date</p><br>
      <input tab="Admin" oninput="updateList(this.id,'bod','`+meetingId+`')"  type="date" id="bod`+bodsIndex+`-date" name="meetingDate">
    </div>
    <div class="col-lg-3">
      <p class="label"><i class="fa fa-user-times" aria-hidden="true"></i>&nbsp;&nbsp;Attendees</p><b style="color:red"> *</b><br>
      <input tab="Admin" type="number" min=0 step=1 max=99999 oninput="validity.valid||(value='');updateList(this.id,'bod','`+meetingId+`')" id="bod`+bodsIndex+`-attendance" name="meetingAttendance">
    </div>
    <div class="col-lg-2">
      <p class="label">ByLaws Passed?</p><br>
      <select tab="Admin" id="bod`+bodsIndex+`-bylawsBoolean" name="bylawsBoolean" oninput="updateList(this.id,'bod','`+meetingId+`')">
        <option disabled selected value>Select :</option>
        <option value="True">Yes</option>
        <option value="False">No</option>
      </select>
    </div>
    <div class="col-lg-2">
      <p class="label">Budget Passed?</p><br>
      <select tab="Admin" id="bod`+bodsIndex+`-budgetBoolean" value="False" name="budgetBoolean" oninput="updateList(this.id,'bod','`+meetingId+`')">
        <option disabled selected value>Select :</option>
        <option value="True">Yes</option>
        <option value="False">No</option>
      </select>
    </div>
    <div class="col-lg-9">
      <p class="label"><i class="fa fa-file-text" aria-hidden="true"></i>&nbsp;&nbsp;Agenda of the Meeting (brief)</p><br>
      <input tab="Admin" oninput="updateList(this.id,'bod','`+meetingId+`')" type="text" maxlength='1000' id="bod`+bodsIndex+`-agenda" name="meetingAgenda">
    </div>
    <div class="col-lg-3">
      <br>
      <button type="button" id="bod`+meetingId+`Del" onclick="deleteRow('bod',this.id)">Delete Row</button>
    </div>
    <div class="col-lg-12">
      <hr style="border-width : thin; border-color:grey;border-radius : 4px;">
    </div>
  </div>

  `);

  day1 = year+'-'+monthNo+'-01';
  daylast = year+'-'+monthNo+'-31';
  $("#bod"+bodsIndex+"-date").attr("min", day1);
  $("#bod"+bodsIndex+"-date").attr("max", daylast);

  if(meetingNo!=null) $("#"+"bod"+bodsIndex+"-no").val(meetingNo); 
  $("#"+"bod"+bodsIndex+"-date").val(meetingDate);
  if(meetingAgenda!=null) $("#"+"bod"+bodsIndex+"-agenda").val(meetingAgenda); 
  if(bylawsBoolean!='None')
  $("#"+"bod"+bodsIndex+"-bylawsBoolean").val(bylawsBoolean);
  if(budgetBoolean!='None')
  $("#"+"bod"+bodsIndex+"-budgetBoolean").val(budgetBoolean);
  if(meetingAttendance!=null) $("#"+"bod"+bodsIndex+"-attendance").val(meetingAttendance); 

  updateProgress();

  
}

function appendFEvent(eventId=null, eventName=null, eventStartDate=null, eventEndDate=null, eventAvenue=null, eventDescription=null) {
  feventsIndex+=1;
  if (eventId==null)
  eventId="E-"+feventsIndex+"-"+month+"-"+makeid(5);
  
  $("#futureEvents").append(`
  <div class="row" id="fevent`+eventId+`">
    <div class="col-lg-3">
      <p class="label"><i class="fa fa-file-text" aria-hidden="true"></i>&nbsp;&nbsp;Name of the Event</p><br>
      <input tab="Others" oninput="updateList(this.id,'fevent','`+eventId+`')" maxlength="50" type="text" id="fevent`+feventsIndex+`-name" name="eventName">
    </div>
    <div class="col-lg-3">
      <p class="label"><i class="fa fa-calendar" aria-hidden="true"></i>&nbsp;&nbsp;Start Date</p><br>
      <input tab="Others" oninput="$('#fevent`+feventsIndex+`-endDate').attr('min', this.value);updateList(this.id,'fevent','`+eventId+`')" type="date" id="fevent`+feventsIndex+`-startDate" name="eventStartDate">
    </div>
    <div class="col-lg-3">
      <p class="label"><i class="fa fa-calendar" aria-hidden="true"></i>&nbsp;&nbsp;End Date</p><br>
      <input tab="Others" oninput="$('#fevent`+feventsIndex+`-startDate').attr('max', this.value);updateList(this.id,'fevent','`+eventId+`')" type="date" id="fevent`+feventsIndex+`-endDate" name="eventEndDate">
    </div>
    <div class="col-lg-3">
      <p class="label"><i class="fa fa-hashtag" aria-hidden="true"></i>&nbsp;&nbsp;Avenue</p><br>
      <select tab="Others" oninput="updateList(this.id,'fevent','`+eventId+`')" id="fevent`+feventsIndex+`-Avenue" name="eventAvenue">
        <option disabled selected value>Select :</option>
        <option value="CM">Community Service</option>
        <option value="CS">Club Service</option>
        <option value="IS">International Service</option>
        <option value="PD">Professional Development</option>
      </select>
    </div>
    <div class="col-lg-9">
      <p class="label"><i class="fa fa-info-circle" aria-hidden="true"></i>&nbsp;&nbsp;Event Description</p><br>
      <input tab="Others" oninput="updateList(this.id,'fevent','`+eventId+`')" maxlength="1000" type="text" id="fevent`+feventsIndex+`-description" name="eventDescription">
    </div>
    <div class="col-lg-3">
      <br>
      <button type="button" id="fevent`+eventId+`Del" onclick="deleteRow('fevent',this.id)">Delete Row</button>
    </div>
    <div class="col-lg-12">
      <hr style="border-width : thin; border-color:grey;border-radius : 4px;">
    </div>
  </div>

  `);

  day1 = year+'-'+((today.getMonth()<10)?("0"+today.getMonth()):today.getMonth())+'-01';
  
  $("#fevent"+feventsIndex+"-startDate").attr("min", day1);
  $("#fevent"+feventsIndex+"-endDate").attr("min", day1);


  if(eventName!=null) $("#"+"fevent"+feventsIndex+"-name").val(eventName);
  if(eventStartDate!=null) $("#"+"fevent"+feventsIndex+"-startDate").val(eventStartDate);
  if(eventEndDate!=null) $("#"+"fevent"+feventsIndex+"-endDate").val(eventEndDate);
  if(eventAvenue!=null) $("#"+"fevent"+feventsIndex+"-Avenue").val(eventAvenue);
  if(eventDescription!=null) $("#"+"fevent"+feventsIndex+"-description").val(eventDescription);

  updateProgress();
}

function appendEvent(eventId=null, eventName=null, eventStartDate=null, eventEndDate=null, eventAvenue=null, eventAttendance=null, eventHours=null, eventFundsRaised=null, eventDescription=null, eventLink=null) {
  eventsIndex+=1;
  if (eventId==null)
  eventId="E-"+eventsIndex+"-"+month+"-"+makeid(5);
  
  $("#events").append(`
  <div class="row" id="event`+eventId+`">
    <div class="col-lg-3">
      <p class="label"><i class="fa fa-file-text" aria-hidden="true"></i>&nbsp;&nbsp;Name of the Event</p><br>
      <input tab="Avenue" oninput="updateList(this.id,'event','`+eventId+`')" maxlength="50" type="text" id="event`+eventsIndex+`-name" name="eventName">
    </div>
    <div class="col-lg-3">
      <p class="label"><i class="fa fa-calendar" aria-hidden="true"></i>&nbsp;&nbsp;Start Date</p><br>
      <input tab="Avenue" oninput="$('#event`+eventsIndex+`-endDate').attr('min', this.value);updateList(this.id,'event','`+eventId+`')" type="date" id="event`+eventsIndex+`-startDate" name="eventStartDate">
    </div>
    <div class="col-lg-3">
      <p class="label"><i class="fa fa-calendar" aria-hidden="true"></i>&nbsp;&nbsp;End Date</p><br>
      <input tab="Avenue" oninput="updateList(this.id,'event','`+eventId+`')" type="date" id="event`+eventsIndex+`-endDate" name="eventEndDate">
    </div>
    <div class="col-lg-3">
      <p class="label"><i class="fa fa-hashtag" aria-hidden="true"></i>&nbsp;&nbsp;Avenue</p><br>
      <select tab="Avenue" oninput="updateList(this.id,'event','`+eventId+`')" id="event`+eventsIndex+`-Avenue" name="eventAvenue">
        <option disabled selected value>Select :</option>
        <option value="CM">Community Service</option>
        <option value="CS">Club Service</option>
        <option value="IS">International Service</option>
        <option value="PD">Professional Development</option>
      </select>
    </div>
    <div class="col-lg-12">
      <p class="label"><i class="fa fa-info-circle" aria-hidden="true"></i>&nbsp;&nbsp;Event Description</p><br><br>
      <textarea tab="Avenue" oninput="updateList(this.id,'event','`+eventId+`')" maxlength="1000" rows="10" id="event`+eventsIndex+`-description" name="eventDescription"></textarea>
    </div>
    <div class="col-lg-2">
      <p class="label"><i class="fa fa-user-times" aria-hidden="true"></i>&nbsp;&nbsp;Attendees<b style="color:red"> *</b></p><br>
      <input tab="Avenue" min=0 step=1 max=999999 oninput="validity.valid||(value='');updateList(this.id,'event','`+eventId+`')" type="number" id="event`+eventsIndex+`-attendance" name="eventAttendance">
    </div>
    <div class="col-lg-2">
      <p class="label"><i class="fa fa-clock-o" aria-hidden="true"></i>&nbsp;Volunteer Hrs<b style="color:red"> *</b></p><br>
      <input tab="Avenue" type="number" Placeholder="Hrs" min=0 step=1 max=999999 oninput="validity.valid||(value='');updateList(this.id,'event','`+eventId+`')" id="event`+eventsIndex+`-hours" name="eventHours">
    </div>
    <div class="col-lg-2">
      <p class="label"><i class="fa fa-inr" aria-hidden="true"></i>&nbsp;&nbsp;Funds raised<b style="color:red"> *</b></p><br>
      <input tab="Avenue" type="number" Placeholder="Rs. " min=0 max=99999999 step=1 oninput="validity.valid||(value='');updateList(this.id,'event','`+eventId+`')" id="event`+eventsIndex+`-fundsRaised" name="eventFundRaised">
    </div>
    <div class="col-lg-3">
      <p class="label"><i class="fa fa-link" aria-hidden="true"></i>&nbsp;&nbsp;Instagram Link of the Event</p><br>
      <input tab="Avenue" Placeholder="Copy and paste your link" type="url" maxlength="150" oninput="validateUrl(this.id)||(value='');updateList(this.id,'event','`+eventId+`');" id="event`+eventsIndex+`-link" name="eventLink">
    </div>
    <div class="col-lg-3">
      <br>
      <button type="button" id="event`+eventId+`Del" onclick="deleteRow('event',this.id)">Delete Row</button>
    </div>
    <div class="col-lg-12">
      <hr style="border-width : thin; border-color:grey;border-radius : 4px;">
    </div>
  </div>

  `);

  day1 = year+'-'+monthNo+'-01';
  daylast = year+'-'+monthNo+'-31';
  $("#event"+eventsIndex+"-startDate").attr("min", day1);
  $("#event"+eventsIndex+"-startDate").attr("max", daylast);
  $("#event"+eventsIndex+"-endDate").attr("min", day1);
  

  if(eventName!=null) $("#"+"event"+eventsIndex+"-name").val(eventName);
  if(eventStartDate!=null) $("#"+"event"+eventsIndex+"-startDate").val(eventStartDate);
  if(eventEndDate!=null) $("#"+"event"+eventsIndex+"-endDate").val(eventEndDate);
  if(eventAvenue!=null) $("#"+"event"+eventsIndex+"-Avenue").val(eventAvenue);
  if(eventAttendance!=null) $("#"+"event"+eventsIndex+"-attendance").val(eventAttendance);
  if(eventHours!=null) $("#"+"event"+eventsIndex+"-hours").val(eventHours);
  if(eventFundsRaised!=null) $("#"+"event"+eventsIndex+"-fundsRaised").val(eventFundsRaised);
  if(eventDescription!=null) $("#"+"event"+eventsIndex+"-description").val(eventDescription);
  if(eventLink!=null) $("#"+"event"+eventsIndex+"-link").val(eventLink);   

  updateProgress();
}

function appendBulletin(bulletinId=null,bulletinName=null,bulletinType=null,bulletinLink=null,bulletinIssuedOn=null,lastBulletinIssuedOn=null,bulletinFrequency=null) {
  bulletinsIndex+=1;
  
  if (bulletinId==null)
  bulletinId='404-B';
  $("#bulletins").html(`
  <div class="row" id='Bulletin`+bulletinId+`'>
    <div class="col-lg-4">
      <p class="label">Name of Bulletin</p><br>
      <input tab="Others" oninput="updateList(this.id,'bulletin','`+bulletinId+`')" type="text" maxlength="50" name="bulletinName" id="bulletin`+bulletinsIndex+`-name">
    </div>  
    <div class="col-lg-4">
      <p class="label">Type of Bulletin</p><br>
      <select tab="Others" oninput="updateList(this.id,'bulletin','`+bulletinId+`')" name="bulletinType" id="bulletin`+bulletinsIndex+`-type">
      <option disabled selected value>Select :</option>
        <option value="E-Bulletin">E-Bulletin</option>
        <option value="Print">Print</option>
        <option value="">NA</option>
    </select>
    </div>
    <div class="col-lg-4">
      <p class="label">Drive Link</p><br>
      <input tab="Others" type="url" maxlength="150" oninput="validateUrl(this.id)||(value='');updateList(this.id,'bulletin','`+bulletinId+`')" name="bulletinLink" id="bulletin`+bulletinsIndex+`-link">
    </div>
    <div class="col-lg-4">
      <p class="label">Issued on</p><br>
      <input tab="Others" oninput="$('#bulletin`+bulletinsIndex+`-lastIssued').attr('max', this.value);updateList(this.id,'bulletin','`+bulletinId+`')" type="date" name="bulletinIssuedOn" id="bulletin`+bulletinsIndex+`-issuedOn">
    </div>
    <div class="col-lg-4">
      <p class="label">Last Issued on</p><br>
      <input tab="Others" oninput="updateList(this.id,'bulletin','`+bulletinId+`')" type="date" name="lastBulletinIssuedOn" id="bulletin`+bulletinsIndex+`-lastIssued">
    </div>
    <div class="col-lg-4">
      <p class="label">Frequency</p><br>
      <input tab="Others" oninput="updateList(this.id,'bulletin','`+bulletinId+`')" type="text" maxlength="20" name="bulletinFrequency" id="bulletin`+bulletinsIndex+`-frequency">
    </div>
  `);

  day1 = year+'-'+monthNo+'-01';
  daylast = year+'-'+monthNo+'-31';
  $("#bulletin"+bulletinsIndex+"-issuedOn").attr("min", day1);
  $("#bulletin"+bulletinsIndex+"-issuedOn").attr("max", daylast);
  $("#bulletin"+bulletinsIndex+"-lastIssued").attr("max", daylast);

  if(bulletinName!=null) $("#"+"bulletin"+bulletinsIndex+"-name").val(bulletinName);
  if(bulletinType!=null) $("#"+"bulletin"+bulletinsIndex+"-type").val(bulletinType);
  if(bulletinLink!=null) $("#"+"bulletin"+bulletinsIndex+"-link").val(bulletinLink);
  if(bulletinIssuedOn!=null) $("#"+"bulletin"+bulletinsIndex+"-issuedOn").val(bulletinIssuedOn);
  if(lastBulletinIssuedOn!=null) $("#"+"bulletin"+bulletinsIndex+"-lastIssued").val(lastBulletinIssuedOn);
  if(bulletinFrequency!=null) $("#"+"bulletin"+bulletinsIndex+"-frequency").val(bulletinFrequency);

  updateProgress();
  
}

function appendFeedback(questionText = '', questionId = '', booleanResponse = '') {

    $("#feedback").append(`
            <div class="col-lg-8">
                <p class="label" style="word-break: normal;white-space:normal;">`+questionText+`</p>
            </div>
            <div class="col-lg-4">
                <select tab="Others" name="booleanResponse"  id="`+questionId+`-feedback" oninput="updateList(this.id,'feedback','`+questionId+`')">
                    <option disabled selected value>Select :</option>
                    <option value="True">Yes</option>
                    <option value="False">No</option>
                </select>
            </div>
            `);
            if(booleanResponse!='None')
            $("#"+questionId+"-feedback").val(booleanResponse);

    updateProgress();
}

function appendMemberMatrixRow(attributeId = '', attributeText = '', operation = '', maleCount = '', femaleCount = '', othersCount = '' ) {
    $("#memberMatrix").append(`
    <div class="row m-memberMatrix">
        <div class="col-xs-2 col-lg-4" id="`+attributeId+`-header">
            <p>`+attributeText+`</p>
        </div>
        <div class="col-xs-2">
            <input tab="Admin" Placeholder = "Male" type="number" min=0 step=1 max=9999 oninput="validity.valid||(value='');updateMatrix(`+attributeId+`,'Male',this.id);updateList(this.id,'matrix','`+attributeId+`');"  name="maleCount"  id="M-`+attributeId+`-M">
        </div>
        <div class="col-xs-2">
            <input tab="Admin" Placeholder = "Female" type="number" min=0 step=1 max=9999 oninput="validity.valid||(value='');updateMatrix(`+attributeId+`,'Female',this.id);updateList(this.id,'matrix','`+attributeId+`');"  name="femaleCount"  id="M-`+attributeId+`-F">
        </div>
        <div class="col-xs-2">
            <input tab="Admin" Placeholder = "Others" type="number" min=0 step=1 max=9999 oninput="validity.valid||(value='');updateMatrix(`+attributeId+`,'Others',this.id);updateList(this.id,'matrix','`+attributeId+`');"  name="othersCount"  id="M-`+attributeId+`-O">
        </div>
        <div class="col-xs-2">
            <input tab="Admin" Placeholder = "Total" type="number" id="M-`+attributeId+`-T" readonly>
        </div>
    </div>
    `);
    
    $("#"+"M-"+attributeId+"-M").val(maleCount);
    $("#"+"M-"+attributeId+"-F").val(femaleCount);
    $("#"+"M-"+attributeId+"-O").val(othersCount);
    matrix[attributeId] = {
        'Male' : (isNaN(maleCount) || maleCount=='')? 0 : parseInt(maleCount),
        'Female' : (isNaN(femaleCount) || femaleCount=='')? 0 : parseInt(femaleCount),
        'Others' : (isNaN(othersCount) || othersCount=='')? 0 : parseInt(othersCount),
        'Operator': operation,
    };

    var mq = window.matchMedia( "(max-width: 1000px)" );
    if (mq.matches) {
      $("#"+attributeId+"-header").html("<p>"+rowCount+"</p>");
      rowCount+=1;
    }
    
    updateProgress();
}

function appendMemberMatrixTotalRow(maleCount, femaleCount, othersCount, totalCount) {
    $("#memberMatrixTotal").html(`
    <div class="row m-memberMatrix">
        <div class="col-xs-2 col-lg-4" id="header">
            <p>Total</p>
        </div>
        <div class="col-xs-2">
            <input type="number" id = "maleTotal" readonly>
        </div>
        <div class="col-xs-2">
            <input type="number" id = "femaleTotal" readonly>
        </div>
        <div class="col-xs-2">
            <input type="number" id = "othersTotal" readonly>
        </div>
        <div class="col-xs-2">
            <input type="number" id = "totalTotal" readonly>
        </div>
    </div>
    `);
    
    $("#maleTotal").val(maleCount);
    $("#femaleTotal").val(femaleCount);
    $("#othersTotal").val(othersCount);
    $("#totalTotal").val(totalCount);

    var mq = window.matchMedia( "(max-width: 1000px)" );
    if (mq.matches) {

      $("#"+"header").html("<p>T</p>");
    }

    updateProgress();
}

function deleteRow(parent, child) {
  $('#'+child.replace("Del", "")).html('');
  deletedData[parent].push(child.replace("Del", "").replace(parent,""));

  updateProgress();
}

function validateUrl(id) {
  let input=document.getElementById(id);
  var str=input.value;
  var patt1=/^(https:\/\/www.instagram.com\/|-|https:\/\/drive.google.com\/)/g;
  var res=patt1.test(str);
  return res;
}

function updateMonth(reportingMonth=null) {

  let now=new Date();
  monthNo=reportingMonth.toString();
  
  if(monthNo == "01")
  month="January";
  else if(monthNo == "02")
  month="February";
  else if(monthNo == "03")
  month="March";
  else if(monthNo == "04")
  month="April";
  else if(monthNo == "05")
  month="May";
  else if(monthNo == "06")
  month="June";
  else if(monthNo == "07")
  month="July";
  else if(monthNo == "08")
  month="August";
  else if(monthNo == "09")
  month="September";
  else if(monthNo == "10")
  month="October";
  else if(monthNo == "11")
  month="November";
  else if(monthNo == "12")
  month="December";

  if($(window).width()>1000)
  $("#data10").html("<p>Members at the beginning of "+month+" <b style=\"color:red\"> **</b>");
  
  $("input[type=month]").val(now.getFullYear()+"-"+monthNo);

}

function makeid(length) {
  var result     ='';
  var characters   ='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  var charactersLength=characters.length;
  for ( var i=0; i < length; i++ ) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

function updateList(id,parent,child) {
  if(parent==null){
    data[$("#"+id).attr('name')]=document.getElementById(id).value;
  }
  else if (child in data[parent]){
    data[parent][child][$("#"+id).attr('name')]=document.getElementById(id).value;
  }
  else {
    data[parent][child]={};
    data[parent][child][$("#"+id).attr('name')]=document.getElementById(id).value;
  }

  updateProgress();
}

function updateTotalNumberOfMembers() {
  $("#totalNumberOfMembers").val(countN);
}

function updateTotalNumberOfInductedMembers() {
  $("#totalNumberOfAddedMembers").val(countn);
}

function updateDuesAlreadyPaid(paidAlreadyAttr = paidAlready) {
  paidAlready = (isNaN(paidAlreadyAttr) || paidAlreadyAttr == '') ? 0 : parseInt(paidAlreadyAttr);
  $("#paidAlready").val(paidAlready);
  updatePending();
}

function updatePaid(paidAttr = paid) {
  paid = (isNaN(paidAttr) || paidAttr == '') ? 0 : parseInt(paidAttr);
  $("#duesPaidInThisMonth").val(paid);
  updatePending();
}

function updateOwedMoney() {
  owedMoney = (parseInt(countN) + parseInt(countn))*300;
  $("#owed").val(owedMoney);
}

function updatePending(paidAttr = paid) {
  paid = (isNaN(paidAttr) || paidAttr == '') ? 0 : parseInt(paidAttr);
  pending = parseInt(owedMoney) - parseInt(paidAlready) - parseInt(paid);
  if (pending>0) $("#pending").val(pending);
  else $("#pending").val(0);
}

