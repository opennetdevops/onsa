import React, {Component} from 'react';
import {HTTPGet, ServiceURLs} from '../../../middleware/api'
// import { Card, CardText, CardBody, CardTitle } from 'reactstrap';
import ResourcesCard from './ResourcesCard'

class ResourcesDetailRow extends Component {

    state = {
        resources: null,
        customerData: [],
        accessNodeData:[],
        

    }
  componentDidMount() {
    let url = ServiceURLs("resources", this.props.serviceData.id);

    HTTPGet(url).then(
      jsonResponse => {
        let ctmData = []
        let anData = []
        let serviceData = []
        
        // ctmData.push(jsonResponse.)
        ctmData.push(
            {field:"Name", value:jsonResponse["customer"]},
            {field:"CUIT", value:"112456798"},
            {field:"Product Id", value:this.props.serviceData.id},
            {field:"CPE Location", value:jsonResponse["customer_location"]},
        )

        // let list = Object.keys(jsonResponse).map( key => {
            
        //      return {[key]:jsonResponse[key] }})


        this.setState({
          resources: jsonResponse, customerData: ctmData
        });
      },
      error => {
        this.showAlertBox(false, error.message);
      }
    );

  }

  render() {
     let tableRows = <div>{JSON.stringify(this.state.resources, null,2)}</div>

     // = this.state.resources.map(resource => {
    //     return (<p>{resource.att} : {resource.value}</p>)
    // })
    console.log("json resources: ",this.state.resources)
    console.log("ctmData: ",this.state.customerData)
    console.log("service: ", this.props.serviceData)
    // let resources =  this.state.resources
    //  let tableRows = null
    // if (resources) {
    // tableRows =  Object.keys(resources).map((key, i) => {
    //   let resourcesTable = resources.map( resource => {
    //     <tr key={key}>
    //     <td>{key}</td>
    //     <td>{resources[key]}</td>
    // </tr>
        // return (<p key={key}>{JSON.stringify(resources[key], null,2)}</p> )
        // let value = resources[key]
        // return (<p key={key}>{JSON.stringify(resources[key], null,2)}</p> )
    //     return {}
    //     }

    //   )
   
    //  console.log("recurso: ",tableRows)
    return (
      <div className="row">
        <div className="col-4">
          <div className="p-2 my-2 ml-2 rounded">
            <ResourcesCard
              title="Billing Info"
              data={this.state.customerData}
            />
            {/* Customer Info, Access Node , Networking: */}
          </div>
        </div>
        {/* <div className="col-12">
        <h6>Service data:</h6>
         <p>{JSON.stringify(this.props.data,null,2)}</p>
        </div> */}
      </div>
    );
  }
}

export default ResourcesDetailRow;