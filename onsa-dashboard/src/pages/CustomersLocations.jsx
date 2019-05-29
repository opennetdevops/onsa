import React from "react";
import FormAlert from "../components/Form/FormAlert";
import { URLs, HTTPGet, HTTPPost, ClientURLs } from "../middleware/api.js";
import Select from "react-select";

class CustomersLocations extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      address: "",
      clientName: "",
      clientId: "",
      clientOptions: [],
      description: "",
      dialogSuccess: false,
      dialogText: "",
      dialogShow: false
    };
  }

  componentDidMount() {
    HTTPGet(URLs["clients"]).then(
      jsonResponse => {
        let options = jsonResponse.map(client => {
          return { value: client.id, label: client.name }
        });
        this.setState({ clientOptions: options });
      }, // onRejected:
      error => {
        this.showAlertBox(false, error.message);
        this.setState({ clientOptions: [] });
        
      }
    );

    this.props.displayNavbar(false);
  }

  resetFormFields = () => {
    this.setState({
      clientName: "",
      clientId: "",
      address: "",
      description: ""
    });
  };

  showAlertBox = (result, message) => {
    this.setState({
      dialogSuccess: result,
      dialogText: message,
      dialogShow: ( message || result) ? true : false
    });
  };

  handleChange = event => {
    const value = event.target.value;
    const name = event.target.name;

    this.setState({ [name]: value });
  };
  
  handleSelectOnChange = selectedOption => {
    this.showAlertBox();
    this.setState({
      clientName: selectedOption.label,
      clientId: selectedOption.value
    });
  };

  handleSubmit = event => {
    event.preventDefault();
    const data = {
      address: this.state.address,
      description: this.state.description
    };

    let url = ClientURLs("customerLocations", this.state.clientId);

    HTTPPost(url, data).then(
      () => {
        this.showAlertBox(true, "Customer Location Added");
        this.resetFormFields();
      },
      error => {
        this.showAlertBox(false, error.message);
      }
    );
  };

  render() {
    return (
      <React.Fragment>
        <div className="row justify-content-center">
        <div className="col-md-8">
          <FormAlert
            dialogSuccess={this.state.dialogSuccess}
            dialogText={this.state.dialogText}
            dialogShow={this.state.dialogShow}
          />
        </div>
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
                <Select
                  onChange={this.handleSelectOnChange}
                  options={this.state.clientOptions}
                  name="client"
                  placeholder="Choose a client.."
                />
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
                  maxLength="50"
                  placeholder="Some address 123"
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
                  maxLength="50"
                  placeholder="Enter a description"
                  required
                />
              </div>
            </div>
            <hr className="mb-4" />

            <button
              className="btn btn-primary btn-lg btn-block"
              disabled={
                this.state.clientName &&
                this.state.address &&
                this.state.description
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
        </div>
      </React.Fragment>
    );
  }
}

export default CustomersLocations;
