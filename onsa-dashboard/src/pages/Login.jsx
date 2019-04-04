import React from "react";

import signInIcon from "../images/onsa-logo.png";
import { Form, FormInput } from "../components/Form";
import { Alert } from "reactstrap";

async function coreLogin(url, username, password) {
  let response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
        },
    body: JSON.stringify({
      username: username,
      password: password
    })
  });
  let jsonResponse = await response.json();
  // this.setState({ token: jsonResponse });

  return jsonResponse;
}

const spanStlye = {
  fontWeight: "bold"
};

class Login extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      email: "",
      password: ""
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

  handleSubmit = event => {
    event.preventDefault();
    const username = this.state.email
    const password = this.state.password 

    // let url = "http://10.120.78.60:8000/core/api/login";
    let url = process.env.REACT_APP_CORE_URL + "/core/api/login";
    
    coreLogin(url,username, password)
      .then(jsonResponse => {
        if ("token" in jsonResponse) {
          sessionStorage.setItem("token", jsonResponse.token);
        } else {
          sessionStorage.setItem("token", "invalid");
        }
      })
      .then(() => {
        this.props.history.push("/dashboard");
      });
  };

  render() {
    return (
      <React.Fragment>
        <div>
          {sessionStorage.getItem("token") === "invalid" ? (
            <Alert color="danger">
              <strong>Error!</strong> Invalid credentials.
            </Alert>
          ) : null}
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
