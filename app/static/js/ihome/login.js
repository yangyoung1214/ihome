function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    $("#mobile").focus(function () {
        $("#mobile-err").hide();
    });
    $("#password").focus(function () {
        $("#password-err").hide();
    });
    $(".form-login").submit(function (e) {
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        }
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }

        var req_dict = {
            mobile: mobile,
            password:passwd
        };

        var req_data = JSON.stringify(req_dict)

        $.ajax({
            url: "/api/v1.0/session",
            type: "post",
            data: req_data,
            contentType: "application/json",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno == "0") {
                    location.href="/index.html"
                } else {
                    alert(resp.errmsg)
                }
            }
        })
    });
})