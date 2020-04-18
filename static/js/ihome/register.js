function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

var imageCodeId;
function generateImageCode() {
    imageCodeId = generateUUID();
    $(".image-code img").attr("src", "/api/getImageCode?codeid="+imageCodeId);
}

function sendSMSCode() {
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    var sdata = {mobile:mobile, image_code_id:imageCodeId, image_code_text:imageCode};
    $.ajax({
        url: '/api/smsCode',
        method: 'POST',
        data: JSON.stringify(sdata),
        headers: {
          'X-XSRFTOKEN': getCookie('_xsrf'),
        },
        contentType: 'application/json',
        dataType: 'json',
        success: function (data) {
            if ("0" == data.errorcode) {
                var duration = 60;
                var timeObj = setInterval(function () {
                    duration = duration - 1;
                    $(".phonecode-a").html(duration+"秒");
                    if (1 == duration) {
                        clearInterval(timeObj);
                        $(".phonecode-a").html("获取验证码");
                        $(".phonecode-a").attr("onclick", "sendSMSCode();")
                    }
                }, 1000, 60)
            } else {
                $("#image-code-err span").html(data.errormsg);
                $("#image-code-err").show();
                $(".phonecode-a").attr("onclick", "sendSMSCode();");
                if (data.errorcode == "4002" || data.errorcode == "4004") {
                    generateImageCode();
                }
            }
        }
    });

}

$(document).ready(function() {
    generateImageCode();
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });

    // 当用户点击表单提交按钮时执行自己定义的函数
    $(".form-register").submit(function(e){
        // 阻止浏览器对于表单的默认行为
        e.preventDefault();

        // 校验用户填写的参数
        mobile = $("#mobile").val();
        phoneCode = $("#phonecode").val();
        password = $("#password").val();
        password2 = $("#password2").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        }
        if (!phoneCode) {
            $("#phone-code-err span").html("请填写短信验证码！");
            $("#phone-code-err").show();
            return;
        }
        if (!password) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        if (password != password2) {
            $("#password2-err span").html("两次密码不一致!");
            $("#password2-err").show();
            return;
        }

        // 声明一个要保存结果的变量,把表单中的数据填充到data中
        // $(".form-register").serializeArray().map(function(x){data[x.name]=x.value});
        var sdata = {
            "mobile": mobile,
            "phoneCode": phoneCode,
            "password": password,
            "password2": password2
        };
        // 向后端发送请求
        $.ajax({
            url: "/api/register",
            method: 'POST',
            data: JSON.stringify(sdata),
            dataType: 'json',
            headers: {
                'X-XSRFTOKEN': getCookie("_xsrf"),
            },
            contentType: "application/json",
            success: function (rdata) {
                if ("0" == rdata.errorcode){
                    // alert("注册成功，请登录");
                    location.href = "/";
                }else{
                    $("#phone-code-err>span").html(rdata.errormsg);
                    $("#phone-code-err").show();
                }

            }
        });
    });





























})