import React, {Component} from 'react';
import {HTTPGet, ServiceURLs} from '../../../middleware/api'
import ResourcesCard from './ResourcesCard'


class ResourcesDetailRow extends Component {

    state = {
        resources: null,
        customerData: [],
        accessNodeData:[],
        networkingData:[]
    }
  componentDidMount() {
    let url = ServiceURLs("resources", this.props.serviceData.id);

    HTTPGet(url).then(
      jsonResponse => {
        this.mapJsonToArrays(jsonResponse)
      },
      error => {
        this.props.alert(false, error.message);
      }
    );
  }

  mapJsonToArrays = (rscJson) => {
    let ctmData = []
    let anData = []
    let ntwData = []

    for (let key in rscJson) {
      if (key === "access_node") {// deconstruc acces_node obj.
        let an = { ...rscJson[key] };
        anData = Object.keys(an).map(key => {
          return { field: key, value: an[key] };
        });

      } else if (key === "customer") {
        ctmData.push(
          { field: "CUIT", value: "22-9999999-5" }, // change value to props.servicedata
          { field: "Product Id", value: this.props.serviceData.id },
          { field: "Name", value: rscJson[key] }
        );

      } else if (key === "customer_location") {
        ctmData.push({
          field: "CPE Location",
          value: rscJson[key]
        });

      } else if (key === "location") {
        ctmData.push({ field: "HUB", value: rscJson[key] });

      } else if (key === "loopback") {
        ntwData.push({ field: "Loopback", value: rscJson[key] });
        
      } else if (key === "router_node") {
        let routerNode = { field: "Router Node", value: rscJson[key].name };
        anData.push(routerNode);

      } else if (key === "vlan_id") {
        ntwData.push({ field: "VLan", value: rscJson[key] });

      } else if (key === "wan_network") {
        ntwData.push({ field: "WAN", value: rscJson[key] });

      } else if (key === "vrf_id") {
        ntwData.push({ field: "VRF", value: rscJson[key] });
      }
    }
    this.setState({
      resources: rscJson, customerData: ctmData , accessNodeData: anData, networkingData: ntwData
    });
    
  }

  render() {
    console.log("json resources: ",this.state.resources)
    console.log("ctmData: ",this.state.customerData)
    console.log("service: ", this.props.serviceData)

    return (
      <div className="row">
        <div className="col-4">
          <ResourcesCard
            title="Customer & Service"
            data={this.state.customerData}
          />
        </div>

        <div className="col-4">
          <ResourcesCard
            title="Access Node"
            data={this.state.accessNodeData}
          />
        </div>
        <div className="col-4">
          <ResourcesCard
            title="Networking"
            data={this.state.networkingData}
          />
        </div>
        {/* Customer Info, Access Node , Networking: */}
        {/* <div className="col-12">
        <h6>Service data:</h6>
         <p>{JSON.stringify(this.props.data,null,2)}</p>
        </div> */}
      </div>
    );
  }
}

export default ResourcesDetailRow;