
function getSalt() {
    $.ajax({
        url: "http://jxglstu.hfut.edu.cn/eams5-student/login-salt",
        type: "GET",
        headers: {
            "Cookie": "SRVID=s114;"
        },
        success: function(response) {
            console.log(response);
        }
    });
}

function checkUserIdenty(){
    var username = document.getElementById('student_id').value.trim();
    var password = document.getElementById('pwd').value;
    document.getElementById('username').value = username;
    var param = {
        username : username,
        password : encryptionPwd(password)
    }
    jQuery.ajax({
    url: 'login?service=https%3A%2F%2Fcas.hfut.edu.cn%2Fcas%2Foauth2.0%2FcallbackAuthorize%3Fclient_id%3DBsHfutEduPortal%26redirect_uri%3Dhttps%253A%252F%252Fone.hfut.edu.cn%252Fhome%252Findex%26response_type%3Dcode%26client_name%3DCasOAuthClient',
    type: 'POST',
    dataType: 'json',
    data: param,
    success: function (result) {
        console.log("POST请求返回值:" + result);
    },
    error: function (jqXHR, textStatus, errorThrown) {
        // 处理请求失败的情况
        console.error('Error message:' , errorThrown);
    }
});
}

function validateForm() {
    const password = document.getElementById("register_password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    if (password !== confirmPassword) {
        alert("密码不匹配");
        return false;
    }
    const studentId = document.getElementById("student_id").value;
    if (isNaN(studentId) || studentId.length !== 10) {
        alert("学号输入错误");
        return false;
    }

    // 信息门户api

    return true;
}

// 密码加密
function encryptionPwd(pwd) {
    var secretKey = getCookie("LOGIN_FLAVORING"),
    key = CryptoJS.enc.Utf8.parse(secretKey),
    password = CryptoJS.enc.Utf8.parse(pwd),
    encrypted = CryptoJS.AES.encrypt(password, key, {mode: CryptoJS.mode.ECB, padding: CryptoJS.pad.Pkcs7}),
    encryptedPwd = encrypted.toString();
    return encryptedPwd;
}

// 获取cookie中的值 LOGIN_FLAVORING就是加密所需要的秘钥
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++)
    {
        var c = ca[i].trim();
        if (c.indexOf(name)===0) return c.substring(name.length,c.length);
    }
    return "";
}

// form表单提交之前 给密码加密
function formSubmit() {
    var password = document.getElementById('pwd').value;
    document.getElementById('password').value = encryptionPwd(password);
}
