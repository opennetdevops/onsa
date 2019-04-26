import React from 'react';
import { Alert } from 'reactstrap';

async function postJson(url, data) {

    let response = await fetch(url, {
        method: "POST",
        mode: "cors", 
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + sessionStorage.getItem('token')
        },
        body: JSON.stringify(data)
      });
    // ver opcion de devolver response.
    let jsonResponse = await response.json();

    return jsonResponse;} 


class Customers extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      client: '',
      cuic: '',
      successBox: null
    };
  }

  componentDidMount() {
   

    this.props.displayNavbar(false); 
  }

  resetFormFields = () => {
    this.setState({
      client: "",
      cuic: "",
    })
  }

  handleChange = (event) => {

    const value = event.target.value;
    const name = event.target.name

    this.setState({[name]: value})
  }

  handleSubmit = (event) => {
    event.preventDefault();

    const data = { "name": this.state.client, 
                    "cuic": this.state.cuic, };
    
    
    let url = process.env.REACT_APP_CORE_URL + "/core/api/clients";

    postJson(url, data).then(() => this.setState({successBox: true} ) ) //acá pregunto por el status, 2xx o 5xx y en base a eso seteo success  box.
    
    
    this.resetFormFields();
  }

    render() {

      let alertBox = null;
      if (this.state.successBox) {
        alertBox = <Alert className="success"><strong>Success!</strong> Customer created.</Alert>;
        } 
       else if (this.state.successBox!= null) {
        alertBox = <Alert className="alert-danger"><strong>Error!</strong> Customer not created.</Alert>;

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
                  <label htmlFor="cuic">ID</label>
                  <input type="text" className="form-control" id="cuic" name="cuic" value={this.state.cuic} onChange={this.handleChange} placeholder="Id" required/>
                </div>
              </div>
              <hr className="mb-4"/>
             
              <button className="btn btn-primary btn-lg btn-block" disabled={!(this.state.client && this.state.cuic) ? true : false} type="submit" value="Submit">Create</button>
            </form>
            </div>
          </React.Fragment>
    );
   }
};

export default Customers;