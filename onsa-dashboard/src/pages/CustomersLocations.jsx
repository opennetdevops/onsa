import React from "react";
import {
  Form,
  FormRow,
  FormTitle,
  FormInput,
  FormSelect
} from "../components/Form";
import { Alert } from "reactstrap";

async function getJson(url) {
  let response = await fetch(url, {
    method: "GET",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + sessionStorage.getItem('token')
    }
  });

  let jsonResponse = await response.json();
  return jsonResponse;
}

async function postJson(url, data) {
  let response = await fetch(url, {
    method: "POST",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + sessionStorage.getItem('token')
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
      address: '',
      description: ''
    };
  }

  componentDidMount() {

      let url = process.env.REACT_APP_CORE_URL + "/core/api/clients";

      getJson(url).then(jsonResponse => {
        this.setState({ clients: jsonResponse });
      });

    this.props.displayNavbar(false);
  }

  resetFormFields = () => {
    this.setState({
      client: "",
      clientId: "",
      address: '',
      description:'',
      successBox: false
    });
  };

  handleChange = event => {
    const value = event.target.value;
    const name = event.target.name;

    this.setState({ [name]: value });
  };

  handleOnSelect = event => {
    let selectedClient = this.state.clients.filter(function(client) {
      return client.id == event.target.value;
    });

    if (selectedClient.length > 0){
      console.log('el id seleccionado es: ', selectedClient[0].id);
      console.log('el cliente seleccionado es: ', selectedClient[0].name);
      this.setState({ client: selectedClient[0].name, clientId: selectedClient[0].id });
    } else {
      this.setState({ client:''});
    }
  };

  handleSubmit = event => {
    event.preventDefault();
    const data = {
      address: this.state.address,
      description: this.state.description
    };
    console.log(this.state.clientId)
    let url =
      process.env.REACT_APP_CORE_URL + "/core/api/clients/" +
      this.state.clientId +
      "/customerlocations";
    postJson(url, data).then(() => {
      this.setState({ successAlert: true });
    });

    this.resetFormFields();
  };

  render() {
    const clientsList = this.state.clients.map(client => (
      <option key={client.id} value={client.id}>
        {client.name}
      </option>
    ));

    let alertBox = null;
    if (this.state.successAlert) {
      alertBox = (
        <Alert className="success">
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
                  onChange={this.handleOnSelect}
                  required
                >
                  <option value="">Choose...</option>
                  {clientsList}
                </FormSelect>
                <div className="invalid-feedback">
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
                  maxLength= "50"
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
                  maxLength= "50"
                  placeholder="Description"
                  required
                />
              </div>
            </div>
            <hr className="mb-4" />

            <button
              className="btn btn-primary btn-lg btn-block"
              disabled={
                (
                  this.state.client &&
                  this.state.address &&
                  this.state.description
                )
                  ? false
                  : true
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
