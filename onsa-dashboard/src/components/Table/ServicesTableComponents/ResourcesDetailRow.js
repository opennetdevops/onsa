import React, {Component} from 'react';
import {HTTPGet, ServiceURLs} from '../../../middleware/api'
import ResourcesCard from './ResourcesCard'
import { lowerCase, startCase } from 'lodash';



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
      switch (key) {
        case "access_node":
          let an = { ...rscJson[key] }; // deconstruc acces_node obj.
          Object.keys(an).forEach(key => {
            let item = {
              field: startCase(lowerCase(key.replace(/_/g, " "))),
              value: an[key]
            };
            if (key === "name") {
              anData.unshift(item);
            } else if (key === "model") {
              anData.splice(1, 0, item);
            } else {
              anData.push(item);
            }
          });
          break;

        case "customer":
          ctmData.push(
            { field: "CUIT", value: "22-9999999-5" }, // TODO change value to props.servicedata
            { field: "Product Id", value: this.props.serviceData.id },
            { field: "Name", value: rscJson[key] }
          );
          break;

        case "customer_location":
          ctmData.push({
            field: "CPE Location",
            value: rscJson[key]
          });
          break;
        case "location":
          ctmData.push({ field: "HUB", value: rscJson[key] });
          break;

        case "loopback":
          ntwData.push({ field: "Loopback", value: rscJson[key] });
          break;
        case "router_node":
          let routerNode = {
            field: "Router Node",
            value: rscJson[key].name
          };
          anData.push(routerNode);
          break;
        case "vlan_id":
          ntwData.push({ field: "Vlan", value: rscJson[key] });

          break;
        case "wan_network":
          ntwData.push({ field: "WAN", value: rscJson[key] });
          break;
        case "vrf_id":
          ntwData.push({ field: "VRF", value: rscJson[key] });
          break;
        case "public_network":
          ntwData.push({ field: "Public Network", value: rscJson[key] });
          break;

        default:
          break;
      }
    }
        this.setState({
          resources: rscJson, customerData: ctmData , accessNodeData: anData, networkingData: ntwData
        });
        
      }
  render() {
    console.log("json resources: ",this.state.resources)
    // console.log("ctmData: ",this.state.customerData)
    console.log("service: ", this.props.serviceData)

    return (
      <div className="row p-2" style={{backgroundColor: "#f2f2f2" }}>
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