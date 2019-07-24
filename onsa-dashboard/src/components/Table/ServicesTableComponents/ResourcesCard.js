import React from 'react';
import { Toast, ToastBody, ToastHeader } from 'reactstrap';
import PropTypes from 'prop-types';
import classes from "./ResourcesDetailRow.module.css"



const ResourcesCard = (props) => {
    
    return (
        <Toast className={classes.resourceCardBody}>
          <ToastHeader className={classes.resourceCardHeader}>
            {props.title}
          </ToastHeader>
          <ToastBody className="text-left">
            <ul className="list-unstyled pl-2">
              {props.data.map(item => (
                <li key={item.field}>
                  <strong> {item.field}: </strong>
                  <label className={classes.resourceCardValue}>
                    {item.value}
                  </label>
                </li>
              ))}
            </ul>
          </ToastBody>
        </Toast>
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