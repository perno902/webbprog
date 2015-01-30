/**
 * Created by cake on 2015-01-26.
 */

function validateForm(){

    window.alert("YESSSSS");

    var password = document.forms["signUpForm"]["password"].value;
    var repeatPSW = document.forms["signUpForm"]["repeatPSW"].value;

    document.write(password);

    /*if(password != repeatPSW){
        window.alert("Passwords does not match!");
        return false;
    }*/

}