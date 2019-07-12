import React from "react";
import { Button, Badge } from "reactstrap";
import {
  serviceEnum,
  serviceStatesEnum,
  notDeletableStates,
  resultantStates,
  retryableStates
} from "../site-constants.js";
import {
  ResourcesModal,
  ActivateModal,
  AccessNodeModal,
  TerminateModal,
  UnsubscribeModal
} from "../components/Modals";

import FormAlert from "../components/Form/FormAlert";
import { URLs, HTTPGet, ServiceURLs } from "../middleware/api";
import RetryModal from "../components/Modals/RetryModal";
import Spinner from "../components/UI/Spinner/Spinner"
import ServicesTable from "../components/Table/ServicesTable"

class Dashboard extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      activateModal: false,
      accessNodeActivateModal: false,
      displayMessage: "",
      dialogLabel: "",
      modalService: { id: null, type: null },
      resources: null,
      resourcesModal: false,

      retryModal: false,
      services: [],
      serviceChanged: null,
      successAlert: null,
      terminateModal: false,
      unsubscribeModal: false,
      updatingServices: [] // [{id: serviceId, retryCounter:0}]
    };
  }

  componentDidMount() {
    this.getServices();
    this.props.displayNavbar(false);
  }

  getServices() {
    HTTPGet(URLs["services"]).then(
      jsonResponse => this.setState({ services: jsonResponse }),
      error => this.showAlertBox(false, error.message)
    );
  }

  getOneService = serviceID =>
    new Promise((resolve, reject) => {
      HTTPGet(ServiceURLs("service", serviceID)).then(
        jsonResponse => {
          resolve(jsonResponse);
        },
        error => {
          reject(error);
        }
      );
    });

  showAlertBox = (result, message, label) => {
    this.setState({
      dialogSuccess: result,
      dialogText: message,
      dialogShow: message || result ? true : false,
      dialogLabel: label
    });
  };

  handleErrorOnUpdating = (message, serviceId) => {
    this.showAlertBox(false, message);

    this.updateUpdatingServices(serviceId, true);
  };

  // handleOnClick = event => {
  //   const value = event.target.value;
  //   const name = event.target.name;

    handleActionClick = (action, serviceId, serviceType, prevServState) => {

    this.setState({
      modalService: {
        id: serviceId,
        type: serviceType,
        prevServState: prevServState
      }
    });

    switch (action) {
      case "resources":
        let url = ServiceURLs("resources", serviceId);

        HTTPGet(url).then(
          jsonResponse => {
            this.setState({
              resources: jsonResponse,
              resourcesModal: !this.state.resourcesModal
            });
          },
          error => {
            this.showAlertBox(false, error.message);
          }
        );

        break;
      case "activate":
        this.setState({
          activateModal: !this.state.accessNodeActivateModal
        });
        break;
      case "anActivate":
        this.setState({
          accessNodeActivateModal: !this.state.accessNodeActivateModal
        });
        break;
      case "retry":
        this.setState({
          // retryModal: !this.state.retryModal
          accessNodeActivateModal: !this.state.accessNodeActivateModal
        });
        break;
      case "terminate":
        this.setState({
          terminateModal: !this.state.terminateModal
        });
        break;
      case "unsubscribe":
        this.setState({
          unsubscribeModal: !this.state.unsubscribeModal
        });
        break;
      default:
        break;
    }
  };

  handleToggle = (name, value, serviceId) => {
    this.setState({ [name]: !value });
    if (serviceId) {
      this.updateUpdatingServices(serviceId);
    }
  };

  getMsgLabel = (processResult) => {
    let actionMsg = ""
            
    switch (processResult) {
      case "configSCO" :
          actionMsg = "updated"
      break;
      case "unsubscribeCompleted" :
          actionMsg = "removed"
      break;
      case "unsubscribeInProgress" :
          actionMsg = "unsubscribed"
      break;
      case "terminateServ" :
          actionMsg = "successfully configured"
      break;
      default: 
        actionMsg = "updated"
      break;
    }
    return actionMsg
  }

  updateOneService = (serviceId, processResult) => {
    let updatedServices = [];
    // console.log("1 - Ready to update id:", serviceId, "processResult: ",processResult);

    this.getOneService(serviceId).then(
      responseService => {
        updatedServices = [...this.state.services];
        let selectedIndex = updatedServices.findIndex(x => x.id === serviceId);

        if (processResult === "unsubscribeCompleted") {
          updatedServices.splice(selectedIndex, 1);
          this.showAlertBox(true, "The service with product ID " + serviceId + " has been removed.");
        } else {
          updatedServices[selectedIndex] = responseService;

          // console.log( "2 - Is ", responseService.id, "state: ", responseService.service_state,
          //   " in a definitive state?: ", resultantStates.includes(responseService.service_state));

          if (resultantStates.includes(responseService.service_state)) { 
            // **checks if it is a definitive state.*
            this.updateUpdatingServices(serviceId, true);
            // console.log( "State - list - finished: ",this.state.updatingServices);
           
            let actionMsg = this.getMsgLabel(processResult)
            
            this.showAlertBox( true, "The service with product ID " + serviceId + " has been " + actionMsg + ".");

          } else {
            this.updateUpdatingServices(serviceId);

            // console.log( "State - list - inProgress: ", this.state.updatingServices);

            this.refreshAfterUpdate(serviceId);
          }
        }
        this.setState({ services: updatedServices });
      },
      error => this.showAlertBox(false, error.message)
    );
  };

  getActualUpdatingService = serviceId => {
    let newList = [...this.state.updatingServices];
    let indx = this.state.updatingServices.findIndex(
      serviceItem => serviceId === serviceItem.id
    );
    let updatingService = {
      service: { ...newList[indx] }, //{ id: serviceId, retryCounter:0},
      indexOnList: indx
    };

    return updatingService;
  };

  refreshAfterUpdate = serviceId => {
    //checks retry counter of the selected service, if its not timeout,
    //lops for another update.

    let updatingService = this.getActualUpdatingService(serviceId);

    if (updatingService.service.retryCounter <= 5) {
      setTimeout(() => {
        // its mandatory to get the updated list of updatingServices because of the async timer
        let newList = [...this.state.updatingServices];
        let updatingItem = this.getActualUpdatingService(serviceId);

        this.updateOneService(serviceId, "refreshingAfterUpdate");

        updatingItem.service.retryCounter += 1;

        newList[updatingItem.indexOnList] = updatingItem.service;

        // console.log("3 - Refreshing service: ", updatingItem.service.id , "attempt # ", updatingItem.retryCounter );

        this.setState({
          retryCounter: 0,
          updatingServices: newList
        });
      }, 5000);
    } else {
      this.showAlertBox(
        false, "Server timed out after " + updatingService.service.retryCounter +
        " attempts. Please try again later.");

      // console.log("** TIME OUT on retry attempts ** ", updatingService.id, "attempt # ",
      //   updatingService.service.retryCounter);

      this.updateUpdatingServices(serviceId, true);
    }
  };

  updateUpdatingServices = (serviceId, finished = false) => {
    //updates updatingServicesLists
    let newList = [...this.state.updatingServices];
    let alreadyExists = newList.some(
      serviceItem => serviceId === serviceItem.id
    );

    // console.log("already exists?:", alreadyExists);
    if (!alreadyExists && !finished) {

      let newItem = { id: serviceId, retryCounter: 0 };
      newList.push(newItem);
    }
    if (alreadyExists && finished) {
      let indx = newList.findIndex(serviceItem => serviceId === serviceItem.id);
      newList.splice(indx, 1);
    }
    this.setState({ updatingServices: newList });
  };

  render() {
    let serviceIsUpdating = false;
    
    const servicesData = this.state.services.map( service => {
      serviceIsUpdating = this.state.updatingServices.some(
        serviceItem => service.id === serviceItem.id
      )
      let newServ = {...service, isUpdating:serviceIsUpdating } 
      return newServ
    } )
    
    let isUpdating = false;
    const tableRows = this.state.services.map(service => {
      isUpdating = this.state.updatingServices.some(
        serviceItem => service.id === serviceItem.id
      );

      return (
        <tr className="table-borderless" key={service.id}>
          <td>
            <Badge color="primary">{service.id}</Badge>
          </td>
          <td>
            <Badge color="secondary">{service.gts_id}</Badge>
          </td>
          <td>
            <Badge color="success">{serviceEnum[service.service_type]}</Badge>
          </td>
          <td>
            <Badge color="secondary">
              {serviceStatesEnum[service.service_state]}
            </Badge>
          </td>
          <td>{isUpdating ? <Spinner /> : null}</td>

          <td>
            <Button
              className="btn btn-primary btn-sm btn-block"
              color="primary"
              name="resources"
              onClick={this.handleOnClick}
              type="button"
              value={JSON.stringify(service)}
            >
              View details
            </Button>
          </td>
          {service.service_state === "in_construction" ? (
            <td>
              <Button
                className="btn btn-primary btn-sm btn-block"
                color="success"
                name="anActivate"
                onClick={this.handleOnClick}
                type="button"
                value={JSON.stringify(service)}
                disabled={isUpdating}
              >
                Configure SCO
              </Button>
            </td>
          ) : null}

          {service.service_state === "an_activated" ? (
            <td>
              <Button
                className="btn btn-primary btn-sm btn-block"
                color="info"
                name="terminate"
                onClick={this.handleOnClick}
                type="button"
                value={JSON.stringify(service)}
                disabled={isUpdating}

              >
                Terminate
              </Button>
            </td>
          ) : null}
          {notDeletableStates.indexOf(service.service_state) === -1 ? (
            <td>
              <button
                className="btn btn-danger btn-sm btn-block"
                color="danger"
                name="unsubscribe"
                onClick={this.handleOnClick}
                type="button"
                value={JSON.stringify(service)}
                disabled={isUpdating}

              >
                Unsubscribe
              </button>
            </td>
          ) : null}
          {retryableStates.indexOf(service.service_state) !== -1 ? (
            <td>
              <Button
                className="btn btn-primary btn-sm btn-block"
                color="success"
                name="retry"
                onClick={this.handleOnClick}
                type="button"
                value={JSON.stringify(service)}
                disabled={isUpdating}

              >
                Retry
              </Button>
            </td>
          ) : null}
        </tr>
      );
    });

    return (
      <div className="container-fluid">
        <div className="row justify-content-center">
          <FormAlert
            dialogSuccess={this.state.dialogSuccess}
            dialogText={this.state.dialogText}
            dialogShow={this.state.dialogShow}
            msgLabel={this.state.dialogLabel}
          />
        </div>
        <div className="row justify-content-center" style={{marginTop: "5vh"}}>
          
          <ServicesTable 
          services= {servicesData}
          onClickedAction={this.handleActionClick}
          />
          
          {/* <table className="table table-hover col-md-12">
            <thead>
              <tr>
                <th scope="col">Product ID</th>
                <th scope="col">GTS </th>
                <th scope="col">Service Type</th>
                <th scope="col">Service State</th>
              </tr>
            </thead>
            <tbody>{tableRows}</tbody>
          </table> */}
        </div>

        <ResourcesModal
          isOpen={this.state.resourcesModal}
          service={this.state.modalService}
          toggle={this.handleToggle}
        >
          {JSON.stringify(this.state.resources, null, 2)}
        </ResourcesModal>
        <ActivateModal
          isOpen={this.state.activateModal}
          service={this.state.modalService}
          toggle={this.handleToggle}
        />
        <AccessNodeModal
          isOpen={this.state.accessNodeActivateModal}
          service={this.state.modalService}
          toggle={this.handleToggle}
          alert={this.showAlertBox}
          serviceHasChanged={this.updateOneService}
          onUpdateError={this.handleErrorOnUpdating}
        />
        <RetryModal
          isOpen={this.state.retryModal}
          service={this.state.modalService}
          toggle={this.handleToggle}
          alert={this.showAlertBox}
          serviceHasChanged={this.updateOneService}
          onUpdateError={this.handleErrorOnUpdating}
        />
        <TerminateModal
          isOpen={this.state.terminateModal}
          service={this.state.modalService}
          toggle={this.handleToggle}
          alert={this.showAlertBox}
          serviceHasChanged={this.updateOneService}
          onUpdateError={this.handleErrorOnUpdating}
        />
        <UnsubscribeModal
          isOpen={this.state.unsubscribeModal}
          service={this.state.modalService}
          toggle={this.handleToggle}
          alert={this.showAlertBox}
          serviceHasChanged={this.updateOneService}
          onUpdateError={this.handleErrorOnUpdating}
        />
      </div>
    );
  }
}

export default Dashboard;
