import React from "react";

import signInIcon from "../images/onsa-logo.png";
import { Form, FormInput } from "../components/Form";
import FormAlert from "../components/Form/FormAlert";

async function coreLogin(url, username, password) {
  let response = await fetch(url, {
    method: "POST",
    mode: "cors",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username: username,
      password: password
    })
  });
  if (!response.ok) {
    if (response.status === 400) {
      throw new Error("Invalid credentials");
    }
    throw new Error(
      "HTTP error code: " + response.status + " (" + response.statusText + ")"
    );
  }
  let jsonResponse = await response.json();

  return jsonResponse;
}
class Login extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      dialogSuccess: false,
      dialogText: "",
      dialogShow: false,
      email: "",
      password: "",
      successAlert: null,
      displayMessage: ""
    };
  }
  componentDidMount() {
    sessionStorage.clear();
  }

  handleChange = event => {
    const value = event.target.value;
    const name = event.target.name;

    this.setState({ [name]: value });
  };

  showAlertBox = (result, message) => {
    this.setState({
      dialogSuccess: result,
      dialogText: message,
      dialogShow: message || result ? true : false
    });
  };

  handleSubmit = event => {
    event.preventDefault();
    const username = this.state.email;
    const password = this.state.password;

    let url = process.env.REACT_APP_CORE_URL + "/core/api/login";

    coreLogin(url, username, password).then(
      jsonResponse => {
        if ("token" in jsonResponse) {
          sessionStorage.setItem("token", jsonResponse.token);
          this.props.history.push("/dashboard");
        } else {
          this.showAlertBox(false, "Invalid operation");
        }
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
          <FormAlert
            dialogSuccess={this.state.dialogSuccess}
            dialogText={this.state.dialogText}
            dialogShow={this.state.dialogShow}
            msgLabel="Unable to login: "
            className="col-md-8"
          />
        </div>
        <div className="text-center form-div">
          <Form className="form-signin" onSubmit={this.handleSubmit}>
            <img
              className="mb-1"
              src={signInIcon}
              alt=""
              width="327"
              height="147"
            />
            <label htmlFor="inputEmail" className="sr-only">
              Email address
            </label>
            <FormInput
              type="email"
              id="inputEmail"
              className="form-control"
              name="email"
              value={this.state.email}
              onChange={this.handleChange}
              placeholder="Email address"
              required
              autoFocus
            />
            <label htmlFor="inputPassword" className="sr-only">
              Password
            </label>
            <FormInput
              type="password"
              id="inputPassword"
              className="form-control"
              name="password"
              value={this.state.password}
              onChange={this.handleChange}
              placeholder="Password"
              required
            />
            <button className="btn btn-lg btn-primary btn-block" type="submit">
              Sign in
            </button>
          </Form>
        </div>
      </React.Fragment>
    );
  }
}

export default Login;
