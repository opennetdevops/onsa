async function HTTPGet(url, signal) {
  let response = await fetch(url, {
    method: "GET",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      Authorization: "Bearer " + sessionStorage.getItem("token")
    },
    signal: signal
  });

  if (!response.ok) {
    throw new Error(
      "HTTP error - " + response.status + " (" + response.statusText + ")"
    );
  }

  let jsonResponse = await response.json();

  return jsonResponse;
}

async function HTTPDelete(url) {
  let response = await fetch(url, {
    method: "DELETE",
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
    if (response.statusText === "Unknown Status Code") {
      let msg = await response.json();
      throw new Error(
        "HTTP error - " + response.status + " (" + msg["msg"] + ")"
      );
    } else {
      throw new Error(
        "HTTP error - " + response.status + " (" + response.statusText + ")"
      );
    }
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
  locations: process.env.REACT_APP_CORE_URL + "/core/api/locations",
  clients: process.env.REACT_APP_CORE_URL + "/core/api/clients",
  device_models: process.env.REACT_APP_CORE_URL + "/core/api/device_models"
};

const ServiceURLs = (key, serviceID) => {
  const dict = {
    service: process.env.REACT_APP_CORE_URL + "/core/api/services/" + serviceID,
    resources:
      process.env.REACT_APP_CORE_URL +
      "/core/api/services/" +
      serviceID +
      "/resources"
  };
  return dict[key];
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
      "/accessports",
    multiClientPorts:
      process.env.REACT_APP_CORE_URL + "/core/api/multiclient_access_ports"
  };
  return dict[key];
};

export {
  URLs,
  ClientURLs,
  HTTPGet,
  HTTPPost,
  HTTPPut,
  HTTPDelete,
  ServiceURLs
};
