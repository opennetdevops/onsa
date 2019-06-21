import React from "react";
import FormAlert from "../components/Form/FormAlert";
import { HTTPPost, ClientURLs } from "../middleware/api.js";
import ClientSelect from "../components/Clients/ClientSelect";
import { validationSchema } from "../components/Validators/CustomerLocations";

class CustomersLocations extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      address: "",
      clientOptions: [],
      description: "",
      dialogLabel: "",
      dialogSuccess: false,
      dialogText: "",
      dialogShow: false,
      selectedClient: []
    };
  }

  componentDidMount() {
    this.props.displayNavbar(false);
  }

  resetFormFields = () => {
    this.setState({
      address: "",
      description: "",
      selectedClient: []
    });
  };

  showAlertBox = (result, message, label) => {
    this.setState({
      dialogSuccess: result,
      dialogText: message,
      dialogShow: message || result ? true : false,
      dialogLabel: label
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
      selectedClient: selectedOption
    });
  };

  handleSubmit = event => {
    event.preventDefault();
    let data = {
      address: this.state.address,
      description: this.state.description
    };
    let dataToValidate = { ...data, client: this.state.selectedClient.value };

    validationSchema()
      .validate(dataToValidate)
      .then(
        () => {
          //isValid = true
          let url = ClientURLs(
            "customerLocations",
            this.state.selectedClient.value
          );
          this.submitRequest(url, data);
        }, //isValid = false
        err => {
          this.showAlertBox(false, err.message, "Validation Error: ");
        }
      );
  };

  submitRequest = (url, data) => {
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
              msgLabel={this.state.dialogLabel}
            />
          </div>
          <div className="col-md-8 order-md-1">
            <h4 className="mb-3">Add customer location</h4>
            <form onSubmit={this.handleSubmit}>
              <div className="row">
                <div className="col-lg-6 mb-3">
                  <label htmlFor="client">Client Name</label>
                  <ClientSelect
                    onChange={this.handleSelectOnChange}
                    value={this.state.selectedClient}
                    name="client"
                    searchByMT="3"
                  />
                </div>
                <div className="col-lg-6 mb-3">
                  <label htmlFor="address">Address</label>
                  <input
                    type="text"
                    className="form-control"
                    id="address"
                    name="address"
                    value={this.state.address}
                    onChange={this.handleChange}
                    maxLength="50"
                    placeholder="Some address 123"
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
                    maxLength="80"
                    placeholder="Enter a description"
                  />
                </div>
              </div>
              <hr className="mb-4" />


              <div className="row justify-content-center">
                <div className="col-sm-6 ">
                  <button
                    className="btn btn-primary btn-lg btn-block"
                    type="submit"
                    value="Submit"
                  >
                    Create
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default CustomersLocations;
