const TEAMS = [];
var currentPage = "";
var currentPoints = 0;

$(function() {
	showPage("#setteams", false);
  	$("#play-game").on("click", playGame);
  	$("#add-team").on("click", addTeam);
  	$("#team-name").on("keydown", hideTeamError);
  	$(".show-help").on("click", showHelp);
  	$(".close-help").on("click", closeHelp);
  	$(".points-link").on("click", showClue);
  	$(".back-to-main").on("click", backToBoard);
  	$(".show-answer").on("click", showAnswer);
});

function hideTeamError(ev) {
	$("#team-error").hide();
}

function slugify(name) {
	return name.replace(/\s/g, "-").replace(/[^a-z0-9\-]/gi,'');
}

function addTeam(ev) {
	var teamName = $("#team-name").val().trim();

	// Check for similar slugs (used for ids)
	var slugifiedMatch = false;
	var slugName = slugify(teamName);
	for(let i = 0; i < TEAMS.length; i++) {
		if(slugify(TEAMS[i]) === slugName) {
			slugifiedMatch = true;
			break;
		}
	}

	// Validate name
	if(!teamName) {
		$("#team-error").text("Enter team name first");
		$("#team-error").show();
	} else if(TEAMS.indexOf(teamName) >= 0) {
		$("#team-error").text("Team with this name already exists");
		$("#team-error").show();
	} else if(slugifiedMatch) {
		$("#team-error").text("Team with similar name already exists");
		$("#team-error").show();
	} else {
		TEAMS.push(teamName);

		// Add to team list
		$("#team-list").append("<li>" + teamName + "</li>")
		$("#team-name").val("");

		// Add to score board
		var teamId = slugify(teamName);
		var htmlString = "<div class=\"team-card\" id=\"" + teamId + "\">" +
						 	"<div class=\"points\">0</div>" +
						 	"<div class=\"team-name\">" + teamName + "</div>" +
						 	"<div class=\"set-points\">" +
						 		"<div class=\"add-points\" title=\"Add Points\" data-card=\"" + teamId + "\">+</div>" +
						 		"<div class=\"point\"></div>" +
						 		"<div class=\"subtract-points\" title=\"Subtract Points\" data-card=\"" + teamId + "\">-</div>" +
						 	"</div>" +
						"</div>";

		$("#team-display").append(htmlString);
	}

}

function showHelp() {
	$(".page").hide();
	$("#instructions").show();
	$("#score").hide();
}

function closeHelp() {
	showPage(currentPage, false);
}

function showClue(ev) {
	var clue = $(ev.target).data("clue");
	currentPoints = Number($(ev.target).data("points"));

	$(".point").text(currentPoints).removeClass("gray");

	showPage("#" + clue, true);
	showPoints(true);
}

function showPage(page, showScore) {
	showPoints(false)
	currentPage = page;
	$(".page").hide();
	$(page).show();

	(showScore)? $("#score").show() : $("#score").hide();
}

function playGame(ev) {
	if(TEAMS.length === 0) {
		$("#team-error").text("Must have at least one team to play");
		$("#team-error").show();
	} else {
		showPage("#main", true);
		$(".add-points").on("click", addPoints);
	  	$(".subtract-points").on("click", subtractPoints);
	}
}

function showPoints(show) {
	(show)? $(".set-points").show() : $(".set-points").hide();
}

function backToBoard(ev) {
	// Remove card from board
	var cardId = $(ev.target).data("card");
	$("#" + cardId).remove();

	// Switch to main view
	showPage("#main", true);

	// Declare winner if board is clear
	if(!$(".points-link").length) {
		endGame();
	}
}

function showAnswer(ev) {
	$(ev.target).hide();
	var answerId = $(ev.target).data("answer");
	$("#" + answerId).fadeIn(500);
	setTimeout(function() {
		$("#" + answerId + "-prompt").fadeIn(500);
	}, 2000);
}

function addPoints(ev) {
	var card = $("#" + $(ev.target).data("card"));
	card.find(".point").addClass("gray");

	var total = Number(card.find(".points").text());
	card.find(".points").text(total + currentPoints);
}

function subtractPoints(ev){
	var card = $("#" + $(ev.target).data("card"));
	card.find(".point").addClass("gray");

	var total = Number(card.find(".points").text());
	card.find(".points").text(total - currentPoints);
}

function endGame() {
	var winners = [];
	var maxPoints = Number.MIN_SAFE_INTEGER;

	// Figure out who winner is (if multiple, add to win message)
	$(".team-card").each(function(i, card) {
		var score = Number($(card).find(".points").text());
		var name = $(card).find(".team-name").text();

		if(score === maxPoints) {
			winners.push(name);
		} else if(score > maxPoints) {
			maxPoints = score;
			winners = [name];
		}
	});

	if(winners.length === 1) {
		$("#win-message").text(winners[0] + " wins!");
	} else {
		$("#win-message").text("Draw: " + winners.join(", "))
	}

	showPage("#winner", true);
}
