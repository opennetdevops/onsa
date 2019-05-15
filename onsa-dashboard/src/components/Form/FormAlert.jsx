import React from "react";

//Stateless component to show alert messages.

const customAlert = props => {
  //specify props: Succesfull:boolean and displayMessage:string to display.
  //icnludeLabel prop: Overrides default label


  let alertBox = null;
  // if (props.visible === true) {
    if (props.succesfull) {
      alertBox = (
        <div className="alert alert-success visibilityAlert fadeOutAlert">
          <strong>{props.msgLabel ? props.msgLabel : "Success! "}</strong>
          {props.displayMessage}
        </div>
      );
    } else if (props.succesfull === false) {
      alertBox = (
        <div className="alert alert-danger visibilityAlert fadeOutAlert">
          {/* visibilityAlert fadeOutAlert */}
          <strong>
            {props.msgLabel ? props.msgLabel : "Something went wrong: "}
          </strong>
          {props.displayMessage}
        </div>
      );
    }
  // } else {
  //   alertBox = null;
  // }


  return alertBox;
};
export default customAlert;
