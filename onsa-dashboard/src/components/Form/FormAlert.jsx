import React from "react";
import { Alert } from "reactstrap";

//Stateless component to show alert messages.

const customAlert = props => {
  //specify props: Succesfull:boolean and displayMessage:string to display.
  //icnludeLabel prop: Overrides default label

  let alertBox = null;

  if (props.succesfull) {
    alertBox = (
      <Alert className="alert-success">
        {/* <strong>Success!</strong> {props.displayMessage} */}
        <strong>{props.msgLabel ? props.msgLabel : "Success! "}</strong>
        {props.displayMessage}
      </Alert>
    );
  } else if (props.succesfull == false) {
    alertBox = (
      <Alert className="alert-danger">
        <strong>
          {props.msgLabel ? props.msgLabel : "Something went wrong: "}
        </strong>
        {props.displayMessage}
      </Alert>
    );
  }

  return alertBox;
  //return an alert component based on reacstrap
};
export default customAlert;
