import React from "react";
import { Alert } from "reactstrap";

//Stateless component to show alert messages

const customAlert = props => {
    //specify props: Succesfull:boolean and displayMessage:string to display    
    let alertBox = null;
    
    if (props.succesfull) {
      alertBox = 
        <Alert className="alert-success">
          <strong>Success!</strong> {props.displayMessage}
        </Alert>;
    
    }else if (props.succesfull == false) {
      alertBox = <Alert className="alert-danger">
        <strong>Something went wrong: </strong> {props.displayMessage}
      </Alert>;
    }

    return (alertBox)
    //return an alert component based on reacstrap
};
export default customAlert;