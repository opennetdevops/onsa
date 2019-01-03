import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';


const Footer = (props) => {

  const { className, 
          bsClassName,
          ...attributes } = props;

  return (
      <footer className={classNames(className,bsClassName)} {...attributes}>
        <p className="mb-1">FibercorpLabs © 2018-2019 </p>
        <ul className="list-inline">
          <li className="list-inline-item"><a href="example.com/#">Privacy</a></li>
          <li className="list-inline-item"><a href="example.com/#">Terms</a></li>
          <li className="list-inline-item"><a href="example.com/#">Support</a></li>
        </ul>
      </footer>
    );

}

Footer.propTypes = {
    className: PropTypes.string,
    bsClassName: PropTypes.string
}; 

Footer.defaultProps = {
  className: "my-auto pt-5 text-muted text-center text-small fixed-bottom",
};

export default Footer;