import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';

class Nav extends React.Component {

	static propTypes = {

		className: PropTypes.string,
		bsSuffix: PropTypes.string

	};

	static defaultProps = {

		className: "navbar-nav",

	};


	render() {

  	const { children,
  			className,
  			bsSuffix,
  			...props
		
		} = this.props

    return ( 	  
	   <ul className={classNames(className,bsSuffix)} {...props}>
	   	{children}
	   </ul>
    );
  }
}

export default Nav;
