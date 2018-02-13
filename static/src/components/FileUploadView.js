/* eslint camelcase: 0, no-underscore-dangle: 0 */

import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import Button from 'material-ui/Button';
import Icon from 'material-ui/Icon';
import FileUpload from 'material-ui-icons/FileUpload';

import { withStyles } from 'material-ui/styles';

import Paper from 'material-ui/Paper';
import * as actionCreators from '../actions/data';

function mapStateToProps(state) {
    return {
        token: state.auth.token,
    };
}

function mapDispatchToProps(dispatch) {
    return bindActionCreators(actionCreators, dispatch);
}

const style = {
    /*marginTop: 100,*/
    paddingBottom: 50,
    paddingTop: 10,
    width: '100%',
    textAlign: 'center',
    display: 'inline-block',
};

const styles = theme => ({
  fileInput: {
    cursor: 'pointer',
    position: 'absolute',
    top: 0,
    bottom: 0,
    right: 0,
    left: 0,
    width: '100%',
    opacity: 0,
  },  
  button: {
    margin: theme.spacing.unit,
    margin: 12,
    marginTop: 50,
  },
  leftIcon: {
    marginRight: theme.spacing.unit,
  },
  rightIcon: {
    marginLeft: theme.spacing.unit,
  },
});

@connect(mapStateToProps, mapDispatchToProps)
class FileUploadView extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            protocol: '',
            protocol_error_text: null,
            disabled: true,
        };
    }

    isDisabled() {
        let protocol_is_valid = false;

        if (this.state.protocol === '' || !this.state.protocol) {
            this.setState({
                protocol_error_text: null,
            });
        } else if (this.state.protocol instanceof File) {
            protocol_is_valid = true;
            this.setState({
                protocol_error_text: null,
            });
        } else {
            this.setState({
                protocol_error_text: 'Your protocol file must be a HTML File',
            });

        }

        if (protocol_is_valid) {
            this.setState({
                disabled: false,
            });
        }
    }

    onChangeFile(e) {
        const next_state = { protocol: e.target.files[0] };
        this.setState(next_state, () => {
            this.isDisabled();
        });
    }

    _handleKeyPress(e) {
        if (e.key === 'Enter') {
            if (!this.state.disabled) {
                this.upload(e);
            }
        }
    }

    upload(e) {
        e.preventDefault();
        this.props.processProtocol(this.state.protocol, this.props.token);
    }

    render() {
        const { classes, theme } = this.props;

        return (
            <div className="col-md-12" onKeyPress={(e) => this._handleKeyPress(e)}>
                <Paper style={style}>
                    <div>
                        <div className="col-md-12">
                            <Button className={classes.button}
                              variant="raised"
                              color="default">
                              <input type="file" className={classes.fileInput}
                               onChange={(e) => this.onChangeFile(e)}/>Choose a HTML Protocol File
                                <FileUpload className={classes.rightIcon} />
                            </Button>

                            <Button className={classes.button}
                              variant="raised"
                              color="primary"
                              disabled={this.state.disabled}
                              onClick={(e) => this.upload(e)}>Upload</Button>
                        </div>
                    </div>
                </Paper>
            </div>
        );

    }
}

FileUploadView.propTypes = {
    processProtocol: React.PropTypes.func,
};

export default withStyles(styles, { withTheme: true })(FileUploadView);
