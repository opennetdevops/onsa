import React from 'react';
// import { onsaServices, onsaVrfServices, serviceEnum } from '../site-constants.js';
import { Form, FormRow, FormTitle, FormInput, FormSelect } from '../components/Form';
import { URLs, HTTPGet, HTTPPost } from '../middleware/api.js'
import { Alert } from 'reactstrap';

class ProjectCreate extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      clients: [],
      client: {'id': null, 'name': null },
      projectId: '',
      successAlert: false
    };


  }

  componentDidMount() {

    HTTPGet(URLs['clients']).then((jsonResponse) => {
      this.setState({ clients: jsonResponse })
    })

    this.props.displayNavbar(false);
  }

  handleChange = (event) => {

    const value = event.target.value;
    const name = event.target.name;

    switch(name) {
      default:
        this.setState({[name]: value})

    }

  }

  handleOnSelect = (event) => {

    const value = event.target.value;
    const name = event.target.name;

    console.log(value)

     switch(name) {
      case "client":
        this.setState({[name]: JSON.parse(value)})
        break
      default:
        this.setState({[name]: value})

    }
  }

  resetFormFields = () => {
    this.setState({
      projectId: "",
      client: "",
    })
  }

  handleSubmit = (event) => {
    event.preventDefault();

    let data = { "client": this.state.client.id,
                 "id": this.state.projectId };

    HTTPPost(URLs['projects'], data).then(() => { this.setState({successAlert: true}) })

    this.resetFormFields();

    // this.props.history.push('/dashboard');
  }


    render() {

        const clientsList = this.state.clients.map((client) => <option key={client.id} value={JSON.stringify(client)}>{client.name}</option>)

        let alertBox = null;
        if (this.state.successAlert) {
        alertBox = <Alert bsStyle="success"><strong>Success!</strong> Service created.</Alert>;
        }

        return (
            <React.Fragment>
            <div>{alertBox}</div>
            <div className="col-md-6 order-md-1">
                <FormTitle>New project</FormTitle>
                <Form className="needs-validation" noValidate onSubmit={this.handleSubmit}>
                    <FormRow className="row">

                    <div className="col-md-6 mb-3">
                        <label htmlFor="client">Client</label>
                        <FormSelect className="custom-select d-block w-100" id="client" name="client" value={JSON.stringify(this.state.client)} defaultValue={JSON.stringify(this.state.client)} onChange={this.handleOnSelect} required>
                        <option value="">Choose...</option>
                        {clientsList}
                        </FormSelect>
                        <div class="invalid-feedback">Example invalid feedback text</div>
                    </div>

                    <div className="col-md-6 mb-3">
                        <label htmlFor="projectId">ID</label>
                        <FormInput type="text" className="form-control" id="projectId" placeholder="Id" name="projectId" value={this.state.projectId} onChange={this.handleChange} required/>
                    </div>
                    </FormRow>

                    <hr className="mb-4"/>

                    <button className="btn btn-primary btn-lg btn-block" disabled={!this.state.projectId ? true : false} type="submit">Create</button>
                </Form>
                </div>
                </React.Fragment>

    );
  }
};

export default ProjectCreate;