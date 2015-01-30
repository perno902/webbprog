displayView = function(){
    //the code required to display view
    //document.getElementById("divTest").innerHTML = document.getElementById("welcomeView").innerHTML;


    if(localStorage.getItem("userToken")){
        document.getElementById("divTest").innerHTML = document.getElementById("profileView").innerHTML;
       	selectTab(document.getElementById("home"));


    }else{
        document.getElementById("divTest").innerHTML = document.getElementById("welcomeView").innerHTML;

    }




};

window.onload = function(){
    //code that executes as the page is loaded.
    //You shall put your own custom code here.
    displayView();
    console.log("AJAJAJAJA");

};



validateForm = function(){

    var password = document.getElementById("signUpForm").elements.namedItem("password").value;
    var passwordRepeat = document.getElementById("signUpForm").elements.namedItem("repeatPSW").value;

    if(checkPasswordLength(password) || checkPasswordLength(passwordRepeat)){
        window.alert("Passwords must be at least 4 characters long.");
    }
    //checkPasswordLength(password);
    //checkPasswordLength(passwordRepeat);
    /*if(password.length < 4 || passwordRepeat.length < 4){
        window.alert("Passwords must be at least 4 characters long.");
        return false;
    }*/

    if(password == passwordRepeat ){
        return true;
    }
    window.alert("Passwords do not match.");
    return false;

};
//Return true for passwords which lenght is <= 3
checkPasswordLength = function(password){
    return password.length <= 3;
};


sendForm = function(){



    var e = document.getElementById("signUpForm");
    var d = document.getElementById("genderSelect");

    var formData = {
        email: e.elements.namedItem("email").value,
        password: e.elements.namedItem("password").value,
        firstname: e.elements.namedItem("firstname").value,
        familyname: e.elements.namedItem("familyname").value,
        gender: d.options[d.selectedIndex].text,
        city: e.elements.namedItem("city").value,
        country: e.elements.namedItem("country").value
    };


    if(validateForm()){
        var result = serverstub.signUp(formData);
        if(!result.success){
            window.alert(result.message);
        }
    }

    return false;
};


loginForm = function(){
    var username = document.getElementById("loginForm").elements.namedItem("username").value;
    var password = document.getElementById("loginForm").elements.namedItem("password").value;

    var result = serverstub.signIn(username, password);

    if(!result.success){
        window.alert(result.message);

    }else{
        localStorage.setItem("userToken", result.data);
        displayView();
    }
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

    if(checkPasswordLength(newPassword)) {
        window.alert("New password has to be 4 characters or more");
    }else if(oldPassword == newPassword) {
        window.alert("You picked the same password. Please pick another.");
    }
    else{
        var result = serverstub.changePassword(token, oldPassword, newPassword);


        if(result.success){
            window.alert(result.message);
            return true;
        }else if(!result.success){
            window.alert(result.message);
            return false;
        }
    }
};



  
selectTab = function(item){

    console.log(item.id);
    
    if(item.innerHTML =="Home") {
	document.getElementById("displayHome").style.display = "block";
	document.getElementById("displayBrowse").style.display = "none";
	document.getElementById("displayAccount").style.display = "none";
	getProfile(getCurrentEmail());

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



//-----------------------------------------------------


getCurrentEmail = function() {
    var userData = serverstub.getUserDataByToken(localStorage.getItem('userToken'));
    return userData.data.email;
};

searchUser = function() {
    userEmail = document.getElementById("searchForm").elements.namedItem("searchEmail").value;
    getProfile(userEmail);
    selectHomeTab();
   
};


getProfile = function(userEmail) {
    getUserData(userEmail);
    getMessages(userEmail);
};

getUserData = function(userEmail) {
    var userData = serverstub.getUserDataByEmail(localStorage.getItem('userToken'), userEmail);


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
    var email = document.getElementById("userEmail").innerHTML;
    
    
    var sentMessage = serverstub.postMessage(token, message, email);
    
    if(!sentMessage.success){
	window.alert(sentMessage.message);
    }
};


getMessages = function(userEmail) {
    var messages = serverstub.getUserMessagesByEmail(localStorage.getItem("userToken"), userEmail);
    var wall = document.getElementById("wall");

    while (wall.hasChildNodes()) {   
	wall.removeChild(wall.firstChild);
    }
    
    wall.appendChild(document.createElement("hr"));

    for (i = 0; i < messages.data.length; i++) {
	var message = document.createTextNode(messages.data[i].content);
	var writer = document.createTextNode(messages.data[i].writer);
	
	wall.appendChild(message);
	wall.appendChild(document.createElement("br"));
	wall.appendChild(document.createTextNode(" posted by "));
	wall.appendChild(writer);
	wall.appendChild(document.createElement("hr"));
    }
};