import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';

class FormTitle extends React.Component {

  static propTypes = {

    className: PropTypes.string

  };

  static defaultProps = {

    className: "mb-3",

  };

    render() {
      const { children,
              className,
              ...props
        } = this.props

      return (
          <h4 className={classNames(className)} {...props}>{children}</h4>
    );
   }
};

export default FormTitle;