API_URL = "http://127.0.0.1:5000/"

get_wall = function() {
	var request = new XMLHttpRequest();
	request.open("GET", API_URL + "wall/", false);
	request.send();

	if (request.status !== 200){
		return
	}

	return JSON.parse(request.responseText);
}

vote_add = function(wall, candidate) {
	var request = new XMLHttpRequest();
	request.open("POST", API_URL + "vote/", false);
	request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	request.send(JSON.stringify({"wall": wall, "candidate": candidate}));
	return request.status === 201
}

result_by_candidate = function(wall) {
	var request = new XMLHttpRequest();
	request.open("GET", API_URL + "wall/" + wall + "/candidate/", false);
	request.send();

	if (request.status !== 200){
		return
	}
	
	return JSON.parse(request.responseText);
}

result_by_hour = function(wall) {
	var request = new XMLHttpRequest();
	request.open("GET", API_URL + "wall/" + wall + "/hour/", false);
	request.send();

	if (request.status !== 200){
		return
	}
	
	return JSON.parse(request.responseText);
}