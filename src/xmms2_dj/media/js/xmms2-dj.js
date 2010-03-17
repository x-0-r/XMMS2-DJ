function updateStatus(url) {
	var req = new Request.HTML({
		url: url,
		onSuccess: function(html) {
			$('player_status').set('text', '');
			$('player_status').adopt(html);
		},
		onFailure: function() {
			$('player_status').set('text', 'The request failed.');
		}
	});

	req.send();
}

function getPlaylist(url) {
	var req = new Request.HTML({
	url: url,
	onSuccess: function(html) {
		$('col3_content').set('text', '');
		$('col3_content').adopt(html);
	},
	onFailure: function() {
		$('col3_content').set('text', 'The request failed.');
	}
	});

	req.send();
}

function getTitles (url) {
	var req = new Request.HTML({
		url: url,
		onSuccess: function(html) {
			$('col4_content').set('text', '');
			$('col4_content').adopt(html);
		},
		onFailure: function() {
			$('col4_content').set('text', 'Request failed.');
		}
	});

	req.send();
}


function getAlbum (url) {
	var req = new Request.HTML({
	url: url,
	onSuccess: function(html) {
		$('col2_content').set('text', '');
		$('col2_content').adopt(html);
	},
	onFailure: function() {
		$('col2_content').set('text', 'The request failed.');
	}
	});

	req.send();
}
