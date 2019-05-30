async function HTTPGet(url) {
  let response = await fetch(url, {
    method: "GET",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      Authorization: "Bearer " + sessionStorage.getItem("token")
    }
  });

  if (!response.ok) {
    throw new Error(
      "HTTP error - " + response.status + " (" + response.statusText + ")"
    );
  }

  let jsonResponse = await response.json();

  return jsonResponse;
}

async function HTTPPost(url, data) {
  let response = await fetch(url, {
    method: "POST",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      Authorization: "Bearer " + sessionStorage.getItem("token")
    },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    throw new Error(
      "HTTP error - " + response.status + " (" + response.statusText + ")"
    );
  }

  let jsonResponse = await response.json();
  return jsonResponse;
}

async function HTTPPut(url, data) {
  let response = await fetch(url, {
    method: "PUT",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      Authorization: "Bearer " + sessionStorage.getItem("token")
    },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    throw new Error(
      "HTTP error - " + response.status + " (" + response.statusText + ")"
    );
  }

  let jsonResponse = await response.json();
  return jsonResponse;
}

const URLs = {
  services: process.env.REACT_APP_CORE_URL + "/core/api/services",
  projects: process.env.REACT_APP_CORE_URL + "/core/api/projects",
  //client is used as clientId or clientName
  locations: process.env.REACT_APP_CORE_URL + "/core/api/locations",
  clients: process.env.REACT_APP_CORE_URL + "/core/api/clients"
};

const ClientURLs = (key, client, customerLocId) => {
  //client is used as clientId or clientName.
  const dict = {
    customerLocations:
      process.env.REACT_APP_CORE_URL +
      "/core/api/clients/" +
      client +
      "/customerlocations",
    clientVRFs:
      process.env.REACT_APP_CORE_URL + "/core/api/vrfs?client_id=" + client,
    clientAccessPorts:
      process.env.REACT_APP_CORE_URL +
      "/core/api/clients/" +
      client +
      "/customerlocations/" +
      customerLocId +
      "/accessports"
  };
  return dict[key];
};

export { URLs, ClientURLs, HTTPGet, HTTPPost, HTTPPut };
