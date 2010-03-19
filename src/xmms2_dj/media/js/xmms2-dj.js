Clientcide.setAssetLocation("/media/clientcide/");

/*
window.addEvent('domready', function() {
	$('search_artist').addEvent('change', searchTimer('/search/artist/'));
});
*/


function updateStatus(url) {
	new Request.HTML({
		url: url,
		update: $('player_status'),
	}).send();
}

function getPlaylistList(url) {
	var waiter = new Waiter($('playlist_list'));
	waiter.start();
	new Request.HTML({
		url:url,
		update: $('playlist_list'),
	}).send();
	waiter.stop();
}

function getPlaylist(url) {
	var waiter= new Waiter($('playlist'));
	waiter.start();
	new Request.HTML({
		url: url,
		update: $('playlist'),
	}).send();
	waiter.stop();
}

function loadPlaylist (select) {
	var url = select.options[select.options.selectedIndex].value;
	getPlaylist(url);
}

function createPlaylist (playlist_url, playlist_list_url) {
	var name = $('playlist-new').get('value');

	var waiter = new Waiter($('playlist'));
	waiter.start();
	new Request.HTML({
		url: playlist_url,
		method: "post",
		update: $('playlist'),
		data: "playlist="+name
	}).send();
	waiter.stop();

	getPlaylistList(playlist_list_url);
}

function getTitles (url) {
	var waiter = new Waiter('titles');
	waiter.start();
	new Request.HTML({
		url: url,
		onSuccess: function(html) {
			$('titles').set('text', '');
			$('titles').adopt(html);
			waiter.stop();
		},
		onFailure: function () {
			waiter.stop();
		}
	}).send();
}

function getAlbum (url) {
	var waiter = new Waiter('albums');
	waiter.start();
	new Request.HTML({
		url: url,
		onSuccess: function(html) {
			$('albums').set('text', '');
			$('albums').adopt(html);
		}
	}).send();
	waiter.stop();
}

var t;

function searchTimer (url, functionName) {
	clearTimeout(t);
	t = setTimeout(functionName + "('" + url + "')", 500);
}

function searchArtist (url) {
	var searchstring = $('search_artist').get('value');
	var artistSearchWaiter = new Waiter('artists');
	artistSearchWaiter.start();
	new Request.HTML({
		url: url,
		method: "post",
		onSuccess: function(html) {
			$('artists').set('text', '');
			$('artists').adopt(html);
			artistSearchWaiter.stop();
		},
		onFailure: function() {
			$('artists').set('text', 'The request failed.');
			artistSearchWaiter.stop();
		},
		data: "artist="+searchstring
	}).send();
}

function searchAlbum (url) {
	var searchstring = $('search_album').get('value');
	var selectedArtist = $('selected_artist').get('value');
	var artistSearchWaiter = new Waiter('albums');
	artistSearchWaiter.start();
	new Request.HTML({
		url: url,
		method: "post",
		onSuccess: function(html) {
			$('albums').set('text', '');
			$('albums').adopt(html);
			artistSearchWaiter.stop();
		},
		onFailure: function() {
			$('albums').set('text', 'The request failed.');
			artistSearchWaiter.stop();
		},
		data: "album="+searchstring+"&artist="+selectedArtist
	}).send();
}

function searchTitle (url) {
	var searchstring = $('search_title').get('value');
	var artistSearchWaiter = new Waiter('titles');
	artistSearchWaiter.start();
	new Request.HTML({
		url: url,
		method: "post",
		onSuccess: function(html) {
			$('titles').set('text', '');
			$('titles').adopt(html);
			artistSearchWaiter.stop();
		},
		onFailure: function() {
			$('titles').set('text', 'The request failed.');
			artistSearchWaiter.stop();
		},
		data: "title="+searchstring
	}).send();
}
