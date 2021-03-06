
var websocket = new WebSocket("ws://127.0.0.1:5000/api");

var tokenList = [];

/*
connect = function(){
    websocket = new WebSocket(url);
    websocket.onopen = function(){};
    websocket.onclose = function(){};
    websocket.onmessage = function(){
        if(e.data == "logout"){
        localStorage.removeItem('userToken');
    }
    };
};
*/

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




websocket.onopen = function(){
    console.log("open")
};



websocket.onclose = function(){
    displayView();
    //websocket.send("connection closed");
};


websocket.onmessage = function(e){
    if(e.data == "logout") {
        console.log("removing usertoken: " + localStorage.getItem('userToken'));

        localStorage.removeItem('userToken');
        websocket.onclose();
    }
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


    if(validateForm()){
        xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST","http://127.0.0.1:5000/signUp",true);
        xmlhttp.send(formData);

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
                console.log("innan " + localStorage.getItem('userToken'));
                localStorage.setItem("userToken", result.data);
                console.log("efter " + localStorage.getItem('userToken'));


                websocket.send(e.elements.namedItem("username").value);


                displayView();
            }
        }
    };
};

logout = function(){

    var formData = new FormData();
    formData.append("token", localStorage.getItem('userToken'));
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", "http://127.0.0.1:5000/signOut", true);
    xmlhttp.send(formData);

    localStorage.removeItem('userToken');
    displayView();
};


changePassword = function(){

    var formData = new FormData();
    formData.append("token", localStorage.getItem('userToken'));
    formData.append("oldPassword", document.getElementById("changePasswordForm").elements.namedItem("oldPassword").value);
    formData.append("newPassword", document.getElementById("changePasswordForm").elements.namedItem("newPassword").value);
    var changePasswordText = document.getElementById("changePasswordText");

    var oldPassword = document.getElementById("changePasswordForm").elements.namedItem("oldPassword").value;
    var newPassword = document.getElementById("changePasswordForm").elements.namedItem("newPassword").value;


    if(checkPasswordLength(newPassword)) {
        changePasswordText.innerHTML="Password has to be 4 characters or more";
    }else if(oldPassword == newPassword) {
        changePasswordText.innerHTML="You picked the same password. Please pick another.";
    }
    else {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST", "http://127.0.0.1:5000/changePassword", true);
        xmlhttp.send(formData);
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                var result = JSON.parse(xmlhttp.responseText);

                if (result.success) {
                    changePasswordText.innerHTML = result.message;
                    return true;
                } else if (!result.success) {
                    changePasswordText.innerHTML = result.message;
                    return false;
                }
            }
        }
    }
};

selectTab = function(item){

    console.log(localStorage.getItem('userToken'));

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
};

getProfile = function(userEmail, currentUser) {
    getUserData(userEmail, currentUser);
    getMessages(userEmail, currentUser);
};

getUserData = function(userEmail, currentUser) {
    var token = localStorage.getItem('userToken');
    //var token = 'DGk6eSkYXk4OwckycafJrkhVvh3OtcNPVoZUYIbBV4HGgClZadrsWCAont39Zb';
    var result;

    if (currentUser) {
        var url = "/getUserDataByToken/" + token;
    } else {
        var url = "/getUserDataByEmail?token=" + token + "&email=" + userEmail;
    }


    var xmlhttp = new XMLHttpRequest();

    xmlhttp.open("GET", url, true);
    xmlhttp.send();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            result = JSON.parse(xmlhttp.responseText);
            if (!result.success) {
                document.getElementById("browseMessage").innerHTML = result.message;
            } else {
                setUserData(JSON.parse(result.data));
            }
        }
    };

};

setUserData = function(userData) {
    document.getElementById("userEmail").innerHTML = userData.email;
    document.getElementById("userFirstName").innerHTML = userData.firstname;
    document.getElementById("userFamilyName").innerHTML = userData.familyname;
    document.getElementById("userGender").innerHTML = userData.gender;
    document.getElementById("userCity").innerHTML = userData.city;
    document.getElementById("userCountry").innerHTML = userData.country;

};

sendMessage = function() {
    var formData = new FormData();

    formData.append("token", localStorage.getItem("userToken"));
    //formData.append("token", 'DGk6eSkYXk4OwckycafJrkhVvh3OtcNPVoZUYIbBV4HGgClZadrsWCAont39Zb')
    formData.append("content", document.getElementById("postMessageForm").elements.namedItem("message").value);
    formData.append("toEmail", document.getElementById("userEmail").innerText);

    var url = "/postMessage";
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.open("POST", url, true);
    xmlhttp.send(formData);

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            result = JSON.parse(xmlhttp.responseText);
            if(!result.success){
	            console.log(result.message);
            }else {
                console.log(result.message);
            }
        }
    };



};


getMessages = function(userEmail, currentUser) {
    var wall = document.getElementById("wall");

    var token = localStorage.getItem('userToken');
    //var token = 'DGk6eSkYXk4OwckycafJrkhVvh3OtcNPVoZUYIbBV4HGgClZadrsWCAont39Zb';

    if (currentUser) {
        var url = "/getMessagesByToken/" + token;
    } else {
        var url = "/getMessagesByEmail?token=" + token + "&email=" + userEmail;
    }

    var xmlhttp = new XMLHttpRequest();

    xmlhttp.open("GET", url, true);
    xmlhttp.send();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            result = JSON.parse(xmlhttp.responseText);
            if (!result.success) {
                document.getElementById("browseMessage").innerHTML = result.message;
            } else {
                var messages = JSON.parse(result.data);

                while (wall.hasChildNodes()) {
                    wall.removeChild(wall.firstChild);
                }

                for (i = 0; i < messages.length; i++) {
                    var tempDiv = document.createElement("div");
                    var message = document.createTextNode(messages[i].content);
                    var writer = document.createTextNode(messages[i].writer);

                    tempDiv.className = "messageDiv";

                    wall.appendChild(tempDiv);
                    tempDiv.appendChild(message);
                    tempDiv.appendChild(document.createElement("br"));
                    tempDiv.appendChild(document.createTextNode(" posted by "));
                    tempDiv.appendChild(writer);
                    tempDiv.appendChild(document.createElement("br"))
                }

                document.getElementById("browseMessage").innerHTML = "";
                selectHomeTab();
            }
        }
    };
};




