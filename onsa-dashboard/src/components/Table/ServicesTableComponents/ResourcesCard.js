import React from 'react';
import { Toast, ToastBody, ToastHeader } from 'reactstrap';
import PropTypes from 'prop-types';
import classes from "./ResourcesDetailRow.module.css"



const ResourcesCard = (props) => {
    // console.log("[Card - render]")
    return (
      <div className="p-2 ">
        <Toast className={classes.resourceCardBody}>
          {/* <ToastHeader className="text-muted h6 my-1" style={{letterSpacing: "0.1rem"}}>{props.title}</ToastHeader> */}
          <ToastHeader className={classes.resourceCardHeader}>
            {props.title}
          </ToastHeader>
          <ToastBody className="text-left">
            {/* Customer Info, Access Node , Networking: */}
            <ul className="list-unstyled pl-2">
              {props.data.map(item => (
                <li key={item.field}>
                  <strong> {item.field}: </strong>
                  <label className={classes.resourceCardValue}>
                    {" "}
                    {item.value}
                  </label>
                </li>
              ))}
            </ul>
          </ToastBody>
        </Toast>
      </div>
    );
}
ResourcesCard.propTypes = {
    title: PropTypes.string.isRequired,
    data: PropTypes.arrayOf(PropTypes.shape({
        field: PropTypes.string.isRequired,
        value: PropTypes.string.isRequired
    })).isRequired
};


export default ResourcesCard;