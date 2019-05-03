import React from "react";
import {
  Form,
  FormRow,
  FormTitle,
  FormInput,
  FormSelect
} from "../components/Form";
import { URLs, HTTPGet, HTTPPost } from '../middleware/api.js'
import { Alert } from "reactstrap";

class CustomersLocations extends React.Component {
  constructor(props) {
    super(props);

    this.state = {

      clients: [],
      clientName: '',
      clientId: '',
      address: '',
      description: '',
      successAlert: null
    };
  }

  componentDidMount() {
    HTTPGet(URLs['clients']).then(jsonResponse => {
      this.setState({ clients: jsonResponse });
    } // onRejected: 
      ,(error)=> {
        console.error('Something happened!!: \n ', error);
        this.setState({ clients: [] });
    });

  this.props.displayNavbar(false);
  }

  resetFormFields = () => {
    this.setState({
      clientName: "",
      clientId: "",
      address: '',
      description:'',
      successAlert: null
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

    if (selectedClient.length > 0 ){
      this.setState({ clientName: selectedClient[0].name, clientId: selectedClient[0].id });
    } else {
      this.setState({ clientName:''});
    }
  };

  handleSubmit = event => {
    event.preventDefault();
    const data = {
      address: this.state.address,
      description: this.state.description
    };
    
    let url =
      process.env.REACT_APP_CORE_URL + "/core/api/clients/" + this.state.clientId + "/customerlocations";
    
    HTTPPost(url, data)
      .then(() => {
        this.setState({ successAlert: true });
        this.resetFormFields();
      },
      (error)=> {
        console.error('Something happened!!: \n ', error);
        this.setState({ successAlert: false });
      }
    );
  };

  render() {
    let clientsList = this.state.clients.map(client => (
      <option key={client.id} value={client.id}>
        {client.name}
      </option>
    ));

    let alertBox = null;
    
    if (this.state.successAlert) {
      alertBox = (
        <Alert className="success col-md-8">
          <strong>Success!</strong> Customer location added.
        </Alert>
      );
    } else if (this.state.successAlert == false) {
      alertBox = <Alert className="alert-danger col-8"><strong>Error:</strong> Customer location not created.
      </Alert>;
      
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
                  this.state.clientName &&
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
