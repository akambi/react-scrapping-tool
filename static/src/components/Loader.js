/* eslint camelcase: 0, no-underscore-dangle: 0 */

import React, { Component } from 'react';
import { withStyles } from 'material-ui/styles';
import { CircularProgress } from 'material-ui/Progress';

const styles = theme => ({
  progress: {
    margin: `-${theme.spacing.unit * 3}px 0 0 -${theme.spacing.unit * 3}px`,
    position: 'absolute',
    left: '50%',
    top: '50%' 
  },
  bodybackground: {
    backgroundColor: '#FCFCFC',
    opacity: 0.3,
    width: window.innerWidth,
    height: window.innerHeight,
    position: 'absolute',
    top: 0,
    left: 0,
    zIndex: 99999,
  }
});

class LoaderView extends Component {

    constructor(props) {
        super(props);
        this.state = {
            email: '',
            password: '',
            email_error_text: null,
            password_error_text: null,
            disabled: true,
        };
    }

    render() {
        const { classes, isFetching } = this.props;
        return isFetching ? <div className={classes.bodybackground}>
          <CircularProgress className={classes.progress} size={50} />
          </div> : <span/>;
    }
}

LoaderView.propTypes = {
    isFetching: React.PropTypes.bool,
};

export default withStyles(styles, { withTheme: true })(LoaderView);
