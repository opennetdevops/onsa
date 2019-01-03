import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';

class NavLink extends React.Component {

  static propTypes = {
    className: PropTypes.string,
    bsSuffix: PropTypes.string,
    href: PropTypes.string,
    toggle: PropTypes.string
  };

  static defaultProps = {
    className: "nav-link"
  };

  render() {

  	const { children,
  		      className,
            bsSuffix,
            href,
            toggle,
            ...props
  		  } = this.props;

    return ( 	  
  		<a className={classNames(className, bsSuffix)} href={href} {...props}>
  			{children} 
  		</a>
    );
  }
}

export default NavLink;