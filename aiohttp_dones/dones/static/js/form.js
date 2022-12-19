regexes = {
  'mobile': /09([0-9])\d{8}$/,
  'email': /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/,
  'username': /\d{8}$/,
  'min_length': /^.{6,}$/
}
function validateForm(formId) {
  let fieldIsInvalid = false;
  let formIsInvalid = false;
  $("#" + formId + " .form-field").each(function () {
    fieldIsInvalid = false;
    let ffInput = $(this).find("input, textarea");
    let ffError = $(this).find(".field-error");
    let ffRequired = ffInput.data("required");
    let ffValidation = ffInput.data("validation")
    if (ffInput.data("fftype") == "mobile" || ffInput.data("fftype") == "national_id") ffInput.val(farsiFix(ffInput.val()));
    $(this).removeClass("has-error");
    ffError.text("");
    if (ffRequired !== undefined && ffValidation !== undefined) {
      if (ffInput.val().trim() == "") {
        ffError.text("الزامی");
        fieldIsInvalid = true;
      } else if (!isValid(ffInput.val(), ffValidation)) {
        ffError.text(ffError.data("error"));
        fieldIsInvalid = true;
      }
    } else if (ffRequired !== undefined) {
      if (ffInput.val().trim() == "") {
        ffError.text("الزامی");
        fieldIsInvalid = true;
      }
    } else if (ffValidation !== undefined) {
      if (!isValid(ffInput.val(), ffValidation) && ffInput.val().trim() != "") {
        ffError.text(ffError.data("error"));
        fieldIsInvalid = true;
      }
    }
    if (fieldIsInvalid) {
      $(this).addClass("has-error");
      formIsInvalid = true;
    }
  });
  if (!formIsInvalid) $("#" + formId).submit();
}
function isValid(inputValue, inputType) {
  return inputType == 'national_id' ? isValidNationalId(inputValue) : regexes[inputType].test(inputValue);
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
      return -1;
    }
  }
  return result;
}
function isValidNationalId(input) {
  if (!/^\d{10}$/.test(input)
    || input == '0000000000'
    || input == '1111111111'
    || input == '2222222222'
    || input == '3333333333'
    || input == '4444444444'
    || input == '5555555555'
    || input == '6666666666'
    || input == '7777777777'
    || input == '8888888888'
    || input == '9999999999')
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