displayView = function(){
   //the code required to display view
    if(localStorage.getItem("userToken")){
        document.getElementById("divTest").innerHTML = document.getElementById("profileView").innerHTML;
        selectTab(document.getElementById("home"));
    }else{
        document.getElementById("divTest").innerHTML = document.getElementById("welcomeView").innerHTML;
    }
};

window.onload = function(){
    displayView();
};



validateForm = function(){

    var password = document.getElementById("signUpForm").elements.namedItem("password").value;
    var passwordRepeat = document.getElementById("signUpForm").elements.namedItem("repeatPSW").value;

    if(checkPasswordLength(password) || checkPasswordLength(passwordRepeat)){
	    document.getElementById("signupMessage").innerHTML = "Passwords must be at least 4 characters long.";
	    return false;
    }

    if(!checkEmail(document.getElementById("signUpForm").elements.namedItem("email").value)){
        document.getElementById("signupMessage").innerHTML = "Not a legit email.";
        return false;
    }

    if(password == passwordRepeat ){
    	return true;
    }
    document.getElementById("signupMessage").innerHTML = "Passwords do not match.";
    return false;

};

//Return true for passwords which lenght is <= 3
checkPasswordLength = function(password){
    return password.length <= 3;
};


checkEmail = function(email){
    var re = /\S+@\S+\.\S+/;

    if(re.test(email)){
        return true;
    }
    return false;

};


function sendForm(){
    var xmlhttp;

    var e = document.getElementById("signUpForm");
    var d = document.getElementById("genderSelect");

    checkEmail(e.elements.namedItem("email").value);

    var formData = new FormData();
    formData.append("email", e.elements.namedItem("email").value);
    formData.append("password", e.elements.namedItem("password").value);
    formData.append("firstname", e.elements.namedItem("firstname").value);
    formData.append("familyname",e.elements.namedItem("familyname").value);
    formData.append("gender", d.options[d.selectedIndex].text);
    formData.append("city", e.elements.namedItem("city").value);
    formData.append("country", e.elements.namedItem("country").value);


/*
            email: e.elements.namedItem("email").value,
            password: e.elements.namedItem("password").value,
            firstname: e.elements.namedItem("firstname").value,
            familyname: e.elements.namedItem("familyname").value,
            gender: d.options[d.selectedIndex].text,
            city: e.elements.namedItem("city").value,
            country: e.elements.namedItem("country").value

*/
    if(validateForm()){
        xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST","http://127.0.0.1:5000/signUp","false");
        xmlhttp.send(formData);
        //var result = serverstub.signUp(formData);

        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                document.getElementById("signupMessage").innerHTML = JSON.parse(xmlhttp.responseText).message;
            }
        };
        return false;
    }

}


loginForm = function(){
    var e = document.getElementById("loginForm");
    var formData = new FormData();
    formData.append("email", e.elements.namedItem("username").value);
    formData.append("password", e.elements.namedItem("password").value);


    var url = "/signIn";
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.open("POST", url, true);
    xmlhttp.send(formData);

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            result = JSON.parse(xmlhttp.responseText);

            if(!result.success){
	            document.getElementById("loginMessage").innerHTML = result.message;
            }else {
                document.getElementById("loginMessage").innerHTML = "";
                localStorage.setItem("userToken", result.data);
                displayView();
            }
        }
    };
};

logout = function(){
    serverstub.signOut(localStorage.getItem('userToken'));
    localStorage.removeItem('userToken');
    displayView();
};


changePassword = function(){
    var oldPassword = document.getElementById("changePasswordForm").elements.namedItem("oldPassword").value;
    var newPassword = document.getElementById("changePasswordForm").elements.namedItem("newPassword").value;
    var token = localStorage.getItem('userToken');
    var changePasswordText = document.getElementById("changePasswordText");

    if(checkPasswordLength(newPassword)) {
        changePasswordText.innerHTML="Password has to be 4 characters or more";
    }else if(oldPassword == newPassword) {
        changePasswordText.innerHTML="You picked the same password. Please pick another.";
    }
    else{
        var result = serverstub.changePassword(token, oldPassword, newPassword);
        if(result.success){
            changePasswordText.innerHTML=result.message;
            return true;
        }else if(!result.success){
            changePasswordText.innerHTML=result.message;
            return false;
        }
    }
};

selectTab = function(item){

    console.log(item.id);

    var changePasswordText = document.getElementById("changePasswordText");
    changePasswordText.innerHTML ="";
    
    if(item.innerHTML =="Home") {
	document.getElementById("displayHome").style.display = "block";
	document.getElementById("displayBrowse").style.display = "none";
	document.getElementById("displayAccount").style.display = "none";
	getProfile(null, true);

    }else if(item.innerHTML == "Browse"){

        document.getElementById("displayHome").style.display = "none";
        document.getElementById("displayBrowse").style.display = "block";
        document.getElementById("displayAccount").style.display = "none";


    }else if (item.innerHTML =="Account") {

        document.getElementById("displayHome").style.display = "none";
        document.getElementById("displayBrowse").style.display = "none";
        document.getElementById("displayAccount").style.display = "block";

    }
};

selectHomeTab = function() {
    document.getElementById("displayHome").style.display = "block";
    document.getElementById("displayBrowse").style.display = "none";
    document.getElementById("displayAccount").style.display = "none";
};


searchUser = function() {
    userEmail = document.getElementById("searchForm").elements.namedItem("searchEmail").value;
    getProfile(userEmail, false);
    selectHomeTab();
};

getProfile = function(userEmail, currentUser) {
    getUserData(userEmail, currentUser);
    getMessages(userEmail, currentUser);
};

getUserData = function(userEmail, currentUser) {
    if (currentUser) {
	var userData = serverstub.getUserDataByToken(localStorage.getItem('userToken'));	
    } else {
	var userData = serverstub.getUserDataByEmail(localStorage.getItem('userToken'), userEmail);	
    }

    document.getElementById("userEmail").innerHTML = userData.data.email;
    document.getElementById("userFirstName").innerHTML = userData.data.firstname;
    document.getElementById("userFamilyName").innerHTML = userData.data.familyname;
    document.getElementById("userGender").innerHTML = userData.data.gender;
    document.getElementById("userCity").innerHTML = userData.data.city;
    document.getElementById("userCountry").innerHTML = userData.data.country;  

};

sendMessage = function() {
    
    var message = document.getElementById("postMessageForm").elements.namedItem("message").value;
    var token = localStorage.getItem("userToken");
    var email = document.getElementById("userEmail").innerText;
    var sentMessage = serverstub.postMessage(token, message, email);
    
    if(!sentMessage.success){
	window.alert(sentMessage.message);
    }
};


getMessages = function(userEmail, currentUser) {
    var wall = document.getElementById("wall");

    if (currentUser) {
	var messages = serverstub.getUserMessagesByToken(localStorage.getItem("userToken"));	
    } else {
	var messages = serverstub.getUserMessagesByEmail(localStorage.getItem("userToken"), userEmail);		
    }

    while (wall.hasChildNodes()) {   
	wall.removeChild(wall.firstChild);
    }

    for (i = 0; i < messages.data.length; i++) {
	var tempDiv = document.createElement("div");
	var message = document.createTextNode(messages.data[i].content);
	var writer = document.createTextNode(messages.data[i].writer);
	
	tempDiv.className = "messageDiv";

	wall.appendChild(tempDiv);
	tempDiv.appendChild(message);
	tempDiv.appendChild(document.createElement("br"));
	tempDiv.appendChild(document.createTextNode(" posted by "));
	tempDiv.appendChild(writer);
	tempDiv.appendChild(document.createElement("br"))

    }
};