import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';


const Footer = (props) => {

  const { className, 
          bsClassName,
          ...attributes } = props;

  return (
      <footer className={classNames(className,bsClassName)} {...attributes}>
        <p className="mb-1 mt-3 h6">FibercorpLabs © 2018-2019 </p>
        <ul className="list-inline">
          <li className="list-inline-item"><button className="btn btn-link ">Privacy</button></li>
          <li className="list-inline-item"><button className="btn btn-link">Terms</button></li>
          <li className="list-inline-item"><button className="btn btn-link">Support</button></li>
        </ul>
      </footer>
    );

}

Footer.propTypes = {
    className: PropTypes.string,
    bsClassName: PropTypes.string
}; 

Footer.defaultProps = {
  className: "my-auto pt-5 text-muted text-center text-small my-5 "
  // className: "footer mt-auto py-3 "

};

export default Footer;