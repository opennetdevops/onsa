import React from 'react'

async function HTTPGet(url) {

	let response = await fetch(url, {
				method: "GET",
				mode: "cors",
				headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
				},
		});

	let jsonResponse = await response.json();

	return jsonResponse;
}

async function HTTPPost(url, data) {

    let response = await fetch(url, {
        method: "POST",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify(data)
      });

    let jsonResponse = await response.json();

    return jsonResponse;
}

const URLs = { "service_creation": "http://localhost:8000/core/api/services",
         "projects": "http://localhost:8000/core/api/projects",
         "locations": "http://localhost:8000/core/api/locations",
         "clients": "http://localhost:8000/core/api/clients"
         }

export { URLs, HTTPGet, HTTPPost }
