import React from "react";
import { URLs, HTTPPost } from "../middleware/api.js";
import FormAlert from "../components/Form/FormAlert";
// import * as yup from "yup";
import { validationSchema } from "../components/Validators/Customers";
import Button from '@material-ui/core/Button';
import DoneAll from '@material-ui/icons/DoneAll'


const btnStyle =   {
  fontWeight: "bold",
  display: "block",
  fontSize: "1.2rem",
  margin: "auto",
  paddingLeft: "6rem",
  paddingRight: "5rem"
}
const iconBtnStyle= {
  fontSize: "2.2rem",
  paddingBottom: "0.4rem "
}

class Customers extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      client: "",
      cuic: "",
      dialogLabel: "",
      dialogSuccess: false,
      dialogText: "",
      dialogShow: false
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

  handleSubmit = event => {
    event.preventDefault();

    const data = { name: this.state.client, cuic: this.state.cuic };

    validationSchema()
      .validate(data)
      .then(
        () => {
          //isValid = true
          this.submitRequest(URLs["clients"], data);
        }, //isValid = false
        err => {
          this.showAlertBox(false, err.message, "Validation Error: ");
        }
      );
  };

  submitRequest = (url, data) => {
    HTTPPost(url, data).then(
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
              dialogSuccess={this.state.dialogSuccess}
              dialogText={this.state.dialogText}
              dialogShow={this.state.dialogShow}
              msgLabel={this.state.dialogLabel}
            />
          </div>
          <div className="col-md-8 order-md-1">
            <h4 className="mb-3">Create New Customer</h4>
            <form onSubmit={this.handleSubmit}>
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label htmlFor="name">Customer</label>
                  <input
                    type="text"
                    className="form-control"
                    id="client"
                    name="client"
                    maxLength="100"
                    value={this.state.client}
                    onChange={this.handleChange}
                    placeholder="Name"
                  />
                </div>
                <div className="col-md-6 mb-3">
                  <label htmlFor="cuic">CUIC</label>
                  <input
                    type="text"
                    className="form-control"
                    id="cuic"
                    maxLength="11"
                    name="cuic"
                    value={this.state.cuic}
                    onChange={this.handleChange}
                    placeholder="Id"
                  />
                </div>
              </div>
              <hr className="mb-4" />

              <div className="row justify-content-center">
                <div className="col-sm-6 ">
                  <Button
                    variant="contained"
                    color="secondary"
                    size="large"
                    type="submit"
                    className="confirmCustomButton"
                    style={btnStyle}
                  >
                    Create
                    <DoneAll className="ml-2" style={iconBtnStyle} />
                  </Button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default Customers;
