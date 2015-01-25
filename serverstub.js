/**
 * Created by TDDD97.
 */

var serverstub = new Object();
var users = null;
var loggedInUsers = null;

if (localStorage.getItem("users") == null) {
    users = {};
}else users = JSON.parse(localStorage.getItem("users"));

if (localStorage.getItem("loggedinusers") == null) {
    loggedInUsers = {};
}else loggedInUsers = JSON.parse(localStorage.getItem("loggedinusers"));

// Local methods
persistUsers = function(){
    localStorage.setItem("users", JSON.stringify(users));
};
persistLoggedInUsers = function(){
    localStorage.setItem("loggedinusers", JSON.stringify(loggedInUsers));
};
tokenToEmail = function(token){
    return loggedInUsers[token];
};
copyUser = function(user){
    return JSON.parse(JSON.stringify(user));
};


// Public methods
serverstub.signIn = function(email, password){
    if(users[email] != null && users[email].password == password){
        var letters = "abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890";
        var token = "";
        for (var i = 0 ; i < 36 ; ++i) {
            token += letters[Math.floor(Math.random() * letters.length)];
        }
        loggedInUsers[token] = email;
        persistLoggedInUsers();
        return {"success": true, "message": "Successfully signed in.", "data": token};
    } else {
        return {"success": false, "message": "Wrong username or password."};
    }
};

serverstub.postMessage = function(token, content, toEmail){
    var fromEmail = tokenToEmail(token);
    if (fromEmail != null) {
        if (toEmail == null) {
            toEmail = fromEmail;
        }
        if(users[toEmail] != null){
            var recipient = users[toEmail];
            var message = {"writer": fromEmail, "content": content};
            recipient.messages.unshift(message);
            persistUsers();
            return {"success": true, "message": "Message posted"};
        } else {
            return {"success": false, "message": "No such user."};
        }
    } else {
        return {"success": false, "message": "You are not signed in."};
    }
};

serverstub.getUserDataByToken = function(token){
    var email = tokenToEmail(token);
    return serverstub.getUserDataByEmail(token, email);
};

serverstub.getUserDataByEmail = function(token, email){
    if (loggedInUsers[token] != null){
        if (users[email] != null) {
            var match = copyUser(users[email]);
            delete match.messages;
            delete match.password;
            return {"success": true, "message": "User data retrieved.", "data": match};
        } else {
            return {"success": false, "message": "No such user."};
        }
    } else {
        return {"success": false, "message": "You are not signed in."};
    }
};
serverstub.getUserMessagesByToken = function(token){
    var email = tokenToEmail(token);
    return serverstub.getUserMessagesByEmail(token,email);
};
serverstub.getUserMessagesByEmail = function(token, email){
    if (loggedInUsers[token] != null){
        if (users[email] != null) {
            var match = copyUser(users[email]).messages;
            return {"success": true, "message": "User messages retrieved.", "data": match};
        } else {
            return {"success": false, "message": "No such user."};
        }
    } else {
        return {"success": false, "message": "You are not signed in."};
    }
};
serverstub.signOut = function(token){
    if (loggedInUsers[token] != undefined){
        delete loggedInUsers[token];
        persistLoggedInUsers();
        return {"success": true, "message": "Successfully signed out."};
    } else {
        return {"success": false, "message": "You are not signed in."};
    }
};
serverstub.signUp = function(formData){ // {email, password, firstname, familyname, gender, city, country}
    if (users[formData.email] === undefined){
        if(formData.email != undefined && formData.password != undefined && formData.firstname != undefined && formData.familyname != undefined && formData.gender != undefined && formData.city != undefined && formData.country != undefined){
            var user = {"email": formData.email,
                "password": formData.password,
                "firstname": formData.firstname,
                "familyname": formData.familyname,
                "gender": formData.gender,
                "city": formData.city,
                "country": formData.country,
                "messages": []};
            users[formData.email] = user;
            persistUsers();
            return {"success": true, "message": "Successfully created a new user."};
        }else{
            return {"success": false, "message": "Formdata not complete."};
        }

    } else {
        return {"success": false, "message": "User already exists."};
    }
};
serverstub.changePassword = function(token, oldPassword, newPassword){
    if (loggedInUsers[token] != null){
        var email = tokenToEmail(token);
        if (users[email].password == oldPassword){
            users[email].password = newPassword;
            return {"success": true, "message": "Password changed."};
        } else {
            return {"success": false, "message": "Wrong password."};
        }
    } else {
        return {"success": false, "message": "You are not logged in."};
    }
};