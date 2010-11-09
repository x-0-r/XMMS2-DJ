/*** jQery ***/

function update_playlist(url) {
	counter ++;

	$('#playlist a.jump').unbind();
	$('#playlist a.remove').unbind();

	if(url) {
		$('#playlist').load(url, function() {
			$('#playlist a.jump').click( function(e) {
				e.preventDefault();
				$.get($(this).attr('href'));
			});
			$('#playlist a.remove').click( function(e) {
				e.preventDefault();
				update_playlist($(this).attr('href'));
			});
		});
	} else {
		$('#playlist a.jump').click( function(e) {
			e.preventDefault();
			$.get($(this).attr('href'));
		});
		$('#playlist a.remove').click( function(e) {
			e.preventDefault();
			update_playlist($(this).attr('href'));
		});
	}

}

function record_list(list) {
	// add handler to the add-link
	list.find("a.add").click( function(e) {
		e.preventDefault();
		var url = $(this).attr("href");

		update_playlist(url);
	});	

	// add handler to the view-link
	list.find("a.view").click( function(e) {
		e.preventDefault();
		url = $(this).attr("href");

		update = $(this).siblings("ul.titles").first();
		if( !update.html().trim() ) {
			update.hide();
			update.load(url, function() {
				update.slideDown();

				title_list(update);
			});
		} else {
			update.slideToggle();
		}
	});
}

function title_list(list) {
	// add a handler to the add-link
	list.find("a.add").click( function(e) {
		e.preventDefault();
		var url = $(this).attr("href");

		update_playlist(url);
	});

	list.find("a.info").click( function(e) {
		e.preventDefault();
		url = $(this).attr("href");

		$('#popup').bPopup({
			'loadUrl': url,
			'contentContainer': '#popupContent',
		});
	});
}


$(document).ready(function() {
		counter = 0;

		$("#media-list li>a").click( function(e) {
			/** click handler for artist entries
			 */
			e.preventDefault();
			var url = $(this).attr('href');

			var update = $(this).next("ul");
			if( !update.html().trim() ) {
				update.hide();
				update.load(url, function() {
					update.slideDown();

					record_list(update);
				});
			} else {
				update.slideToggle();
			}
		});

		$("#player-controls a").click( function(e) {
			e.preventDefault();
			url = $(this).attr('href');

			$.get(url);
		});

		update_playlist();
});
