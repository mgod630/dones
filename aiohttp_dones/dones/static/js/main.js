$(function () {
  $("#post_comment").click(function () {
    const section_id = $("#section_id").val();
    const reply_to = $("#reply_to").val();
    const comment_text = $("#reply_text").val();
    $("#result_message").removeClass("text-danger text-success");
    $.ajax({
      method: "POST",
      url: "/post-comment",
      data: { section_id, reply_to, comment_text },
    })
      .done(function (resp) {
        if (resp.result == "not_logged_in") {
          $("#result_message")
            .addClass("text-danger")
            .text("لطفا ابتدا وارد حساب کاربری خود شوید.")
            .slideDown();
        } else if (resp.result == "you_cant_answer_to_this_comment") {
          $("#result_message")
            .addClass("text-danger")
            .text("دسترسی به این قسمت برای شما مقدور نمی باشد.")
            .slideDown();
        } else if (resp.result == "succeed") {
          $("#result_message")
            .addClass("text-success")
            .text("پیام شما با موفقیت ارسال شد.")
            .slideDown();
          location.reload();
        } else {
          $("#result_message")
            .addClass("text-danger")
            .text("خطای غیر منتظره. لطفا مجدداً تلاش نمایید.")
            .slideDown();
        }
      })
      .fail(function (err) {
        $("#result_message")
          .addClass("text-danger")
          .text("خطای غیر منتظره. لطفا مجدداً تلاش نمایید.")
          .slideDown();
      });
  });
  $("#comments_container").on("click", ".reply-button", function (e) {
    e.preventDefault();
    $("#adressee").text($(this).closest(".comment").find(".usc-name").text());
    $("#reply_to").val($(this).data("postid"));
    $(".notices").eq(0).removeClass("d-none");
    $(".notices").eq(1).addClass("d-none");
    $("#reply_text").focus();
    $("#cancel_reply")[0].scrollIntoView();
  });
  $("#cancel_reply").click(function () {
    $("#reply_to").val(-1);
    $(".notices").eq(0).addClass("d-none");
    $(".notices").eq(1).removeClass("d-none");
    $("#reply_text").focus();
  });
  // if (
  //   $("#comments_container .comment-wrapper").attr("style", "padding-right") ==
  //   "0px"
  // ) {
  //   console.log("block");
  // } else {
  //   console.log("none");
  //   $(".comment .usc-a a").text("");
  // }
  //End Comments
});
handleObject = (template, data) => {
  let rendered_html = template;
  for (const [key, value] of Object.entries(data)) {
    let transformed_value = value;
    switch (key) {
      case "price":
        transformed_value = value === 0 ? "رایگان" : `${value} تومان`;
        break;
      case "depth":
        transformed_value = Number(value) * 15;
        break;
    }
    if ($("#ut").text() !== "-2" || key === "depth")
      rendered_html = $("<div>")
        .append(rendered_html)
        .find(".usc-buttons")
        .remove()
        .end()
        .html();
    if (key === "depth" && transformed_value > 0)
      rendered_html = $("<div>")
        .append(rendered_html)
        .find(".usc-a")
        .remove()
        .end()
        .html();
    $.ajax({
      method: "GET",
      url: "/get-admin",
    }).done(function (resp) {
      if (resp.result == "admin") {
        $(".deletComment").css("display", "block");
      }
    });
    rendered_html = rendered_html.replace(
      new RegExp(`{{${key}}}`, "g"),
      transformed_value
    );
  }
  return $.parseHTML(rendered_html);
};
handleText = (template, data) => {
  return $.parseHTML(template.replace(new RegExp("{{text}}", "g"), data));
};
JSONFormatter = (resp, struct) => {
  let result = resp[struct.data];
  if (struct.data === "course_details") {
    const { id, is_enrolled, price, video } = result;
    result.url =
      price === 0 || is_enrolled ? `/course-overview/${id}` : "#payment_modal";
    result.attr = price === 0 || is_enrolled ? "" : "data-toggle='modal'";
    result.has_video = video ? "" : "collapse";
  } else if (struct.data === "sections") {
    const pallete = [
      "blue-green",
      "lime",
      "cyan",
      "yellow",
      "pink",
      "orange",
      "green",
      "gray",
    ];
    result = result.map((item, index) => {
      item.row = index + 1;
      item.color = pallete[index % 8];
      return item;
    });
  }
  return result;
};
isObject = (inp) => typeof inp === "object" && inp !== null;

loadJson = (url, structure, callback) => {
  $.ajax({ method: "GET", url: url })
    .done(function (resp) {
      if (resp.error === "Not Found") {
        $(".busy-overlay").addClass("error");
      } else {
        structure.map((struct, index) => {
          $.get(
            `/static/html_bits/${struct.template}`,
            (template) => {
              const rawData = resp[struct.data];
              if (
                (rawData && rawData.length) ||
                (isObject(rawData) && Object.keys(rawData).length)
              ) {
                $(`#${struct.id} .busy-overlay`).addClass("collapse");
                let result = $(document.createDocumentFragment());
                if (Array.isArray(rawData)) {
                  rawData.map((data) => {
                    const rendered_html = isObject(data)
                      ? handleObject(template, data)
                      : handleText(template, data);
                    result.append(rendered_html);
                  });
                } else if (isObject(rawData)) {
                  result = handleObject(template, rawData);
                } else {
                  result = handleText(template, rawData);
                }
                $(`#${struct.id}`).empty().append(result);
              } else {
                $(`#${struct.id} .busy-overlay`).addClass("empty");
              }
              callback &&
              struct.data === "all_comments" &&
              index === structure.length - 1
                ? callback({
                    current_page: resp.current_page,
                    pages_count: resp.pages_count,
                  })
                : null;
            },
            "html"
          );
        });
      }
    })
    .fail(function (err) {
      $(".busy-overlay").addClass("error");
    });
};
