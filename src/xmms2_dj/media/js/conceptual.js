/*** jQery ***/

function create_playlist_sortable() {
	$('#playlist>ul').sortable({
		update: function(e, ui) {
			//alert('ID: ' + parseInt(ui.item.attr('id').substr(8)) + ", Pos: " + $('#playlist>ul>li').index(ui.item));

			var old_pos = parseInt(ui.item.attr('id').substr(8));
			var new_pos = $('#playlist>ul>li').index(ui.item);

			$('#playlist>ul>li').each( function(index) {
				$(this).attr('id', 'pl_item_' + index);
			});

			var url = $('form#move-entry').attr('action');
			$.post( url, {'old_pos': old_pos, 'new_pos': new_pos}, function(data) {
				if (data=='True') {
					// TODO
				} else {
					// TODO
				}
			});
		}
	});
}

function update_playlist(url, data) {
	if(data == null)
		data = "";

	$('#playlist a.jump').unbind();
	$('#playlist a.remove').unbind();
	$('#playlist>ul').sortable('destroy');

	if(url) {
		$('#playlist').load(url, data, function() {
			$('#playlist a.jump').click( function(e) {
				e.preventDefault();
				$.get($(this).attr('href'));
			});
			$('#playlist a.remove').click( function(e) {
				e.preventDefault();
				update_playlist($(this).attr('href'));
			});

			create_playlist_sortable();
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
		
		create_playlist_sortable();
	}

}

function record_list_ajax(list) {
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

				title_list_ajax(update);
			});
		} else {
			update.slideToggle();
		}
	});
}

function title_list_ajax(list) {
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

function artist_list() {
	$("#media-list>li>a").click( function(e) {
		/** click handler for artist entries
		 */
		e.preventDefault();

		var update = $(this).next("ul");
		update.slideToggle();
	});
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

		update = $(this).siblings("ul.titles").first();
		update.slideToggle();
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

					record_list_ajax(update);
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

		$("#search-button").click( function(e) {
			/** click handler for search button
			 */
			e.preventDefault();
			var url = $(this).parents('form').attr('action');
			var data = $(this).parents('form').serializeArray();
			$("#media-list").load(url, data, function(){
				artist_list();
				record_list($('#media-list'));
			});
		});
		
		$('#playlist-select').change( function(e) {
				var url = $('#playlist-select').attr('value');
				update_playlist(url);
		});

		$('#form-create-playlist').hide();

		$('#new-playlist').click( function(e) {
				e.preventDefault();
				$('#form-create-playlist').slideDown();
		});

		$('#form-create-playlist input[type="submit"]').click( function(e) {
				e.preventDefault();
				var url = $('#form-create-playlist').attr('action');
				var data = $('#form-create-playlist').serializeArray();
				update_playlist(url, data);

				url = $('#playlist-select').parents('form').attr('action');
				$('#playlist-select').load( url );

				$('#form-create-playlist').slideUp();
		});

		$('#remove-playlist').click( function(e) {
				e.preventDefault();
				var url = $('#remove-playlist').attr('href');
				update_playlist(url);

				url = $('#playlist-select').parents('form').attr('action');
				$('#playlist-select').load(url);
		});

		update_playlist();
});
