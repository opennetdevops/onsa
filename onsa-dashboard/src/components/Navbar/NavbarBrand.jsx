import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';

class NavbarBrand extends React.Component {

	static propTypes = {

		className: PropTypes.string,
		bsSuffix: PropTypes.string

	};

	static defaultProps = {

		className: "navbar-brand",
	};

  render() {

  	const { className,
  			bsSuffix,
  			children,
  			href,
  			...props } = this.props

    return ( 	  
	    <a className={classNames(className, bsSuffix)} href={href} {...props}>
		    {children}
	    </a>
    );
  }
}

export default NavbarBrand;