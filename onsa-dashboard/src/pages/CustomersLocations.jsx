import React from "react";
import {
  Form,
  FormRow,
  FormTitle,
  FormInput,
  FormSelect
} from "../components/Form";
import { Alert } from "reactstrap";

async function coreLogin(url) {
  let response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username: "fc__netauto@lab.fibercorp.com.ar",
      password: "F1b3rc0rp!"
    })
  });
  let jsonResponse = await response.json();
  // this.setState({ token: jsonResponse });

  return jsonResponse;
}

async function getJson(url, token) {
  let response = await fetch(url, {
    method: "GET",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token
    }
  });

  let jsonResponse = await response.json();
  return jsonResponse;
}

async function postJson(url, token, data) {
  let response = await fetch(url, {
    method: "POST",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token
    },
    body: JSON.stringify(data)
  });

  let jsonResponse = await response.json();
  // response.json();

  return jsonResponse;
}

class CustomersLocations extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      token: "",
      clients: [],
      client: null,
      clientId: null,
      address: null,
      description: null
    };
  }

  componentDidMount() {
    let url = "http://localhost:8000/core/api/login";

    coreLogin(url).then(jsonResponse => {
      this.setState({ token: jsonResponse.token });

      url = "http://localhost:8000/core/api/clients";

      getJson(url, jsonResponse.token).then(jsonResponse => {
        this.setState({ clients: jsonResponse });
      });
    });
    this.props.displayNavbar(false);
  }

  resetFormFields = () => {
    this.setState({
      client: "",
      clientId: "",
      address: "",
      description: "",
      successBox: false
    });
  };

  handleChange = event => {
    const value = event.target.value;
    const name = event.target.name;

    this.setState({ [name]: value });
  };

  handleOnSelect = event => {
    const value = event.target.value;
    const name = event.target.name;
    let id = event.target.options.selectedIndex;

    switch (name) {
      default:
        this.setState({ [name]: value, clientId: id });
    }
  };

  handleSubmit = event => {
    event.preventDefault();
    const data = {
      address: this.state.address,
      description: this.state.description
    };

    let url =
      "http://localhost:8000/core/api/clients/" +
      this.state.clientId +
      "/customerlocations";
    postJson(url, this.state.token, data).then(() => {
      this.setState({ successAlert: true });
    });

    this.resetFormFields();
  };

  render() {
    const clientsList = this.state.clients.map(client => (
      <option key={client.id} value={client.name}>
        {client.name}
      </option>
    ));

    let alertBox = null;
    if (this.state.successAlert) {
      alertBox = (
        <Alert bsStyle="success">
          <strong>Success!</strong> Customer location added.
        </Alert>
      );
    }

    return (
      <React.Fragment>
        <div>{alertBox}</div>
        <div className="col-md-8 order-md-1">
          <h4 className="mb-3">Add customer location</h4>
          <form
            className="needs-validation"
            noValidate
            onSubmit={this.handleSubmit}
          >
            <div className="row">
              <div className="col-md-6 mb-3">
                <label htmlFor="client">Client</label>
                <FormSelect
                  className="custom-select d-block w-100"
                  id="client"
                  name="client"
                  value={this.state.client}
                  onChange={this.handleOnSelect}
                  required
                >
                  <option value="">Choose...</option>
                  {clientsList}
                </FormSelect>
                <div class="invalid-feedback">
                  Example invalid feedback text
                </div>
              </div>
              <div className="col-md-6 mb-3">
                <label htmlFor="clientId">Address</label>
                <input
                  type="text"
                  className="form-control"
                  id="address"
                  name="address"
                  value={this.state.address}
                  onChange={this.handleChange}
                  placeholder="Calle Falsa 123"
                  required
                />
              </div>
            </div>

            <div className="row">
              <div className="col-md-12 mb-3">
                <label htmlFor="name">Description</label>
                <input
                  type="text"
                  className="form-control"
                  id="description"
                  name="description"
                  value={this.state.description}
                  onChange={this.handleChange}
                  placeholder="Description"
                  required
                />
              </div>
            </div>
            <hr className="mb-4" />

            <button
              className="btn btn-primary btn-lg btn-block"
              disabled={
                !(
                  this.state.client &&
                  this.state.address &&
                  this.state.description
                )
                  ? true
                  : false
              }
              type="submit"
              value="Submit"
            >
              Create
            </button>
          </form>
        </div>
      </React.Fragment>
    );
  }
}

export default CustomersLocations;
