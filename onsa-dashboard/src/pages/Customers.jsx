import React from 'react';
import { Alert } from 'reactstrap';

async function postJson(url, data) {

    let response = await fetch(url, {
        method: "POST",
        mode: "cors", 
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
      });

    let jsonResponse = await response.json();

    return jsonResponse;
}


class Customers extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      client: '',
      clientId: '',
      successBox: false
    };
  }

  componentDidMount() {
    this.props.displayNavbar(false); 
  }

  resetFormFields = () => {
    this.setState({
      client: "",
      clientId: "",
    })
  }

  handleChange = (event) => {

    const value = event.target.value;
    const name = event.target.name

    this.setState({[name]: value})
  }

  handleSubmit = (event) => {
    event.preventDefault();

    const data = { "name": this.state.client };
    let url = "http://localhost:8000/core/api/clients";

    postJson(url, data).then(() => { this.setState({successAlert: true}) })

    this.resetFormFields();
  }

    render() {

      let alertBox = null;
      if (this.state.successAlert) {
        alertBox = <Alert bsStyle="success"><strong>Success!</strong> Customer created.</Alert>;
      }


      return (
          <React.Fragment>
          <div>{alertBox}</div>
          <div className="col-md-8 order-md-1">
            <h4 className="mb-3">Create New Customer</h4>
            <form className="needs-validation" noValidate onSubmit={this.handleSubmit}>
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label htmlFor="name">Customer</label>
                  <input type="text" className="form-control" id="client" name="client" value={this.state.client} onChange={this.handleChange} placeholder="Name" required/>
                </div>
                <div className="col-md-6 mb-3">
                  <label htmlFor="clientId">ID</label>
                  <input type="text" className="form-control" id="clientId" name="clientId" value={this.state.clientId} onChange={this.handleChange} placeholder="Id" required/>
                </div>
              </div>
              <hr className="mb-4"/>
             
              <button className="btn btn-primary btn-lg btn-block" disabled={!(this.state.client && this.state.clientId) ? true : false} type="submit" value="Submit">Create</button>
            </form>
            </div>
          </React.Fragment>
    );
   }
};

export default Customers;