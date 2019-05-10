import React from "react";
import { URLs, HTTPPost } from "../middleware/api.js";
import FormAlert from "../components/Form/FormAlert";

class Customers extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      client: "",
      cuic: "",
      successAlert: null,
      displayMessage: ""
    };
  }

  componentDidMount() {
    this.props.displayNavbar(false);
  }

  resetFormFields = () => {
    this.setState({
      client: "",
      cuic: ""
    });
  };

  showAlertBox = (result, message) => {
    this.setState({
      successAlert: result,
      displayMessage: message
    });
  };

  handleChange = event => {
    const value = event.target.value;
    const name = event.target.name;

    this.setState({ [name]: value });
  };

  handleSubmit = event => {
    event.preventDefault();

    const data = { name: this.state.client, cuic: this.state.cuic };

    HTTPPost(URLs["clients"], data).then(
      () => {
        this.showAlertBox(true, "Customer created.");
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
              succesfull={this.state.successAlert}
              displayMessage={this.state.displayMessage}
            />
          </div>
          <div className="col-md-8 order-md-1">
            <h4 className="mb-3">Create New Customer</h4>
            <form
              className="needs-validation"
              noValidate
              onSubmit={this.handleSubmit}
            >
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label htmlFor="name">Customer</label>
                  <input
                    type="text"
                    className="form-control"
                    id="client"
                    name="client"
                    maxLength="50"
                    value={this.state.client}
                    onChange={this.handleChange}
                    placeholder="Name"
                    required
                  />
                </div>
                <div className="col-md-6 mb-3">
                  <label htmlFor="cuic">CUIC</label>
                  <input
                    type="text"
                    className="form-control"
                    id="cuic"
                    maxLength="20"
                    name="cuic"
                    value={this.state.cuic}
                    onChange={this.handleChange}
                    placeholder="Id"
                    required
                  />
                </div>
              </div>
              <hr className="mb-4" />

              <button
                className="btn btn-primary btn-lg btn-block"
                disabled={
                  !(this.state.client && this.state.cuic) ? true : false
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

export default Customers;
