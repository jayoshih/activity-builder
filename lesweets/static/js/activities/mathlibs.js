const correctMessages = ["Nice Work!", "Correct!", "You got it!"];

$(function() {
  	$("#submit-answer").on("click", submitAnswer);
  	$("#answer").on("keypress", hideMessages);
  	$("#blanks").on("submit", submitBlanks);
  	$("#review-link").on("click", showReview);
  	$(".blanks-link").on("click", showForm);
  	$("#clear-answers").on("click", clearForm);
});

function enterText(ev) {
	var id = $(ev.target).data('id');
	var value = $("#" + id + "-input").val();
	$("." + id).text(value);
}

function hideMessages(ev) {
	$(".message").hide();
}

function submitAnswer(ev) {
	if(eval($("#hidden-formula").text()) == $("#answer").val()) {
		var message = correctMessages[Math.floor(Math.random()*correctMessages.length)];
		$("#correct").text(message);
		$("#correct").fadeIn(500);
		$("#submit-answer").hide();
		setTimeout(function() {
			$("#new-story").fadeIn(500);
		}, 1000);
	} else {
		$("#incorrect").fadeIn(500);
	}
}

function showReview() {
	$(".page").hide();
	$("#review").fadeIn(500);
}

function showForm() {
	$(".page").hide();
	$("#blanks").fadeIn(500);
	$("#correct, #new-story").hide();
	$("#answer").val("");
	$("#submit-answer").show();
}

function clearForm() {
	$("#blanks input").val("");
}

function showStory() {
	$(".page").hide();
	$("#story").fadeIn(500);
}

function submitBlanks(ev) {
	ev.preventDefault();
	$("#blanks").find(".blank").each(function(i, item) {
		$("." + item.id).text($(item).val().trim());
	});

	showStory();
}