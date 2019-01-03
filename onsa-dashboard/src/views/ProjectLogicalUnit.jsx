import React from 'react';
import { Form, FormRow, FormTitle, FormInput, FormSelect } from '../components/Form';
import { URLs, HTTPGet, HTTPPost } from '../middleware/api.js'
import { Alert } from 'reactstrap';

class ProjectLogicalUnit extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      projects: [],
      locations: [],
      projectId: '',
      locationId: '',
      logicalUnitId: '',
      successAlert: false
    };


  }

  componentDidMount() {
    HTTPGet(URLs['projects'])
    .then((jsonResponse) => {
      this.setState({ projects: jsonResponse })
    })
    .catch(() => { console.log("error") })

    HTTPGet(URLs['locations'])
    .then((jsonResponse) => {
      this.setState({ locations: jsonResponse })
    })
    .catch(() => { console.log("error") })

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

    // Request inventory for access port and vlan. 
    // Save access port id.

    let url = URLs['projects'] + "/" + this.state.projectId + "/locations/" + this.state.locationId + "/logicalunits"

    let data = { "logical_unit_id": this.state.logicalUnitId };

    HTTPPost(url, data).then(() => { this.setState({successAlert: true}) })

    this.resetFormFields();

    // this.props.history.push('/dashboard');
  }


    render() {

        const projectsList = this.state.projects.map((project) => <option key={project.svc_id} value={JSON.stringify(project)}>{project.svc_id}</option>)
        const locationsList = this.state.locations.map((location) => <option key={location.id} value={JSON.stringify(location)}>{location.name}</option>)

        let alertBox = null;
        if (this.state.successAlert) {
        alertBox = <Alert bsStyle="success"><strong>Success!</strong> Service created.</Alert>;
        }

        return (
            <React.Fragment>
            <div>{alertBox}</div>
            <div className="col-md-6 order-md-1">
                <FormTitle>Add logical unit to project</FormTitle>
                <Form className="needs-validation" noValidate onSubmit={this.handleSubmit}>
                    <FormRow className="row">

                    <div className="col-md-12 mb-3">
                        <label htmlFor="client">Project</label>
                        <FormSelect className="custom-select d-block w-100" id="project" name="project" value={JSON.stringify(this.state.project)} defaultValue={JSON.stringify(this.state.project)} onChange={this.handleOnSelect} required>
                        <option value="">Choose...</option>
                        {projectsList}
                        </FormSelect>
                        <div className="invalid-feedback">Example invalid feedback text</div>
                    </div>
                    </FormRow>

                    <FormRow className="row">
                        <div className="col-md-12 mb-3">
                            <label htmlFor="client">Location</label>
                            <FormSelect className="custom-select d-block w-100" id="location" name="location" value={JSON.stringify(this.state.location)} defaultValue={JSON.stringify(this.state.location)} onChange={this.handleOnSelect} required>
                            <option value="">Choose...</option>
                            {locationsList}
                            </FormSelect>
                            <div className="invalid-feedback">Example invalid feedback text</div>
                        </div>
                    </FormRow>

                    <hr className="mb-4"/>

                    <button className="btn btn-primary btn-lg btn-block" disabled={!this.state.projectId ? true : false} type="submit">Add</button>
                </Form>
                </div>
                </React.Fragment>

    );
  }
};

export default ProjectLogicalUnit;