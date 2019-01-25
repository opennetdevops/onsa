import React from 'react'

import signInIcon from '../images/onsa-logo.png'
import { Form, FormInput } from '../components/Form';


const spanStlye = {
  fontWeight: 'bold'
}

class Login extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      email: '',
      password: ''
    };
  }
  componentDidMount() {
		sessionStorage.clear()
	}

  handleChange = (event) => {

    const value = event.target.value;
    const name = event.target.name

    this.setState({[name]: value})
  }

  handleSubmit = (event) => {
    event.preventDefault()
    const data = { "username": this.state.email,
                   "password": this.state.password };

    fetch("http://localhost:8000/core/api/login",
      {
        method: "POST",
        mode: "cors", 
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(myJson => {
        if ('token' in myJson) {
          sessionStorage.setItem('token', myJson['token'])
        }
      })
      .then(() => {
        this.props.history.push('/dashboard');
      })


    
  }

  render() {

    return (
      <div className="text-center form-div">
        <Form className="form-signin" onSubmit={this.handleSubmit}>
          <img className="mb-1" src={signInIcon} alt="" width="327" height="147"/>
          <label htmlFor="inputEmail" className="sr-only">Email address</label>
          <FormInput type="email" id="inputEmail" className="form-control" name="email" value={this.state.email} onChange={this.handleChange} placeholder="Email address" required autoFocus/>
          <label htmlFor="inputPassword" className="sr-only">Password</label>
          <FormInput type="password" id="inputPassword" className="form-control" name="password" value={this.state.password} onChange={this.handleChange} placeholder="Password" required/>
          <button className="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
        </Form>
      </div>
    );
  }

}

export default Login;