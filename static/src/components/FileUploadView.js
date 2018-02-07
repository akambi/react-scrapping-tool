/* eslint camelcase: 0, no-underscore-dangle: 0 */

import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import RaisedButton from 'material-ui/RaisedButton';
import FontIcon from 'material-ui/FontIcon';

const styles = {
  button: {
    margin: 12,
  },
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
};

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
    marginTop: 10,
    paddingBottom: 35,
    paddingTop: 0,
    width: '100%',
    textAlign: 'center',
    display: 'inline-block',
};

@connect(mapStateToProps, mapDispatchToProps)
export default class FileUploadView extends React.Component {

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
        return (
            <div className="col-md-12" onKeyPress={(e) => this._handleKeyPress(e)}>
                <Paper style={style}>
                    <div>
                        <div className="col-md-12">

                            <RaisedButton
                              label="Choose a HTML Protocol File"
                              labelPosition="before"
                              primary={true}
                              icon={<FontIcon className="muidocs-icon-custom-github" />}
                              style={styles.button}
                              containerElement="label">
                              <input type="file" style={styles.fileInput}
                               onChange={(e) => this.onChangeFile(e)}/>
                            </RaisedButton>

                            <RaisedButton
                              disabled={this.state.disabled}
                              style={{ marginTop: 50 }}
                              label="Upload"
                              onClick={(e) => this.upload(e)}/>
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
