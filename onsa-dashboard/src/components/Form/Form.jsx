import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';

class Form extends React.Component {

  static propTypes = {

    className: PropTypes.string,
    bsSuffix: PropTypes.string

  };

  static defaultProps = {

    className: "col-md-8 order-md-1",

  };

    render() {
      const { children,
              className,
              bsSuffix,
              ...props
        } = this.props

      return (
          <form className={classNames(className)} {...props}>
            {children}
          </form>
    );
   }
};

export default Form;