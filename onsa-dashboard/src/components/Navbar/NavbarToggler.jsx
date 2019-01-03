import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';

class NavbarToggler extends React.Component {

	static propTypes = {
		className: PropTypes.string,
		tag: PropTypes.string,
		type: PropTypes.string
	};

	static defaultProps = {
		className: "navbar-toggler",
		tag: 'button',
		type: 'button',
	};


	render() {

  	const { children,
  			className,
  			type,
  			tag: Tag,
  			...props } = this.props

    return ( 	  
	  <Tag className={classNames(className)} type={type} {...props}>
	        <span className="navbar-toggler-icon"></span>
	  </Tag>
    );
  }
}

export default NavbarToggler;