$(function () {
  let timerBase = 120;
  let intrvl = setInterval(() => {
    if (timerBase > 0) {
      timerBase--;
      $("#resend_code span").text(timerBase);
    } else {
      timerBase = 0;
      $("#resend_code").addClass("clickable");
      $("#resend_code").text("ارسال مجدد پین");
      clearInterval(intrvl);
    }
  }, 1000);
  $("#resend_code").click(() => {
    if (!$("#resend_code").hasClass("clickable")) return;
    $("#resend_code_form").submit();
  });
  $("#mb_login").click(function () {
    toggleTo("login");
  });
  $("#mb_signup").click(function () {
    toggleTo("signup");
  });
  $(".forgotten-password").click(function () {
    toggleTo("reset");
  });
  $("#signup_form button").click(function () {
    toggleTo("afterSignUp");
  });
  function toggleTo(tab) {
    switch (tab) {
      case "login":
        $("#signup_form, #reset_form, #set_password_form")
          .fadeOut(500)
          .removeClass("active");
        $(".login-body").removeClass("expand");
        $("#login_form").delay(500).fadeIn(500).addClass("active");
        $("#mb_signup").removeClass("active");
        $("#mb_login").addClass("active");
        break;
      case "signup":
        $("#login_form, #reset_form, #set_password_form")
          .fadeOut(500)
          .removeClass("active");
        $(".login-body").addClass("expand");
        $("#signup_form").delay(500).fadeIn(500).addClass("active");
        $("#mb_login").removeClass("active");
        $("#mb_signup").addClass("active");
        break;
      case "reset":
        $("#login_form").fadeOut(500).removeClass("active");
        $("#reset_form").delay(500).fadeIn(500).addClass("active");
        $("#mb_login, #mb_signup").removeClass("active");
        break;
      // case "afterSignUp":
      //   $("#login_form, #reset_form, #signup_form")
      //     .fadeOut(500)
      //     .removeClass("active");
      //   $(".login-body").addClass("expand");
      //   $("#set_password_form").delay(500).fadeIn(500).addClass("active");
      //   $("#mb_login").removeClass("active");
      //   $("#mb_signup").addClass("active");
    }
  }

  $("#reset_form button").click(function () {
    validateForm("reset_form");
  });
  $("#login_form button").click(function () {
    validateForm("login_form");
  });
  $("#signup_form button").click(function () {
    validateForm("signup_form");
  });
  $("#set_password_form button").click(function () {
    validateForm("set_password_form");
  });
  $("#login_form").on("keydown", function (e) {
    if (e.keyCode == 13) $("#login_form button").click();
  });
  $("#signup_form").on("keydown", function (e) {
    if (e.keyCode == 13) $("#signup_form button").click();
  });
  function validateForm(formId) {
    let fieldIsInvalid = false;
    let formIsInvalid = false;
    $("#" + formId + " .form-field").each(function () {
      // fieldIsInvalid = $(this).val(false);
      let ffInput = $(this).find("input");
      let ffError = $(this).find(".field-error");
      let ffRequired = ffInput.data("required");
      let ffValidation = ffInput.data("validation");

      if (
        ffInput.data("fftype") == "mobile" ||
        ffInput.data("fftype") == "national_id"
      )
        ffInput.val(farsiFix(ffInput.val()));

      $(this).removeClass("has-error");
      ffError.text("");
      if (ffRequired !== undefined && ffValidation !== undefined) {
        if (ffInput.val().trim() == "") {
          ffError.fadeIn(100);
          ffError.text("الزامی");
          fieldIsInvalid = true;
          ffError.delay(500).fadeOut(3000);
          // fieldIsInvalid.delay(500).fadeOut(3000).val(false);
        } else if (!isValid(ffInput.val(), ffValidation)) {
          ffError.fadeIn(100);
          ffError.text(ffError.data("error"));
          fieldIsInvalid = true;
          ffError.delay(500).fadeOut(3000);
        }
      } else if (ffRequired !== undefined) {
        if (ffInput.val().trim() == "") {
          ffError.fadeIn(100);
          ffError.text("الزامی");
          fieldIsInvalid = true;
          ffError.delay(500).fadeOut(3000);
        }
      } else if (ffValidation !== undefined) {
        if (
          !isValid(ffInput.val(), ffValidation) &&
          ffInput.val().trim() != ""
        ) {
          ffError.fadeIn(100);
          ffError.text(ffError.data("error"));
          ffError.delay(500).fadeOut(3000);
          fieldIsInvalid = true;
        }
      }
      if (fieldIsInvalid) {
        $(this).addClass("has-error");
        formIsInvalid = true;
      }
    });
    if (!formIsInvalid) {
      $(".busy-overlay").addClass("visible");
      $("#" + formId).submit();
    }
  }
  $(".show-pass").on("click", function () {
    let passField = $(this).closest("div").find("input.form-control");
    if (passField.attr("type") == "password") {
      passField.attr("type", "text");
    } else {
      console.log("sss");
      passField.attr("type", "password");
    }
  });
});
regexes = {
  mobile: /09([0-9])\d{8}$/,
  email: /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/,
  username: /\d{8}$/,
  min_length: /^.{6,}$/,
  min_length4: /^.{4,}$/,
};
function isValid(inputValue, inputType) {
  let result = true;
  if (inputType == "national_id") {
    result = isValidNationalId(inputValue);
  } else if (inputType == "repeat") {
    console.log;
    result = $("[name=rp_new_password]").val() == inputValue;
  } else {
    result = regexes[inputType].test(inputValue);
  }
  return result;
}
function farsiFix(input) {
  var result = "";
  for (i in input) {
    if (input[i] === undefined) break;
    charCode = input[i].charCodeAt(0);
    if (charCode < 1786 && charCode > 1775) {
      result += String.fromCharCode(charCode - 1728);
    } else if (charCode < 58 && charCode > 47) {
      result += input[i];
    } else {
      return result;
    }
  }
  return result;
}
function isValidNationalId(input) {
  if (
    !/^\d{10}$/.test(input) ||
    input == "0000000000" ||
    input == "1111111111" ||
    input == "2222222222" ||
    input == "3333333333" ||
    input == "4444444444" ||
    input == "5555555555" ||
    input == "6666666666" ||
    input == "7777777777" ||
    input == "8888888888" ||
    input == "9999999999"
  )
    return false;
  var check = parseInt(input[9]);
  var sum = 0;
  var i;
  for (i = 0; i < 9; ++i) {
    sum += parseInt(input[i]) * (10 - i);
  }
  sum %= 11;
  return (sum < 2 && check == sum) || (sum >= 2 && check + sum == 11);
}
// function showPass() {
//   var x = document.getElementById("passInput");
//   if (x.type === "password") {
//     x.type = "text";
//   } else {
//     x.type = "password";
//   }
// }
