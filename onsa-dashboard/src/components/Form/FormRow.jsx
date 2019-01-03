import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';

class FormRow extends React.Component {

  static propTypes = {

    className: PropTypes.string,
    
  };

  static defaultProps = {

    className: "row",

  };

    render() {
      const { children,
              className,
              ...props
        } = this.props

      return (
          <div className={classNames(className)} {...props}>
            {children}
          </div>
    );
   }
};

export default FormRow;